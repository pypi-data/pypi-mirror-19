#!/usr/bin/env python3
# -*- coding: utf-8 -*-





import sh
import os
import sys
import json
import codecs
import dicttoxml						# https://pypi.python.org/pypi/dicttoxml

import jk_temporary

from json import *

from .AbstractFormatConverter import AbstractFormatConverter




class FormatConverterJson2XmlStr(AbstractFormatConverter):

	def getFromFormat(self):
		return "json"

	def getToFormat(self):
		return "xmlstr"

	def getConversionCost(self):
		return 20

	def convert(self, tempDir, inputData):
		return dicttoxml.dicttoxml(inputData)


















