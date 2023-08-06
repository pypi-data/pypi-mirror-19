#!/usr/bin/env python3
# -*- coding: utf-8 -*-





import sh
import os
import sys

import jk_temporary

from .AbstractFormatConverter import AbstractFormatConverter
from .FormatConverterChain import FormatConverterChain

from .FormatConverterXml2XmlFile import FormatConverterXml2XmlFile
from .FormatConverterXmlFile2Xml import FormatConverterXmlFile2Xml
from .FormatConverterJsonFile2Json import FormatConverterJsonFile2Json
from .FormatConverterJson2JsonFile import FormatConverterJson2JsonFile
from .FormatConverterXmlStr2XmlFile import FormatConverterXmlStr2XmlFile
from .FormatConverterJson2XmlStr import FormatConverterJson2XmlStr
from .FormatConverterXmlStr2Xml import FormatConverterXmlStr2Xml
from .FormatConverterJson2JsonStr import FormatConverterJson2JsonStr
from .FormatConverterJsonStr2Json import FormatConverterJsonStr2Json
from .FormatConverterJsonFile2JsonStr import FormatConverterJsonFile2JsonStr
from .FormatConverterXmlStr2Json import FormatConverterXmlStr2Json
from .FormatConverterXmlFile2XmlStr import FormatConverterXmlFile2XmlStr




#
# This class will manage indiviudal format converters internally and with their help will perform the format conversions as desired.
#
class FormatConverter(object):

	def __init__(self, tempDirPath):
		assert isinstance(tempDirPath, str)

		self.__tempDir = jk_temporary.TempDir(tempDirPath)
		self.__tempDir.clear()

		self.__allBasicConverters = [	# the instances
				FormatConverterXml2XmlFile(),
				FormatConverterXmlFile2Xml(),
				FormatConverterXmlStr2XmlFile(),
				FormatConverterXmlStr2Xml(),
				FormatConverterJson2JsonFile(),
				FormatConverterJson2JsonStr(),
				FormatConverterJson2XmlStr(),
				FormatConverterJsonFile2Json(),
				FormatConverterJsonStr2Json(),
				FormatConverterJsonFile2JsonStr(),
				FormatConverterXmlStr2Json(),
				FormatConverterXmlFile2XmlStr(),
			]

		allFormats = set()
		for converter in self.__allBasicConverters:
			allFormats.add(converter.getFromFormat())
			allFormats.add(converter.getToFormat())

		self.__chains = {}
		for chain in self.__buildAllPossibleConversionChains():
			convID = chain.convID
			if convID in self.__chains:
				existingChain = self.__chains[convID]
				if chain.getConversionCost() < existingChain.getConversionCost():
					self.__chains[convID] = chain
			else:
				self.__chains[convID] = chain

	#
	# Get a list of formats supported.
	#
	# @return		string[]		Returns a list of IDs.
	#
	def listFormats(self):
		ret = set()
		for c in self.__allBasicConverters:
			ret.add(c.fromFormat)
			ret.add(c.toFormat)
		ret = list(ret)
		ret.sort()
		return ret

	#
	# Get a list of all conversions supported.
	#
	# @return		string[]		Returns a list of IDs.
	#
	def listConversions(self):
		ret = list(self.__chains.keys())
		ret.sort()
		return ret

	#
	# Convert the input data.
	#
	# @param		string convID			A conversion ID such as f.e. "xmlstr->jsonstr".
	# @param		object inputData		The input data. The type of this data must correlate with the source format type specified.
	# @return		object					The result data. The type of this data will depend on the conversion specified.
	#
	def convert1(self, convID, inputData):
		c = self.getConverter1(convID)
		if c is None:
			return None
		return c.convert(self.__tempDir, inputData)

	#
	# Convert the input data.
	#
	# @param		string fromFormat		The source format of the conversion.
	# @param		string toFormat			The target format desired.
	# @param		object inputData		The input data. The type of this data must correlate with the source format type specified.
	# @return		object					The result data. The type of this data will depend on the conversion specified.
	#
	def convert2(self, fromFormat, toFormat, inputData):
		c = self.getConverter2(fromFormat, toFormat)
		if c is None:
			return None
		return c.convert(self.__tempDir, inputData)

	#
	# Get a converter by conversion ID.
	#
	# @param		string convID			A conversion ID such as f.e. "xmlstr->jsonstr".
	# @return		AbstractConverter		Eiter returns <c>None</c> if no converter is available or the converter object that performs the conversion.
	#
	def getConverter1(self, convID):
		if convID in self.__chains:
			return self.__chains[convID]
		return None

	#
	# Get a converter by conversion ID.
	#
	# @param		string fromFormat		The source format of the conversion.
	# @param		string toFormat			The target format desired.
	# @return		AbstractConverter		Eiter returns <c>None</c> if no converter is available or the converter object that performs the conversion.
	#
	def getConverter2(self, fromFormat, toFormat):
		formatConvIDStr = fromFormat + "->" + toFormat
		if formatConvIDStr in self.__chains:
			return self.__chains[formatConvIDStr]
		return None

	def __buildAllPossibleConversionChains(self):
		chains = []
		# build initial chains
		for c in self.__allBasicConverters:
			chains.append(FormatConverterChain(c))
		# loop building new chains
		nGen = 0
		lastChains = chains
		while True:
			# build all possible derivations
			nextChains = []
			# print("\tGeneration: " + str(nGen))
			for chain in lastChains:
				newChains = chain.deriveAllChains(self.__allBasicConverters)
				nextChains.extend(newChains)
			nGen += 1
			# no more derivations?
			if len(nextChains) == 0:
				break
			# add created derivations
			chains.extend(nextChains)
			lastChains = nextChains
			# if nGen == 10:
			#	exit()
		# return all created chains
		return chains

	def __getAllPossibleFromConverters(self, fromFormat):
		ret = []
		for converter in self.__allBasicConverters:
			if converter.getFromFormat() == fromFormat:
				ret.append(converter)
		return ret







