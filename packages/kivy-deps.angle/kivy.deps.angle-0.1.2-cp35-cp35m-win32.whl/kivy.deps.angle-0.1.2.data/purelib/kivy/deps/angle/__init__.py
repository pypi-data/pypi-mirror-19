
"""The following code is required to make the dependency binaries available to
kivy when it imports this package.
"""

__all__ = ('dep_bins', )

import sys
import os
from os.path import join, isdir, dirname


dep_bins = []
"""A list of paths that contain the binaries of this distribution.
Can be used e.g. with pyinstaller to ensure it copies all the binaries.
"""

_root = sys.prefix
dep_bins = [join(_root, 'share', 'angle', 'bin')]
if isdir(dep_bins[0]):
    os.environ["PATH"] += os.pathsep + dep_bins[0]
else:
    dep_bins = []


