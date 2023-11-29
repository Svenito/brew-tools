# -*- coding: utf-8 -*-
import importlib.metadata


try:
    __version__ = importlib.metadata.version("brew-tools")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"
