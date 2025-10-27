#!/usr/bin/env python3
"""
Setup script for Whisper Dictation Tool
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="whisper-dictation-tool",
    version="1.0.0",
    author="Zihan",
    author_email="zihan@example.com",
    description="A speech-to-text dictation tool using OpenAI's Whisper model",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zihan/whisper-dictation-tool",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    # Removed console_scripts to prevent old interface access
    include_package_data=True,
    zip_safe=False,
)
