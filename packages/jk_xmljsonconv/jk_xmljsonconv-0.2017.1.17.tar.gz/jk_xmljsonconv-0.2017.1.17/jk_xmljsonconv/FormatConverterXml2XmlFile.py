#!/usr/bin/env python3
# -*- coding: utf-8 -*-





import sh
import os
import sys

import jk_temporary

from xml.dom import *

from .AbstractFormatConverter import AbstractFormatConverter




class FormatConverterXml2XmlFile(AbstractFormatConverter):

	def getFromFormat(self):
		return "xml"

	def getToFormat(self):
		return "xmlfile"

	def getConversionCost(self):
		return 20

	def convert(self, tempDir, inputData):
		filePath = tempDir.newFilePath(extension = ".xml")
		with open(filePath,"wb") as f:
			inputData.writexml(f)
		return filePath

















