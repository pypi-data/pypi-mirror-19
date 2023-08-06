try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='ptfutils',
    version='0.0.1',
    packages=['tfutils', 'tfutils.data', 'tfutils.training'],
    url='https://github.com/PiotrDabkowski/',
    install_requires = ['tensorflow>=0.12', 'numpy>=1.11', 'cv2>=1.0'],
    license='MIT',
    author='Piotr Dabkowski',
    author_email='piodrus@gmail.com',
    description='Useful modules for tensorflow',
)