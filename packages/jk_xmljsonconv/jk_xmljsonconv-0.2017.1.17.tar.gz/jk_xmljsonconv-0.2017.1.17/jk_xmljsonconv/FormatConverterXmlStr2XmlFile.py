#!/usr/bin/env python3
# -*- coding: utf-8 -*-





import sh
import os
import sys

import jk_temporary

from xml.dom import *

from .AbstractFormatConverter import AbstractFormatConverter




class FormatConverterXmlStr2XmlFile(AbstractFormatConverter):

	def getFromFormat(self):
		return "xmlstr"

	def getToFormat(self):
		return "xmlfile"

	def getConversionCost(self):
		return 10

	def convert(self, tempDir, inputData):
		(filePath, fd) = tempDir.createFileUTF8(extension = ".xml")
		fd.write(inputData)
		fd.close()
		return filePath

















