"""BigNumFloat.py -> My implementation of arbitrary precision floats using the BigNum behaviour from Python
"""

#Libraries used
import logging
from typing import Self
# import math

#Handle logging
LOGLEVEL = logging.DEBUG

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)
logging.getLogger().setLevel(LOGLEVEL)

DECIMALPRECISIONINDIGITS: int = 7

class BigNumFloat():
	def __init__(self: Self, Sign: bool, Exponent: int, IntegerPart: int, DecimalPart: int, DecimalPrecisionInDigits: int = DECIMALPRECISIONINDIGITS, DoDebugging: bool = False) -> None:
		self.Sign: bool = Sign
		self.Exponent: int = Exponent
		self.IntegerPartMantissa: int = IntegerPart
		self.DecimalPartMantissa: int = DecimalPart

		self.DECIMALPRECISIONINDIGITS: int = DecimalPrecisionInDigits

		#Debugging shit
		self.DODEBUGGING: bool = DoDebugging
	
	def CheckLargerThanDecimalDigitLength(self: Self, IntegerToCheck: int) -> list[int]:
		CarryOut: int = 0
		OutputInteger: int = IntegerToCheck
		DecimalSize: int = 10**self.DECIMALPRECISIONINDIGITS

		if IntegerToCheck >= DecimalSize:
			OutputInteger = IntegerToCheck % DecimalSize
			CarryOut = 1

		return [CarryOut, OutputInteger]
	
	def ConvertUnsignedToSigned(self: Self, InputDecimalMantissa: int = 0, InputIntegerMantissa: int = 0, Sign: bool = True) -> list[int]:
		if not Sign:
			InputDecimalMantissa *= -1
			InputIntegerMantissa *= -1
		
		return [InputDecimalMantissa, InputIntegerMantissa]
	
	def ConvertSignedToUnsigned(self: Self, InputDecimalMantissa: int, inputIntegerMantissa: int) -> list[int]:
		OutputSign: int = 1
		if inputIntegerMantissa < 0:
			InputDecimalMantissa *= -1
			inputIntegerMantissa *= -1
			OutputSign = 0
		
		return [OutputSign, InputDecimalMantissa, inputIntegerMantissa]

	def __add__(self: Self, Other: "BigNumFloat") -> "BigNumFloat":
		self.DoDebuggingAtFunctionStart("__add__", [self.__repr__(), Other.__repr__()])
		#Boring setup
		OutputSign: bool = self.Sign
		OutputSignInt: int
		OutputExponent: int = 0
		OutputIntegerPartMantissa: int
		OutputDecimalPartMantissa: int

		#Making sure the input numbers are signed for easier computations
		self.DecimalPartMantissa, self.IntegerPartMantissa = self.ConvertUnsignedToSigned(self.DecimalPartMantissa, self.IntegerPartMantissa, self.Sign)
		Other.DecimalPartMantissa, Other.IntegerPartMantissa = Other.ConvertUnsignedToSigned(Other.DecimalPartMantissa, Other.IntegerPartMantissa, Other.Sign)

		#Do the actual computation on the decimal part
		OutputDecimalPartMantissa = self.DecimalPartMantissa + Other.DecimalPartMantissa
		self.DoDebuggingLog("DecimalPartMantissa computation: %s" % (OutputDecimalPartMantissa))
		
		#Make sure the decimal part is within the defined size
		DecimalPartCarryOut, OutputDecimalPartMantissa = self.CheckLargerThanDecimalDigitLength(OutputDecimalPartMantissa)
		self.DoDebuggingLog("DecimalPartMantissa computation: %s" % (OutputDecimalPartMantissa))

		#Do the actual computation on the integer part
		OutputIntegerPartMantissa = self.IntegerPartMantissa + Other.IntegerPartMantissa + DecimalPartCarryOut

		#Making sure the output is unsigned, but using the self.Signed bool for sign
		OutputSignInt, OutputDecimalPartMantissa, OutputIntegerPartMantissa = self.ConvertSignedToUnsigned(OutputDecimalPartMantissa, OutputIntegerPartMantissa)
		self.DoDebuggingLog("DecimalPartMantissa computation: %s" % (OutputDecimalPartMantissa))
		if OutputSignInt == 1:
			OutputSign = True
		else:
			OutputSign = False

		return BigNumFloat(OutputSign, OutputExponent, OutputIntegerPartMantissa, OutputDecimalPartMantissa)
	
	def __sub__(self: Self, Other: "BigNumFloat") -> "BigNumFloat":
		self.DoDebuggingAtFunctionStart("__sub__", [self.__repr__(), Other.__repr__()])
		#Boring setup
		OutputSign: bool = self.Sign
		OutputSignInt: int
		OutputExponent: int = 0
		OutputIntegerPartMantissa: int
		OutputDecimalPartMantissa: int

		#Making sure the input numbers are signed for easier computations
		self.DecimalPartMantissa, self.IntegerPartMantissa = self.ConvertUnsignedToSigned(self.DecimalPartMantissa, self.IntegerPartMantissa, self.Sign)
		Other.DecimalPartMantissa, Other.IntegerPartMantissa = Other.ConvertUnsignedToSigned(Other.DecimalPartMantissa, Other.IntegerPartMantissa, Other.Sign)

		#Do the actual computation on the decimal part
		OutputDecimalPartMantissa = self.DecimalPartMantissa - Other.DecimalPartMantissa
		
		#Make sure the decimal part is within the defined size
		DecimalPartCarryOut, OutputDecimalPartMantissa = self.CheckLargerThanDecimalDigitLength(OutputDecimalPartMantissa)

		#Do the actual computation on the integer part
		OutputIntegerPartMantissa = self.IntegerPartMantissa + Other.IntegerPartMantissa - DecimalPartCarryOut

		#Making sure the output is unsigned, but using the self.Signed bool for sign
		OutputSignInt, OutputDecimalPartMantissa, OutputIntegerPartMantissa = self.ConvertSignedToUnsigned(OutputDecimalPartMantissa, OutputIntegerPartMantissa)
		if OutputSignInt == 1:
			OutputSign = True
		else:
			OutputSign = False

		return BigNumFloat(OutputSign, OutputExponent, OutputIntegerPartMantissa, OutputDecimalPartMantissa)
	
	def __mul__(self: Self, Other: "BigNumFloat") -> "BigNumFloat":
		self.DoDebuggingAtFunctionStart("__mul__", [self.__repr__(), Other.__repr__()])
		#Boring setup
		OutputSign: bool = self.Sign
		OutputSignInt: int
		OutputExponent: int = 0
		OutputIntegerPartMantissa: int = 0
		OutputDecimalPartMantissa: int = 0
		OutputMantissaWorker: int
		WorkerMantissaA: int
		WorkerMantissaB: int
		ShiftingFactor: int = 10**(self.DECIMALPRECISIONINDIGITS)

		#Making sure the input numbers are signed for easier computations
		self.DecimalPartMantissa, self.IntegerPartMantissa = self.ConvertUnsignedToSigned(self.DecimalPartMantissa, self.IntegerPartMantissa, self.Sign)
		Other.DecimalPartMantissa, Other.IntegerPartMantissa = Other.ConvertUnsignedToSigned(Other.DecimalPartMantissa, Other.IntegerPartMantissa, Other.Sign)

		#Convert input numbers to singular integers for easier computation
		WorkerMantissaA = self.IntegerPartMantissa * ShiftingFactor + self.DecimalPartMantissa
		WorkerMantissaB = Other.IntegerPartMantissa * ShiftingFactor + Other.DecimalPartMantissa

		#Do the actual computation
		OutputMantissaWorker = WorkerMantissaA * WorkerMantissaB

		#Make sure the output is within specs of format
		OutputDecimalPartMantissa = int(OutputMantissaWorker / ShiftingFactor) % ShiftingFactor
		OutputIntegerPartMantissa = int(OutputMantissaWorker / (ShiftingFactor * ShiftingFactor))

		#Making sure the output is unsigned, but using the self.Signed bool for sign
		OutputSignInt, OutputDecimalPartMantissa, OutputIntegerPartMantissa = self.ConvertSignedToUnsigned(OutputDecimalPartMantissa, OutputDecimalPartMantissa)
		if OutputSignInt == 1:
			OutputSign = True
		else:
			OutputSign = False

		return BigNumFloat(OutputSign, OutputExponent, OutputIntegerPartMantissa, OutputDecimalPartMantissa)

	def IsZero(self: Self) -> bool:
		if self.DecimalPartMantissa == 0 and self.IntegerPartMantissa == 0:
			return True
		return False
	
	def DoDebuggingAtFunctionStart(self: Self, FunctionName: str, vArgs: list[str]) -> None:
		if self.DODEBUGGING:
			OutputString: str = "BigNumFloat.%s(%s)" % (FunctionName, vArgs)
			logging.debug(OutputString)

	def DoDebuggingLog(self: Self, Log: str) -> None:
		if self.DODEBUGGING:
			logging.debug(Log)

	def __repr__(self: Self) -> str:
		OutputString: str = ""

		OutputString = "BigNumFloat.BigNumFloat(Sign: bool = %s, Exponent: int = %s, IntegerPart: int = %s, DecimalPart: int = %s, DecimalPrecisionInDigits: int = %s)" % (self.Sign, self.Exponent, self.IntegerPartMantissa, self.DecimalPartMantissa, self.DECIMALPRECISIONINDIGITS)

		return OutputString
