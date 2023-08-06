# -*- coding: utf-8 -*-
"""
    pyedna
    ~~~~~
    A set of Python wrappers for functions in the eDNA API.

    :copyright: (c) 2017 by Eric Strong.
    :license: Refer to LICENSE.txt for more information.
"""

__version__ = '0.12'

from .ezdna import DoesIDExist, GetRTFull, GetHistAvg, GetHistInterp, GetHistMax, \
                 GetHistMin, GetHistRaw, GetHistSnap, SelectPoint, LoadDll, \
				 GetMultipleTags, HistAppendValues, HistUpdateInsertValues