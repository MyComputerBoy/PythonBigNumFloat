import math # type: ignore
import BigNumFloat
from typing import Self # type: ignore

def PrintEndOfTestFile() -> None:
	print("\n\n-----------------------------------")
	print("Test file done.")
	print("-----------------------------------\n\n")
	input()

def __main__(vArgs: list[str] = []) -> bool:
	a: "BigNumFloat.BigNumFloat" = BigNumFloat.BigNumFloat(True, 0, 3, 141592, 6)
	b: "BigNumFloat.BigNumFloat" = BigNumFloat.BigNumFloat(True, 0, 2, 718271, 6)

	c: "BigNumFloat.BigNumFloat" = a + b

	print("a: %a" % (a.__repr__()))
	print("b: %a" % (b.__repr__()))
	print("c: %a" % (c.__repr__()))

	PrintEndOfTestFile()

	return True

__main__()
