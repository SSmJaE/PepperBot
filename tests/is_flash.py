import sys
from os import path

BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(BASE_DIR)


from pepperbot import *
from pepperbot.message.segment import Image
from pepperbot.message.utils import is_flash

assert is_flash(Image("", mode="flash")) == True
assert is_flash(Image("")) == False
