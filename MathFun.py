import BigNumFloat
from typing import Self

BigNumFloat.DIVISIONPRECISIONINDIGITSGLOBAL = 10

class BigNumComplex():
	def __init__(self: Self, Real: "BigNumFloat.BigNumFloat", Imaginary: "BigNumFloat.BigNumFloat") -> None:
		self.Real: "BigNumFloat.BigNumFloat" = Real
		self.Imaginary: "BigNumFloat.BigNumFloat" = Imaginary
	
	def __add__(self: Self, Other: "BigNumComplex") -> "BigNumComplex":
		RealPart: "BigNumFloat.BigNumFloat" = self.Real + Other.Real
		ImaginaryPart: "BigNumFloat.BigNumFloat" = self.Imaginary + Other.Imaginary

		return BigNumComplex(RealPart, ImaginaryPart)
	
	def __sub__(self: Self, Other: "BigNumComplex") -> "BigNumComplex":
		RealPart: "BigNumFloat.BigNumFloat" = self.Real - Other.Real
		ImaginaryPart: "BigNumFloat.BigNumFloat" = self.Imaginary - Other.Imaginary

		return BigNumComplex(RealPart, ImaginaryPart)
	
	def __mul__(self: Self, Other: "BigNumComplex") -> "BigNumComplex":
		RealPart: "BigNumFloat.BigNumFloat" = (self.Real * Other.Real) - (self.Imaginary * Other.Imaginary)
		ImaginaryPart: "BigNumFloat.BigNumFloat" = (self.Real * Other.Imaginary) + (self.Imaginary * Other.Real)

		return BigNumComplex(RealPart, ImaginaryPart)
	
	def __truediv__(self: Self, Other: "BigNumComplex") ->"BigNumComplex":
		RealPartDivisor: "BigNumFloat.BigNumFloat" = (self.Real*Other.Real) + (self.Imaginary * Other.Imaginary)
		RealPartDividend: "BigNumFloat.BigNumFloat" = Other.Real * Other.Real + Other.Imaginary * Other.Imaginary
		ImaginaryPartDivisor: "BigNumFloat.BigNumFloat" = (self.Imaginary * Other.Real) - (self.Real * Other.Imaginary)
		ImaginaryPartDividend: "BigNumFloat.BigNumFloat" = Other.Real * Other.Real + Other.Imaginary * Other.Imaginary

		RealPart: "BigNumFloat.BigNumFloat" = RealPartDivisor / RealPartDividend
		ImaginaryPart: "BigNumFloat.BigNumFloat" = ImaginaryPartDivisor / ImaginaryPartDividend

		return BigNumComplex(RealPart, ImaginaryPart)
	
	def GetMagnitudeSquared(self: Self) -> "BigNumFloat.BigNumFloat":
		return self.Real * self.Real + self.Imaginary * self.Imaginary

	def __str__(self: Self) -> str:
		return "%s + %si" % (str(self.Real), str(self.Imaginary))

BNFHandlerGlobal: "BigNumFloat.BigNumFloat" = BigNumFloat.BigNumFloat()
FOUR: "BigNumFloat.BigNumFloat" = BNFHandlerGlobal.ConvertIEEEFloatToBigNumFloat(4)

def SingleMandelbrotCalculation(InputComplexNumber: "BigNumComplex", OffsetComplexNumber: "BigNumComplex") -> "BigNumComplex":
	return InputComplexNumber * InputComplexNumber + OffsetComplexNumber

def DepthInMandelbrotSet(InputComplexNumber: "BigNumComplex", IterationDepth: int) -> int:
	global FOUR
	SignToTest: "BigNumFloat.BigNumFloat" = InputComplexNumber.GetMagnitudeSquared() - FOUR
	if not SignToTest.Sign:
		return 0
	
	IterationComplexNumber: "BigNumComplex" = InputComplexNumber
	for i in range(IterationDepth):
		IterationComplexNumber = SingleMandelbrotCalculation(IterationComplexNumber, InputComplexNumber)

		SignToTest: "BigNumFloat.BigNumFloat" = InputComplexNumber.GetMagnitudeSquared() - FOUR
		if not SignToTest.Sign:
			return i
	
	return IterationDepth

def __main__(DoDebug: bool = True):
	BNFHandler: "BigNumFloat.BigNumFloat" = BigNumFloat.BigNumFloat()

	IterationDepth: int = 100

	XResolution: int = 1024
	YResolution: int = 1024
	XStart: float = -1
	YStart: float = -1
	XEnd: float = 1
	YEnd: float = 1

	XResolutionBN: "BigNumFloat.BigNumFloat" = BNFHandler.ConvertIEEEFloatToBigNumFloat(XResolution)
	YResolutionBN: "BigNumFloat.BigNumFloat" = BNFHandler.ConvertIEEEFloatToBigNumFloat(YResolution)

	XStartBN: "BigNumFloat.BigNumFloat" = BNFHandler.ConvertIEEEFloatToBigNumFloat(XStart)
	XEndBN: "BigNumFloat.BigNumFloat" = BNFHandler.ConvertIEEEFloatToBigNumFloat(XEnd)

	YStartBN: "BigNumFloat.BigNumFloat" = BNFHandler.ConvertIEEEFloatToBigNumFloat(YStart)
	YEndBN: "BigNumFloat.BigNumFloat" = BNFHandler.ConvertIEEEFloatToBigNumFloat(YEnd)

	XDXBN: "BigNumFloat.BigNumFloat" = (XStartBN - XEndBN)/XResolutionBN
	YDYBN: "BigNumFloat.BigNumFloat" = (YStartBN - YEndBN)/YResolutionBN

	XScalar: "BigNumFloat.BigNumFloat"
	YScalar: "BigNumFloat.BigNumFloat"
	XPosition: "BigNumFloat.BigNumFloat"
	YPosition: "BigNumFloat.BigNumFloat"
	TemporaryComplexNumber: "BigNumComplex"

	if DoDebug:
		input()

	for i in range(XResolution):
		TemporaryOutputString: str = ""
		for j in range(YResolution):
			XScalar = BNFHandler.ConvertIEEEFloatToBigNumFloat(i)
			YScalar = BNFHandler.ConvertIEEEFloatToBigNumFloat(j)

			XPosition = XStartBN + (XDXBN * XScalar)
			YPosition = YStartBN + (YDYBN * YScalar)

			TemporaryComplexNumber = BigNumComplex(XPosition, YPosition)
			TemporaryDepthInMandelbrot: int = DepthInMandelbrotSet(TemporaryComplexNumber, IterationDepth)
			if TemporaryDepthInMandelbrot == IterationDepth:
				TemporaryOutputString += "■"
			else:
				TemporaryOutputString += " "
		print(TemporaryOutputString)
	
	input()

# __main__()

a: "BigNumFloat.BigNumFloat" = BNFHandlerGlobal.ConvertIEEEFloatToBigNumFloat(1)
b: "BigNumFloat.BigNumFloat" = BNFHandlerGlobal.ConvertIEEEFloatToBigNumFloat(1000)

c: "BigNumFloat.BigNumFloat" = a/b
print(c)

input()
