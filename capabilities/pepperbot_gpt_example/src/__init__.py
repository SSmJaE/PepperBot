import sys
from os import path

BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(BASE_DIR)

from src.main import GPTExample
from src.config import GPTExampleConfig

__all__ = (
    "GPTExample",
    "GPTExampleConfig",
)
