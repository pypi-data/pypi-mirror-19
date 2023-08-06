#!/usr/bin/env python3
# -*- coding: utf-8 -*-





import sh
import os
import sys

import jk_temporary

from .AbstractFormatConverter import AbstractFormatConverter




class FormatConverterChain(AbstractFormatConverter):

	#
	# Initialization method.
	#
	# @param		any converterOrConverters		Either an instance of <c>AbstractFormatConverter</c> or a list of
	#												instances of <c>AbstractFormatConverter</c> objects.
	#
	def __init__(self, converterOrConverters):
		if converterOrConverters is None:
			raise Exception("Argument converterOrConverters must either be a converter or a list of converters!")

		if isinstance(converterOrConverters, FormatConverterChain):
			# clone
			self.__converters = list(converterOrConverters.__converters)
			self.__fromFormat = converterOrConverters.getFromFormat()
			self.__toFormat = converterOrConverters.getToFormat()
			self.__conversionCost = converterOrConverters.getConversionCost()
		else:
			# build from data
			if isinstance(converterOrConverters, list):
				for converter in converterOrConverters:
					if not isinstance(converter, AbstractFormatConverter):
						raise Exception("Converter of unsuitable class type: " + type(converter))
				self.__converters = converterOrConverters
			else:
				if not isinstance(converterOrConverters, AbstractFormatConverter):
					raise Exception("Converter of unsuitable class type: " + type(converterOrConverters))
				self.__converters = [ converterOrConverters ]

			self.__fromFormat = self.__converters[0].getFromFormat()
			self.__toFormat = self.__converters[len(self.__converters) - 1].getToFormat()
			self.__conversionCost = 0
			for converter in self.__converters:
				self.__conversionCost += converter.getConversionCost()

	@property
	def length(self):
		return len(self.__converters)

	#
	# check wether this converter can be appended to the chain
	#
	def canAppend(self, converter):
		if converter.getFromFormat() != self.getToFormat():
			return False
		for c in self.__converters:
			if c.objID == converter.objID:
				return False
			if converter.getToFormat() == c.getFromFormat():
				return False
		# print("\tcan append: " + str(self) + "  and  " + str(converter))
		return True

	def deriveAllChains(self, allConverters):
		ret = []
		for converter in allConverters:
			if self.canAppend(converter):
				newChain = FormatConverterChain(self)
				newChain.append(converter)
				# print("\tBUILDING CHAIN: existing: " + str(self) + ",  adding: " + str(converter) + ",  result: " + str(newChain))
				ret.append(newChain)
		return ret

	@property
	def convID(self):
		return self.getFromFormat() + "->" + self.getToFormat()

	def __str__(self):
		s = self.__converters[0].getFromFormat()
		for converter in self.__converters:
			s += "->"
			s += converter.getToFormat()
		return s

	#
	# append a converter to the chain
	#
	def append(self, converter):
		if not self.canAppend(converter):
			raise Exception("Converter can not be appended to chain: " + self.__str__())

		self.__converters.append(converter)
		self.__toFormat = converter.getToFormat()
		self.__conversionCost += converter.getConversionCost()

	def getFromFormat(self):
		return self.__fromFormat

	def getToFormat(self):
		return self.__toFormat

	def getConversionCost(self):
		return self.__conversionCost + len(self.__converters)

	def convert(self, tempDir, inputData):
		data = inputData
		for converter in self.__converters:
			# print(">> CONVERTING WITH: " + str(converter))
			# print(">> IN: " + str(data))
			data = converter.convert(tempDir, data)
			# print(">> OUT: " + str(data))
		# print(">> RESULT: " + str(data))
		return data















