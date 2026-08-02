import xml.etree.ElementTree as ET  # nosec
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple, Union, cast

import numpy as np
from language_tags import tags

from camoufox.pkgman import LOCAL_DATA, GitHubDownloader, rprint, webdl
from camoufox.warnings import LeakWarning

from .exceptions import (
    InvalidLocale,
    MissingRelease,
    NotInstalledGeoIPExtra,
    UnknownIPLocation,
    UnknownLanguage,
    UnknownTerritory,
)
from .ip import validate_ip

try:
    import geoip2.database  # type: ignore
except ImportError:
    ALLOW_GEOIP = False
else:
    ALLOW_GEOIP = True


"""
Data structures for locale and geolocation info
"""


@dataclass
class Locale:
    """
    Stores locale, region, and script information.
    """

    language: str
    region: Optional[str] = None
    script: Optional[str] = None

    @property
    def as_string(self) -> str:
        if self.region:
            return f"{self.language}-{self.region}"
        return self.language

    def as_config(self) -> Dict[str, str]:
        """
        Converts the locale to a intl config dictionary.
        """
        assert self.region
        data = {
            'locale:region': self.region,
            'locale:language': self.language,
        }
        if self.script:
            data['locale:script'] = self.script
        return data


@dataclass(frozen=True)
class Geolocation:
    """
    Stores geolocation information.
    """

    locale: Locale
    longitude: float
    latitude: float
    timezone: str
    accuracy: Optional[float] = None

    def as_config(self) -> Dict[str, Any]:
        """
        Converts the geolocation to a config dictionary.
        """
        data = {
            'geolocation:longitude': self.longitude,
            'geolocation:latitude': self.latitude,
            'timezone': self.timezone,
            **self.locale.as_config(),
        }
        if self.accuracy:
            data['geolocation:accuracy'] = self.accuracy
        return data


"""
Helpers to validate and normalize locales
"""


def verify_locale(loc: str) -> None:
    """
    Verifies that a locale is valid.
    Takes either language-region or language.
    """
    if tags.check(loc):
        return
    raise InvalidLocale.invalid_input(loc)


def normalize_locale(locale: str) -> Locale:
    """
    Normalizes and validates a locale code.
    """
    verify_locale(locale)

    # Parse the locale
    parser = tags.tag(locale)
    if not parser.region:
        raise InvalidLocale.invalid_input(locale)

    record = parser.language.data['record']

    # Only an explicitly supplied script is meaningful. `Suppress-Script` is
    # the IANA registry's marker for the script that is REDUNDANT for a
    # language and must therefore be *omitted* from its tags -- for `en` it is
    # `Latn`, which is why nobody writes `en-Latn-GB`. Emitting it as the
    # script to apply inverted the field's meaning and built exactly that tag.
    # ICU does not list `en-Latn-GB`, so SpiderMonkey's BestAvailableLocale
    # truncated from the right (en-Latn-GB -> en-Latn -> en) and took the
    # region with it: navigator.language and Accept-Language said en-GB while
    # Intl.DateTimeFormat().resolvedOptions().locale said plain "en" and dates
    # formatted US-style as 3/9/2026 instead of 09/03/2026. Measured per key:
    # language+region alone resolved to en-GB, adding locale:script collapsed
    # it to en. Languages with a genuine script choice (zh, sr, ...) carry no
    # Suppress-Script, which is why zh-Hant-TW was the one case that worked.
    script = parser.script.data['record']['Subtag'] if parser.script else None

    # Return a formatted locale object
    return Locale(
        language=record['Subtag'],
        region=parser.region.data['record']['Subtag'],
        script=script,
    )


def handle_locale(locale: str, ignore_region: bool = False) -> Locale:
    """
    Handles a locale input, normalizing it if necessary.
    """
    # If the user passed in `language-region` or `language-script-region`, normalize it.
    if len(locale) > 3:
        return normalize_locale(locale)

    # Case: user passed in `region` and needs a full locale
    try:
        return SELECTOR.from_region(locale)
    except UnknownTerritory:
        pass

    # Case: user passed in `language`, and doesn't care about the region
    if ignore_region:
        verify_locale(locale)
        return Locale(language=locale)

    # Case: user passed in `language` and wants a region
    try:
        language = SELECTOR.from_language(locale)
    except UnknownLanguage:
        pass
    else:
        LeakWarning.warn('no_region')
        return language

    # Locale is not in a valid format.
    raise InvalidLocale.invalid_input(locale)


