import sys
from os import path

BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(BASE_DIR)


from src import *

from src.message.utils import is_flash
from src.message.segment import Image


assert is_flash(Image("", mode="flash")) == True
assert is_flash(Image("")) == False
