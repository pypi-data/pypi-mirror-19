## build with command:
#python _setup.py build_ext --inplace

# Two identical ways to compile the code.  
# I will use the second version for now and comment out the first.

# Version 1 (simpler)
## Version 1 compiles, but puts the .so in a subfolder...WHY?
"""
from __future__ import absolute_import
from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize(["cytools.pyx"])
)

## Version 2 does not seem to compile the code into a .so and causes an error,
## but the above simpler Version 1 code does seem to build properly during install.
"""
# Version 2 (more robust?)
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [
               Extension("cytools",["cytools.pyx"],include_dirs=['.'])               
               ]
    
setup(
      name = 'ExoSOFTmodel',
      cmdclass = {'build_ext':build_ext},
      ext_modules = ext_modules,   
      script_args=['build_ext'],   
      options={'build_ext':{'inplace':True, 'force':True}}
      )
