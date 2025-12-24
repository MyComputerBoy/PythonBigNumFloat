"""BigNumFloat.py -> My implementation of arbitrary precision floats using the BigNum behaviour from Python
"""

#Libraries used
import logging
from typing import Self
import math

#Handle logging
LOGLEVEL = logging.DEBUG

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)
logging.getLogger().setLevel(LOGLEVEL)

DECIMALPRECISIONINDIGITS: int = 7

class BigNumFloat():
	def __init__(self: Self, Sign: bool, Exponent: int, IntegerPart: int, DecimalPart: int, DecimalPrecisionInDigits: int = DECIMALPRECISIONINDIGITS) -> None:

		self.Sign: bool = Sign
		self.Exponent: int = Exponent
		self.IntegerPartMantissa: int = IntegerPart
		self.DecimalPartMantissa: int = DecimalPart

		self.DECIMALPRECISIONINDIGITS: int = DecimalPrecisionInDigits
	
	def CheckLargerThanDecimalDigitLength(self: Self, IntegerToCheck: int) -> list[int]:
		CarryOut: int
		OutputInteger: int

		if IntegerToCheck >= 10**self.DECIMALPRECISIONINDIGITS:
			OutputInteger = IntegerToCheck % (10**self.DECIMALPRECISIONINDIGITS)
			CarryOut = 1

		return [CarryOut, OutputInteger]
	
	def ConvertUnsignedToSigned(self: Self, InputDecimalMantissa: int, InputIntegerMantissa: int, Sign: bool) -> list[int]:
		if not Sign:
			InputDecimalMantissa *= -1
			InputIntegerMantissa *= -1
		
		return InputDecimalMantissa, InputIntegerMantissa
	
	def ConvertSignedToUnsigned(self: Self, InputDecimalMantissa: int, inputIntegerMantissa) -> list[int]:
		OutputSign: int = 1
		if inputIntegerMantissa < 0:
			InputDecimalMantissa *= -1
			inputIntegerMantissa *= -1
			OutputSign = 0
		
		return OutputSign, InputDecimalMantissa, inputIntegerMantissa

	def __add__(self: Self, Other: "BigNumFloat") -> "BigNumFloat":
		OutputSign: bool = self.Sign
		OutputExponent: int
		OutputIntegerPartMantissa: int
		OutputDecimalPartMantissa: int

		self.DecimalPartMantissa, self.IntegerPartMantissa = self.ConvertUnsignedToSigned(self.DecimalPartMantissa, self.IntegerPartMantissa, self.Sign)
		Other.DecimalPartMantissa, Other.IntegerPartMantissa = self.CheckLargerThanDecimalDigitLength(Other.DecimalPartMantissa, Other.IntegerPartMantissa, Other.Sign)
		
		DecimalPartCarryOut, OutputDecimalPartMantissa = self.CheckLargerThanDecimalDigitLength(self.DecimalPartMantissa + Other.DecimalPartMantissa)
		OutputIntegerPartMantissa = self.IntegerPartMantissa + Other.IntegerPartMantissa + DecimalPartCarryOut

		OutputSignInt, OutputDecimalPartMantissa, OutputIntegerPartMantissa = self.ConvertSignedToUnsigned(OutputDecimalPartMantissa, OutputIntegerPartMantissa)
		if OutputSignInt == 1:
			OutputSign = True
		else:
			OutputSign = False

		return BigNumFloat(OutputSign, OutputExponent, OutputIntegerPartMantissa, OutputDecimalPartMantissa)

