"""
human_mouse.py
══════════════════════════════════════════════════════════════════════
Pure-Python-Port von Camoufox' C++ `HumanizeMouseTrajectory`
(additions/camoucfg/MouseTrajectories.hpp).

WICHTIG: Diese Implementierung läuft KOMPLETT auf der Python-Seite
(über Playwright's `page.mouse`-API). Sie ist *separat* vom Browser —
es wird kein C++- oder Juggler-Code aufgerufen. Damit funktionieren
die CAPTCHA-Solver auch ohne das Camoufox-Patch-Set, z.B. unter
vanilla Playwright-Firefox oder Chromium.

Algorithmus (identisch zum C++-Original, das wiederum auf riflosnake's
`humancursor` basiert):

  1. Bounding-Box ±80 px um die Linie vom Start- zum Endpunkt
  2. Zwei zufällige interne Knotenpunkte werden innerhalb dieser Box
     gewählt → erzeugt einen Bezier-Curve mit Krümmung
  3. Bernstein-Polynom (4 Kontrollpunkte: start + 2 knots + end)
     wird mit `n = max(|dx|, |dy|, 2)` Samples ausgewertet
  4. Y-Achsen-Distortion: Gauss-Noise (mean=1, stddev=1) wird auf
     ~50 % der inneren Punkte addiert
  5. Tween mit `easeOutQuad`-Easing → langsamer am Ende
  6. Endgültige Punkt-Anzahl: `pow(totalLength, 0.25) * 20`,
     geclampt auf [min_time+2, max_time]
  7. Duplikate (gleiche int-Koordinate) werden entfernt

Verwendung:
    from .human_mouse import humanized_drag, humanized_click, humanized_move

    # Slider ziehen:
    await humanized_drag(page, (knob_x, knob_y), (target_x, target_y))

    # Klick auf Koordinate:
    await humanized_click(page, target_x, target_y)

    # Nur Bewegung (kein Click):
    await humanized_move(page, (knob_x, knob_y), (target_x, target_y))
"""

from __future__ import annotations

import asyncio
import math
import random
from typing import List, Tuple

Point = Tuple[float, float]


# ══════════════════════════════════════════════════════════════════
#  Bezier-Mathematik  (1:1 Port der C++-Bezier-Klasse)
# ══════════════════════════════════════════════════════════════════

def _binomial(n: int, k: int) -> float:
    """Iterativer Binomialkoeffizient (double-stabil für n > 20)."""
    if k < 0 or k > n:
        return 0.0
    if k == 0 or k == n:
        return 1.0
    if k > n - k:
        k = n - k
    result = 1.0
    for i in range(k):
        result *= (n - i)
        result /= (i + 1)
    return result


def _bernstein_point(x: float, i: int, n: int) -> float:
    return _binomial(n, i) * (x ** i) * ((1 - x) ** (n - i))


def _bernstein(points: List[Point], t: float) -> Point:
    n = len(points) - 1
    x = 0.0
    y = 0.0
    for i in range(n + 1):
        bern = _bernstein_point(t, i, n)
        x += points[i][0] * bern
        y += points[i][1] * bern
    return (x, y)


def _calculate_points_in_curve(n_points: int, control_points: List[Point]) -> List[Point]:
    """Sampelt `n_points` gleichmäßig entlang der Bezier-Kurve."""
    if n_points <= 1:
        return [control_points[0], control_points[-1]]
    curve: List[Point] = []
    for i in range(n_points):
        t = i / (n_points - 1)
        curve.append(_bernstein(control_points, t))
    return curve


# ══════════════════════════════════════════════════════════════════
#  HumanizeMouseTrajectory
# ══════════════════════════════════════════════════════════════════

def _ease_out_quad(n: float) -> float:
    """Easing-Funktion: -n * (n - 2). Macht den Slider am Ziel langsamer."""
    if n < 0.0:
        n = 0.0
    elif n > 1.0:
        n = 1.0
    return -n * (n - 2)


def _generate_internal_knots(
    l_bound: float, r_bound: float, d_bound: float, u_bound: float,
    knots_count: int,
    rng: random.Random,
) -> List[Point]:
    """Erzeugt N zufällige interne Knotenpunkte innerhalb der Bounding-Box."""
    knots: List[Point] = []
    for _ in range(knots_count):
        kx = rng.uniform(l_bound, r_bound)
        ky = rng.uniform(d_bound, u_bound)
        knots.append((kx, ky))
    return knots


