#!/usr/bin/env python3
# -*- coding: utf-8 -*-





import sh
import os
import sys

import jk_temporary

from xml.dom import minidom

from .AbstractFormatConverter import AbstractFormatConverter




class FormatConverterXmlFile2Xml(AbstractFormatConverter):

	def getFromFormat(self):
		return "xmlfile"

	def getToFormat(self):
		return "xml"

	def getConversionCost(self):
		return 20

	def convert(self, tempDir, inputData):
		return minidom.parse(inputData)


















