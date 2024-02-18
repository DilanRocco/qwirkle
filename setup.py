from setuptools import setup

setup(
    name = "proj-directory",
    version = "0.0.1",
    description = ("The Q Game details"),
    packages=['Q', 'Q.Common', 'Q.Common.Board', 'Q.Player', 'Q.Referee', 'Q.Tests', 'Q.Util', 'Q.Server','Q.Client'],
)
