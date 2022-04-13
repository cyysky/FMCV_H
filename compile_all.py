#Reference https://stackoverflow.com/questions/11507101/how-to-compile-and-link-multiple-python-modules-or-packages-using-cython
#from distutils.core import setup
from setuptools import setup
from distutils.extension import Extension
from Cython.Build import cythonize

import os
import sys
import sysconfig

import glob
from os.path import join, isfile
from shutil import copytree
from pathlib import Path

def distutils_dir_name(dname):
    """Returns the name of a distutils build directory"""
    f = "{dirname}.{platform}-{version[0]}.{version[1]}"
    return f.format(dirname=dname,
                    platform=sysconfig.get_platform(),
                    version=sys.version_info)

print(sys.version)

# ignore any files but files with '.py' extension
ignore_func = lambda d, files: [f for f in files if (Path(d) / Path(f)).is_file() and f.endswith('.py') and not f.endswith('Camera.py')]
copytree("FMCV", os.path.join("build",distutils_dir_name('lib'),"FMCV"), ignore=ignore_func, dirs_exist_ok=True)

from distutils.dir_util import copy_tree
#copy_tree("/a/b/c", "/x/y/z")

print(f"Arguments count: {len(sys.argv)}")
for i, arg in enumerate(sys.argv):
    print(f"Argument {i:>6}: {arg}")
    
sys.argv.append("build_ext")

#current_path = os.path.join(os.getcwd())
current_path = ""
extensions = []
#extensions.append(Extension("fmc_vision", ["fmc_vision.py"]))

module = "FMCV"
for filename in os.listdir(os.path.join(os.getcwd(),module)):
    if (filename.endswith(".py") and not filename.startswith("Camera") 
                                    and not filename.startswith("serial_callback")): 
        command = "Extension(\"{0}.{1}\", [r\"{2}\"])".format(module,os.path.splitext(filename)[0],os.path.join(current_path,module,filename))
        print(command)
        extensions.append(eval(command))


submodules = ['Ai','Ui','Camera','Comm','Processor','Logger']#['tools','hci','sys']#["cameras","io"]
for obj in submodules:
    for filename in os.listdir(os.path.join(os.getcwd(),module,obj)):
        if filename.endswith(".py"): 
            command = "Extension(\"{0}.{1}.{2}\", [r\"{3}\"])".format(module,obj,os.path.splitext(filename)[0],os.path.join(current_path,module,obj,filename))
            print(command)
            extensions.append(eval(command))

for file_path in glob.glob(os.path.join(os.getcwd(),module, '**', '*.html'), recursive=True):
    new_path = os.path.join(os.path.basename(file_path))
    print(file_path)
    
for ext in extensions:
    print(ext)
    
c_ext = cythonize(extensions,build_dir="build",
                            compiler_directives={'always_allow_keywords': True},
                            language_level = 3)
print(c_ext)

setup(
   name = "FMCV",
   ext_modules = c_ext
)

# python3 setup.py build_ext --inplace