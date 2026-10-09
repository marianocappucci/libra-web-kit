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
            # Persona trabajando en su escritorio (foto aportada por el humano).
            "    url('/img/escritorio-hero.jpg') center center / cover no-repeat;\n"
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
            # Restaurante con gente en las mesas (foto aportada por el humano).
            "    url('/img/restaurante-hero.jpg') 40% center / cover no-repeat;\n"
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
            "    linear-gradient(to bottom, rgba(15,10,35,.86) 0%, rgba(15,10,35,.70) 55%, rgba(15,10,35,.90) 100%),\n"
            # Collage: agenda en una tablet, barberia y taller (foto aportada por el humano).
            "    url('/img/servicios-hero.jpg') 30% center / cover no-repeat,\n"
            "    #2e1065;\n"
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
            "    linear-gradient(to bottom, rgba(4,20,20,.86) 0%, rgba(4,20,20,.70) 55%, rgba(4,20,20,.90) 100%),\n"
            # Recepcion de una clinica (foto aportada por el humano).
            "    url('/img/clinica-hero.jpg') 40% center / cover no-repeat,\n"
            "    #042f2e;\n"
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
            # Comerciante en la puerta de su local (foto aportada por el humano,
            # antes en ContaLibra). 22% horizontal: en celular queda la cara.
            "    url('/img/comerciante-hero.jpg') 22% center / cover no-repeat,\n"
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
        # El pulido que nacio aca vive ahora en templates/pulido.css (ADR-010).
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
            "    linear-gradient(to bottom, rgba(15,14,40,.86) 0%, rgba(15,14,40,.70) 55%, rgba(15,14,40,.90) 100%),\n"
            # Tecnicos en un cuarto de racks (foto aportada por el humano).
            "    url('/img/soporte-hero.jpg') 45% 50% / cover no-repeat,\n"
            "    #1e1b4b;\n"
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
            "    linear-gradient(to bottom, rgba(0,10,32,.84) 0%, rgba(0,10,32,.64) 55%, rgba(0,10,32,.88) 100%),\n"
            # Camiones de granos en una ruta entre campos (foto aportada por el humano).
            "    url('/img/camiones-hero.jpg') 72% 60% / cover no-repeat,\n"
            "    #001233;\n"
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
            # 90% horizontal: en pantallas angostas deja ver al jugador de padel;
            # en escritorio la foto ocupa todo el ancho y no cambia nada.
            "    url('/img/canchas-hero.jpg') 90% 45% / cover no-repeat,\n"
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


