"""BigNumFloat.py -> My implementation of arbitrary precision floats using the BigNum behaviour from Python
Work In Progress!
Main user classes:

BigNumFloat.BigNumFloat(Sign: bool, Exponent: int, Mantissa: int) -> Main user class for storing and working with the BigNum class
	Main User Functions:

	__add__(self: Self, Other: "BigNumFloat") -> "BigNumFloat" -> Main function to add BigNumFloats
	__sub__(self: Self, Other: "BigNumFloat") -> "BigNumFloat" -> Main function to sub BigNumFloats
	__mul__(self: Self, Other: "BigNumFloat") -> "BigNumFloat" -> Main function to mul BigNumFloats
	__div__(self: Self, Other: "BigNumFloat") -> "BigNumFloat" -> Main function to div BigNumFloats
	ConvertIEEEFloatToBigNumFloat(self: Self, InputFloat: float) -> "BigNumFloat" -> Main function to convert Python native floats to BigNumFloats
"""

#Libraries used
import logging
from typing import Self
import math

#Handle logging
LOGLEVEL = logging.WARNING

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)
logging.getLogger().setLevel(LOGLEVEL)

DIVISIONPRECISIONINDIGITSGLOBAL: int = 10

class BigNumFloat():
	"""BigNumFloat.BigNumFloat(Sign: bool, Exponent: int, Mantissa: int) -> Main user class for storing and working with the BigNum class
	Main User Functions:

	__add__(self: Self, Other: "BigNumFloat") -> "BigNumFloat" -> Main function to add BigNumFloats
	__sub__(self: Self, Other: "BigNumFloat") -> "BigNumFloat" -> Main function to sub BigNumFloats
	__mul__(self: Self, Other: "BigNumFloat") -> "BigNumFloat" -> Main function to mul BigNumFloats
	__div__(self: Self, Other: "BigNumFloat") -> "BigNumFloat" -> Main function to div BigNumFloats
	ConvertIEEEFloatToBigNumFloat(self: Self, InputFloat: float) -> "BigNumFloat" -> Main function to convert Python native floats to BigNumFloats
	"""

	def __init__(self: Self, Sign: bool = True, Exponent: int = 0, Mantissa: int = 0, DivisionPrecisionInDigits: int = DIVISIONPRECISIONINDIGITSGLOBAL) -> None:
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

		#Create initial output variables to work on
		OutputSign: bool = True
		OutputExponent: int = 0
		OutputMantissa: int = 0

		LargerExponentMantissa: int = 0
		SmallerExponentMantissa: int = 0

		LargerExponent: int = 0
		SmallerExponent: int = 0

		#Figure out which variable has a higher or lower exponent
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
		
		#Make sure the mantissas are aligned according to their exponents
		DeltaExponent: int = LargerExponent - SmallerExponent
		LargerExponentMantissa = LargerExponentMantissa * 10**(DeltaExponent)

		#Do the actual adding
		OutputMantissa = LargerExponentMantissa + SmallerExponentMantissa
		#Make sure signs are handled properly
		if OutputMantissa < 0:
			OutputSign = False
			OutputMantissa *= -1
		
		if (not self.Sign) and (not Other.Sign):
			OutputSign = False
		elif (self.Sign) and (not Other.Sign):
			OutputSign = False

		Result: "BigNumFloat" = BigNumFloat(OutputSign, OutputExponent, OutputMantissa)
		return Result
	
	def __raw_sub__(self: Self, Other: "BigNumFloat") -> "BigNumFloat":

		#Create initial output variables to work on
		OutputSign: bool = self.Sign
		OutputExponent: int = 0
		OutputMantissa: int = 0

		LargerExponentMantissa: int = 0
		SmallerExponentMantissa: int = 0

		LargerExponent: int = 0
		SmallerExponent: int = 0

		#Figure out which variable has a higher or lower exponent
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
		
		#Make sure the mantissas are aligned according to their exponents
		DeltaExponent: int = LargerExponent - SmallerExponent
		LargerExponentMantissa = LargerExponentMantissa * 10**(DeltaExponent)

		#Do the actual subtracting
		OutputMantissa = LargerExponentMantissa - SmallerExponentMantissa
		
		#Make sure signs are handled properly
		if OutputMantissa < 0:
			OutputSign = False
			OutputMantissa *= -1

		Result: "BigNumFloat" = BigNumFloat(OutputSign, OutputExponent, OutputMantissa)
		return Result
	
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
				return Other.__raw_add__(self)
			else:
				return self.__raw_sub__(Other)

	def __mul__(self: Self, Other: "BigNumFloat") -> "BigNumFloat":

		#Create initial output variables to work on
		OutputSign: bool = True
		OutputExponent: int = 0

		LargerExponentMantissa: int = 0
		SmallerExponentMantissa: int = 0

		LargerExponent: int = 0
		SmallerExponent: int = 0

		#Figure out which variable has a higher or lower exponent
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
		
		#Make sure the mantissas are aligned according to their exponents
		DeltaExponent: int = LargerExponent - SmallerExponent
		LargerExponentMantissa = LargerExponentMantissa * 10**(DeltaExponent)
		
		#Do the actual multiplication
		OutputMantissa = int(LargerExponentMantissa * SmallerExponentMantissa)

		#Make sure signs are handled properly
		OutputSign = bool(int((int(self.Sign)+int(Other.Sign))/2))

		#Make sure the exponent is handled properly
		OutputExponent = SmallerExponent - DeltaExponent

		Result: "BigNumFloat" = BigNumFloat(OutputSign, OutputExponent, OutputMantissa)
		return Result

	def __truediv__(self: Self, Other: "BigNumFloat", ) -> "BigNumFloat":

		if Other.IsZero():
			raise ZeroDivisionError
		
		if self.IsZero():
			return self

		#Create initial output variables to work on
		OutputSign: bool = True
		OutputExponent: int = 0
		OutputMantissa: int = 0
		OutputMantissaAsString: str = ""

		LargerExponentMantissa: int = 0
		SmallerExponentMantissa: int = 0

		LargerExponent: int = 0
		SmallerExponent: int = 0
		TemporaryScaledDividend: int = 0
		TemporaryMultipliedScaledDividend: int = 0
		SubtractionResult: int = 0
		SelfIsLarger: bool = True

		#Figure out which variable has a higher or lower exponent
		if Other.Exponent - self.Exponent >= 0:
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
		
		#Make sure the mantissas are aligned according to their exponents
		DeltaExponent: int = LargerExponent - SmallerExponent
		LargerExponentMantissa = LargerExponentMantissa * 10**(DeltaExponent)

		#Make sure the dividend and divisor are the right ones after alignment from exponents
		DivisorMantissa: int = 0
		DividendMantissa: int = 0

		if SelfIsLarger:
			DivisorMantissa = LargerExponentMantissa
			DividendMantissa = SmallerExponentMantissa
		else:
			DivisorMantissa = SmallerExponentMantissa
			DividendMantissa = LargerExponentMantissa
		
		#Save lengths for looping
		DivisorLength: int = len(str(DivisorMantissa))
		DividendLength: int = len(str(DividendMantissa))

		#Compensate for DivisionPrecisionInDigits
		DivisorMantissa *= 10**(self.DivisionPrecisionInDigits+DividendLength)
		
		#Do the actual long ass division
		DivisionIterationLength: int = (DivisorLength+DividendLength+self.DivisionPrecisionInDigits)-1
		for i in range(DivisionIterationLength, 0, -1):
			#Practically bute forcing the long ass division for easier implementation
			TemporaryScaledDividend = DividendMantissa * 10**i

			#Iterate through the different digits it could be computing
			#Since I basically brute force this, I 'need' to check for multiplying the dividend by 0 to not omit 0's in the result
			for j in range(9, -1, -1):
				TemporaryMultipliedScaledDividend = j * TemporaryScaledDividend

				#Calculate final subtraction with everything compensated for and aligned properly
				SubtractionResult = DivisorMantissa - TemporaryMultipliedScaledDividend

				if SubtractionResult >= 0:
					#Write the result to OutputMantissaAsString
					OutputMantissaAsString += str(j)
					if j == 0:
						continue

					#Make sure the DivisorMantissa is kept up to date
					DivisorMantissa = DivisorMantissa-TemporaryMultipliedScaledDividend
					break
		
		#Final conversion from string to int
		OutputMantissa = int(OutputMantissaAsString)

		#Make sure the exponent is handled properly
		OutputExponent = self.Exponent + Other.Exponent - self.DivisionPrecisionInDigits - DividendLength + 1

		#Make sure signs are handled properly
		OutputSign = bool(int((int(self.Sign)+int(Other.Sign))/2))

		Result: "BigNumFloat" = BigNumFloat(OutputSign, OutputExponent, OutputMantissa)
		return Result

	def ConvertIEEEFloatToBigNumFloat(self: Self, InputFloat: float) -> "BigNumFloat":
		#Create initial output variables to work on
		OutputSign: bool = True
		OutputExponent: int = 0
		OutputMantissa: int = 0
		TemporaryMantissa: float = InputFloat

		#Handle the sign first
		if InputFloat < 0:
			OutputSign = False
			TemporaryMantissa *= -1

		#Handle digits properly
		if math.floor(InputFloat)-InputFloat != 0:
			OutputExponent = -self.DivisionPrecisionInDigits
			TemporaryMantissa = InputFloat*(10**self.DivisionPrecisionInDigits)
		
		#Make sure mantissa is an int
		OutputMantissa = int(TemporaryMantissa)

		return BigNumFloat(OutputSign, OutputExponent, OutputMantissa)

	def IsZero(self: Self) -> bool:
		return self.Mantissa == 0

	def __repr__(self) -> str:
		return "BigNumFloat.BigNumFloat(Sign=%s, Exponent=%s, Mantissa=%s)" % (self.Sign, int(self.Exponent), int(self.Mantissa))
	
	def __str__(self) -> str:
		#Handle 0 or sign properly
		logging.debug("BigNumFloat.__str__():")
		OutputString: str = ""
		if not self.IsZero():
			if self.Sign:
				OutputString += "+"
			else:
				OutputString += "-"
		else:
			self.Sign = True
			return "0"
		
		#Lazily convert to string
		logging.debug("Exponent: %s" % (self.Exponent))
		OutputString += str(int(self.Mantissa * 10**(self.Exponent)))

		#Actually show decimals too
		OutputString += "."

		TemporaryStringMantissa: str = str(self.Mantissa)

		#Handle leading zeros if they are there
		LeadinZeros: int = -self.Exponent - len(TemporaryStringMantissa)
		if LeadinZeros > 0:
			OutputString += "0" * LeadinZeros
		else:
			#Apparently if there are no leading zeros I need to pop the first digit?
			TemporaryStringMantissa = TemporaryStringMantissa[1:]
		
		logging.debug("TemporaryStringMantissa: %s, Exponent: %s, LeadingZeros: %s" % (TemporaryStringMantissa, self.Exponent, LeadinZeros))
		TemporaryMantissa: str = TemporaryStringMantissa[:-self.Exponent]
		logging.debug("TemporaryMantissa: %s" % (TemporaryMantissa))
		OutputString += TemporaryMantissa

		return OutputString