def handle_locales(locales: Union[str, List[str]], config: Dict[str, Any]) -> None:
    """
    Handles a list of locales.
    """
    if isinstance(locales, str):
        locales = [loc.strip() for loc in locales.split(',')]

    # First, handle the first locale. This will be used for the intl api.
    intl_locale = handle_locale(locales[0])
    config.update(intl_locale.as_config())

    if len(locales) < 2:
        return

    # If additional locales were passed, validate them.
    # Note: in this case, we do not need the region.
    config['locale:all'] = _join_unique(
        handle_locale(locale, ignore_region=True).as_string for locale in locales
    )


def _join_unique(seq: Iterable[str]) -> str:
    """
    Joins a sequence of strings without duplicates
    """
    seen: Set[str] = set()
    return ', '.join(x for x in seq if not (x in seen or seen.add(x)))


"""
Helpers to fetch geolocation, timezone, and locale data given an IP.
"""

MMDB_FILE = LOCAL_DATA / 'GeoLite2-City.mmdb'
MMDB_REPO = "P3TERX/GeoLite.mmdb"


class MaxMindDownloader(GitHubDownloader):
    """
    MaxMind database downloader from a GitHub repository.
    """

    def check_asset(self, asset: Dict) -> Optional[str]:
        # Check for the first -City.mmdb file
        if asset['name'].endswith('-City.mmdb'):
            return asset['browser_download_url']
        return None

    def missing_asset_error(self) -> None:
        raise MissingRelease('Failed to find GeoIP database release asset')


def geoip_allowed() -> None:
    """
    Checks if the geoip2 module is available.
    """
    if not ALLOW_GEOIP:
        raise NotInstalledGeoIPExtra(
            'Please install the geoip extra to use this feature: pip install camoufox[geoip]'
        )


def download_mmdb() -> None:
    """
    Downloads the MaxMind GeoIP2 database.
    """
    geoip_allowed()

    asset_url = MaxMindDownloader(MMDB_REPO).get_asset()

    with open(MMDB_FILE, 'wb') as f:
        webdl(
            asset_url,
            desc='Downloading GeoIP database',
            buffer=f,
        )


def remove_mmdb() -> None:
    """
    Removes the MaxMind GeoIP2 database.
    """
    if not MMDB_FILE.exists():
        rprint("GeoIP database not found.")
        return

    MMDB_FILE.unlink()
    rprint("GeoIP database removed.")


def get_geolocation(ip: str) -> Geolocation:
    """
    Gets the geolocation for an IP address.
    """
    # Check if the database is downloaded
    if not MMDB_FILE.exists():
        download_mmdb()

    # Validate the IP address
    validate_ip(ip)

    with geoip2.database.Reader(str(MMDB_FILE)) as reader:
        resp = reader.city(ip)
        iso_code = cast(str, resp.registered_country.iso_code).upper()
        location = resp.location

        # Check if any required attributes are missing
        if any(not getattr(location, attr) for attr in ('longitude', 'latitude', 'time_zone')):
            raise UnknownIPLocation(f"Unknown IP location: {ip}")

        # Get a statistically correct locale based on the country code
        locale = SELECTOR.from_region(iso_code)

        return Geolocation(
            locale=locale,
            longitude=cast(float, resp.location.longitude),
            latitude=cast(float, resp.location.latitude),
            timezone=cast(str, resp.location.time_zone),
        )


"""
Gets a random language based on the territory code.
"""


def get_unicode_info() -> ET.Element:
    """
    Fetches supplemental data from the territoryInfo.xml file.
    Source: https://raw.githubusercontent.com/unicode-org/cldr/master/common/supplemental/supplementalData.xml
    """
    with open(LOCAL_DATA / 'territoryInfo.xml', 'rb') as f:
        data = ET.XML(f.read())
    assert data is not None, 'Failed to load territoryInfo.xml'
    return data


