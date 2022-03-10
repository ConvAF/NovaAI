"""
Path handling.
"""
import inspect
from pathlib import Path

import chatbot

def get_package_root():
    """
    Get the path of the package repository.
    """
    package_path = Path(inspect.getfile(chatbot))
    pkg_root = package_path.parents[0]
    return pkg_root