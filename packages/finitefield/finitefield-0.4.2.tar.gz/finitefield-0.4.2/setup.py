from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

setup(name='finitefield',
      version='0.4.2',
      author='ipetraki',
      author_email='petrakiev@hotmail.com',
      url='http://pythonhosted.org/finitefield',
      ext_modules = cythonize('finitefield/finitefield.pyx')
)