def _distort_points(
    points: List[Point],
    distortion_mean: float,
    distortion_stddev: float,
    distortion_frequency: float,
    rng: random.Random,
) -> List[Point]:
    """Y-Achsen-Gauss-Noise auf inneren Punkten (≈50 % betroffen)."""
    if len(points) <= 2:
        return list(points)
    distorted: List[Point] = [points[0]]
    for i in range(1, len(points) - 1):
        x, y = points[i]
        delta = 0.0
        if rng.random() < distortion_frequency:
            delta = round(rng.gauss(distortion_mean, distortion_stddev))
        distorted.append((x, y + delta))
    distorted.append(points[-1])
    return distorted


def _tween_points(
    points: List[Point],
    max_time: int = 150,
    min_time: int = 2,
) -> List[Point]:
    """Re-samplet die Kurve mit easeOutQuad-Zeitmapping.

    Die Punkt-Anzahl wird über `pow(totalLength, 0.25) * 20` skaliert
    und auf [min_time+2, max_time] geclamped — exakt wie das C++-Original.
    """
    if len(points) < 2:
        return list(points)

    total_length = 0.0
    for i in range(1, len(points)):
        dx = points[i][0] - points[i - 1][0]
        dy = points[i][1] - points[i - 1][1]
        total_length += math.sqrt(dx * dx + dy * dy)

    target_points = min(
        max_time,
        max(min_time + 2, int((total_length ** 0.25) * 20)),
    )

    res: List[Point] = []
    n = len(points)
    for i in range(target_points):
        t = i / (target_points - 1) if target_points > 1 else 0.0
        eased = _ease_out_quad(t)
        index = int(eased * (n - 1))
        if index >= n:
            index = n - 1
        res.append(points[index])
    return res


def generate_curve(
    from_xy: Point,
    to_xy: Point,
    *,
    boundary_padding: float = 80.0,
    internal_knots: int = 2,
    distortion_mean: float = 1.0,
    distortion_stddev: float = 1.0,
    distortion_frequency: float = 0.5,
    max_time: int = 150,
    min_time: int = 2,
    seed: int | None = None,
) -> List[Tuple[int, int]]:
    """Erzeugt eine menschlich wirkende Punkt-Kette von `from_xy` nach `to_xy`.

    Returns:
        Liste von (x, y)-int-Tupeln. Aufeinanderfolgende Duplikate sind
        bereits entfernt. Erster Punkt = from_xy, letzter = to_xy.
    """
    rng = random.Random(seed) if seed is not None else random.Random()

    fx, fy = from_xy
    tx, ty = to_xy

    left = min(fx, tx) - boundary_padding
    right = max(fx, tx) + boundary_padding
    down = min(fy, ty) - boundary_padding
    up = max(fy, ty) + boundary_padding

    knots = _generate_internal_knots(left, right, down, up, internal_knots, rng)

    # Punkt-Anzahl proportional zur Distanz, mindestens 2.
    mid_pts = int(max(abs(fx - tx), abs(fy - ty), 2.0))

    control_points: List[Point] = [from_xy, *knots, to_xy]
    curve = _calculate_points_in_curve(mid_pts, control_points)

    distorted = _distort_points(
        curve, distortion_mean, distortion_stddev, distortion_frequency, rng
    )
    tweened = _tween_points(distorted, max_time=max_time, min_time=min_time)

    # Int-Konvertierung + Duplikate entfernen
    out: List[Tuple[int, int]] = []
    prev: Tuple[int, int] | None = None
    for px, py in tweened:
        ix, iy = int(round(px)), int(round(py))
        if (ix, iy) == prev:
            continue
        out.append((ix, iy))
        prev = (ix, iy)

    # Sicherheit: erster + letzter Punkt müssen exakt stimmen
    if out and out[0] != (int(round(fx)), int(round(fy))):
        out.insert(0, (int(round(fx)), int(round(fy))))
    if out and out[-1] != (int(round(tx)), int(round(ty))):
        out.append((int(round(tx)), int(round(ty))))
    return out


# ══════════════════════════════════════════════════════════════════
#  Playwright-Bindings  (drag / click / move)
# ══════════════════════════════════════════════════════════════════

# Per-Step-Pause-Range. Wird zwischen jedem trajectory-Punkt gewartet.
# Default ergibt eine Gesamt-Bewegungszeit von ca. 0.3-1.5s je nach
# Distanz (Anzahl Punkte × Pause).
_DEFAULT_STEP_DELAY_MIN_MS = 4
_DEFAULT_STEP_DELAY_MAX_MS = 12


async def _walk_curve(
    page,
    curve: List[Tuple[int, int]],
    step_delay_min_ms: int,
    step_delay_max_ms: int,
) -> None:
    """Bewegt die Maus entlang einer pre-computed Trajektorie."""
    rng = random.Random()
    for (x, y) in curve:
        # Jeder einzelne move ist `steps=1` damit die Pausen wirken.
        # Würden wir steps>1 nehmen, würde Playwright intern linear
        # interpolieren und unsere Bezier-Punkte überrennen.
        await page.mouse.move(float(x), float(y), steps=1)
        if step_delay_max_ms > 0:
            await asyncio.sleep(rng.randint(step_delay_min_ms, step_delay_max_ms) / 1000.0)


