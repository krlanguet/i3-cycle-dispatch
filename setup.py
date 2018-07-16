#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(  name="i3cd",
        version="0.1",
        description="Enables modifying i3 focus and move behavior depending on the focused window.",
        long_description=open('README.md').read(),
        url="https://github.com/krlanguet/i3-cycle-dispatch",
        license="GPL",
        author="Keith Languet",
        keywords=["i3", "neovim"],
        packages=['i3cd'],
        py_modules=['i3cd'],
        entry_points={
            'console_scripts': [
                'i3cd = i3cd.i3cd:i3cd'
            ]
        },
        install_requires=[
            'neovim',
            'psutil',
        ],
    )
