from testPackage.subPackage2.calc_class import Calculator


def main():
	obj = Calculator()
	obj.my_method(arg1=10, arg2=20)

	calc = Calculator()
	result = calc.addNums(x1=1, x2=2, x3=3)
	print("Sum of numbers:", result)


if __name__ == "__main__":
	main()

