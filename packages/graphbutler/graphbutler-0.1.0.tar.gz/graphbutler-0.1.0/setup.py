from setuptools import setup

setup(
    name="graphbutler",
    version="0.1.0",
    description="Simple, reproducible SVG graphs",
    url="https://github.com/jacwah/graphbutler",
    author="Jacob Wahlgren",
    author_email="jacob.wahlgren@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 2 :: Only",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Visualization"
    ],
    keywords="graph plot matplotlib",
    py_modules=["graphbutler"],
    install_requires=["matplotlib"]
)
