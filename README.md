# PythonBigNumFloat
Floating point format with BigNum for arbitrary resolution

BigNumFloat.py -> My implementation of arbitrary precision floats using the BigNum behaviour from Python
Work In Progress!
Main user classes:

BigNumFloat.BigNumFloat(Sign: bool, Exponent: int, Mantissa: int) -> Main user class for storing and working with the BigNum class
	Main User Functions:

	__add__(self: Self, Other: "BigNumFloat") -> "BigNumFloat" -> Main function to add BigNumFloats
	__sub__(self: Self, Other: "BigNumFloat") -> "BigNumFloat" -> Main function to sub BigNumFloats
	__mul__(self: Self, Other: "BigNumFloat") -> "BigNumFloat" -> Main function to mul BigNumFloats
	__div__(self: Self, Other: "BigNumFloat") -> "BigNumFloat" -> Main function to div BigNumFloats
	ConvertIEEEFloatToBigNumFloat(self: Self, InputFloat: float) -> "BigNumFloat" -> Main function to convert Python native floats to BigNumFloats

I have also made a math library using my BigNumFloat library, right now it's just some basic complex numbers and Mandelbrot set somputation.
I have plans on doing other fun maths implementations to test both speed and for bugs
