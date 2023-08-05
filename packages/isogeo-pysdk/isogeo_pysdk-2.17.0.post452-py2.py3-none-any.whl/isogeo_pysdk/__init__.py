﻿#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This module is an abstraction calls about the Isogeo REST API.
    http://www.isogeo.com/
"""

from .isogeo_sdk import Isogeo
from .translator import IsogeoTranslator

__version__ = "2.17.0-452"
VERSION = __version__
