import BigNumFloat
from typing import Self

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
	
	def __str__(self: Self) -> str:
		return "%s + %si" % (str(self.Real), str(self.Imaginary))