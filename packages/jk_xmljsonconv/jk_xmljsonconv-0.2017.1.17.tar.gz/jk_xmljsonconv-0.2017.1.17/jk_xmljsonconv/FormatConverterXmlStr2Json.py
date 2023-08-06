#!/usr/bin/env python3
# -*- coding: utf-8 -*-





import sh
import os
import sys

import jk_temporary

import xmltodict
import json



from .AbstractFormatConverter import AbstractFormatConverter




class FormatConverterXmlStr2Json(AbstractFormatConverter):

	def getFromFormat(self):
		return "xmlstr"

	def getToFormat(self):
		return "json"

	def getConversionCost(self):
		return 20

	def convert(self, tempDir, inputData):
		ret = xmltodict.parse(inputData)
		return ret
















