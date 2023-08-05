from setuptools import setup, find_packages

setup(
    name='manyquery',
    version='0.0.1',
    author='Billy Jarnagin',
    author_email='jarnabi@gmail.com',
    license=open('LICENSE').read(),
    keywords='mysql query database',
    long_description=open('README.md').read(),
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'pymysql',
    ],
    entry_points="""
        [console_scripts]
        manyquery=manyquery.cli:cli
    """,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
)