def _as_float(element: ET.Element, attr: str) -> float:
    """
    Converts an attribute to a float.
    """
    return float(element.get(attr, 0))


# Language subtags Firefox actually ships a localisation for, taken from
# browser/locales/shipped-locales (FF152) with region/variant suffixes
# stripped.
#
# CLDR's territoryInfo lists every language *spoken* in a territory, including
# ones that exist only as a spoken dialect. Sampling that list unfiltered gave
# Germany `nds-DE` (Low German) or `bar-DE` (Bavarian) for 11% of identities,
# Great Britain `sco`, Poland `szl`. There is no Firefox build in Low German,
# so a real Firefox can never report `navigator.language = "nds-DE"` — it is a
# fingerprint no human produces, and a very distinctive one to cluster on.
# Filtering against what Firefox ships keeps the genuinely shipped minority
# locales (sco, szl, oc, hsb all have real builds) and drops only the
# impossible ones.
FIREFOX_UI_LANGUAGES = frozenset((
    'ach', 'af', 'an', 'ar', 'ast', 'az', 'be', 'bg', 'bn', 'br', 'bs', 'ca',
    'cak', 'cs', 'cy', 'da', 'de', 'dsb', 'el', 'en', 'eo', 'es', 'et', 'eu',
    'fa', 'ff', 'fi', 'fr', 'fur', 'fy', 'ga', 'gd', 'gl', 'gn', 'gu', 'he',
    'hi', 'hr', 'hsb', 'hu', 'hy', 'ia', 'id', 'is', 'it', 'ja', 'ka', 'kab',
    'kk', 'km', 'kn', 'ko', 'lij', 'lt', 'lv', 'mk', 'mr', 'ms', 'my', 'nb',
    'ne', 'nl', 'nn', 'oc', 'pa', 'pl', 'pt', 'rm', 'ro', 'ru', 'sat', 'sc',
    'sco', 'si', 'sk', 'skr', 'sl', 'son', 'sq', 'sr', 'sv', 'szl', 'ta',
    'te', 'tg', 'th', 'tl', 'tr', 'trs', 'uk', 'ur', 'uz', 'vi', 'xh', 'zh',
))


# Regions Firefox actually ships an English build for. Its accept-language
# table (intl/locale/rust/locale_service_glue/src/lib.rs) special-cases "en":
# CA, GB and ZA keep their region, and *every other region falls back to
# en-US*. So a real Firefox on a German machine with an English UI reports
# `en-US`, never `en-DE`.
_FIREFOX_EN_REGIONS = frozenset(('CA', 'GB', 'ZA', 'US'))


# browser/locales/shipped-locales (FF152), verbatim. These are the only values
# Firefox's *app locale* can take, and the app locale is what drives
# navigator.language / navigator.languages / Accept-Language.
FIREFOX_SHIPPED_LOCALES = frozenset((
    'ach', 'af', 'an', 'ar', 'ast', 'az', 'be', 'bg', 'bn', 'br', 'bs', 'ca',
    'ca-valencia', 'cak', 'cs', 'cy', 'da', 'de', 'dsb', 'el', 'en-CA',
    'en-GB', 'en-US', 'eo', 'es-AR', 'es-CL', 'es-ES', 'es-MX', 'et', 'eu',
    'fa', 'ff', 'fi', 'fr', 'fur', 'fy-NL', 'ga-IE', 'gd', 'gl', 'gn',
    'gu-IN', 'he', 'hi-IN', 'hr', 'hsb', 'hu', 'hy-AM', 'ia', 'id', 'is',
    'it', 'ja', 'ka', 'kab', 'kk', 'km', 'kn', 'ko', 'lij', 'lt', 'lv', 'mk',
    'mr', 'ms', 'my', 'nb-NO', 'ne-NP', 'nl', 'nn-NO', 'oc', 'pa-IN', 'pl',
    'pt-BR', 'pt-PT', 'rm', 'ro', 'ru', 'sat', 'sc', 'sco', 'si', 'sk',
    'skr', 'sl', 'son', 'sq', 'sr', 'sv-SE', 'szl', 'ta', 'te', 'tg', 'th',
    'tl', 'tr', 'trs', 'uk', 'ur', 'uz', 'vi', 'xh', 'zh-CN', 'zh-TW',
))

