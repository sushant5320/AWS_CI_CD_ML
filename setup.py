from setuptools import setup, find_packages
from typing import List

Hypen_E = '-e.'
def get_requirements(file_path:str) -> List[str]:
    requirements = []

    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n", "") for req in requirements]

        if Hypen_E in requirements:
            requirements.remove(Hypen_E)

    return requirements
       

setup(
    name='mlproject',
    version='0.0.1',
    author='sks',
    author_email='sushantshewale12@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)