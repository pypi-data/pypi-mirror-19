#!/usr/bin/env python3
# -*- coding: utf-8 -*-





import os
import sys
import sh





class AbstractFormatConverter(object):
	__nextID = 1

	@property
	def objID(self):
		if not hasattr(self, '__id'):
			setattr(self, '__id', AbstractFormatConverter.__nextID)
			AbstractFormatConverter.__nextID += 1
		return getattr(self, '__id')

	def getFromFormat(self):
		raise NotImplementedError('subclasses must override getFromFormat()!')

	def getToFormat(self):
		raise NotImplementedError('subclasses must override getToFormat()!')

	def getConversionCost(self):
		raise NotImplementedError('subclasses must override getConversionCost()!')

	def convert(self, tempDir, inputData):
		raise NotImplementedError('subclasses must override convert()!')

	def __str__(self):
		return self.getFromFormat() + "->" + self.getToFormat()

	@property
	def fromFormat(self):
		return self.getFromFormat()

	@property
	def toFormat(self):
		return self.getToFormat()

	@property
	def conversionCost(self):
		return self.getConversionCost()


















