#!/usr/bin/env python
"""SQuaRE Status Microservice proxy (api.lsst.codes-compliant)"""
from .server import server, standalone
__all__ = ["server", "standalone"]
