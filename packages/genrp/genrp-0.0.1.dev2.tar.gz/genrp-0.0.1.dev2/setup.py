#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import glob
import numpy
import shutil

from setuptools import setup, Extension

# Publish the library to PyPI.
if "publish" in sys.argv[-1]:
    os.system("python setup.py sdist upload")
    sys.exit()

# Default compile arguments.
compile_args = dict(libraries=[], define_macros=[("NDEBUG", None)])
if os.name == "posix":
    compile_args["libraries"].append("m")

localincl = os.path.join("genrp", "include")
compile_args["include_dirs"] = [
    localincl,
    numpy.get_include(),
]

# Move the header files to the correct directory.
dn = os.path.dirname
incldir = os.path.join(dn(dn(os.path.abspath(__file__))), "cpp", "include")
if os.path.exists(os.path.join(incldir, "genrp", "genrp.h")):
    print("Dev mode...")
    headers = (
        glob.glob(os.path.join(incldir, "*", "*.h")) +
        glob.glob(os.path.join(incldir, "*", "*", "*.h"))
    )
    for fn in headers:
        dst = os.path.join(localincl, fn[len(incldir)+1:])
        try:
            os.makedirs(os.path.split(dst)[0])
        except os.error:
            pass
        shutil.copyfile(fn, dst)

# Check to make sure that the header files are in place
if not os.path.exists(os.path.join(localincl, "genrp", "version.h")):
    raise RuntimeError("couldn't find genrp headers")

ext = Extension("genrp._genrp",
                sources=[os.path.join("genrp", "genrp.cpp")],
                language="c++",
                **compile_args)

# Hackishly inject a constant into builtins to enable importing of the
# package before the library is built.
if sys.version_info[0] < 3:
    import __builtin__ as builtins
else:
    import builtins
builtins.__GENRP_SETUP__ = True
import genrp  # NOQA
from genrp.build import build_ext  # NOQA

setup(
    name="genrp",
    version=genrp.__version__,
    author="Daniel Foreman-Mackey",
    author_email="foreman.mackey@gmail.com",
    url="https://github.com/dfm/genrp",
    license="MIT",
    packages=["genrp"],
    install_requires=["numpy>=1.9", "pybind11>=1.7"],
    ext_modules=[ext],
    description="Scalable 1D Gaussian Processes",
    long_description=open("README.rst").read(),
    package_data={"": ["README.rst", "LICENSE",
                       os.path.join(localincl, "*.h"),
                       os.path.join(localincl, "*", "*.h")]},
    include_package_data=True,
    cmdclass=dict(build_ext=build_ext),
    classifiers=[
        # "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
)
