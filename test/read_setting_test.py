import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from read_setting import readSetting

read = readSetting()

print(read.EmptyFile)