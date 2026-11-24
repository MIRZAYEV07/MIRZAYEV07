#!/usr/bin/env python3
"""Render the profile's SVG panels, in a dark and a light variant, into ../assets.

Edit the CONTENT block, then run:  python3 tools/build.py
No dependencies. System fonts only, so GitHub can render every panel as an <img>.
"""
from __future__ import annotations

from datetime import date
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"
W = 960
PAD = 32  # air above each section panel (GitHub collapses <br> between images)
TODAY = date.today()

# ─────────────────────────────────────────────────────────── CONTENT ──
HANDLE = "MIRZAYEV07"
PLACE = "TASHKENT, UZBEKISTAN · UTC+5"
STATUS = "IN PRODUCTION SINCE 2020"
NAME_TOP, NAME_BOTTOM = "OGABEK", "MIRZOYEV"
SPEC = [
    ("ROLE", "Senior Backend Engineer"),
    ("FOCUS", "High-load · real-time data"),
    ("CORE", "Python · FastAPI · Django"),
    ("DATA", "PostgreSQL · ClickHouse"),
]
# headline figure, shown full width above the grid
LEAD = ("40M", "+", "REGISTERED IN UZBEKISTAN'S NATIONAL CENSUS",
        "Population + agriculture · end to end, from pre-census to the final count")
FIGURES = [  # value, accented suffix, caption, where
    ("15M", "+", "USER ACTIVITIES HANDLED", "census.stat.uz"),
    ("8K", "+", "RPS DURING THE CENSUS", "census.stat.uz"),
    ("5", "+ TB", "IN REAL-TIME STATISTICS", "PostgreSQL + ClickHouse"),
    ("50K", "+", "DAILY ACTIVE USERS", "census + pre-census"),
    ("2.5K", "+", "RPS ON THE AUTH SERVICE", "minisurvey.stat.uz"),
    ("2,000", "+", "STATIONS REGISTERED, LICENSED", "ugaz.uz · live, per dispenser"),
]

# (group, [tech, ...]); a leading "*" marks the tools used most
STACK = [
    ("BACKEND", ["*Python", "*FastAPI", "*Django", "DRF", "SQLAlchemy 2.0", "Pydantic",
                 "Celery", "asyncio", "WebSockets", "Alembic"]),
    ("DATA", ["*PostgreSQL", "*ClickHouse", "PgBouncer", "Redis", "DragonflyDB", "MongoDB",
              "MinIO", "Parquet"]),
    ("STREAMING", ["*Kafka", "Debezium", "PeerDB", "RabbitMQ", "Logical replication"]),
    ("SECURITY", ["OAuth 2.0", "JWT RS256", "RBAC", "OneID SSO", "LDAP / AD", "django-tenants",
                  "KrakenD"]),
    ("DEVOPS", ["*Docker", "Docker Compose", "GitHub Actions", "GitLab CI", "Nginx", "Linux",
                "Nuitka"]),
    ("OBSERVE · TEST", ["Prometheus", "Grafana", "Loki", "pytest", "Locust"]),
    ("INTEGRATIONS", ["OpenAI API", "1C ERP", "RTSP / HLS cameras"]),
]


# ──────────────────────────────────────────────────────────── THEMES ──
THEMES = {
    "dark": dict(
        fg="#F0F6FC", fg2="#C2CAD3", fg3="#959DA8", line="#3D444D", faint="#262C34",
        panel="#161B22", accent="#3FDC5F", tint="#3FDC5F",
        levels=["#1F2630", "#0E4429", "#006D32", "#26A641", "#3FDC5F"],
    ),
    "light": dict(
        fg="#1F2328", fg2="#3D444D", fg3="#636C76", line="#D0D7DE", faint="#EAEEF2",
        panel="#F6F8FA", accent="#1A7F37", tint="#1A7F37",
        levels=["#EBEDF0", "#9BE9A8", "#40C463", "#30A14E", "#216E39"],
    ),
}

MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono','DejaVu Sans Mono',monospace"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif"