# Languages that ship in several regional flavours, where the region the IP
# resolves to gives no answer (a Spanish speaker in Germany still runs one of
# the four es-* builds). Every other regional-only language ships exactly one
# variant, so it is derived instead of listed.
_FIREFOX_DEFAULT_REGION = {'en': 'US', 'es': 'ES', 'pt': 'PT', 'zh': 'CN'}

# Verbatim port of locale_service_default_accept_languages()
# (intl/locale/rust/locale_service_glue/src/lib.rs, FF152). Generated from that
# file; scripts/check_accept_languages.py re-parses the Rust source and fails if
# the two ever drift apart, so a Firefox rebase cannot silently invalidate it.
_FIREFOX_ACCEPT_LANGUAGES = {
    'ace': 'ace, id',
    'ach': 'ach, en-GB',
    'af': 'af, en-ZA, en-GB',
    'ak': 'ak, ak-GH',
    'an': 'an, es-ES, es, ca',
    'ast': 'ast, es-ES, es',
    'az': 'az-AZ, az',
    'bo': 'bo-CN, bo-IN, bo',
    'br': 'br, fr-FR, fr',
    'brx': 'brx, as',
    'bs': 'bs-BA, bs',
    'cak': 'cak, kaq, es',
    'crh': 'tr-TR, tr',
    'cs': 'cs, sk',
    'csb': 'csb, csb-PL, pl',
    'cy': 'cy-GB, cy',
    'dsb': 'dsb, hsb, de',
    'el': 'el-GR, el',
    'et': 'et, et-EE',
    'fa': 'fa-IR, fa',
    'ff': 'ff, fr-FR, fr, en-GB',
    'fi': 'fi-FI, fi',
    'fr': 'fr, fr-FR',
    'frp': 'frp, fr-FR, fr',
    'fur': 'fur-IT, fur, it-IT, it',
    'fy': 'fy-NL, fy, nl',
    'ga': 'ga-IE, ga, en-IE, en-GB',
    'gd': 'gd-GB, gd, en-GB',
    'gl': 'gl-ES, gl',
    'gn': 'gn, es',
    'gv': 'gv, en-GB',
    'he': 'he, he-IL',
    'hr': 'hr, hr-HR',
    'hsb': 'hsb, dsb, de',
    'hto': 'es-MX, es-ES, es, es-AR, es-CL',
    'hu': 'hu-HU, hu',
    'hye': 'hye, hy',
    'ilo': 'ilo-PH, ilo',
    'it': 'it-IT, it',
    'ixl': 'ixl, es-MX, es',
    'ja': 'ja',
    'ka': 'ka-GE, ka',
    'kab': 'kab-DZ, kab, fr-FR, fr',
    'kk': 'kk, ru, ru-RU',
    'kn': 'kn-IN, kn',
    'ko': 'ko-KR, ko',
    'lb': 'lb, de-DE, de',
    'lg': 'lg, en-GB',
    'lij': 'lij, it',
    'lt': 'lt, en-US, en, ru, pl',
    'ltg': 'ltg, lv',
    'mai': 'mai, hi-IN, en',
    'meh': 'meh, es-MX, es',
    'mix': 'mix, es-MX, es',
    'mk': 'mk-MK, mk',
    'ml': 'ml-IN, ml',
    'mr': 'mr-IN, mr',
    'my': 'my, en-GB, en',
    'nb': 'nb-NO, nb, no-NO, no, nn-NO, nn',
    'nn': 'nn-NO, nn, no-NO, no, nb-NO, nb',
    'nr': 'nr-ZA, nr, en-ZA, en-GB',
    'nso': 'nso-ZA, nso, en-ZA, en-GB',
    'oc': 'oc, ca, fr, es, it',
    'pa': 'pa, pa-IN',
    'ppl': 'ppl, es-MX, es',
    'rm': 'rm, rm-CH, de-CH, de',
    'ro': 'ro-RO, ro-GB, en',
    'ru': 'ru-RU, ru',
    'sah': 'sah, ru-RU, ru',
    'sc': 'sc, it-IT, it',
    'scn': 'scn, it-IT, it',
    'sco': 'sco, en-GB, en',
    'si': 'si-LK, si',
    'sk': 'sk, cs',
    'sl': 'sl, en-GB, en',
    'son': 'son, son-ML, fr',
    'sq': 'sq, sq-AL',
    'sr': 'sr-RS, sr',
    'st': 'st-ZA, st, en-ZA, en-GB',
    'szl': 'szl, pl-PL, pl, en, de',
    'ta': 'ta-IN, ta',
    'te': 'te-IN, te',
    'tl': 'tl-PH, tl',
    'tr': 'tr-TR, tr',
    'trs': 'trs, es-MX, es',
    'ts': 'ts-ZA, ts, en-ZA, en-GB',
    'uk': 'uk-UA, uk',
    'ur': 'ur-PK, ur',
    'uz': 'uz, ru',
    've': 've-ZA, ve, en-ZA, en-GB',
    'vi': 'vi-VN, vi',
    'xcl': 'xcl, hy',
    'xh': 'xh-ZA, xh',
    'zam': 'zam, es-MX, es',
}

