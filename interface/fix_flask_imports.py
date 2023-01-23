import os
import sys


def fix_path():
    sys_path = sys.path
    desired_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
    sys.path.append(desired_path)
    new_path = sys.path
    return [path for path in new_path if path not in sys_path]


def __main():
    aux = fix_path()
    return


if __name__ == "__main__":
    __main()
