from setuptools import setup, find_packages

setup(
    name="fxdgm",
    version="1.1.1",
    description="A description is yet to follow",
    url="https://git.rwth-aachen.de/JanHab/fxdgm",
    author="Jan Habscheid, Lambert Theisen, Satyvir Singh, Stefanie Braun, Manuel Torrilhon",
    author_email="Jan.Habscheid@rwth-aachen.de, lambert.theisen@rwth-aachen.de, singh@acom.rwth, braun@acom.rwth, mt@mathcces.rwth-aachen.de",
    packages=["fxdgm"],
    package_dir={"fxdgm":"fxdgm"},
    package_data={"fxdgm": ["tests/*"]},
    python_requires=">=3.12",
    install_requires=[
        "pyvista == 0.43.10",
        "numpy == 1.26.4",
        "scipy == 1.14.1"
    ],
    setup_requires=["pytest-runner"],
    tests_require=["pytest>=7.4.0"],
    test_suite="tests"
)
