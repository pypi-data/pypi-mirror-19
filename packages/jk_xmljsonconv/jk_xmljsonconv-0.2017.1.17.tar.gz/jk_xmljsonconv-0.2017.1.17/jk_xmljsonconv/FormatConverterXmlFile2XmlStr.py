#!/usr/bin/env python3
# -*- coding: utf-8 -*-





import sh
import os
import sys
import json
import codecs

import jk_temporary

from json import *

from .AbstractFormatConverter import AbstractFormatConverter




class FormatConverterXmlFile2XmlStr(AbstractFormatConverter):

	def getFromFormat(self):
		return "xmlfile"

	def getToFormat(self):
		return "xmlstr"

	def getConversionCost(self):
		return 10

	def convert(self, tempDir, inputData):
		with codecs.open(inputData, 'r', 'utf-8') as f:
			return "".join(f.readlines())


















