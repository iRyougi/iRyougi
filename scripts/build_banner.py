"""生成 assets/banner.svg（浅色）与 assets/banner-dark.svg（深色）。

用法：python scripts/build_banner.py
两版共用同一份模板，只换配色，改动这里即可同步两边。
"""
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"

CLAY = "#D97757"
CLAY_DEEP = "#C6613F"
INK = "#141413"
PETAL = "#F5E9D8"

THEMES = {
    "banner.svg": {
        "bg": "#F0EEE6", "frame": "#E3DACC", "title": INK, "sub": "#3D3D3A",
        "muted": "#87867F", "pill_fill": INK, "pill_text": "#F0EEE6",
        "outline": INK, "outline_text": INK, "ghost": "#87867F",
    },
    "banner-dark.svg": {
        "bg": "#1F1E1D", "frame": "#3A3936", "title": "#F0EEE6", "sub": "#C2C0B6",
        "muted": "#87867F", "pill_fill": CLAY, "pill_text": INK,
        "outline": "#87867F", "outline_text": "#F0EEE6", "ghost": "#F0EEE6",
    },
}

# (起点 x, 终点 x, 时长 s, 延迟 s, 大小倍率)
PETALS = [
    (1010, 900, 9.0, -1.0, 1.0),
    (1080, 1150, 11.0, -4.0, 0.8),
    (960, 760, 10.0, -6.5, 0.9),
    (1120, 1000, 8.0, -2.5, 0.7),
    (900, 640, 12.0, -8.0, 0.8),
    (1040, 1180, 9.5, -5.0, 0.6),
    (840, 560, 13.0, -10.0, 0.7),
]

STRIPES = [  # (path, 方向 1=从右滑入 -1=从左滑入)
    ("M1200 34 L1068 62 L1200 88 Z", 1),
    ("M1200 128 L1110 146 L1200 160 Z", 1),
    ("M1200 300 L1052 332 L1200 352 Z", 1),
    ("M812 52 L900 74 L822 92 Z", -1),
    ("M800 236 L884 252 L808 270 Z", -1),
    ("M818 344 L912 362 L826 382 Z", -1),
]

BLOB = "M820 0 C 770 70, 860 120, 805 200 C 755 270, 850 330, 800 400 L1200 400 L1200 0 Z"


def petal_css() -> str:
    rules = []
    for i, (x0, x1, dur, delay, _) in enumerate(PETALS):
        rules.append(
            f"@keyframes fall{i} {{"
            f"0% {{ transform: translate({x0}px,-30px) rotate(0deg); opacity: 0; }}"
            f"8% {{ opacity: .95; }}"
            f"85% {{ opacity: .9; }}"
            f"100% {{ transform: translate({x1}px,430px) rotate(600deg); opacity: 0; }} }}"
            f".pt{i} {{ animation: fall{i} {dur}s linear {delay}s infinite; }}"
        )
    return "\n      ".join(rules)


def stripe_css() -> str:
    rules = []
    for i, (_, direction) in enumerate(STRIPES):
        rules.append(f".st{i} {{ animation: slide{'R' if direction > 0 else 'L'} .7s cubic-bezier(.2,.8,.2,1) {0.5 + i * 0.12:.2f}s both; }}")
    return "\n      ".join(rules)


def petals_svg() -> str:
    out = []
    for i, (*_, scale) in enumerate(PETALS):
        rx, ry = 6 * scale, 15 * scale
        out.append(
            f'<g class="pt{i}"><ellipse rx="{rx:.1f}" ry="{ry:.1f}" fill="{PETAL}" '
            f'stroke="{INK}" stroke-width="1.6"/></g>'
        )
    return "\n    ".join(out)


def daisy_svg() -> str:
    petals = "\n        ".join(
        f'<ellipse cx="1040" cy="132" rx="15" ry="52" transform="rotate({k * 22.5} 1040 184)"/>'
        for k in range(16)
    )
    return f"""<g class="daisy">
      <g fill="{PETAL}" stroke="{INK}" stroke-width="2.5">
        {petals}
      </g>
      <circle cx="1040" cy="184" r="34" fill="{INK}"/>
      <circle cx="1040" cy="184" r="21" fill="{PETAL}"/>
      <circle cx="1040" cy="184" r="11" fill="{INK}"/>
    </g>"""


