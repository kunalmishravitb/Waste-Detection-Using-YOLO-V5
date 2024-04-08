from setuptools import find_packages, setup

setup(
    name='wasteDetection',
    version='0.0.0',
    author='Kunal Mishra',
    author_email='mishrakunal065@gmail.com',
    packages=find_packages(), # Look for the constructor file (__init__.py) in the folders and install that particular folder as a local package
    install_requires=[]
)