# Languages whose table entry already ends in an English fallback; Firefox sets
# add_en_us = false for these and does not append ", en-US, en".
_FIREFOX_NO_EN_FALLBACK = frozenset(('en', 'lt', 'my', 'ro', 'sco', 'sl', 'szl'))


def firefox_app_locale(language: str, region: Optional[str] = None) -> str:
    """Map a drawn language + IP region onto a locale Firefox actually ships.

    Firefox only has the builds listed in shipped-locales, and most languages
    ship without a region at all. Picking the app locale here is what keeps
    navigator.language inside the set of values a real Firefox can report.
    """
    language = language.split('-')[0].lower()
    if region:
        tagged = f"{language}-{region.upper()}"
        if tagged in FIREFOX_SHIPPED_LOCALES:
            return tagged
    if language in FIREFOX_SHIPPED_LOCALES:
        return language
    default_region = _FIREFOX_DEFAULT_REGION.get(language)
    if default_region:
        return f"{language}-{default_region}"
    # Languages that ship exactly one regional flavour (fy-NL, sv-SE, ...):
    # take it, whatever the IP says.
    shipped = sorted(
        loc for loc in FIREFOX_SHIPPED_LOCALES if loc.startswith(f"{language}-")
    )
    return shipped[0] if shipped else language


def firefox_accept_languages(app_locale: str) -> str:
    """Reproduce Firefox's default `intl.accept_languages` for an app locale.

    Port of locale_service_default_accept_languages(). Camoufox previously
    composed `<language>-<IP country>, <language>, en-US, en` itself, which put
    a leading tag no Firefox build emits on *every request* — a German identity
    sent `de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7` where a real German Firefox
    sends `de,en-US;q=0.9,en;q=0.8`, and a Dutch speaker on a German IP got the
    outright impossible `nl-DE`. navigator.language then also disagreed with
    Intl.DateTimeFormat().resolvedOptions().locale, which is free to check.
    """
    parts = app_locale.split('-')
    language = parts[0].lower()
    region = parts[1].upper() if len(parts) > 1 and len(parts[1]) == 2 else None

    if language == 'en':
        # Firefox keeps the region only for CA/GB/ZA; everything else is en-US.
        langs = {
            'CA': 'en-CA, en-US, en',
            'GB': 'en-GB, en',
            'ZA': 'en-ZA, en-GB, en-US, en',
        }.get(region or '', 'en-US, en')
    elif language == 'zh' and region == 'CN':
        langs = 'zh-CN, zh, zh-TW, zh-HK'
    elif app_locale == 'ca-valencia':
        langs = 'ca-valencia, ca'
    elif language in _FIREFOX_ACCEPT_LANGUAGES:
        langs = _FIREFOX_ACCEPT_LANGUAGES[language]
    elif region:
        langs = f"{language}-{region}, {language}"
    else:
        langs = language

    if language in _FIREFOX_NO_EN_FALLBACK:
        return langs
    return f"{langs}, en-US, en"


