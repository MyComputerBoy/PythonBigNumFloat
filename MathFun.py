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
LOGLEVEL = logging.DEBUG

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)
logging.getLogger().setLevel(LOGLEVEL)

class RealMathClass():
	def __init__(self: Self, DoDebugging: bool = False) -> None:
		self.BNFFHandler: "BigNumFloat.BigNumFloat" = BigNumFloat.BigNumFloat()

		self.ONE: "BigNumFloat.BigNumFloat" = self.BNFFHandler.ConvertIEEEFloatToBigNumFloat(1)

		self.DODEBUGGING: bool = DoDebugging

	def Factulty(self: Self, Input: "BigNumFloat.BigNumFloat") -> "BigNumFloat.BigNumFloat":
		if self.DODEBUGGING:
			logging.debug("MathFun.Faculty(%s):" % (Input))
		Output: "BigNumFloat.BigNumFloat" = self.BNFFHandler.ConvertIEEEFloatToBigNumFloat(1)
		# Scalar: "BigNumFloat.BigNumFloat"

		# # try:
		# FacultyInIEEEInt: int = math.floor(float(Input.__str__()))
		# # except ValueError:
		# # 	raise ValueError("Error: Input must be of type BigNumFloat.BigNumFloat.")
		
		for i in Input:
			# if self.DODEBUGGING:
			# 	logging.debug("i: %s" % (i))
			# 	logging.debug("Output: %s" % (Output))
			Output *= i
		
		return Output
	
	def Knr(self: Self, n: "BigNumFloat.BigNumFloat", r:"BigNumFloat.BigNumFloat") -> "BigNumFloat.BigNumFloat":
		OutputDivisor: "BigNumFloat.BigNumFloat" = self.Factulty(n)
		OutputDividend: "BigNumFloat.BigNumFloat" = self.Factulty(n-r)

		return OutputDivisor/OutputDividend

	def IntegerExponentiation(self: Self, Base: "BigNumFloat.BigNumFloat", Exponent: "BigNumFloat.BigNumFloat") -> "BigNumFloat.BigNumFloat":
		# if self.DODEBUGGING:
		# 	logging.debug("MathFun.RealMathClass.IntegerExponentiation(%s, %s)" % (Base, Exponent))
		
		# if Exponent.IsZero():
		# 	if self.DODEBUGGING:
		# 		logging.debug("Exponent is ZERO! Return 1 automatically.")
		# 		OutputInteger = self.BNFFHandler.ConvertIEEEFloatToBigNumFloat(1)
		# 		# input("IntegerExponentiation Output: %s from %s,%s" % (OutputInteger, Base, Exponent))
		# 		return OutputInteger
		
		OutputInteger: "BigNumFloat.BigNumFloat" = self.BNFFHandler.ConvertIEEEFloatToBigNumFloat(1)

		AddedExponent: "BigNumFloat.BigNumFloat" = Exponent
		for _ in AddedExponent:
			OutputInteger = OutputInteger * Base
		
		# if self.DODEBUGGING:
		# 	logging.debug("IntegerExponentiation Output: %s from %s,%s" % (OutputInteger.__repr__(), Base, Exponent))

		return OutputInteger
	
	def Exp(self: Self, Exponent: "BigNumFloat.BigNumFloat", IterationDepth: int = 50) -> "BigNumFloat.BigNumFloat":
		Output: "BigNumFloat.BigNumFloat" = self.BNFFHandler.ConvertIEEEFloatToBigNumFloat(0)

		for i in range(IterationDepth):
			IterationIndexInBigNum: "BigNumFloat.BigNumFloat" = self.BNFFHandler.ConvertIEEEFloatToBigNumFloat(i)
			Output += self.IntegerExponentiation(Exponent, IterationIndexInBigNum)/self.Factulty(IterationIndexInBigNum)
		
		return Output
	
	def SquareRoot(self: Self, Input: "BigNumFloat.BigNumFloat", IterationDepth: int = 50) -> "BigNumFloat.BigNumFloat":
		if self.DODEBUGGING:
			logging.debug("MathFun.RealMathClass.SquareRoot(%s)" % (Input.__repr__()))
		TWO: "BigNumFloat.BigNumFloat" = self.BNFFHandler.ConvertIEEEFloatToBigNumFloat(2)
		OutputEstimate: "BigNumFloat.BigNumFloat" = self.BNFFHandler.ConvertIEEEFloatToBigNumFloat(1)

		Divisor: "BigNumFloat.BigNumFloat"
		Dividend: "BigNumFloat.BigNumFloat"
		EstimateSquared: "BigNumFloat.BigNumFloat"

		for _ in range(IterationDepth):
			if self.DODEBUGGING:
				logging.debug("Estimate: %s" % (OutputEstimate))

			EstimateSquared = OutputEstimate*OutputEstimate
			Divisor = EstimateSquared-Input
			Dividend = TWO * OutputEstimate

			if self.DODEBUGGING:
				logging.debug("Divisor: %s, Dividend: %s" % (Divisor, Dividend))

			OutputEstimate -= Divisor/Dividend
		
		return OutputEstimate

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
RMHandlerGlobal: "RealMathClass" = RealMathClass()
BNFHandlerGlobal: "BigNumFloat.BigNumFloat" = BigNumFloat.BigNumFloat()
ONE: "BigNumFloat.BigNumFloat" = BNFHandlerGlobal.ConvertIEEEFloatToBigNumFloat(1)
TWO: "BigNumFloat.BigNumFloat" = BNFHandlerGlobal.ConvertIEEEFloatToBigNumFloat(2)
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

