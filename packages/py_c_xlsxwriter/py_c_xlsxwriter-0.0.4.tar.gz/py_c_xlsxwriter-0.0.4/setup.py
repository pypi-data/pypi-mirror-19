# from distutils.core import setup, Extension
# setup(name='helloworld', version='1.0',\
#         ext_modules=[Extension('helloworld', ['hello.c'], \
#         library_dirs=['/home/linlin/Desktop/libxlsxwriter-master/lib'],
#         libraries=['xlsxwriter'])])

# from distutils.core import setup
# from distutils.extension import Extension
from Cython.Build import cythonize
from setuptools import setup, find_packages, Extension


ext_modules = cythonize([
    Extension("py_c_xlsxwriter", ["excel.pyx"],
              libraries=["xlsxwriter"], include_dirs=['/home/linl/Desktop/py_c_xlsxwriter/libxlsxwriter/lib'])])

setup(
  name = "py_c_xlsxwriter",
  version = '0.0.4',
  keywords = 'c xlsxwriter cython',
  license = 'MIT License',
  url = 'https://github.com/drinksober',
  install_requires = ['Cython'],
  author = 'drinksober',
  author_email = 'drinksober@foxmail.com',
  packages = find_packages(),
  platforms = 'any',
  ext_modules = cythonize(ext_modules)
)
