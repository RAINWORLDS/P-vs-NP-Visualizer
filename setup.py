from setuptools import setup, find_packages

setup(
    name="p-vs-np-visualizer",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.21.0",
        "matplotlib>=3.5.0",
        "networkx>=2.8.0",
    ],
    python_requires=">=3.8",
)