def MainMandelbrotRendering():
	#Handle basic variables
	StartTime = time.time()
	BNFHandler: "BigNumFloat.BigNumFloat" = BigNumFloat.BigNumFloat()

	#Resolution stuff
	IterationDepth: int = 1024
	XResolution: int = 2560
	YResolution: int = 1440

	#Convert static variables
	XResolutionBN: "BigNumFloat.BigNumFloat" = BNFHandler.ConvertIEEEFloatToBigNumFloat(XResolution)
	YResolutionBN: "BigNumFloat.BigNumFloat" = BNFHandler.ConvertIEEEFloatToBigNumFloat(YResolution)

	XStartBN: "BigNumFloat.BigNumFloat" = BigNumFloat.BigNumFloat(False, -14, 115033999708200)
	XEndBN:   "BigNumFloat.BigNumFloat" = BigNumFloat.BigNumFloat(False, -14, 115033805557266)

	YStartBN:  "BigNumFloat.BigNumFloat" = BigNumFloat.BigNumFloat(True, -12, 275698882967)
	YEndBN:    "BigNumFloat.BigNumFloat" = BigNumFloat.BigNumFloat(True, -12, 275699975066)

	#Handle path to save to image
	FormatName: str = "%s.%s,%s.%s,IterationDepth%s,Resolution%s" % (XStartBN.Mantissa, YStartBN.Mantissa, XEndBN.Mantissa, YEndBN.Mantissa, IterationDepth, XResolution)
	ImagePath: str = "D:/Users/hatel/Pictures/BigNumFloat/" + FormatName

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
	#Invert y axis for making the console output match the final output
	for j in range(YResolution-1, -1, -1):
		TemporaryOutputString: str = ""
		for i in range(XResolution):
			TemporaryComplexNumber = BigNumComplex(XPosition, YPosition)
			# logging.debug("Position: %s" % (TemporaryComplexNumber))

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
	print("Delta Time: %s" % (dTime))
	WorkingImage.save("%s,%ss.tiff" % (ImagePath, dTime)) # type: ignore

