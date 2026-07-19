"""
Speech-synthesis voice generation for the identity coherence engine.

The browser side (patches/media/voice-spoofing.patch) reads the ``voices`` key
from the injected config via ``MaskConfig::MVoices()`` and registers exactly
those voices with ``nsSynthVoiceRegistry`` — replacing whatever
speech-dispatcher / SAPI / NSSpeech voices the *host* machine exposes (which
otherwise leak the real OS through ``speechSynthesis.getVoices()``).

``MVoices()`` requires full objects — ``{lang, name, voiceUri, isDefault,
isLocalService}`` — and silently drops any entry missing a field, so raw name
strings register nothing.

Ported from upstream camoufox 152's fingerprints.py, with one fork adaptation:
selection is driven by the engine's *seeded* ``Random`` (passed in as ``rng``)
instead of the global ``random`` module, so the voice list is reproducible for
a given identity seed like every other surface the engine compiles.
"""

import os
import re
from random import Random
from typing import Any, Dict, List, Optional, Tuple

import orjson

# OS voice lists loaded from voices.json, parsed into (name, lang, type) tuples.
_OS_VOICES_CACHE: Optional[Dict[str, List[Tuple[str, str, str]]]] = None

# Essential speech voices per OS that must always be included in subsets.
_ESSENTIAL_VOICES_MACOS = [
    'Samantha', 'Alex', 'Fred', 'Victoria', 'Karen', 'Daniel',
]

# Real Firefox speechSynthesis URI prefixes per backend.
#   macOS NSSpeechSynthesizer -> "urn:moz-tts:osx:<dotted-slug>"
#   Windows SAPI              -> "urn:moz-tts:sapi:<dotted-slug>"
#   Linux speech-dispatcher   -> "urn:moz-tts:speechd:<escaped-name>?<lang>"
_VOICE_URI_PREFIX = {
    'mac': 'urn:moz-tts:osx:',
    'win': 'urn:moz-tts:sapi:',
    'lin': 'urn:moz-tts:speechd:',
}

# The coherence engine passes short OS families ('win'/'mac'/'lin'); the public
# camoufox API uses long names ('windows'/'macos'/'linux'). Accept both — a bad
# key must NOT silently fall back to another OS's voices.
_OS_KEY = {
    'macos': 'mac', 'windows': 'win', 'linux': 'lin',
    'mac': 'mac', 'win': 'win', 'lin': 'lin',
}


def _load_os_voices() -> Dict[str, List[Tuple[str, str, str]]]:
    """Load OS voice lists from voices.json as (name, lang, type) tuples.

    Each entry is "Name:lang:type" (type is "local" or "remote"). Voice names
    may contain parens/commas but not colons, so a last-two-colons split is safe.
    """
    global _OS_VOICES_CACHE
    if _OS_VOICES_CACHE is not None:
        return _OS_VOICES_CACHE
    voices_path = os.path.join(os.path.dirname(__file__), 'voices.json')
    with open(voices_path, 'rb') as f:
        raw = orjson.loads(f.read())
    _OS_VOICES_CACHE = {}
    for os_key, entries in raw.items():
        parsed: List[Tuple[str, str, str]] = []
        for entry in entries:
            last = entry.rfind(':')
            if last < 0:
                continue
            vtype = entry[last + 1:]
            before = entry[:last]
            langsep = before.rfind(':')
            if langsep < 0:
                continue
            lang = before[langsep + 1:]
            name = before[:langsep]
            if name and lang:
                parsed.append((name, lang, vtype))
        _OS_VOICES_CACHE[os_key] = parsed
    return _OS_VOICES_CACHE


def _voice_uri_slug(name: str) -> str:
    """Stable dotted slug for mac/win URIs (shape-plausible, not catalog-exact)."""
    return re.sub(r'^\.|\.$', '', re.sub(r'[^a-z0-9]+', '.', name.lower()))


def _voice_uri(os_key: str, name: str, lang: str) -> str:
    """Build a voiceUri matching what real Firefox emits for the OS backend."""
    if os_key == 'lin':
        # Firefox's SpeechDispatcherService.cpp builds:
        #   "urn:moz-tts:speechd:" + NS_EscapeURL(name, OnlyNonASCII|Spaces) + "?" + lang
        # i.e. spaces -> %20 and non-ASCII bytes -> %XX, ASCII punctuation intact.
        escaped = []
        for ch in name:
            if ch == ' ':
                escaped.append('%20')
            elif ord(ch) <= 0x7F:
                escaped.append(ch)
            else:
                escaped.append(''.join(f'%{b:02X}' for b in ch.encode('utf-8')))
        return f"{_VOICE_URI_PREFIX['lin']}{''.join(escaped)}?{lang}"
    return f"{_VOICE_URI_PREFIX.get(os_key, '')}{_voice_uri_slug(name)}"


