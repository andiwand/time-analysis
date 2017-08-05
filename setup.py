from setuptools import setup

setup(
    name="time-analysis",
    version="0.0.1",
    url="https://github.com/andiwand/time-analysis",
    license="GNU Lesser General Public License",
    author="Andreas Stefl",
    install_requires=[],
    author_email="stefl.andreas@gmail.com",
    description="time analysis scripts",
    long_description="",
    package_dir={"": "src"},
    packages=["timeanalysis", "timeanalysis.delay", "timeanalysis.tvt"],
    platforms=["linux"],
    entry_points={
        "console_scripts": [
            "plot-delay = timeanalysis.delay:main",
            "plot-tvt = timeanalysis.tvt:main"
        ]
    },
)
