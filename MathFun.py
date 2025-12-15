"""MathFun.py -> My math library having fun with my BigNumFloat lobrary
"""

import BigNumFloat
import logging
from typing import Self
from PIL import Image as IM
import time
import math

#Handle logging
LOGLEVEL = logging.WARNING

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)
logging.getLogger().setLevel(LOGLEVEL)

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

	def CopyWithoutCloning(self: Self) -> "BigNumComplex":
		return BigNumComplex(self.Real, self.Imaginary)

	def __str__(self: Self) -> str:
		return "%s + %si" % (str(self.Real), str(self.Imaginary))

#Create BigNumFloat handler for ease of use, and define FUOR preemtively
BNFHandlerGlobal: "BigNumFloat.BigNumFloat" = BigNumFloat.BigNumFloat()
FOUR: "BigNumFloat.BigNumFloat" = BNFHandlerGlobal.ConvertIEEEFloatToBigNumFloat(4)

def SingleMandelbrotCalculation(InputComplexNumber: "BigNumComplex", OffsetComplexNumber: "BigNumComplex") -> "BigNumComplex":
	MultiplicationPart: "BigNumComplex" = (InputComplexNumber * InputComplexNumber)
	AdditionPart: "BigNumComplex" = MultiplicationPart + OffsetComplexNumber
	return AdditionPart

def DepthInMandelbrotSet(InputComplexNumber: "BigNumComplex", IterationDepth: int) -> int:
	global FOUR

	#Preemtive check if the magnitude squared is already over four
	Magnitude: "BigNumFloat.BigNumFloat" = InputComplexNumber.GetMagnitudeSquared()
	SignToTest: "BigNumFloat.BigNumFloat" = Magnitude - FOUR
	if SignToTest.Sign:
		return 0

	#Clone without using pointer
	IterationComplexNumber: "BigNumComplex" = InputComplexNumber.CopyWithoutCloning()
	if IterationComplexNumber is InputComplexNumber:
		raise Exception("Cloned objects, not copied.")

	#Actual Mandelbrot iterations
	for i in range(IterationDepth):
		#Actual computation
		IterationComplexNumber = SingleMandelbrotCalculation(IterationComplexNumber, InputComplexNumber)

		#Computing magnitude squared
		Magnitude: "BigNumFloat.BigNumFloat" = IterationComplexNumber.GetMagnitudeSquared()

		SignToTest: "BigNumFloat.BigNumFloat" = Magnitude - FOUR
		if SignToTest.Sign:
			return i

	return IterationDepth

def __main__():
	#Handle basic variables
	StartTime = time.time()
	BNFHandler: "BigNumFloat.BigNumFloat" = BigNumFloat.BigNumFloat()

	IterationDepth: int = 100

	XResolution: int = 1920
	YResolution: int = 1920
	XStart: float = -1
	YStart: float = -1
	XEnd: float = 1
	YEnd: float = 1

	#Handle path to save to image
	FormatName: str = "%s.%s,%s.%s,IterationDepth%s,Resolution%s" % (XStart, YStart, XEnd, YEnd, IterationDepth, XResolution)
	ImagePath: str = "D:/Users/hatel/Pictures/BigNumFloat/" + FormatName

	#Convert static variables
	XResolutionBN: "BigNumFloat.BigNumFloat" = BNFHandler.ConvertIEEEFloatToBigNumFloat(XResolution)
	YResolutionBN: "BigNumFloat.BigNumFloat" = BNFHandler.ConvertIEEEFloatToBigNumFloat(YResolution)

	XStartBN: "BigNumFloat.BigNumFloat" = BNFHandler.ConvertIEEEFloatToBigNumFloat(XStart)
	XEndBN: "BigNumFloat.BigNumFloat" = BNFHandler.ConvertIEEEFloatToBigNumFloat(XEnd)

	YStartBN: "BigNumFloat.BigNumFloat" = BNFHandler.ConvertIEEEFloatToBigNumFloat(YStart)
	YEndBN: "BigNumFloat.BigNumFloat" = BNFHandler.ConvertIEEEFloatToBigNumFloat(YEnd)

	#Convert more 'dynamic' variables
	DXBN: "BigNumFloat.BigNumFloat" = XEndBN - XStartBN
	DYBN: "BigNumFloat.BigNumFloat" = YEndBN - YStartBN
	XDXBN: "BigNumFloat.BigNumFloat" = DXBN/XResolutionBN
	YDYBN: "BigNumFloat.BigNumFloat" = DYBN/YResolutionBN

	XScalar: "BigNumFloat.BigNumFloat"
	YScalar: "BigNumFloat.BigNumFloat"
	XPosition: "BigNumFloat.BigNumFloat"
	YPosition: "BigNumFloat.BigNumFloat"
	TemporaryComplexNumber: "BigNumComplex"

	#Handle image saving
	
	WorkingImage = IM.new('F', size=(XResolution,YResolution))
	WorkingImagePixels = WorkingImage.load()

	#Do the actual Mandelbrot calculations
	for i in range(XResolution):
		TemporaryOutputString: str = ""
		for j in range(YResolution):
			XScalar = BNFHandler.ConvertIEEEFloatToBigNumFloat(i) * XDXBN
			YScalar = BNFHandler.ConvertIEEEFloatToBigNumFloat(j) * YDYBN
			YPosition = YStartBN + YScalar
			XPosition = XStartBN + XScalar

			TemporaryComplexNumber = BigNumComplex(YPosition, XPosition)

			TemporaryDepthInMandelbrot: int = DepthInMandelbrotSet(TemporaryComplexNumber, IterationDepth)

			PointProcessed: float = TemporaryDepthInMandelbrot/IterationDepth
			WorkingImagePixels[i,j] = PointProcessed
			if TemporaryDepthInMandelbrot == IterationDepth:
				TemporaryOutputString += "■"
			else:
				TemporaryOutputString += " "
		print("|%s|" % (TemporaryOutputString))
	
	EndTime = time.time()
	dTime = math.floor(EndTime-StartTime)
	WorkingImage.save("%s,%ss.tiff" % (ImagePath, dTime))

__main__()

input("End of program.")
