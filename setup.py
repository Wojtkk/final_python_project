from setuptools import setup, find_packages

setup(
    name='bus_analysis',
    version='0.1',
    packages=find_packages(),
    install_requires= [
    'pandas',
    'numpy',
    'matplotlib',
    'requests',
    'geopy',
    'datetime'],
    author='Wojciech Krupiński',
    description='Project for python course.',
    url='https://github.com/Wojtkk/final_python_project.git',
)