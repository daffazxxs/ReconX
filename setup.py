from setuptools import setup, find_packages

setup(
    name="subhttpx",
    version="1.0.0",
    description="Subdomain & HTTP Reconnaissance Toolkit",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="[Nama Lo]",
    author_email="[email@domain.com]",
    url="https://github.com/[username]/SUBHTTPX",
    py_modules=['subhttpx'],
    install_requires=[
        'colorama',
    ],
    entry_points={
        'console_scripts': [
            'subhttpx=subhttpx:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