# ─────────────────────────────────────────────────────────── HELPERS ──
def css(t: dict) -> str:
    return f"""
.m{{font-family:{MONO}}} .s{{font-family:{SANS}}}
.fg{{fill:{t['fg']}}} .fg2{{fill:{t['fg2']}}} .fg3{{fill:{t['fg3']}}} .ac{{fill:{t['accent']}}}
@keyframes pulse{{0%{{transform:scale(1);opacity:.6}}100%{{transform:scale(3.2);opacity:0}}}}
.pulse{{transform-box:fill-box;transform-origin:center;animation:pulse 2.6s ease-out infinite}}
@media (prefers-reduced-motion:reduce){{.pulse{{animation:none}}}}
"""


def svg(t: dict, h: int, title: str, body: str, top: int = 0, bottom: int = 0) -> str:
    if top:
        body = f'<g transform="translate(0,{top})">{body}</g>'
    h += top + bottom
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}" '
        f'role="img" aria-label="{escape(title)}">\n<title>{escape(title)}</title>\n'
        f"<style>{css(t)}</style>\n{body}\n</svg>\n"
    )


def text(x, y, s, cls="m fg", size=12, anchor="start", weight=None, ls=None) -> str:
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    w = f' font-weight="{weight}"' if weight else ""
    l = f' letter-spacing="{ls}"' if ls is not None else ""
    return f'<text x="{x}" y="{y}" class="{cls}" font-size="{size}"{a}{w}{l}>{escape(s)}</text>'


def line(x1, y1, x2, y2, color, width=1) -> str:
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"/>'


def mark(t: dict, x, y, size=10, gap=3) -> str:
    """Five squares in contribution-graph greens."""
    return "".join(
        f'<rect x="{x + i * (size + gap)}" y="{y}" width="{size}" height="{size}" rx="2" fill="{c}"/>'
        for i, c in enumerate(t["levels"])
    )


def header(t: dict, num: str, title: str, meta: str) -> str:
    return (
        (text(0, 24, num, "m ac", 13, weight=700, ls=2) if num else "")
        + text(38 if num else 0, 24, title.upper(), "m fg", 13, weight=600, ls=3)
        + text(W, 24, meta.upper(), "m fg3", 11.5, anchor="end", ls=2)
        + line(0, 42.5, W, 42.5, t["line"])
        + f'<rect x="0" y="41.5" width="26" height="2" fill="{t["accent"]}"/>'
    )


# ───────────────────────────────────────────────────────────── PANELS ──
def hero(t: dict) -> str:
    b = [
        mark(t, 0, 12),
        text(80, 22, HANDLE, "m fg2", 12, weight=600, ls=2.5),
        text(W, 22, PLACE, "m fg2", 12, anchor="end", ls=2),
        line(0, 44.5, W, 44.5, t["line"]),
        f'<circle cx="5" cy="88" r="4" fill="{t["accent"]}" class="pulse"/>'
        f'<circle cx="5" cy="88" r="4" fill="{t["accent"]}"/>',
        text(20, 92, STATUS, "m fg2", 12, ls=2.2),
        text(-3, 178, NAME_TOP, "s fg", 82, weight=700, ls=-1.5),
        text(-3, 262, NAME_BOTTOM, "s fg3", 82, weight=700, ls=-1.5),
        line(540.5, 124, 540.5, 256, t["line"]),
    ]
    for i, (k, v) in enumerate(SPEC):
        y = 140 + i * 36
        b.append(text(566, y, k, "m fg3", 11.5, ls=2))
        b.append(text(640, y, v, "m fg", 15))
    b.append(line(0, 304.5, W, 304.5, t["line"]))
    val, suf, cap, sub = LEAD
    b.append(
        f'<text x="-2" y="390" class="s fg" font-size="72" font-weight="300" letter-spacing="-1.5">'
        f'{escape(val)}<tspan class="ac">{escape(suf)}</tspan></text>'
    )
    b.append(line(280.5, 334, 280.5, 398, t["line"]))
    b.append(text(306, 358, cap, "m fg2", 11.5, ls=1.6))
    b.append(text(306, 386, sub, "s fg", 16))
    b.append(line(0, 428.5, W, 428.5, t["faint"]))
    col_w, row_h, y0 = 320, 120, 428
    for i, (val, suf, cap, where) in enumerate(FIGURES):
        col, row = i % 3, i // 3
        x, y = col * col_w + (24 if col else 0), y0 + row * row_h
        if col:
            b.append(line(col * col_w + .5, y + 20, col * col_w + .5, y + row_h - 16, t["line"]))
        b.append(
            f'<text x="{x}" y="{y + 64}" class="s fg" font-size="42" font-weight="300" letter-spacing="-0.5">'
            f'{escape(val)}<tspan class="ac">{escape(suf)}</tspan></text>'
        )
        b.append(text(x, y + 88, cap, "m fg2", 11.5, ls=1.6))
        b.append(text(x, y + 106, where, "m fg3", 12))
    b.append(line(0, y0 + row_h + .5, W, y0 + row_h + .5, t["faint"]))
    title = (
        "Ogabek Mirzoyev — Senior Backend Engineer, high-load and real-time data systems. "
        "Python, FastAPI, Django, PostgreSQL, ClickHouse. Tashkent, Uzbekistan. "
        + f"{LEAD[0]}{LEAD[1]} {LEAD[2].lower()}: {LEAD[3].lower()}. "
        + " ".join(f"{v}{s} {c.lower()} ({w})." for v, s, c, w in FIGURES)
    )
    return svg(t, y0 + 2 * row_h, title, "\n".join(b), bottom=PAD)


