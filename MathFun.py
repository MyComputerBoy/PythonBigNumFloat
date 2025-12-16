"""MathFun.py -> My math library having fun with my BigNumFloat lobrary
Main user classes:

BigNumComplex(self: Self, Real: "BigNumFloat.BigNumFloat", Imaginary: "BigNumFloat.BigNumFloat") -> My BigNum implementation of complex numbers
Main user functions:
	def __add__(self: Self, Other: "BigNumComplex") -> "BigNumComplex" -> adds complex numbers
	def __sub__(self: Self, Other: "BigNumComplex") -> "BigNumComplex" -> subs
	def __mul__(self: Self, Other: "BigNumComplex") -> "BigNumComplex" -> muls
	def __truediv__(self: Self, Other: "BigNumComplex") ->"BigNumComplex" -> divs
	def GetMagnitudeSquared(self: Self) -> "BigNumFloat.BigNumFloat" -> Gets the magnitude without square root, so magnitude squared

Main user functions:
__main__() -> Function to run Mandelbrot Set
NOTE!
I'd highly suggest going into the BigNumFloat.py library to change the DIVISIONPRECISIONINDIGITSGLOBAL per usage, as it can unnescessarily slow down processing
It can also be needed to increase the precision depending on your usage
But you can set starting coordinates and ending coordinates as well as resolution and iteration depths in the start of the function
You should probably also change the ImagePath to a path on your own system to be able to save any renders xD
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
		return BigNumComplex(self.Real + Other.Real, self.Imaginary + Other.Imaginary)

	def __sub__(self: Self, Other: "BigNumComplex") -> "BigNumComplex":
		return BigNumComplex(self.Real - Other.Real, self.Imaginary - Other.Imaginary)

	def __mul__(self: Self, Other: "BigNumComplex") -> "BigNumComplex":
		return BigNumComplex(((self.Real * Other.Real) - (self.Imaginary * Other.Imaginary)), ((self.Real * Other.Imaginary) + (self.Imaginary * Other.Real)))

	def __truediv__(self: Self, Other: "BigNumComplex") ->"BigNumComplex":
		RealPartDivisor: "BigNumFloat.BigNumFloat" = (self.Real*Other.Real) + (self.Imaginary * Other.Imaginary)
		RealPartDividend: "BigNumFloat.BigNumFloat" = Other.Real * Other.Real + Other.Imaginary * Other.Imaginary
		ImaginaryPartDivisor: "BigNumFloat.BigNumFloat" = (self.Imaginary * Other.Real) - (self.Real * Other.Imaginary)
		ImaginaryPartDividend: "BigNumFloat.BigNumFloat" = Other.Real * Other.Real + Other.Imaginary * Other.Imaginary

		return BigNumComplex((RealPartDivisor / RealPartDividend), (ImaginaryPartDivisor / ImaginaryPartDividend))

	def GetMagnitudeSquared(self: Self) -> "BigNumFloat.BigNumFloat":
		return (self.Real * self.Real) + (self.Imaginary * self.Imaginary)

	def CopyWithoutCloning(self: Self) -> "BigNumComplex":
		return BigNumComplex(self.Real, self.Imaginary)

	def __str__(self: Self) -> str:
		return "%s + %si" % (str(self.Real), str(self.Imaginary))

#Create BigNumFloat handler for ease of use, and define FUOR preemtively
BNFHandlerGlobal: "BigNumFloat.BigNumFloat" = BigNumFloat.BigNumFloat()
FOUR: "BigNumFloat.BigNumFloat" = BNFHandlerGlobal.ConvertIEEEFloatToBigNumFloat(4)

def SingleMandelbrotCalculation(InputComplexNumber: "BigNumComplex", OffsetComplexNumber: "BigNumComplex") -> "BigNumComplex":
	return (InputComplexNumber * InputComplexNumber) + OffsetComplexNumber

def DepthInMandelbrotSet(InputComplexNumber: "BigNumComplex", IterationDepth: int) -> int:
	global FOUR

	#Preemtive check if the magnitude squared is already over four
	SignToTest: "BigNumFloat.BigNumFloat" = InputComplexNumber.GetMagnitudeSquared() - FOUR
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
		SignToTest: "BigNumFloat.BigNumFloat" = IterationComplexNumber.GetMagnitudeSquared() - FOUR
		if SignToTest.Sign:
			return i

	return IterationDepth

def __main__():
	#Handle basic variables
	StartTime = time.time()
	BNFHandler: "BigNumFloat.BigNumFloat" = BigNumFloat.BigNumFloat()

	#Resolution stuff
	IterationDepth: int = 1024
	XResolution: int = 1920
	YResolution: int = 1080

	#Coordinate stuff
	XStart: float = -1.150341291421
	YStart: float = 0.275699601513
	XEnd: float = -1.150338702743
	YEnd: float = 0.275701095725

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

	XPosition: "BigNumFloat.BigNumFloat"
	YPosition: "BigNumFloat.BigNumFloat"
	TemporaryComplexNumber: "BigNumComplex"

	#Handle image saving
	
	WorkingImage = IM.new('F', size=(XResolution,YResolution)) # type: ignore
	WorkingImagePixels = WorkingImage.load() # type: ignore

	XPosition = XStartBN
	YPosition = YStartBN

	#Do the actual Mandelbrot calculations
	for j in range(YResolution):
		TemporaryOutputString: str = ""
		for i in range(XResolution):
			TemporaryComplexNumber = BigNumComplex(XPosition, YPosition)
			logging.debug("Position: %s" % (TemporaryComplexNumber))

			#Do actual iterations
			TemporaryDepthInMandelbrot: int = DepthInMandelbrotSet(TemporaryComplexNumber, IterationDepth)

			#Process output to image
			PointProcessed: float = TemporaryDepthInMandelbrot/IterationDepth
			WorkingImagePixels[i,j] = PointProcessed # type: ignore
			if TemporaryDepthInMandelbrot == IterationDepth:
				TemporaryOutputString += "■"
			else:
				TemporaryOutputString += " "
			#Convert to BigNumFloat positions, then BigNumComplex
			XPosition = XPosition + XDXBN
		XPosition = XStartBN
		YPosition = YPosition + YDYBN
		print("|%s|" % (TemporaryOutputString))
	
	EndTime = time.time()
	dTime = math.floor(EndTime-StartTime)
	WorkingImage.save("%s,%ss.tiff" % (ImagePath, dTime)) # type: ignore

__main__()

input("End of program.")
