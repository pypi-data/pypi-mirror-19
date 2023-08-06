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




class FormatConverterJson2JsonStr(AbstractFormatConverter):

	def getFromFormat(self):
		return "json"

	def getToFormat(self):
		return "jsonstr"

	def getConversionCost(self):
		return 20

	def convert(self, tempDir, inputData):
		return json.dumps(inputData, separators=(',', ':'))



















