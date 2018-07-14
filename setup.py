#!/usr/bin/env python3
from setuptools import setup 

setup(  name="i3-cycle-dispatch",
        version="0.1",
        description="Enables modifying i3 focus and move behavior depending on the focused window.",
        long_description=open('README.md').read(),
        url="https://github.com/krlanguet/i3-cycle-dispatch",
        license="GPL",
        author="Keith Languet",
        keywords=["i3 neovim"],
        entry_points='''
            [console_scripts]
            i3cd = dispatch:i3cd
        ''',
        install_requires=[
            'neovim',
            'psutil',
            'Click',
        ],
    )
