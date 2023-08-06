from setuptools import setup, find_packages
from Cython.Build import cythonize

__version__ = '0.55'


setup(
    name="eudplib",
    version=__version__,
    packages=find_packages(),
    package_data={
        '': ['*.pyx', '*.dll', '*.lst', '*.pyd'],
    },
    install_requires=[
        'cython',
    ],
    ext_modules=cythonize([
        "eudplib/core/allocator/*.pyx",
        "eudplib/utils/*.pyx",
    ]),

    # metadata for upload to PyPI
    author="Trgk",
    author_email="whyask37@naver.com",
    description="EUD Trigger generator",
    license="MIT license",
    keywords="starcraft rawtrigger eud",
    url="http://blog.naver.com/whyask37/",  # project home page, if any
)