def RamanujanSatoSeries(IterationDepth: int = 10, DoDebugging: bool = True):
	if DoDebugging:
		logging.debug("MathFun.__main__():")
	BNFHandler: "BigNumFloat.BigNumFloat" = BigNumFloat.BigNumFloat()
	RealMathHandler: "RealMathClass" = RealMathClass()
	
	ONE: "BigNumFloat.BigNumFloat" = BNFHandler.ConvertIEEEFloatToBigNumFloat(1)
	TWO: "BigNumFloat.BigNumFloat" = BNFHandler.ConvertIEEEFloatToBigNumFloat(2)
	FOUR: "BigNumFloat.BigNumFloat" = BNFHandler.ConvertIEEEFloatToBigNumFloat(4)
	NINETYNINE: "BigNumFloat.BigNumFloat" = BNFHandler.ConvertIEEEFloatToBigNumFloat(99)
	THREENINETYSIX: "BigNumFloat.BigNumFloat" = BNFHandler.ConvertIEEEFloatToBigNumFloat(396)
	ELEVENOTHREE: "BigNumFloat.BigNumFloat" = BNFHandler.ConvertIEEEFloatToBigNumFloat(1103)
	LARGE: "BigNumFloat.BigNumFloat" = BNFHandler.ConvertIEEEFloatToBigNumFloat(26390)

	if DoDebugging:
		logging.debug("Static variables declared. Starting dynamic variables.")
	Sum: "BigNumFloat.BigNumFloat" = BNFHandler.ConvertIEEEFloatToBigNumFloat(0)
	SCALAR: "BigNumFloat.BigNumFloat" = TWO*RealMathHandler.SquareRoot(TWO)/(NINETYNINE*NINETYNINE)

	PartOneFacultyDivisor: "BigNumFloat.BigNumFloat"
	PartOneExponentDividend: "BigNumFloat.BigNumFloat"
	PartOneFacultyDividend: "BigNumFloat.BigNumFloat"

	PartTwoDivisor: "BigNumFloat.BigNumFloat"
	PartTwoExponentDividend: "BigNumFloat.BigNumFloat"

	PartOne: "BigNumFloat.BigNumFloat"
	PartTwo: "BigNumFloat.BigNumFloat"

	Output: "BigNumFloat.BigNumFloat"

	# KnownPi: "BigNumFloat.BigNumFloat" = BigNumFloat.BigNumFloat(True, -1000, 31415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679821480865132823066470938446095505822317253594081284811174502841027019385211055596446229489549303819644288109756659334461284756482337867831652712019091456485669234603486104543266482133936072602491412737245870066063155881748815209209628292540917153643678925903600113305305488204665213841469519415116094330572703657595919530921861173819326117931051185480744623799627495673518857527248912279381830119491298336733624406566430860213949463952247371907021798609437027705392171762931767523846748184676694051320005681271452635608277857713427577896091736371787214684409012249534301465495853710507922796892589235420199561121290219608640344181598136297747713099605187072113499999983729780499510597317328160963185950244594553469083026425223082533446850352619311881710100031378387528865875332083814206171776691473035982534904287554687311595628638823537875937519577818577805321712268066130019278766111959092164201989)

	logging.debug("Starting Main Ramanujan Sato loop.")
	for i in range(IterationDepth):
		if DoDebugging:
			logging.debug("Iteration: %s/%s" % (i, IterationDepth))
		IterationIndexInBigNum: "BigNumFloat.BigNumFloat" = BNFHandler.ConvertIEEEFloatToBigNumFloat(i)

		PartOneFacultyDivisor = RealMathHandler.Factulty(FOUR*IterationIndexInBigNum)
		PartOneFacultyDividend = RealMathHandler.Factulty(IterationIndexInBigNum)
		PartOneExponentDividend = RealMathHandler.IntegerExponentiation(PartOneFacultyDividend, FOUR)

		PartTwoDivisor = LARGE * IterationIndexInBigNum + ELEVENOTHREE
		PartTwoExponentDividend = RealMathHandler.IntegerExponentiation(THREENINETYSIX, FOUR*IterationIndexInBigNum)
		# logging.debug("PartTwo: Divisor: %s, Dividend: %s" % (PartTwoDivisor, PartTwoExponentDividend))
        
		PartOne = PartOneFacultyDivisor/PartOneExponentDividend
		PartTwo = PartTwoDivisor/PartTwoExponentDividend
		# logging.debug("PartOne: %s, PartTwo: %s" % (PartOne, PartTwo))
		# input("Important Part!")
		# if DoDebugging:
		# 	logging.debug("\nPartOne:  %s, PartTwo: %s" % (PartOne, PartTwo))

		Sum += PartOne * PartTwo
	
	Output = ONE / (Sum * SCALAR)
	# DeltaOutput: "BigNumFloat.BigNumFloat" = KnownPi - Output

	print("\n\nOutput: %s" % (Output.__repr__()))
	# print("Delta known pi: %s" % (DeltaOutput))

MainMandelbrotRendering()

input("Rendering done.")