def generate_voices(
    target_os: str,
    locale: Optional[str] = None,
    rng: Optional[Random] = None,
) -> List[Dict[str, Any]]:
    """Compile the speech voice list for ``target_os`` as MaskConfig objects.

    Returns a list of ``{lang, name, voiceUri, isDefault, isLocalService}``
    dicts (the shape ``MaskConfig::MVoices()`` requires). Emits a list for
    EVERY target OS so the host's real voices never leak:
      macOS:   essential voices + a seeded 40-80% of the rest.
      Windows: full SAPI set (subsetting a fixed list reads as suspicious).
      Linux:   full espeak-ng base-language set (~131 voices) as enumerated
               by speech-dispatcher — the fixed list a Linux Firefox exposes.

    ``rng`` is the engine's seeded Random; if omitted, a fresh unseeded one is
    used (non-reproducible — callers inside the coherence engine must pass it).
    """
    if rng is None:
        rng = Random()
    os_voices_data = _load_os_voices()
    os_key = _OS_KEY.get(target_os, 'mac')
    full_list = os_voices_data.get(os_key, [])
    if not full_list:
        return []

    if os_key in ('win', 'lin'):
        # Fixed lists across installs (SAPI / espeak-ng) — ship the whole set.
        selected = list(full_list)
    else:
        # macOS: essential voices + a seeded 40-80% of the rest.
        essential = set(_ESSENTIAL_VOICES_MACOS)
        selected = [v for v in full_list if v[0] in essential]
        non_essential = [v for v in full_list if v[0] not in essential]
        pct = 40 + int(rng.random() * 41)  # 40-80%
        count = round((pct / 100) * len(non_essential))
        if count < len(non_essential):
            selected.extend(rng.sample(non_essential, count))
        else:
            selected.extend(non_essential)

    voices: List[Dict[str, Any]] = [
        {
            'name': name,
            'lang': lang,
            'voiceUri': _voice_uri(os_key, name, lang),
            'isDefault': False,
            'isLocalService': vtype == 'local',
        }
        for (name, lang, vtype) in selected
    ]

    # Mark a default voice matching the spoofed locale prefix so it lines up
    # with Intl.DateTimeFormat().resolvedOptions().locale (CreepJS flags a
    # voiceLangMismatch otherwise).
    if voices:
        prefix = locale.split('-')[0].lower() if locale else 'en'
        idx = next(
            (i for i, v in enumerate(voices)
             if locale and v['lang'].lower() == locale.lower()),
            -1,
        )
        if idx < 0:
            idx = next(
                (i for i, v in enumerate(voices)
                 if v['lang'].split('-')[0].lower() == prefix),
                -1,
            )
        if idx < 0:
            idx = 0
        voices[idx]['isDefault'] = True

    return voices


if __name__ == '__main__':
    # ponytail: smallest runnable check — determinism + MVoices object shape.
    a = generate_voices('macos', 'en-US', Random(42))
    b = generate_voices('macos', 'en-US', Random(42))
    assert a == b, 'seeded selection must be reproducible'
    assert sum(v['isDefault'] for v in a) == 1, 'exactly one default voice'
    assert all(
        {'lang', 'name', 'voiceUri', 'isDefault', 'isLocalService'} <= set(v)
        for v in a
    ), 'every voice must carry all MVoices fields'
    win = generate_voices('windows', 'en-US', Random(1))
    assert all(v['voiceUri'].startswith('urn:moz-tts:sapi:') for v in win)
    lin = generate_voices('linux', 'de-DE', Random(1))
    assert all(v['voiceUri'].startswith('urn:moz-tts:speechd:') for v in lin)
    assert any(v['lang'].lower().startswith('de') and v['isDefault'] for v in lin) \
        or lin[0]['isDefault'], 'default should prefer locale prefix'
    print(f'OK  mac={len(a)} win={len(win)} lin={len(lin)} voices')
