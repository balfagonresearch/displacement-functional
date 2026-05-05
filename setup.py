"""
Setup script for displacement-functional package

Install in development mode:
    pip install -e .

Install normally:
    pip install .
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="displacement-functional",
    version="2.0.0",
    author="Christian Balfagón",
    author_email="cb@balfagonresearch.org",
    description="Cramér-Rao bounds for cumulative dissipation in quantum Markov semigroups",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/balfagonresearch/displacement-functional",
    project_urls={
        "Paper": "https://arxiv.org/abs/XXXX.XXXXX",
        "Bug Reports": "https://github.com/balfagonresearch/displacement-functional/issues",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Mathematics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.20.0",
        "scipy>=1.7.0",
        "matplotlib>=3.4.0",
    ],
    extras_require={
        "full": [
            "qutip>=4.6.0",
            "jupyter>=1.0.0",
        ],
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.0.0",
            "black>=21.0",
            "flake8>=3.9.0",
        ],
        "docs": [
            "sphinx>=4.0.0",
            "sphinx-rtd-theme>=0.5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "displacement-functional=displacement_functional:main",
        ],
    },
)
