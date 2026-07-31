"""navigator.language / Accept-Language must stay inside the set of values a
real Firefox can emit.

Firefox derives intl.accept_languages from its *app locale* (the shipped build),
never from the user's country. Camoufox used to compose
`<language>-<IP country>, <language>, en-US, en`, which put a leading tag no
Firefox build emits on every request and made navigator.language contradict
Intl.DateTimeFormat().resolvedOptions().locale.
"""
import pytest

from camoufox.locale import (
    FIREFOX_SHIPPED_LOCALES,
    firefox_accept_languages,
    firefox_app_locale,
)


@pytest.mark.parametrize(
    'language,region,expected',
    [
        # Most languages ship without a region: the IP country is dropped.
        ('de', 'DE', 'de'),
        ('de', 'AT', 'de'),
        ('nl', 'DE', 'nl'),  # the impossible nl-DE that started this
        ('pl', 'PL', 'pl'),
        ('fr', 'BE', 'fr'),
        # Regional builds are picked when the region actually has one.
        ('en', 'GB', 'en-GB'),
        ('en', 'CA', 'en-CA'),
        ('en', 'DE', 'en-US'),  # no en-DE build exists
        ('pt', 'BR', 'pt-BR'),
        ('pt', 'DE', 'pt-PT'),
        ('es', 'MX', 'es-MX'),
        ('es', 'DE', 'es-ES'),
        ('zh', 'TW', 'zh-TW'),
        ('zh', 'DE', 'zh-CN'),
        # Languages with exactly one regional flavour take it regardless.
        ('sv', 'DE', 'sv-SE'),
        ('nb', 'DE', 'nb-NO'),
        ('fy', 'DE', 'fy-NL'),
    ],
)
def test_app_locale_is_one_firefox_ships(language, region, expected):
    assert firefox_app_locale(language, region) == expected


def test_every_app_locale_is_actually_shipped():
    """No region composition may escape the shipped-locales set."""
    languages = sorted({loc.split('-')[0] for loc in FIREFOX_SHIPPED_LOCALES})
    regions = ['DE', 'US', 'GB', 'BR', 'CN', 'MX', 'PL', 'ZA', 'CA', 'AT']
    for language in languages:
        for region in regions:
            assert firefox_app_locale(language, region) in FIREFOX_SHIPPED_LOCALES


@pytest.mark.parametrize(
    'app_locale,expected',
    [
        # The value a real German / Dutch / Polish Firefox ships.
        ('de', 'de, en-US, en'),
        ('nl', 'nl, en-US, en'),
        ('pl', 'pl, en-US, en'),
        # Table arms with their own fallbacks.
        ('cs', 'cs, sk, en-US, en'),
        ('fr', 'fr, fr-FR, en-US, en'),
        ('it', 'it-IT, it, en-US, en'),
        # add_en_us = false arms must not get the tail appended.
        ('sl', 'sl, en-GB, en'),
        ('ro', 'ro-RO, ro-GB, en'),
        ('szl', 'szl, pl-PL, pl, en, de'),
        ('lt', 'lt, en-US, en, ru, pl'),
        # English keeps a region only for CA / GB / ZA.
        ('en-US', 'en-US, en'),
        ('en-GB', 'en-GB, en'),
        ('en-CA', 'en-CA, en-US, en'),
        # Regional builds outside the table use the generic branch.
        ('pt-BR', 'pt-BR, pt, en-US, en'),
        ('sv-SE', 'sv-SE, sv, en-US, en'),
        ('zh-CN', 'zh-CN, zh, zh-TW, zh-HK, en-US, en'),
        ('zh-TW', 'zh-TW, zh, en-US, en'),
        ('ca-valencia', 'ca-valencia, ca, en-US, en'),
    ],
)
def test_accept_languages_matches_firefox(app_locale, expected):
    assert firefox_accept_languages(app_locale) == expected


def test_first_tag_equals_the_app_locale():
    """navigator.language is the first tag; it has to be the app locale itself,
    otherwise it contradicts Intl.DateTimeFormat().resolvedOptions().locale."""
    # The table's own arms may lead with a regional refinement of the same
    # language (it -> it-IT), which is what Firefox itself does; the language
    # subtag must still match.
    for app_locale in sorted(FIREFOX_SHIPPED_LOCALES):
        first = firefox_accept_languages(app_locale).split(',')[0].strip()
        assert first.split('-')[0] == app_locale.split('-')[0], app_locale


def test_no_impossible_region_composition():
    """The regression: a language-region pair Firefox never ships must never
    reach the output."""
    for language, region in [('nl', 'DE'), ('de', 'DE'), ('pl', 'DE'),
                             ('en', 'DE'), ('en', 'PL'), ('en', 'FR')]:
        tags = firefox_accept_languages(firefox_app_locale(language, region))
        assert f"{language}-{region}" not in tags, tags
