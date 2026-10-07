"""Identidad de cada producto de la familia: un color y un ícono.

Es la copia, para las landings, de la tabla «La identidad de cada producto» de
`wiki/analyses/identidad-de-producto-diseno.md` (repo del wiki). La otra copia es
`libra-ui/src/identidad.ts`, que lleva el mismo registro con el nombre del ícono
de lucide en vez del de Bootstrap Icons.

🔴 **Una sola tabla.** Si cambia un color o un ícono, cambia en `identidad.ts`, acá
y en la página del wiki, en la misma tanda. `tests/test_identidad.py` hardcodea la
tabla del documento: si este archivo diverge, el test falla; y si cambia el
documento, quien lo edita tiene que editar también ese test.

Los colores `color`, `color_oscuro` y `color_claro` son los `--brand`, `--brand-dark` y
`--brand-light` de `site_css_tokens.SITES` (el test los compara). `color_sobre_oscuro`
no tiene token en las landings: lo usa la app en modo oscuro y LibraSuite.

Las claves son las de `site_css_tokens.SITES`, `docs_pages.PAGES` y
`docs_sidebars.SIDEBARS`.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Identidad:
    nombre: str
    rubro: str
    color: str
    color_oscuro: str
    color_claro: str
    color_sobre_oscuro: str
    #: Clase de Bootstrap Icons, con el prefijo (`bi-truck`), como en la tabla del
    #: documento. Para el nombre pelado, `nombre_icono(sitio)`.
    icono_bootstrap: str


IDENTIDAD: dict[str, Identidad] = {
    "contalibra": Identidad(
        nombre="ContaLibra",
        rubro="Comercios y PyMEs",
        color="#2563eb",
        color_oscuro="#1d4ed8",
        color_claro="#eff6ff",
        color_sobre_oscuro="#60a5fa",
        icono_bootstrap="bi-receipt-cutoff",
    ),
    "restolibra": Identidad(
        nombre="RestoLibra",
        rubro="Restaurantes, bares y delivery",
        color="#ea580c",
        color_oscuro="#c2410c",
        color_claro="#fff7ed",
        color_sobre_oscuro="#fb923c",
        icono_bootstrap="bi-cup-hot",
    ),
    "gestiolibra": Identidad(
        nombre="GestioLibra",
        rubro="Negocios de servicios",
        color="#7c3aed",
        color_oscuro="#6d28d9",
        color_claro="#f5f3ff",
        color_sobre_oscuro="#a78bfa",
        icono_bootstrap="bi-calendar-check",
    ),
    "medlibra": Identidad(
        nombre="MedLibra",
        rubro="Consultorios y centros médicos",
        color="#0d9488",
        color_oscuro="#0f766e",
        color_claro="#f0fdfa",
        color_sobre_oscuro="#2dd4bf",
        icono_bootstrap="bi-heart-pulse",
    ),
    "ventalibra": Identidad(
        nombre="VentaLibra",
        rubro="Punto de venta para retail",
        color="#d97706",
        color_oscuro="#b45309",
        color_claro="#fffbeb",
        color_sobre_oscuro="#fbbf24",
        icono_bootstrap="bi-upc-scan",
    ),
    "libradesk": Identidad(
        nombre="LibraDesk",
        rubro="Empresas de IT",
        color="#4f46e5",
        color_oscuro="#4338ca",
        color_claro="#eef2ff",
        color_sobre_oscuro="#818cf8",
        icono_bootstrap="bi-headset",
    ),
    "libracargo": Identidad(
        nombre="LibraCargo",
        rubro="Agencias de cargas",
        color="#012c83",
        color_oscuro="#001d5c",
        color_claro="#eef3fc",
        color_sobre_oscuro="#7aa2f7",
        icono_bootstrap="bi-truck",
    ),
    "libraclub": Identidad(
        nombre="LibraClub",
        rubro="Complejos deportivos",
        color="#017b4b",
        color_oscuro="#015c38",
        color_claro="#ecfdf5",
        color_sobre_oscuro="#34d399",
        icono_bootstrap="bi-trophy",
    ),
}


def nombre_icono(sitio: str) -> str:
    """El nombre del ícono sin el prefijo `bi-` (`truck`), que es como se llama el
    archivo en Bootstrap Icons y la clave de `iconos_bootstrap.TRAZOS`."""
    return IDENTIDAD[sitio].icono_bootstrap.removeprefix("bi-")


def marca_icono_html(sitio: str) -> str:
    """El `<i>` que va dentro del cuadrado `.logo-icon` del navbar y del pie, en
    lugar de la inicial del producto."""
    return f'<i class="bi {IDENTIDAD[sitio].icono_bootstrap}"></i>'
