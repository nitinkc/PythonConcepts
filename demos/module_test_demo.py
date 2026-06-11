from testPackage.subPackage1 import subtModule
from testPackage.subPackage2 import multiplyModule
import testPackage as tp


def main():
	print(tp.PI)
	print(tp.multiplyModule.mult(3, 4))

	print(tp.addModule.addition(2, 3))
	print(tp.addModule._private_function())
	print(tp.PI)
	print(tp.initFunction())
	print(multiplyModule.mult(3, 4))
	print(tp.multiplyModule.mult(3, 4))

	print(subtModule.subtract(3, 4))
	print(multiplyModule.mult(2, 6))


if __name__ == "__main__":
	main()


