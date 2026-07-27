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
            "    linear-gradient(to bottom, rgba(35,20,4,.80) 0%, rgba(35,20,4,.64) 60%, rgba(35,20,4,.82) 100%),\n"
            "    linear-gradient(135deg, #451a03 0%, #78350f 100%);\n"
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
            ".hero p { font-size: 1.15rem; color: #94a3b8; margin: 0 auto 2.5rem;\n"
        ),
        "hero_extra": "",
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
}