def _firefox_region_for(language: str, region: str) -> str:
    """Map an IP-derived region onto one Firefox would actually pair with.

    Composing `<language>-<IP country>` unconditionally produced tags no
    Firefox build emits — `en-DE`, `en-PL`, `en-FR` — and English is the most
    common second language everywhere, so this hit roughly a third of the
    identities generated for non-English countries. Only English is remapped:
    for other languages Firefox's generic branch really does emit
    `<lang>-<region>, <lang>`, so `de-DE` or `fr-BE` stay as they are.
    """
    if language.split('-')[0].lower() == 'en' and region.upper() not in _FIREFOX_EN_REGIONS:
        return 'US'
    return region


class StatisticalLocaleSelector:
    """
    Selects a random locale based on statistical data.
    Takes either a territory code or a language code, and generates a Locale object.
    """

    def __init__(self):
        self.root = get_unicode_info()

    def _load_territory_data(self, iso_code: str) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calculates a random language based on the territory code,
        based on the probability that a person speaks the language in the territory.
        """
        territory = self.root.find(f"territory[@type='{iso_code}']")
        if territory is None:
            raise UnknownTerritory(f"Unknown territory: {iso_code}")

        lang_populations = territory.findall('languagePopulation')
        if not lang_populations:
            raise ValueError(f"No language data found for region: {iso_code}")

        # Keep only languages Firefox can actually present as its UI, so the
        # draw cannot produce a navigator.language no real Firefox emits
        # (see FIREFOX_UI_LANGUAGES). Fall back to the raw list if a
        # territory has no shipped language at all, so exotic regions still
        # resolve instead of raising.
        shippable = [
            lang for lang in lang_populations
            if (lang.get('type') or '').split('_')[0].lower() in FIREFOX_UI_LANGUAGES
        ]
        if shippable:
            lang_populations = shippable

        languages = np.array([lang.get('type') for lang in lang_populations])
        percentages = np.array([_as_float(lang, 'populationPercent') for lang in lang_populations])

        return self.normalize_probabilities(languages, percentages)

    def _load_language_data(self, language: str) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calculates a random region for a language
        based on the total speakers of the language in that region.
        """
        territories = self.root.findall(f'.//territory/languagePopulation[@type="{language}"]/..')
        if not territories:
            raise UnknownLanguage(f"No region data found for language: {language}")

        regions = []
        percentages = []

        for terr in territories:
            region = terr.get('type')
            if region is None:
                continue  # Skip if region is not found

            lang_pop = terr.find(f'languagePopulation[@type="{language}"]')
            if lang_pop is None:
                continue  # This shouldn't happen due to our XPath, but just in case

            regions.append(region)
            percentages.append(
                _as_float(lang_pop, 'populationPercent')
                * _as_float(terr, 'literacyPercent')
                / 10_000
                * _as_float(terr, 'population')
            )

        if not regions:
            raise ValueError(f"No valid region data found for language: {language}")

        return self.normalize_probabilities(np.array(regions), np.array(percentages))

    def normalize_probabilities(
        self, languages: np.ndarray, freq: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Normalize probabilities.
        """
        total = np.sum(freq)
        return languages, freq / total

    def from_region(self, region: str) -> Locale:
        """
        Get a random locale based on the territory ISO code.
        Returns as a Locale object.
        """
        languages, probabilities = self._load_territory_data(region)
        language = np.random.choice(languages, p=probabilities).replace('_', '-')
        return normalize_locale(f"{language}-{_firefox_region_for(language, region)}")

    def from_language(self, language: str) -> Locale:
        """
        Get a random locale based on the language.
        Returns as a Locale object.
        """
        regions, probabilities = self._load_language_data(language)
        region = np.random.choice(regions, p=probabilities)
        return normalize_locale(f"{language}-{region}")


SELECTOR = StatisticalLocaleSelector()