#: Colores propios de cada sitio para templates/pulido.css (ADR-010). Los *-rgb
#: van como "r,g,b" para usarse con rgba(var(--p-x-rgb), alfa).
PULIDO_VARS = {
    "contalibra": {
        "hero-accent": "#93c5fd",
        "on-dark-accent": "#60a5fa",
        "brand-rgb": "37,99,235",
        "deep-rgb": "10,18,35",
        "hover-rgb": "30,64,175",
        "card-border": "#e2e8f0",
        "step-end": "#bfdbfe",
        "dark-1": "#0a1223",
        "dark-2": "#13203b",
        "footer-bg": "#070d1a",
        "footer-line": "#1e293b",
        "on-dark-text": "#cbd5e1",
        "on-dark-muted": "#94a3b8",
        "on-dark-faint": "#7c8aa0",
        "on-dark-accent-rgb": "96,165,250",
    },
    "restolibra": {
        "hero-accent": "#fdba74",
        "on-dark-accent": "#fb923c",
        "brand-rgb": "234,88,12",
        "deep-rgb": "28,20,16",
        "hover-rgb": "154,52,18",
        "card-border": "#e7e0d8",
        "step-end": "#fed7aa",
        "dark-1": "#1c1410",
        "dark-2": "#292019",
        "footer-bg": "#140e0b",
        "footer-line": "#2c221c",
        "on-dark-text": "#d6cfc7",
        "on-dark-muted": "#a8a29e",
        "on-dark-faint": "#918a84",
        "on-dark-accent-rgb": "251,146,60",
    },
    "gestiolibra": {
        "hero-accent": "#c4b5fd",
        "on-dark-accent": "#a78bfa",
        "brand-rgb": "124,58,237",
        "deep-rgb": "15,10,35",
        "hover-rgb": "91,33,182",
        "card-border": "#e2e8f0",
        "step-end": "#ddd6fe",
        "dark-1": "#0f0a23",
        "dark-2": "#1e1240",
        "footer-bg": "#0a0618",
        "footer-line": "#241a3d",
        "on-dark-text": "#d4d0e6",
        "on-dark-muted": "#a5a0bd",
        "on-dark-faint": "#8a84a3",
        "on-dark-accent-rgb": "167,139,250",
    },
    "medlibra": {
        "hero-accent": "#5eead4",
        "on-dark-accent": "#2dd4bf",
        "brand-rgb": "13,148,136",
        "deep-rgb": "4,20,20",
        "hover-rgb": "17,94,89",
        "card-border": "#e2e8f0",
        "step-end": "#99f6e4",
        "dark-1": "#041414",
        "dark-2": "#082a28",
        "footer-bg": "#030f0f",
        "footer-line": "#12302d",
        "on-dark-text": "#c7d6d4",
        "on-dark-muted": "#94a8a6",
        "on-dark-faint": "#7a8f8d",
        "on-dark-accent-rgb": "45,212,191",
    },
    "ventalibra": {
        "hero-accent": "#fcd34d",
        "on-dark-accent": "#fbbf24",
        "brand-rgb": "217,119,6",
        "deep-rgb": "28,14,3",
        "hover-rgb": "120,53,15",
        "card-border": "#e7e5e4",
        "step-end": "#fde68a",
        "dark-1": "#1c0e03",
        "dark-2": "#2a1505",
        "footer-bg": "#140b03",
        "footer-line": "#292017",
        "on-dark-text": "#d6d3d1",
        "on-dark-muted": "#a8a29e",
        "on-dark-faint": "#918a84",
        "on-dark-accent-rgb": "251,191,36",
    },
    "libradesk": {
        "hero-accent": "#a5b4fc",
        "on-dark-accent": "#818cf8",
        "brand-rgb": "79,70,229",
        "deep-rgb": "15,14,40",
        "hover-rgb": "55,48,163",
        "card-border": "#e2e8f0",
        "step-end": "#c7d2fe",
        "dark-1": "#0f0e28",
        "dark-2": "#1e1b4b",
        "footer-bg": "#0a0920",
        "footer-line": "#22204a",
        "on-dark-text": "#d1d0e6",
        "on-dark-muted": "#a3a2bd",
        "on-dark-faint": "#8584a3",
        "on-dark-accent-rgb": "129,140,248",
    },
    "libracargo": {
        "hero-accent": "#a8c3ff",
        "on-dark-accent": "#7aa2ff",
        "brand-rgb": "1,44,131",
        "deep-rgb": "0,10,32",
        "hover-rgb": "1,44,131",
        "card-border": "#e2e8f0",
        "step-end": "#bfd0f7",
        "dark-1": "#000a20",
        "dark-2": "#001233",
        "footer-bg": "#000716",
        "footer-line": "#10224a",
        "on-dark-text": "#c9d3e6",
        "on-dark-muted": "#94a3b8",
        "on-dark-faint": "#7a879e",
        "on-dark-accent-rgb": "122,162,255",
    },
    "libraclub": {
        "hero-accent": "#6ee7b7",
        "on-dark-accent": "#34d399",
        "brand-rgb": "1,123,75",
        "deep-rgb": "2,25,17",
        "hover-rgb": "1,92,56",
        "card-border": "#e2e8f0",
        "step-end": "#a7f3d0",
        "dark-1": "#021911",
        "dark-2": "#04231a",
        "footer-bg": "#01110b",
        "footer-line": "#0c2e22",
        "on-dark-text": "#c5d6cf",
        "on-dark-muted": "#93aaa1",
        "on-dark-faint": "#7a9088",
        "on-dark-accent-rgb": "52,211,153",
    },
}
