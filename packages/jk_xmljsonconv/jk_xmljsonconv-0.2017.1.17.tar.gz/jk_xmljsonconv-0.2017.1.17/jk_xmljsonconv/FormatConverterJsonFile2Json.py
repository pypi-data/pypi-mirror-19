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




class FormatConverterJsonFile2Json(AbstractFormatConverter):

	def getFromFormat(self):
		return "jsonfile"

	def getToFormat(self):
		return "json"

	def getConversionCost(self):
		return 20

	def convert(self, tempDir, inputData):
		with codecs.open(inputData, 'r', 'utf-8') as f:
			return json.load(f, strict = False)


















