from setuptools import setup, find_packages

setup(
    name="FENICSxDGM",
    version="1.0",
    description="A description is yet to follow",
    url="https://git.rwth-aachen.de/JanHab/Bsc-ElectrolyteModels",
    author="Jan Habscheid, Lambert Theisen, Manuel Torrilhon",
    author_email="Jan.Habscheid@rwth-aachen.de, lambert.theisen@rwth-aachen.de, mt@mathcces.rwth-aachen.de",
    packages=["FENICSxDGM"],
    package_dir={"FENICSxDGM":"src"},
    package_data={"FENICSxDGM": ["tests/*"]},
    python_requires=">=3.12.3",
    install_requires=[
        "pyvista == 0.43.10",
        "numpy == 1.26.4",
        "scipy == 1.14.0"
    ],
    setup_requires=["pytest-runner"],
    tests_require=["pytest>=7.4.0"],
    test_suite="tests"
)