def build(t: dict) -> str:
    stripes = "\n      ".join(
        f'<path class="st{i}" d="{d}"/>' for i, (d, _) in enumerate(STRIPES)
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 400" width="1200" height="400" role="img" aria-labelledby="t d">
  <title id="t">苏幽璃 · iRyougi</title>
  <desc id="d">Claude 配色的动态个人主页横幅：陶土橙色块、虎纹剪纸、旋转的雏菊发饰与飘落的花瓣。</desc>
  <defs>
    <clipPath id="card"><rect width="1200" height="400" rx="28"/></clipPath>
    <clipPath id="blob"><path d="{BLOB}"/></clipPath>
    <clipPath id="typed"><rect x="192" y="76" height="26" width="0">
      <animate attributeName="width" begin="0.3s" dur="0.9s" fill="freeze" calcMode="discrete"
        values="0;12;23;34;45;56;70" keyTimes="0;0.16;0.33;0.5;0.66;0.83;1"/>
    </rect></clipPath>
    <linearGradient id="shine" x1="0" x2="1" y1="0" y2="0">
      <stop offset="0" stop-color="#fff" stop-opacity="0"/>
      <stop offset=".5" stop-color="#fff" stop-opacity=".38"/>
      <stop offset="1" stop-color="#fff" stop-opacity="0"/>
    </linearGradient>
    <style>
      .serif {{ font-family: "Tiempos Headline", "Noto Serif SC", "Source Han Serif SC", "Songti SC", Georgia, serif; }}
      .sans  {{ font-family: "Styrene A", -apple-system, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif; }}
      .mono  {{ font-family: "JetBrains Mono", "SFMono-Regular", Consolas, Menlo, monospace; }}
      .fb    {{ transform-box: fill-box; }}

      @keyframes blobIn {{ from {{ transform: translateX(440px); }} to {{ transform: none; }} }}
      @keyframes rise   {{ from {{ opacity: 0; transform: translateY(16px); }} to {{ opacity: 1; transform: none; }} }}
      @keyframes grow   {{ from {{ transform: scaleX(0); }} to {{ transform: scaleX(1); }} }}
      @keyframes slideR {{ from {{ opacity: 0; transform: translateX(140px); }} to {{ opacity: 1; transform: none; }} }}
      @keyframes slideL {{ from {{ opacity: 0; transform: translateX(-80px); }} to {{ opacity: 1; transform: none; }} }}
      @keyframes pop    {{ 0% {{ transform: scale(0) rotate(-120deg); }} 70% {{ transform: scale(1.08) rotate(8deg); }} 100% {{ transform: none; }} }}
      @keyframes spin   {{ to {{ transform: rotate(360deg); }} }}
      @keyframes sway   {{ 0%,100% {{ transform: rotate(-2deg); }} 50% {{ transform: rotate(2deg); }} }}
      @keyframes blink  {{ 50% {{ opacity: 0; }} }}
      @keyframes sweep  {{ 0%, 55% {{ transform: translateX(-260px) skewX(-20deg); }} 100% {{ transform: translateX(560px) skewX(-20deg); }} }}
      @keyframes glitchA {{ 0%, 86%, 100% {{ opacity: 0; transform: none; }} 87% {{ opacity: .9; transform: translate(-6px, 2px); }} 89% {{ opacity: .9; transform: translate(5px, -2px); }} 91% {{ opacity: 0; }} }}
      @keyframes glitchB {{ 0%, 87%, 100% {{ opacity: 0; transform: none; }} 88% {{ opacity: .8; transform: translate(6px, -1px); }} 90% {{ opacity: .8; transform: translate(-4px, 2px); }} 92% {{ opacity: 0; }} }}
      @keyframes jitter  {{ 0%, 86%, 92%, 100% {{ transform: none; }} 88% {{ transform: translateX(2px); }} 90% {{ transform: translateX(-2px); }} }}

      .blobIn {{ animation: blobIn 1s cubic-bezier(.2,.8,.2,1) both; }}
      .r1 {{ animation: rise .8s cubic-bezier(.2,.8,.2,1) .2s both; }}
      .r2 {{ animation: rise .8s cubic-bezier(.2,.8,.2,1) .45s both; }}
      .r3 {{ animation: rise .8s cubic-bezier(.2,.8,.2,1) .9s both; }}
      .r4 {{ animation: rise .8s cubic-bezier(.2,.8,.2,1) 1.1s both; }}
      .bar {{ transform-origin: left center; animation: grow .7s cubic-bezier(.2,.8,.2,1) .8s both; }}
      .popIn {{ transform-origin: center; animation: pop 1s cubic-bezier(.2,.8,.2,1) .7s both; }}
      .daisy {{ transform-box: fill-box; transform-origin: center; animation: spin 24s linear 1.7s infinite; }}
      .sway  {{ transform-box: fill-box; transform-origin: top center; animation: sway 6s ease-in-out infinite; }}
      .blink {{ animation: blink 1.1s steps(1) infinite; }}
      .sweep {{ animation: sweep 6s ease-in-out 1.5s infinite; }}
      .gA {{ animation: glitchA 7s steps(1) 2s infinite; }}
      .gB {{ animation: glitchB 7s steps(1) 2s infinite; }}
      .jit {{ animation: jitter 7s steps(1) 2s infinite; }}
      {stripe_css()}
      {petal_css()}

      @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
    </style>
  </defs>

  <g clip-path="url(#card)">
    <rect width="1200" height="400" fill="{t['bg']}"/>
    <rect x="28" y="28" width="1144" height="344" rx="16" fill="none" stroke="{t['frame']}" stroke-width="1.5"/>

    <!-- 陶土橙色块 + 扫光 -->
    <g class="blobIn">
      <path d="{BLOB}" fill="{CLAY}"/>
      <path d="M860 0 C 830 60, 900 110, 860 190 C 825 260, 905 320, 870 400" fill="none" stroke="{CLAY_DEEP}" stroke-width="3" opacity=".6"/>
      <g clip-path="url(#blob)"><rect class="sweep" x="760" y="-40" width="180" height="480" fill="url(#shine)"/></g>
    </g>

    <!-- 虎纹剪纸 -->
    <g fill="{INK}">
      {stripes}
    </g>

    <!-- 缎带 + 雏菊 -->
    <g class="fb popIn">
      <g class="sway">
        <path d="M1000 210 L1040 210 L1066 400 L1028 400 Z" fill="{INK}"/>
        <path d="M1040 210 L1070 210 L1104 400 L1068 400 Z" fill="{PETAL}"/>
        <path d="M1070 210 L1092 210 L1134 400 L1106 400 Z" fill="{INK}"/>
        <path d="M1032 300 L1112 300 L1116 318 L1036 318 Z" fill="{PETAL}" opacity=".9"/>
      </g>
      {daisy_svg()}
    </g>

    <!-- 飘落的花瓣 -->
    {petals_svg()}

    <!-- 左侧文字 -->
    <g class="r1">
      <text x="72" y="96" class="mono" font-size="17" fill="{t['muted']}">~/iRyougi <tspan fill="{CLAY}">❯</tspan></text>
      <text x="194" y="96" class="mono" font-size="17" fill="{t['muted']}" clip-path="url(#typed)">whoami</text>
      <text x="262" y="96" class="mono blink" font-size="17" fill="{CLAY}">▍</text>
    </g>

    <g class="r2">
      <g class="gA"><text x="68" y="196" class="serif" font-size="84" font-weight="600" fill="{CLAY}">苏幽璃</text></g>
      <g class="gB"><text x="68" y="196" class="serif" font-size="84" font-weight="600" fill="{t['ghost']}" opacity=".7">苏幽璃</text></g>
      <g class="jit">
        <text x="68" y="196" class="serif" font-size="84" font-weight="600" fill="{t['title']}">苏幽璃</text>
        <text x="358" y="196" class="serif" font-size="52" font-style="italic" fill="{CLAY}">iRyougi</text>
      </g>
    </g>

    <rect class="fb bar" x="72" y="224" width="56" height="4" rx="2" fill="{CLAY}"/>
    <text class="r3 serif" x="72" y="268" font-size="25" fill="{t['sub']}">无法飞翔的翅膀，也有它存在的意义。</text>

    <g class="r4 sans" font-size="15">
      <rect x="72"  y="300" width="150" height="36" rx="18" fill="{t['pill_fill']}"/>
      <text x="147" y="323" text-anchor="middle" fill="{t['pill_text']}">✳ Slay the Spire 2</text>
      <rect x="234" y="300" width="132" height="36" rx="18" fill="none" stroke="{t['outline']}" stroke-width="1.5"/>
      <text x="300" y="323" text-anchor="middle" fill="{t['outline_text']}">KAMITSUBAKI</text>
      <rect x="378" y="300" width="146" height="36" rx="18" fill="none" stroke="{t['outline']}" stroke-width="1.5"/>
      <text x="451" y="323" text-anchor="middle" fill="{t['outline_text']}">Sydney · AU</text>
    </g>
  </g>
</svg>
"""


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    for name, theme in THEMES.items():
        (ASSETS / name).write_text(build(theme), encoding="utf-8")
        print(f"wrote assets/{name}")


if __name__ == "__main__":
    main()
