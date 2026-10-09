"""Valores por sitio para renderizar `templates/style.css.template`
(ver `css_gen.py`) — extraidos programaticamente (difflib) de los 5
`style.css` reales el 2026-07-27, no reinventados. Cada valor reproduce
EXACTAMENTE lo que el sitio ya tenia desplegado; renderizar con estos
datos contra el template produce el archivo original byte a byte (ver
`tests/test_css_gen.py::test_render_matches_original_bytes`).

Slots vacios ("") son legitimos: no todos los sitios tienen contenido en
todos los puntos de variacion (ej. solo Contalibra tiene `hero_extra` —
el bloque de login-box de la home; solo Restolibra omite `hero_before`,
porque su fondo de hero ya resuelve el degradado en capas propias).
"""

SITES = {
    "contalibra": {
        "tokens": (
            "  --brand:       #2563eb;\n"
            "  --brand-dark:  #1d4ed8;\n"
            "  --brand-light: #eff6ff;\n"
            "  --accent:      #10b981;\n"
            "  --dark:        #0f172a;\n"
            "  --dark-2:      #1e293b;\n"
            "  --muted:       #64748b;\n"
            "  --border:      #e2e8f0;\n"
            "  --bg:          #f8fafc;\n"
        ),
        "hero_bg": (
            "    linear-gradient(to bottom, rgba(10,18,35,.78) 0%, rgba(10,18,35,.62) 60%, rgba(10,18,35,.80) 100%),\n"
            "    url('/img/hero.jpg') center center / cover no-repeat;\n"
        ),
        "hero_before": (
            ".hero::before {\n"
            "  content: '';\n"
            "  position: absolute; inset: 0;\n"
            "  background: radial-gradient(ellipse at 60% 40%, rgba(37,99,235,.18) 0%, transparent 65%);\n"
            "}\n"
        ),
        "hero_badge": (
            "  display: inline-block; background: rgba(37,99,235,.25);\n"
            "  border: 1px solid rgba(37,99,235,.5);\n"
            "  color: #93c5fd; font-size: .82rem; font-weight: 600;\n"
        ),
        "hero_span_p": (
            ".hero h1 span { color: #60a5fa; }\n"
            ".hero p { font-size: 1.15rem; color: #94a3b8; margin: 0 auto 2.5rem;\n"
        ),
        "hero_extra": (
            "\n"
            "/* Login box */\n"
            ".login-box {\n"
            "  background: rgba(255,255,255,.07);\n"
            "  border: 1px solid rgba(255,255,255,.12);\n"
            "  border-radius: 16px; padding: 1.5rem 2rem;\n"
            "  max-width: 480px; margin: 0 auto;\n"
            "  backdrop-filter: blur(8px);\n"
            "}\n"
            ".login-box p { color: #94a3b8; font-size: .9rem; margin: 0 0 .75rem; }\n"
            ".login-input-row {\n"
            "  display: flex; align-items: center; gap: 0;\n"
            "  background: white; border-radius: 10px; overflow: hidden;\n"
            "  border: 2px solid transparent; transition: border-color .15s;\n"
            "}\n"
            ".login-input-row:focus-within { border-color: var(--brand); }\n"
            ".login-input-row input {\n"
            "  flex: 1; border: none; outline: none; padding: .7rem 1rem;\n"
            "  font-size: 1rem; color: var(--dark-2); background: transparent;\n"
            "  min-width: 0;\n"
            "}\n"
            ".login-input-row .domain-suffix {\n"
            "  padding: .7rem .75rem .7rem 0;\n"
            "  color: var(--muted); font-size: .9rem; white-space: nowrap;\n"
            "  background: white;\n"
            "}\n"
            ".login-input-row button {\n"
            "  background: var(--brand); color: white; border: none;\n"
            "  padding: .7rem 1.2rem; font-weight: 600; cursor: pointer;\n"
            "  font-size: .95rem; transition: background .15s; white-space: nowrap;\n"
            "}\n"
            ".login-input-row button:hover { background: var(--brand-dark); }\n"
            ".login-box .login-note { font-size: .78rem; color: #64748b; margin: .6rem 0 0;\n"
            "                          text-align: center; }\n"
        ),
        "badge_estandar": ".badge-estandar { background: #dbeafe; color: #1e40af; }\n",
        "badge_extra": "",
        "plan_featured_shadow": "  box-shadow: 0 8px 32px rgba(37,99,235,.15);\n",
        "plan_features_muted": ".plan-features li.muted { color: #94a3b8; }\n",
        "cta_bg": "  background: linear-gradient(135deg, var(--brand) 0%, #1d4ed8 100%);\n",
        "cta_p": ".cta-section p  { color: #bfdbfe; margin: 0 auto 2rem; max-width: 500px; }\n",
        "footer_bg": "  background: var(--dark); color: #94a3b8;\n",
        "footer_tagline": ".footer-tagline { font-size: .85rem; color: #64748b; margin-top: .3rem; }\n",
        "footer_copy_border": "               border-top: 1px solid #1e293b;\n",
        "footer_copy_text": "               font-size: .82rem; color: #475569; text-align: center; }\n",
        "docs_sidebar_padding": "  padding: 1.5rem 0;\n",
        "trailing": "\n",
    },
    "restolibra": {
        "tokens": (
            "  --brand:       #ea580c;\n"
            "  --brand-dark:  #c2410c;\n"
            "  --brand-light: #fff7ed;\n"
            "  --accent:      #16a34a;\n"
            "  --dark:        #1c1410;\n"
            "  --dark-2:      #292019;\n"
            "  --muted:       #78716c;\n"
            "  --border:      #e7e0d8;\n"
            "  --bg:          #fbf9f6;\n"
        ),
        "hero_bg": (
            "    radial-gradient(ellipse at 20% 20%, rgba(234,88,12,.30) 0%, transparent 55%),\n"
            "    radial-gradient(ellipse at 85% 75%, rgba(194,65,12,.25) 0%, transparent 55%),\n"
            "    linear-gradient(160deg, rgba(28,20,16,.88) 0%, rgba(28,20,16,.80) 55%, rgba(28,20,16,.92) 100%),\n"
            "    url('/img/hero.jpg') center 35% / cover no-repeat;\n"
        ),
        "hero_before": "",
        "hero_badge": (
            "  display: inline-block; background: rgba(234,88,12,.25);\n"
            "  border: 1px solid rgba(234,88,12,.5);\n"
            "  color: #fdba74; font-size: .82rem; font-weight: 600;\n"
        ),
        "hero_span_p": (
            ".hero h1 span { color: #fb923c; }\n"
            ".hero p { font-size: 1.15rem; color: #d6cfc7; margin: 0 auto 2.5rem;\n"
        ),
        "hero_extra": "",
        "badge_estandar": ".badge-estandar { background: #ffedd5; color: #9a3412; }\n",
        "badge_extra": "",
        "plan_featured_shadow": "  box-shadow: 0 8px 32px rgba(234,88,12,.15);\n",
        "plan_features_muted": ".plan-features li.muted { color: #a8a29e; }\n",
        "cta_bg": "  background: linear-gradient(135deg, var(--brand) 0%, #9a3412 100%);\n",
        "cta_p": ".cta-section p  { color: #fed7aa; margin: 0 auto 2rem; max-width: 500px; }\n",
        "footer_bg": "  background: var(--dark); color: #a8a29e;\n",
        "footer_tagline": ".footer-tagline { font-size: .85rem; color: #78716c; margin-top: .3rem; }\n",
        "footer_copy_border": "               border-top: 1px solid #2a2118;\n",
        "footer_copy_text": "               font-size: .82rem; color: #57534e; text-align: center; }\n",
        "docs_sidebar_padding": "  padding: 1.5rem 0 4rem;\n",
        "trailing": "",
    },
    "gestiolibra": {
        "tokens": (
            "  --brand:       #7c3aed;\n"
            "  --brand-dark:  #6d28d9;\n"
            "  --brand-light: #f5f3ff;\n"
            "  --accent:      #10b981;\n"
            "  --dark:        #0f172a;\n"
            "  --dark-2:      #1e293b;\n"
            "  --muted:       #64748b;\n"
            "  --border:      #e2e8f0;\n"
            "  --bg:          #f8fafc;\n"
        ),
        "hero_bg": (
            "    linear-gradient(to bottom, rgba(15,10,35,.80) 0%, rgba(15,10,35,.64) 60%, rgba(15,10,35,.82) 100%),\n"
            "    linear-gradient(135deg, #2e1065 0%, #1e1b4b 100%);\n"
        ),
        "hero_before": (
            ".hero::before {\n"
            "  content: '';\n"
            "  position: absolute; inset: 0;\n"
            "  background: radial-gradient(ellipse at 60% 40%, rgba(124,58,237,.25) 0%, transparent 65%);\n"
            "}\n"
        ),
        "hero_badge": (
            "  display: inline-block; background: rgba(124,58,237,.25);\n"
            "  border: 1px solid rgba(124,58,237,.5);\n"
            "  color: #c4b5fd; font-size: .82rem; font-weight: 600;\n"
        ),
        "hero_span_p": (
            ".hero h1 span { color: #a78bfa; }\n"
            ".hero p { font-size: 1.15rem; color: #94a3b8; margin: 0 auto 2.5rem;\n"
        ),
        "hero_extra": "",
        "badge_estandar": ".badge-estandar { background: #dbeafe; color: #1e40af; }\n",
        "badge_extra": "",
        "plan_featured_shadow": "  box-shadow: 0 8px 32px rgba(124,58,237,.15);\n",
        "plan_features_muted": ".plan-features li.muted { color: #94a3b8; }\n",
        "cta_bg": "  background: linear-gradient(135deg, var(--brand) 0%, var(--brand-dark) 100%);\n",
        "cta_p": ".cta-section p  { color: #e9d5ff; margin: 0 auto 2rem; max-width: 500px; }\n",
        "footer_bg": "  background: var(--dark); color: #94a3b8;\n",
        "footer_tagline": ".footer-tagline { font-size: .85rem; color: #64748b; margin-top: .3rem; }\n",
        "footer_copy_border": "               border-top: 1px solid #1e293b;\n",
        "footer_copy_text": "               font-size: .82rem; color: #475569; text-align: center; }\n",
        "docs_sidebar_padding": "  padding: 1.5rem 0;\n",
        "trailing": "",
    },
    "medlibra": {
        "tokens": (
            "  --brand:       #0d9488;\n"
            "  --brand-dark:  #0f766e;\n"
            "  --brand-light: #f0fdfa;\n"
            "  --accent:      #10b981;\n"
            "  --dark:        #0f172a;\n"
            "  --dark-2:      #1e293b;\n"
            "  --muted:       #64748b;\n"
            "  --border:      #e2e8f0;\n"
            "  --bg:          #f8fafc;\n"
        ),
        "hero_bg": (
            "    linear-gradient(to bottom, rgba(4,20,20,.80) 0%, rgba(4,20,20,.64) 60%, rgba(4,20,20,.82) 100%),\n"
            "    linear-gradient(135deg, #042f2e 0%, #134e4a 100%);\n"
        ),
        "hero_before": (
            ".hero::before {\n"
            "  content: '';\n"
            "  position: absolute; inset: 0;\n"
            "  background: radial-gradient(ellipse at 60% 40%, rgba(13,148,136,.25) 0%, transparent 65%);\n"
            "}\n"
        ),
        "hero_badge": (
            "  display: inline-block; background: rgba(13,148,136,.25);\n"
            "  border: 1px solid rgba(13,148,136,.5);\n"
            "  color: #5eead4; font-size: .82rem; font-weight: 600;\n"
        ),
        "hero_span_p": (
            ".hero h1 span { color: #2dd4bf; }\n"
            ".hero p { font-size: 1.15rem; color: #94a3b8; margin: 0 auto 2.5rem;\n"
        ),
        "hero_extra": "",
        "badge_estandar": ".badge-estandar { background: #dbeafe; color: #1e40af; }\n",
        "badge_extra": ".badge-incluido { background: #ccfbf1; color: #0f766e; }\n",
        "plan_featured_shadow": "  box-shadow: 0 8px 32px rgba(13,148,136,.15);\n",
        "plan_features_muted": ".plan-features li.muted { color: #94a3b8; }\n",
        "cta_bg": "  background: linear-gradient(135deg, var(--brand) 0%, var(--brand-dark) 100%);\n",
        "cta_p": ".cta-section p  { color: #99f6e4; margin: 0 auto 2rem; max-width: 500px; }\n",
        "footer_bg": "  background: var(--dark); color: #94a3b8;\n",
        "footer_tagline": ".footer-tagline { font-size: .85rem; color: #64748b; margin-top: .3rem; }\n",
        "footer_copy_border": "               border-top: 1px solid #1e293b;\n",
        "footer_copy_text": "               font-size: .82rem; color: #475569; text-align: center; }\n",
        "docs_sidebar_padding": "  padding: 1.5rem 0;\n",
        "trailing": "",
    },
    "ventalibra": {
        "tokens": (
            "  --brand:       #d97706;\n"
            "  --brand-dark:  #b45309;\n"
            "  --brand-light: #fffbeb;\n"
            "  --accent:      #10b981;\n"
            "  --dark:        #0f172a;\n"
            "  --dark-2:      #1e293b;\n"
            "  --muted:       #64748b;\n"
            "  --border:      #e2e8f0;\n"
            "  --bg:          #f8fafc;\n"
        ),
        "hero_bg": (
            "    linear-gradient(to bottom, rgba(28,14,3,.88) 0%, rgba(40,20,4,.70) 55%, rgba(28,14,3,.92) 100%),\n"
            "    url('/img/almacen-hero.jpg') center 88% / cover no-repeat,\n"
            "    #2a1505;\n"
        ),
        "hero_before": (
            ".hero::before {\n"
            "  content: '';\n"
            "  position: absolute; inset: 0;\n"
            "  background: radial-gradient(ellipse at 60% 40%, rgba(217,119,6,.25) 0%, transparent 65%);\n"
            "}\n"
        ),
        "hero_badge": (
            "  display: inline-block; background: rgba(217,119,6,.25);\n"
            "  border: 1px solid rgba(217,119,6,.5);\n"
            "  color: #fcd34d; font-size: .82rem; font-weight: 600;\n"
        ),
        "hero_span_p": (
            ".hero h1 span { color: #fbbf24; }\n"
            ".hero p { font-size: 1.15rem; color: #d6d3d1; margin: 0 auto 2.5rem;\n"
        ),
        "hero_extra": (
            ".hero { min-height: min(80vh, 720px); display: flex; align-items: center;\n"
            "        padding: 5rem 2rem; }\n"
            ".hero-content { max-width: 820px; }\n"
            ".hero h1 { font-size: clamp(2.2rem, 5.5vw, 3.8rem); line-height: 1.08;\n"
            "           letter-spacing: -.03em; text-wrap: balance; }\n"
            ".hero h1 span { display: block; margin-top: .5rem; font-size: .5em;\n"
            "                font-weight: 600; letter-spacing: -.01em; color: #fcd34d; }\n"
            ".hero p { text-wrap: pretty; line-height: 1.7; }\n"
            ".hero .btn { margin: .3rem .35rem; }\n"
            ".hero .btn-primary { box-shadow: 0 8px 24px rgba(217,119,6,.35); }\n"
            ".hero .btn-white { background: rgba(255,255,255,.08); color: #fff;\n"
            "                   border: 1px solid rgba(255,255,255,.35);\n"
            "                   backdrop-filter: blur(6px); }\n"
            ".hero .btn-white:hover { background: rgba(255,255,255,.16); color: #fff; }\n"
            "\n"
            "/* Pulido general (solo VentaLibra) */\n"
            "html { scroll-behavior: smooth; }\n"
            "section[id] { scroll-margin-top: 72px; }\n"
            ".navbar { box-shadow: 0 1px 0 rgba(15,23,42,.04); }\n"
            ".btn { letter-spacing: -.005em; }\n"
            ".btn-primary:hover { transform: translateY(-1px); }\n"
            ".section-label { display: inline-flex; align-items: center; gap: .6rem; }\n"
            ".section-label::before { content: ''; width: 24px; height: 2px;\n"
            "                         background: var(--brand); }\n"
            ".section-title { font-size: clamp(1.8rem, 3.4vw, 2.6rem); line-height: 1.15; }\n"
            ".feature-card { padding: 1.75rem; border-color: #e7e5e4; box-shadow: none; }\n"
            ".feature-card:hover { border-color: var(--brand);\n"
            "                      box-shadow: 0 12px 32px rgba(120,53,15,.10); }\n"
            ".feature-icon { width: 48px; height: 48px; border-radius: 12px; }\n"
            ".plan-card { border-radius: 18px; transition: box-shadow .2s, transform .2s; }\n"
            ".plan-card:hover { transform: translateY(-3px); box-shadow: var(--shadow); }\n"
            ".plan-card.featured { background: linear-gradient(180deg, var(--brand-light) 0%, #fff 55%); }\n"
            ".cta-section { background:\n"
            "    radial-gradient(ellipse at 20% 0%, rgba(255,255,255,.14) 0%, transparent 55%),\n"
            "    linear-gradient(135deg, var(--brand) 0%, var(--brand-dark) 100%); }\n"
            ":focus-visible { outline: 3px solid rgba(217,119,6,.5); outline-offset: 2px; }\n"
            "@media (prefers-reduced-motion: reduce) {\n"
            "  html { scroll-behavior: auto; }\n"
            "  *, *::before, *::after { transition: none !important; }\n"
            "}\n"
            "\n"
            "/* Franja de puntos fuertes, rubros, pasos y planes (solo VentaLibra) */\n"
            ".highlights { position: relative; z-index: 2; max-width: 1100px;\n"
            "              width: calc(100% - 4rem); margin: -2.75rem auto 0;\n"
            "              display: grid; grid-template-columns: repeat(4, 1fr);\n"
            "              background: #fff; border: 1px solid #e7e5e4; border-radius: 16px;\n"
            "              box-shadow: 0 20px 48px rgba(28,14,3,.18); }\n"
            ".highlight { display: flex; align-items: center; gap: .85rem; padding: 1.4rem 1.5rem; }\n"
            ".highlight + .highlight { border-left: 1px solid #f1f5f9; }\n"
            ".highlight > i { flex-shrink: 0; width: 44px; height: 44px; border-radius: 12px;\n"
            "                 background: var(--brand-light); color: var(--brand-dark);\n"
            "                 display: flex; align-items: center; justify-content: center;\n"
            "                 font-size: 1.25rem; }\n"
            ".highlight strong { display: block; font-size: .95rem; color: var(--dark); line-height: 1.3; }\n"
            ".highlight span { display: block; font-size: .82rem; color: var(--muted); line-height: 1.4; }\n"
            "#funciones { padding-top: 7rem; }\n"
            ".rubros { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));\n"
            "          gap: 1.25rem; margin-top: 3rem; }\n"
            ".rubro { background: #fff; border: 1px solid #e7e5e4; border-radius: 16px;\n"
            "         padding: 2rem 1.75rem; transition: box-shadow .2s, transform .2s; }\n"
            ".rubro:hover { transform: translateY(-3px); box-shadow: var(--shadow); }\n"
            ".rubro-icon { width: 56px; height: 56px; border-radius: 14px; background: var(--dark);\n"
            "              color: #fbbf24; display: flex; align-items: center;\n"
            "              justify-content: center; font-size: 1.6rem; margin-bottom: 1.25rem; }\n"
            ".rubro h3 { font-size: 1.1rem; font-weight: 800; color: var(--dark); margin: 0 0 .5rem; }\n"
            ".rubro p { font-size: .95rem; color: var(--muted); margin: 0; line-height: 1.6; }\n"
            ".steps { position: relative; }\n"
            ".steps::before { content: ''; position: absolute; top: 24px; left: 16.6%; right: 16.6%;\n"
            "                 height: 2px; background: linear-gradient(90deg, var(--brand) 0%, #fde68a 100%); }\n"
            ".step-num { position: relative; background: #fff; color: var(--brand-dark);\n"
            "            border: 2px solid var(--brand); box-shadow: 0 0 0 8px #fff; }\n"
            ".step p { max-width: 280px; margin: 0 auto; line-height: 1.6; }\n"
            ".pricing-grid { align-items: stretch; }\n"
            ".plan-card { display: flex; flex-direction: column; }\n"
            ".plan-features { flex: 1; }\n"
            ".plan-price { font-size: 1.6rem !important; }\n"
            ".showcase { background: linear-gradient(180deg, #1c0e03 0%, #2a1505 100%); color: #fff;\n"
            "            padding-bottom: 6rem; }\n"
            ".showcase .section-label { color: #fbbf24; }\n"
            ".showcase .section-label::before { background: #fbbf24; }\n"
            ".showcase .section-title { color: #fff; }\n"
            ".showcase .section-sub { color: #d6d3d1; }\n"
            ".browser { margin: 0; border-radius: 12px; overflow: hidden; background: #fff;\n"
            "           border: 1px solid rgba(255,255,255,.14);\n"
            "           box-shadow: 0 30px 60px rgba(0,0,0,.5), 0 0 0 1px rgba(0,0,0,.2); }\n"
            ".browser-bar { display: flex; align-items: center; gap: .4rem; padding: .55rem .85rem;\n"
            "               background: #f1f5f9; border-bottom: 1px solid #e2e8f0; }\n"
            ".browser-bar > span { width: 9px; height: 9px; border-radius: 50%; background: #cbd5e1; }\n"
            ".browser-url { flex: 1; max-width: 300px; margin: 0 auto; padding: .15rem .75rem;\n"
            "               background: #fff; border: 1px solid #e2e8f0; border-radius: 999px;\n"
            "               font-size: .7rem; color: var(--muted); text-align: center; }\n"
            ".browser-bar::after { content: ''; width: 41px; }\n"
            ".browser-body { overflow-x: auto; }\n"
            ".browser-body img { display: block; width: 100%; height: auto; }\n"
            ".showcase-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 2rem;\n"
            "                 margin: 3rem 0 0; }\n"
            ".showcase-fig { margin: 0; }\n"
            ".showcase-fig figcaption { margin-top: 1.1rem; text-align: center; font-size: .92rem;\n"
            "                           color: #d6d3d1; }\n"
            ".showcase-cta { text-align: center; margin-top: 2.5rem; }\n"
            "\n"
            "/* Pie de pagina (solo VentaLibra) */\n"
            ".site-footer { padding: 4rem 2rem 2rem; background: #140b03;\n"
            "               border-top: 3px solid var(--brand); }\n"
            ".f-inner { max-width: 1100px; margin: 0 auto; display: grid;\n"
            "           grid-template-columns: 1.6fr 1fr 1.1fr 1.3fr; gap: 2.5rem; }\n"
            ".f-logo { width: 28px; height: 28px; display: block; flex-shrink: 0; }\n"
            ".f-tagline { margin: 1rem 0 1.5rem; max-width: 300px; font-size: .9rem;\n"
            "             line-height: 1.65; color: #a8a29e; }\n"
            ".f-cta { display: inline-flex; align-items: center; gap: .5rem; padding: .6rem 1.1rem;\n"
            "         border: 1px solid rgba(251,191,36,.45); border-radius: 10px; color: #fcd34d;\n"
            "         font-size: .9rem; font-weight: 600; transition: background .15s; }\n"
            ".f-cta:hover { background: rgba(251,191,36,.1); text-decoration: none; }\n"
            ".f-col { display: flex; flex-direction: column; gap: .6rem; }\n"
            ".f-title { margin-bottom: .4rem; font-size: .75rem; font-weight: 700;\n"
            "           letter-spacing: .1em; text-transform: uppercase; color: #a8a29e; }\n"
            ".f-col a { display: block; color: #d6d3d1; font-size: .92rem; transition: color .15s; }\n"
            ".f-col a:hover { color: #fbbf24; text-decoration: none; }\n"
            ".f-col a i { margin-right: .5rem; color: #a8a29e; }\n"
            ".f-family a small { display: block; font-size: .78rem; color: #918a84; margin-top: .1rem; }\n"
            ".f-bottom { max-width: 1100px; margin: 3rem auto 0; padding-top: 1.5rem;\n"
            "            border-top: 1px solid #292017; display: flex; flex-wrap: wrap;\n"
            "            justify-content: space-between; gap: .75rem; font-size: .82rem;\n"
            "            color: #a8a29e; }\n"
            ".f-bottom a { color: #a8a29e; }\n"
            ".f-bottom a:hover { color: #fbbf24; text-decoration: none; }\n"
            "@media (max-width: 960px) {\n"
            "  .f-inner { grid-template-columns: 1fr 1fr; }\n"
            "  .f-about { grid-column: 1 / -1; }\n"
            "}\n"
            "@media (max-width: 520px) {\n"
            "  .site-footer { padding: 3rem 1.25rem 1.5rem; }\n"
            "  .f-inner { grid-template-columns: 1fr; gap: 2rem; }\n"
            "}\n"
            "\n"
            "/* Preguntas frecuentes (solo VentaLibra) */\n"
            ".faq-container { max-width: 820px; }\n"
            ".faq-list { margin-top: 2.5rem; border-top: 1px solid var(--border); }\n"
            ".faq-item { border-bottom: 1px solid var(--border); }\n"
            ".faq-item summary { list-style: none; cursor: pointer; display: flex;\n"
            "                    align-items: center; justify-content: space-between; gap: 1rem;\n"
            "                    padding: 1.25rem .25rem; font-size: 1.05rem; font-weight: 700;\n"
            "                    color: var(--dark); transition: color .15s; }\n"
            ".faq-item summary::-webkit-details-marker { display: none; }\n"
            ".faq-item summary::after { content: '+'; flex-shrink: 0; width: 28px; height: 28px;\n"
            "                           border-radius: 50%; border: 1px solid var(--border);\n"
            "                           display: flex; align-items: center; justify-content: center;\n"
            "                           font-size: 1.2rem; font-weight: 400; color: var(--brand);\n"
            "                           transition: transform .2s, background .15s; }\n"
            ".faq-item summary:hover { color: var(--brand-dark); }\n"
            ".faq-item[open] summary::after { content: '\\2212'; background: var(--brand-light); }\n"
            ".faq-item p { margin: 0; padding: 0 3rem 1.5rem .25rem; color: var(--muted);\n"
            "              line-height: 1.7; font-size: .98rem; }\n"
            ".faq-more { margin-top: 2rem; color: var(--muted); font-size: .95rem; }\n"
            "@media (max-width: 960px) {\n"
            "  .highlights { grid-template-columns: repeat(2, 1fr); }\n"
            "  .highlight:nth-child(3) { border-left: none; }\n"
            "  .highlight:nth-child(n+3) { border-top: 1px solid #f1f5f9; }\n"
            "}\n"
            "@media (max-width: 768px) {\n"
            "  .steps::before { display: none; }\n"
            "  .showcase-grid { grid-template-columns: 1fr; }\n"
            "  .browser-bar::after { display: none; }\n"
            "}\n"
            "@media (max-width: 520px) {\n"
            "  .highlights { grid-template-columns: 1fr; width: calc(100% - 2.5rem); margin-top: -2rem; }\n"
            "  .highlight + .highlight { border-left: none; border-top: 1px solid #f1f5f9; }\n"
            "  #funciones { padding-top: 5rem; }\n"
            "}\n"
            "@media (max-width: 768px) {\n"
            "  .hero { min-height: auto; padding: 4rem 1.25rem 3.5rem; }\n"
            "  section { padding: 3.5rem 1.25rem; }\n"
            "}\n"
        ),
        "badge_estandar": ".badge-estandar { background: #dbeafe; color: #1e40af; }\n",
        "badge_extra": "",
        "plan_featured_shadow": "  box-shadow: 0 8px 32px rgba(217,119,6,.15);\n",
        "plan_features_muted": ".plan-features li.muted { color: #94a3b8; }\n",
        "cta_bg": "  background: linear-gradient(135deg, var(--brand) 0%, var(--brand-dark) 100%);\n",
        "cta_p": ".cta-section p  { color: #fed7aa; margin: 0 auto 2rem; max-width: 500px; }\n",
        "footer_bg": "  background: var(--dark); color: #94a3b8;\n",
        "footer_tagline": ".footer-tagline { font-size: .85rem; color: #64748b; margin-top: .3rem; }\n",
        "footer_copy_border": "               border-top: 1px solid #1e293b;\n",
        "footer_copy_text": "               font-size: .82rem; color: #475569; text-align: center; }\n",
        "docs_sidebar_padding": "  padding: 1.5rem 0;\n",
        "trailing": "",
    },
    "libradesk": {
        "tokens": (
            "  --brand:       #4f46e5;\n"
            "  --brand-dark:  #4338ca;\n"
            "  --brand-light: #eef2ff;\n"
            "  --accent:      #10b981;\n"
            "  --dark:        #0f172a;\n"
            "  --dark-2:      #1e293b;\n"
            "  --muted:       #64748b;\n"
            "  --border:      #e2e8f0;\n"
            "  --bg:          #f8fafc;\n"
        ),
        "hero_bg": (
            "    linear-gradient(to bottom, rgba(15,14,40,.80) 0%, rgba(15,14,40,.64) 60%, rgba(15,14,40,.82) 100%),\n"
            "    linear-gradient(135deg, #1e1b4b 0%, #312e81 100%);\n"
        ),
        "hero_before": (
            ".hero::before {\n"
            "  content: '';\n"
            "  position: absolute; inset: 0;\n"
            "  background: radial-gradient(ellipse at 60% 40%, rgba(79,70,229,.25) 0%, transparent 65%);\n"
            "}\n"
        ),
        "hero_badge": (
            "  display: inline-block; background: rgba(79,70,229,.25);\n"
            "  border: 1px solid rgba(79,70,229,.5);\n"
            "  color: #a5b4fc; font-size: .82rem; font-weight: 600;\n"
        ),
        "hero_span_p": (
            ".hero h1 span { color: #818cf8; }\n"
            ".hero p { font-size: 1.15rem; color: #94a3b8; margin: 0 auto 2.5rem;\n"
        ),
        "hero_extra": "",
        "badge_estandar": ".badge-estandar { background: #dbeafe; color: #1e40af; }\n",
        "badge_extra": "",
        "plan_featured_shadow": "  box-shadow: 0 8px 32px rgba(79,70,229,.15);\n",
        "plan_features_muted": ".plan-features li.muted { color: #94a3b8; }\n",
        "cta_bg": "  background: linear-gradient(135deg, var(--brand) 0%, var(--brand-dark) 100%);\n",
        "cta_p": ".cta-section p  { color: #c7d2fe; margin: 0 auto 2rem; max-width: 500px; }\n",
        "footer_bg": "  background: var(--dark); color: #94a3b8;\n",
        "footer_tagline": ".footer-tagline { font-size: .85rem; color: #64748b; margin-top: .3rem; }\n",
        "footer_copy_border": "               border-top: 1px solid #1e293b;\n",
        "footer_copy_text": "               font-size: .82rem; color: #475569; text-align: center; }\n",
        "docs_sidebar_padding": "  padding: 1.5rem 0;\n",
        "trailing": "",
    },
    # LibraCargo y LibraClub (2026-08-20) son los dos unicos sitios que NO se
    # extrajeron de un `style.css` ya desplegado: nacen desde el template, con
    # los slots minimos que los otros seis ya habian estabilizado. El
    # `--brand` no se eligio aca — es el color medido de su icono en
    # `diseños/kit-libra-v1/`, el mismo que usa la app (ver el concepto
    # `identidad-visual-suite-libra` del wiki). Elegir un color propio para la
    # landing habria dejado el sitio y el producto de dos colores distintos.
    "libracargo": {
        "tokens": (
            "  --brand:       #012c83;\n"
            "  --brand-dark:  #001d5c;\n"
            "  --brand-light: #eef3fc;\n"
            "  --accent:      #10b981;\n"
            "  --dark:        #0f172a;\n"
            "  --dark-2:      #1e293b;\n"
            "  --muted:       #64748b;\n"
            "  --border:      #e2e8f0;\n"
            "  --bg:          #f8fafc;\n"
        ),
        "hero_bg": (
            "    linear-gradient(to bottom, rgba(0,10,32,.78) 0%, rgba(0,10,32,.60) 60%, rgba(0,10,32,.82) 100%),\n"
            "    linear-gradient(135deg, #001233 0%, #012c83 100%);\n"
        ),
        "hero_before": (
            ".hero::before {\n"
            "  content: '';\n"
            "  position: absolute; inset: 0;\n"
            "  background: radial-gradient(ellipse at 60% 40%, rgba(1,44,131,.35) 0%, transparent 65%);\n"
            "}\n"
        ),
        "hero_badge": (
            "  display: inline-block; background: rgba(1,44,131,.35);\n"
            "  border: 1px solid rgba(122,162,255,.45);\n"
            "  color: #a8c3ff; font-size: .82rem; font-weight: 600;\n"
        ),
        "hero_span_p": (
            ".hero h1 span { color: #7aa2ff; }\n"
            ".hero p { font-size: 1.15rem; color: #94a3b8; margin: 0 auto 2.5rem;\n"
        ),
        "hero_extra": "",
        "badge_estandar": ".badge-estandar { background: #dbeafe; color: #1e40af; }\n",
        "badge_extra": ".badge-incluido { background: #e0e7ff; color: #012c83; }\n",
        "plan_featured_shadow": "  box-shadow: 0 8px 32px rgba(1,44,131,.18);\n",
        "plan_features_muted": ".plan-features li.muted { color: #94a3b8; }\n",
        "cta_bg": "  background: linear-gradient(135deg, var(--brand) 0%, var(--brand-dark) 100%);\n",
        "cta_p": ".cta-section p  { color: #bfd3ff; margin: 0 auto 2rem; max-width: 500px; }\n",
        "footer_bg": "  background: var(--dark); color: #94a3b8;\n",
        "footer_tagline": ".footer-tagline { font-size: .85rem; color: #64748b; margin-top: .3rem; }\n",
        "footer_copy_border": "               border-top: 1px solid #1e293b;\n",
        "footer_copy_text": "               font-size: .82rem; color: #475569; text-align: center; }\n",
        "docs_sidebar_padding": "  padding: 1.5rem 0;\n",
        "trailing": "",
    },
    "libraclub": {
        "tokens": (
            "  --brand:       #017b4b;\n"
            "  --brand-dark:  #015c38;\n"
            "  --brand-light: #ecfdf5;\n"
            # El unico sitio cuyo `--accent` no es verde: con `--brand` ya
            # verde, un accent #10b981 no se distingue de la marca y deja de
            # acentuar nada.
            "  --accent:      #f59e0b;\n"
            "  --dark:        #0f172a;\n"
            "  --dark-2:      #1e293b;\n"
            "  --muted:       #64748b;\n"
            "  --border:      #e2e8f0;\n"
            "  --bg:          #f8fafc;\n"
        ),
        "hero_bg": (
            "    linear-gradient(to bottom, rgba(2,25,17,.86) 0%, rgba(2,25,17,.68) 55%, rgba(2,25,17,.90) 100%),\n"
            # Mitad futsal y mitad padel, fundidas en diagonal: dos fotos CC0
            # de Wikimedia Commons (ver wiki/entities/libraclub-web.md).
            "    url('/img/canchas-hero.jpg') center 45% / cover no-repeat,\n"
            "    #04231a;\n"
        ),
        "hero_before": (
            ".hero::before {\n"
            "  content: '';\n"
            "  position: absolute; inset: 0;\n"
            "  background: radial-gradient(ellipse at 60% 40%, rgba(1,123,75,.32) 0%, transparent 65%);\n"
            "}\n"
        ),
        "hero_badge": (
            "  display: inline-block; background: rgba(1,123,75,.30);\n"
            "  border: 1px solid rgba(52,211,153,.45);\n"
            "  color: #6ee7b7; font-size: .82rem; font-weight: 600;\n"
        ),
        "hero_span_p": (
            ".hero h1 span { color: #34d399; }\n"
            ".hero p { font-size: 1.15rem; color: #a7b8b0; margin: 0 auto 2.5rem;\n"
        ),
        "hero_extra": "",
        "badge_estandar": ".badge-estandar { background: #d1fae5; color: #065f46; }\n",
        "badge_extra": ".badge-incluido { background: #d1fae5; color: #015c38; }\n",
        "plan_featured_shadow": "  box-shadow: 0 8px 32px rgba(1,123,75,.18);\n",
        "plan_features_muted": ".plan-features li.muted { color: #94a3b8; }\n",
        "cta_bg": "  background: linear-gradient(135deg, var(--brand) 0%, var(--brand-dark) 100%);\n",
        "cta_p": ".cta-section p  { color: #a7f3d0; margin: 0 auto 2rem; max-width: 500px; }\n",
        "footer_bg": "  background: var(--dark); color: #94a3b8;\n",
        "footer_tagline": ".footer-tagline { font-size: .85rem; color: #64748b; margin-top: .3rem; }\n",
        "footer_copy_border": "               border-top: 1px solid #1e293b;\n",
        "footer_copy_text": "               font-size: .82rem; color: #475569; text-align: center; }\n",
        "docs_sidebar_padding": "  padding: 1.5rem 0;\n",
        "trailing": "",
    },
}
