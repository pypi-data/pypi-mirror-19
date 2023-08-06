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




class FormatConverterJson2JsonFile(AbstractFormatConverter):

	def getFromFormat(self):
		return "json"

	def getToFormat(self):
		return "jsonfile"

	def getConversionCost(self):
		return 10

	def convert(self, tempDir, inputData):
		newData = json.dumps(inputData, separators=(',',':'))
		(filePath, fd) = tempDir.createFileUTF8(extension = ".json")
		fd.write(newData)
		fd.close()
		return filePath


















