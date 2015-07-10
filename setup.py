# Copyright 2015 Jason Heeris <jason.heeris@gmail.com>
# 
# This file is part of the 'flaskery' application, and is licensed under the MIT
# license.
from setuptools import setup, find_packages

setup(
    name = "Flaskery",
    version = "1.0",
    packages = find_packages(),
    
    package_data = {
        'flaskery': ['switches/templates/*.html'],
    },
    
    install_requires = [
        'flask',
        'alchy',
        'flask_alchy'
    ],
    
    entry_points = {
        'console_scripts': [
            'flaskery = flaskery.app:main',
        ]
    }
)
