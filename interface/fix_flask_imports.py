import os
import sys

new_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(new_path)