def label(t: dict, num: str, title: str, meta: str) -> str:
    return svg(t, 54, f"{num} — {title}", header(t, num, title, meta), top=PAD)


def stack(t: dict) -> str:
    b = [header(t, "", "Stack", "what I run in production")]
    x0, chip_h, gap, row_gap, size = 180, 32, 8, 12, 14
    chip_w = lambda name: round(len(name.lstrip("*")) * size * 0.62 + 26)  # noqa: E731
    y = 72
    for group, items in STACK:
        b.append(text(0, y + 21, group, "m fg2", 11.5, weight=600, ls=2))
        # balanced wrap: split a long group into lines of similar width, no orphans
        total = sum(chip_w(i) + gap for i in items) - gap
        lines = -(-total // (W - x0))
        target = total / lines
        x, used = x0, 0
        for raw in items:
            hot = raw.startswith("*")
            name = raw.lstrip("*")
            w = chip_w(raw)
            if used and (used + w > target + 40 or x + w > W):
                x, y, used = x0, y + chip_h + gap, 0
            used += w + gap
            stroke = t["accent"] if hot else t["line"]
            fill = (f'fill="{t["tint"]}" fill-opacity=".12"' if hot else f'fill="{t["panel"]}"')
            b.append(
                f'<rect x="{x + .5}" y="{y + .5}" width="{w - 1}" height="{chip_h - 1}" rx="6" '
                f'{fill} stroke="{stroke}"/>'
            )
            b.append(text(x + w / 2, y + 21, name, "m fg", size, anchor="middle",
                          weight=600 if hot else None))
            x += w + gap
        y += chip_h + row_gap
        b.append(line(0, y - row_gap / 2 + .5, W, y - row_gap / 2 + .5, t["faint"]))
    h = y
    title = "Stack. " + " ".join(
        f"{g.title()}: " + ", ".join(i.lstrip('*') for i in items) + "." for g, items in STACK
    )
    return svg(t, h, title, "\n".join(b), top=PAD)


def footer(t: dict) -> str:
    b = [line(0, 0.5, W, 0.5, t["line"]), mark(t, W / 2 - 31, 24)]
    return svg(t, 48, "", "\n".join(b), top=PAD)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("*.svg"):
        old.unlink()
    for theme, t in THEMES.items():
        panels = {
            "hero": hero(t),
            "stack": stack(t),
            "footer": footer(t),
        }
        for stem, content in panels.items():
            (OUT / f"{stem}-{theme}.svg").write_text(content, encoding="utf-8")
    print(f"wrote {len(list(OUT.glob('*.svg')))} svgs → {OUT}")


if __name__ == "__main__":
    main()
