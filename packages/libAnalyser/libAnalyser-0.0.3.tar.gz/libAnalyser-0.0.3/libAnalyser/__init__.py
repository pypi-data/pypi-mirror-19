#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import sys

def __libAnalyser():
    from libAnalyser import libAnalyser
    
    return libAnalyser()

sys.modules['libAnalyser'] = __libAnalyser()