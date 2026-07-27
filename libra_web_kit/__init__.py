"""libra-web-kit — backend de login gateado de /docs/ compartido por las
landings de la familia Libra (Contalibra, Restolibra, Gestiolibra,
MedLibra, VentaLibra). Extraído 2026-07-26 de `auth/app.py`, que era
>85% idéntico entre los cinco -- ver
wiki/analyses/auditoria-duplicacion-familia-libra.md.
"""

try:
    from importlib.metadata import version as _version

    __version__ = _version("libra-web-kit")
except Exception:
    __version__ = "0.0.0.dev0"
