# Third-party code notice

This directory contains vendored third-party code for solving reCAPTCHA
v2 challenges. K-11 (`AUDIT_2026-05-18.md`) flagged the absence of a
licence/origin file; this file is the fix.

## `recapctha_v2/` (note the upstream typo, preserved for import compatibility)

The `recapctha_v2/` subtree is derived from
[`playwright-recaptcha`](https://github.com/Xewdy444/Playwright-recaptcha)
by Xewdy444 and contributors, MIT-licensed. The fork present here
includes local modifications (German-language CLI strings, integration
with the Camoufox scanner, swap to `tenacity` retry).

The upstream MIT licence text follows in full so the redistribution
requirement is satisfied:

```
MIT License

Copyright (c) 2023 Xewdy444

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

If you locate a more authoritative upstream than the one cited above (or
find that local modifications crossed the threshold from "derived work"
into "rewrite"), open a PR updating this NOTICE.

## External API dependencies

The solver wrappers under `meta_text.py`, `object_3d.py`, `rotate.py`,
`slide.py` and the `recapctha_v2/` core call out to:

- **CapSolver** (https://capsolver.com) — paid third-party CAPTCHA API.
  Required when the local audio solver path fails. API key is read from
  `CAPSOLVER_API_KEY`.
- **NVIDIA NIM / Build** — vision models for 3D object / meta-text
  challenges. API keys are read from `NVIDIA_API_KEY` (or the
  more specific `NVIDIA_API_KEY_Qwen` / `NVIDIA_API_KEY_Gemma`).

Operators using these APIs are responsible for complying with the
respective provider terms of service. The Camoufox project does not
ship credentials and does not endorse any specific provider.
