import os
import sys

class Test(object):
    def __init__(self):
        self._w = 0
        self._x = 10
        self._y = 20

def main():
    test = Test()
    print(test._x)
    print(test._y)
    while True:
        try:
            rawinput = input(">>> ")
            print(exec(rawinput))
        except KeyboardInterrupt:
            print()
            break
        except (SyntaxError, NameError) as e:
            print(e)

if __name__ == "__main__":
    main()
    sys.exit(0)