async def humanized_move(
    page,
    from_xy: Point,
    to_xy: Point,
    *,
    step_delay_min_ms: int = _DEFAULT_STEP_DELAY_MIN_MS,
    step_delay_max_ms: int = _DEFAULT_STEP_DELAY_MAX_MS,
    max_time: int = 150,
    min_time: int = 2,
) -> None:
    """Reine Mausbewegung von `from_xy` nach `to_xy` entlang Bezier-Kurve."""
    curve = generate_curve(from_xy, to_xy, max_time=max_time, min_time=min_time)
    await _walk_curve(page, curve, step_delay_min_ms, step_delay_max_ms)


async def humanized_drag(
    page,
    from_xy: Point,
    to_xy: Point,
    *,
    pre_press_pause_ms: Tuple[int, int] = (80, 220),
    post_release_pause_ms: Tuple[int, int] = (200, 500),
    step_delay_min_ms: int = _DEFAULT_STEP_DELAY_MIN_MS,
    step_delay_max_ms: int = _DEFAULT_STEP_DELAY_MAX_MS,
    max_time: int = 150,
    min_time: int = 2,
) -> None:
    """Maus-Drag (down → bewegen → up) entlang Bezier-Kurve.

    Reihenfolge:
      1. mouse.move zur Startposition (ohne down)
      2. mouse.down  + kurze menschliche Pause
      3. mouse.move entlang Trajektorie
      4. kurze Pause vor release
      5. mouse.up
    """
    rng = random.Random()

    # 1. Cursor auf Startpunkt setzen (ohne Click)
    await page.mouse.move(float(from_xy[0]), float(from_xy[1]), steps=1)

    # 2. Pressen + kurze Pause (echter Mensch hält den Knopf nicht
    # 0ms gedrückt bevor er zieht — ~80-220ms Reaktionszeit)
    await page.mouse.down()
    await asyncio.sleep(rng.randint(*pre_press_pause_ms) / 1000.0)

    # 3. Curve abfahren
    curve = generate_curve(from_xy, to_xy, max_time=max_time, min_time=min_time)
    await _walk_curve(page, curve, step_delay_min_ms, step_delay_max_ms)

    # 4. Kurze Pause bevor losgelassen wird (Captcha-Server messen oft
    # diese Pause; 0ms wirkt mechanisch)
    await asyncio.sleep(rng.randint(*post_release_pause_ms) / 1000.0)

    # 5. Loslassen
    await page.mouse.up()


async def humanized_click(
    page,
    x: float,
    y: float,
    *,
    from_xy: Point | None = None,
    jitter_px: float = 1.5,
    pre_click_pause_ms: Tuple[int, int] = (60, 180),
    click_hold_ms: Tuple[int, int] = (40, 110),
    step_delay_min_ms: int = _DEFAULT_STEP_DELAY_MIN_MS,
    step_delay_max_ms: int = _DEFAULT_STEP_DELAY_MAX_MS,
) -> None:
    """Bewege Maus menschlich zur Position (x, y) und klicke.

    Wenn `from_xy` None ist, wird ein zufälliger Startpunkt in 100-300 px
    Distanz benutzt (für realistisches Anfahren).
    """
    rng = random.Random()

    # Mikro-Jitter (echter Mensch trifft nie pixel-perfekt)
    tx = x + rng.uniform(-jitter_px, jitter_px)
    ty = y + rng.uniform(-jitter_px, jitter_px)

    if from_xy is None:
        # Zufälliger Startpunkt nahe dem Ziel — simuliert "Maus war
        # gerade irgendwo". Würde der Test-Code immer von (0,0) starten,
        # entstünde ein verräterischer Sweep über den ganzen Schirm.
        angle = rng.uniform(0, 2 * math.pi)
        radius = rng.uniform(80, 220)
        from_xy = (tx + math.cos(angle) * radius, ty + math.sin(angle) * radius)

    # Anfahren
    curve = generate_curve(from_xy, (tx, ty))
    await _walk_curve(page, curve, step_delay_min_ms, step_delay_max_ms)

    # Mini-Pause bevor Click (Reaktionszeit)
    await asyncio.sleep(rng.randint(*pre_click_pause_ms) / 1000.0)

    # Echter Click via down/up mit "hold"-Dauer (manche Sites messen das)
    await page.mouse.down()
    await asyncio.sleep(rng.randint(*click_hold_ms) / 1000.0)
    await page.mouse.up()
