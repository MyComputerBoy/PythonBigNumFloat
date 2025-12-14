"""BigNumFloat.py -> My implementation of arbitrary precision floats using the BigNum behaviour from Python
Work In Progress!
Main user classes:

BigNumFloat.BigNumFloat(Sign: bool, Exponent: int, Mantissa: int) -> Main user class for storing and working with the BigNum class
	Main User Functions:

	__add__(self: Self, Other: "BigNumFloat") -> "BigNumFloat" -> Main function to add BigNumFloats
	__sub__(self: Self, Other: "BigNumFloat") -> "BigNumFloat" -> Main function to sub BigNumFloats
	__raw_mul__(self: Self, Other: "BigNumFloat") -> "BigNumFloat" -> Main function to mul BigNumFloats
	__raw_div__ | (Work In Progress!!)
	ConvertIEEEFloatToBigNumFloat(self: Self, InputFloat: float) -> "BigNumFloat" -> Main function to convert Python native floats to BigNumFloats
"""

import logging
from typing import Self
import math

LOGLEVEL = logging.WARNING

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)
logging.getLogger().setLevel(LOGLEVEL)

class BigNumFloat():
	"""BigNumFloat.BigNumFloat(Sign: bool, Exponent: int, Mantissa: int) -> Main user class for storing and working with the BigNum class
	Main User Functions:

	__add__(self: Self, Other: "BigNumFloat") -> "BigNumFloat" -> Main function to add BigNumFloats
	__sub__(self: Self, Other: "BigNumFloat") -> "BigNumFloat" -> Main function to sub BigNumFloats
	__raw_mul__(self: Self, Other: "BigNumFloat") -> "BigNumFloat" -> Main function to mul BigNumFloats
	__raw_div__ | (Work In Progress!!)
	ConvertIEEEFloatToBigNumFloat(self: Self, InputFloat: float) -> "BigNumFloat" -> Main function to convert Python native floats to BigNumFloats
	"""
	
	def __init__(self: Self, Sign: bool = True, Exponent: int = 0, Mantissa: int = 0, DivisionPrecisionInDigits: int = 10) -> None:
		#Basic structure of IEEE 754 floats
		#NOTE!!
		#Since Python has signed ints by default, I will redefine the exponent to just be normal numbers, no offset or anything
		#Since arbitrary sizes will make everything more difficult to manage where to subtract from, AND python has signed ints
		#By default, I will not offset at all, just use PLAIN ints!!

		self.Sign: bool = Sign
		self.Exponent: int = Exponent
		self.Mantissa: int = Mantissa

		#Variables to handle dynamic problems
		self.DivisionPrecisionInDigits = DivisionPrecisionInDigits
	
	def __raw_add__(self: Self, Other: "BigNumFloat") -> "BigNumFloat":
		OutputSign: bool = True
		OutputExponent: int = 0
		OutputMantissa: int = 0
		logging.debug("RAW ADDING")
		logging.debug("self: %s" % (self.__repr__()))
		logging.debug("Other: %s" % (Other.__repr__()))

		LargerExponentMantissa: int = 0
		SmallerExponentMantissa: int = 0

		LargerExponent: int = 0
		SmallerExponent: int = 0

		if Other.Exponent - self.Exponent > 0:
			LargerExponent = Other.Exponent
			SmallerExponent = self.Exponent

			LargerExponentMantissa = Other.Mantissa
			SmallerExponentMantissa = self.Mantissa
		else:
			LargerExponent = self.Exponent
			SmallerExponent = Other.Exponent

			LargerExponentMantissa = self.Mantissa
			SmallerExponentMantissa = Other.Mantissa
		
		OutputExponent = SmallerExponent
		
		DeltaExponent: int = LargerExponent - SmallerExponent
		logging.debug("DeltaExponent = %s" % (DeltaExponent))
		LargerExponentMantissa = LargerExponentMantissa * 10**(DeltaExponent)

		OutputMantissa = LargerExponentMantissa + SmallerExponentMantissa
		logging.debug("Initial addition: %s" % (OutputMantissa))

		if OutputMantissa < 0:
			OutputSign = False
			OutputMantissa *= -1
		
		if (not self.Sign) and (not Other.Sign):
			OutputSign = False

		return BigNumFloat(OutputSign, OutputExponent, OutputMantissa)
	
	def __raw_sub__(self: Self, Other: "BigNumFloat") -> "BigNumFloat":
		OutputSign: bool = self.Sign
		OutputExponent: int = 0
		OutputMantissa: int = 0
		logging.debug("RAW SUBTRACTING")
		logging.debug("self: %s" % (self.__repr__()))
		logging.debug("Other: %s" % (Other.__repr__()))

		LargerExponentMantissa: int = 0
		SmallerExponentMantissa: int = 0

		LargerExponent: int = 0
		SmallerExponent: int = 0

		if Other.Exponent - self.Exponent > 0:
			LargerExponent = Other.Exponent
			SmallerExponent = self.Exponent

			LargerExponentMantissa = Other.Mantissa
			SmallerExponentMantissa = self.Mantissa
		else:
			LargerExponent = self.Exponent
			SmallerExponent = Other.Exponent

			LargerExponentMantissa = self.Mantissa
			SmallerExponentMantissa = Other.Mantissa
		
		OutputExponent = SmallerExponent
		
		DeltaExponent: int = LargerExponent - SmallerExponent
		logging.debug("DeltaExponent = %s" % (DeltaExponent))
		LargerExponentMantissa = LargerExponentMantissa * 10**(DeltaExponent)

		OutputMantissa = LargerExponentMantissa - SmallerExponentMantissa
		logging.debug("Initial subtracting: %s" % (OutputMantissa))
		
		if OutputMantissa < 0:
			OutputSign = False
			OutputMantissa *= -1

		return BigNumFloat(OutputSign, OutputExponent, OutputMantissa)

	def __raw_mul__(self: Self, Other: "BigNumFloat") -> "BigNumFloat":
		OutputSign: bool = True
		OutputExponent: int = 0
		OutputMantissa: int = 0
		logging.debug("RAW MULTIPLYING")
		logging.debug("self: %s" % (self.__repr__()))
		logging.debug("Other: %s" % (Other.__repr__()))

		LargerExponentMantissa: int = 0
		SmallerExponentMantissa: int = 0

		LargerExponent: int = 0
		SmallerExponent: int = 0

		if Other.Exponent - self.Exponent > 0:
			LargerExponent = Other.Exponent
			SmallerExponent = self.Exponent

			LargerExponentMantissa = Other.Mantissa
			SmallerExponentMantissa = self.Mantissa
		else:
			LargerExponent = self.Exponent
			SmallerExponent = Other.Exponent

			LargerExponentMantissa = self.Mantissa
			SmallerExponentMantissa = Other.Mantissa
		
		logging.debug("LargerExponent: %s" % (LargerExponent))
		logging.debug("SmallerExponent: %s" % (SmallerExponent))
		
		DeltaExponent: int = LargerExponent - SmallerExponent
		logging.debug("DeltaExponent = %s" % (DeltaExponent))

		LargerExponentMantissa = LargerExponentMantissa * 10**(DeltaExponent)
		
		try:
			OutputMantissa = int(LargerExponentMantissa * SmallerExponentMantissa)
		except OverflowError:
			print("Self: %s, Other: %s" % (self.__str__(), Other.__str__()))
			raise OverflowError

		OutputExponent = SmallerExponent - DeltaExponent

		return BigNumFloat(OutputSign, OutputExponent, OutputMantissa)

	def __raw_div__(self: Self, Other: "BigNumFloat", ) -> "BigNumFloat":
		OutputSign: bool = True
		OutputExponent: int = 0
		OutputMantissa: int = 0
		logging.debug("RAW DIVISION")
		logging.debug("self: %s" % (self.__repr__()))
		logging.debug("Other: %s" % (Other.__repr__()))

		LargerExponentMantissa: int = 0
		SmallerExponentMantissa: int = 0

		LargerExponent: int = 0
		SmallerExponent: int = 0
		SelfIsLarger: bool = True

		if Other.Exponent - self.Exponent > 0:
			LargerExponent = Other.Exponent
			SmallerExponent = self.Exponent

			LargerExponentMantissa = Other.Mantissa
			SmallerExponentMantissa = self.Mantissa
			SelfIsLarger = False
		else:
			LargerExponent = self.Exponent
			SmallerExponent = Other.Exponent

			LargerExponentMantissa = self.Mantissa
			SmallerExponentMantissa = Other.Mantissa
		
		logging.debug("LargerExponent: %s" % (LargerExponent))
		logging.debug("SmallerExponent: %s" % (SmallerExponent))
		
		DeltaExponent: int = LargerExponent - SmallerExponent
		logging.debug("DeltaExponent = %s" % (DeltaExponent))

		LargerExponentMantissa = LargerExponentMantissa * 10**(DeltaExponent)

		DivisorMantissa: int = 0
		DividendMantissa: int = 0

		if SelfIsLarger:
			DivisorMantissa = LargerExponentMantissa
			DividendMantissa = SmallerExponentMantissa
		else:
			DivisorMantissa = SmallerExponentMantissa
			DividendMantissa = LargerExponentMantissa
		
		DivisorMantissa *= 10**(self.DivisionPrecisionInDigits)
		logging.debug(DividendMantissa) #Just to stop the errors

		return BigNumFloat(OutputSign, OutputExponent, OutputMantissa)

	def __add__(self: Self, Other: "BigNumFloat") -> "BigNumFloat":
		if self.Sign:
			if Other.Sign:
				return self.__raw_add__(Other)
			else:
				return self.__raw_sub__(Other)
		else:
			if Other.Sign:
				return Other.__raw_sub__(self)
			else:
				return self.__raw_add__(Other)
	
	def __sub__(self: Self, Other: "BigNumFloat") -> "BigNumFloat":
		if self.Sign:
			if Other.Sign:
				return self.__raw_sub__(Other)
			else:
				return self.__raw_add__(Other)
		else:
			if Other.Sign:
				return Other.__raw_sub__(self)
			else:
				return self.__raw_sub__(Other)

	def ConvertIEEEFloatToBigNumFloat(self: Self, InputFloat: float) -> "BigNumFloat":
		OutputSign: bool = True
		OutputExponent: int = 0
		OutputMantissa: int = 0
		TemporaryMantissa: float = InputFloat

		if InputFloat < 0:
			OutputSign = False
			TemporaryMantissa *= -1

		if math.floor(InputFloat)-InputFloat != 0:
			OutputExponent = -10
			TemporaryMantissa = InputFloat*10**10
		
		OutputMantissa = int(TemporaryMantissa)

		return BigNumFloat(OutputSign, OutputExponent, OutputMantissa)

	def __repr__(self) -> str:
		return "BigNumFloat.BigNumFloat(Sign=%s, Exponent=%s, Mantissa=%s)" % (self.Sign, int(self.Exponent), int(self.Mantissa))
	
	def __str__(self) -> str:
		OutputString: str = ""
		if self.Mantissa != 0:
			if self.Sign:
				OutputString += "+"
			else:
				OutputString += "-"
		else:
			self.Sign = True
			return "0"
		
		OutputString += str(int(self.Mantissa * 10**(self.Exponent)))

		return OutputString
