from setuptools import setup
from setuptools.extension import Extension

setup(
    name='nuclitrack',
    version='1.0.2',
    description='Nuclei tracking program',
    author='Sam Cooper',
    author_email='sam@socooper.com',
    license='MIT',
    packages=['nuclitrack'],
    install_requires=['Cython','numpy','matplotlib','scipy','scikit-image','scikit-learn','pygame','kivy'],
    ext_modules=[Extension("tracking_c_tools", ["nuclitrack/tracking_c_tools.c"]),Extension("numpy_to_image", ["nuclitrack/numpy_to_image.c"])]
)
