from setuptools import setup, find_packages
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT_DIR)

package_name = "pydict_surf"

if os.path.exists("requirements.txt"):
    with open("requirements.txt") as req_file:
        requirements = req_file.readlines()
elif os.path.exists("{}.egg-info/requires.txt".format(package_name)):
    with open("{}.egg-info/requires.txt".format(package_name)) as req_file:
        requirements = req_file.readlines()
else:
    requirements = []

with open("README.md", "r") as fh:
    long_description = fh.read()

metadata = dict(
    name=package_name,  # Replace with your own username
    version="0.7.27",
    author=["Soroush Zargar", "Hemen Zandi"],
    author_email=["Soroushzargar@gmail.com", "Hemen.Zandi@gmail.com"],
    description="Performs a walk over all fields of json and python dictionary. Works almost same as os.walk",
    long_description=long_description,
    long_description_data_type="",
    url=None,
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7')
setup(**metadata)
