from setuptools import setup, find_packages

VERSION = '0.2.0' 
DESCRIPTION = 'CLI for tracking pocket money'
LONG_DESCRIPTION = """
Usage↓
https://github.com/bichanna/guineapig
"""

# Setting up
setup(
        name="guineapig", 
        version=VERSION,
        author="bichanna",
        author_email="nobu.bichanna@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type="text/markdown",
        url="https://github.com/bichanna/guineapig",
        packages=find_packages(),
        install_requires=[
            "click",
            "mysql-connector-python",
            "protobuf",
            "six",
        ], 
		license="MIT",
        keywords=["guineapig", "python"],
        classifiers= [
            "Environment :: Console",
            "Development Status :: 4 - Beta",
        ],
        entry_points = """
            [console_scripts]
            guineapig=guineapig.main:main
        """
)