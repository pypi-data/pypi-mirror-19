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




class FormatConverterJsonStr2Json(AbstractFormatConverter):

	def getFromFormat(self):
		return "jsonstr"

	def getToFormat(self):
		return "json"

	def getConversionCost(self):
		return 20

	def convert(self, tempDir, inputData):
		return json.loads(inputData, strict = False)


















