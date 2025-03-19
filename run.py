#import numpy
import sys

def print_interpreter_path():
    interpreter_path = sys.executable
    print(f'The interpreter is located at: {interpreter_path}')


if __name__ == "__main__":
    print("hello world")
    print_interpreter_path()
    