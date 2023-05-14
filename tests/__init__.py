import os
import sys

# 可以直接from tests.conftest import
base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)
