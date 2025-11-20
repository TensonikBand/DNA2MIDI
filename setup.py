#!/usr/bin/env python3
"""
Setup script for DNA Ambient Composer
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="dna-2-midi",
    version="1.0.0",
    author="Tensonik",
    author_email="63404031+TensonikBand@users.noreply.github.com",
    description="Transform DNA sequences into beautiful ambient soundscapes using music theory",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TensonikBand/DNA2MIDI",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Multimedia :: Sound/Audio :: MIDI",
        "Topic :: Artistic Software",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "dna-ambient=src.ambient_composer:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["data/*.fasta", "examples/output/*.mid"],
    },
    keywords="dna, bioinformatics, music, ambient, sonification, midi, composition",
    project_urls={
        "Bug Reports": "https://github.com/TensonikBand/DNA2MIDI/issues",
        "Source": "https://github.com/TensonikBand/DNA2MIDI",
        "Documentation": "https://github.com/TensonikBand/DNA2MIDI",
    },
)