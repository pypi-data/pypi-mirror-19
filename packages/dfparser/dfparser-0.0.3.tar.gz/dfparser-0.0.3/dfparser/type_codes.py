#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 13:00:27 2017

@author: chernov
"""

header_types = {
    "DEFAULT": 0x00014000
  }

meta_types = {
    "UNDEFINED_METATYPE": 0x00000000,
    "JSON_METATYPE": 0x00010000,
    "QDATASTREAM_METATYPE": 0x00010007 
  }

binary_types = {
    "UNDEFINED_BINARY": 0x00000000,
    "POINT_DIRECT_BINARY": 0x00000100,
    "POINT_QDATASTREAM_BINARY": 0x00000107,
    "HV_BINARY": 0x00000200,
    "HV_TEXT_BINARY": 0x00000201 
  }