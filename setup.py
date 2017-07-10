from setuptools import setup

setup(
    name="time-plots",
    version="0.0.1",
    url="https://github.com/andiwand/time-plots",
    license="GNU Lesser General Public License",
    author="Andreas Stefl",
    install_requires=[],
    author_email="stefl.andreas@gmail.com",
    description="time test plot scripts",
    long_description="",
    package_dir={"": "src"},
    packages=["timeplots", "timeplots.delay", "timeplots.tvt"],
    platforms=["linux"],
    entry_points={
        "console_scripts": [
            "delay-plot = timeplots.delay:main",
            "tvt-plot = timeplots.tvt:main"
        ]
    },
)
