'''
the setup.py file is an essential part of packaging and 
distribution python projects.It is used by setuptools
(or distutils in older pyhton verison) to define the
 configuration of project,such as its metadata,dependencies and more
'''
from setuptools import find_packages,setup
from typing import List

def get_requirements()-> List[str]:
    """
    this function will retunr list of requirements
    """
    requirement_lst:List[str]=[]
    try:
        with open('requirements.txt','r') as file:
            lines=file.readlines()
            for li in lines:
                requirement=li.strip()
                # ignore empty lines and -e.
                if requirement and requirement != '-e .':
                    requirement_lst.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file is not found")                
    return requirement_lst

setup(
    name="NetworkSecurity",
    version="0.01",
    author="Vivek Tripathi",
    author_email='vt0514706@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements()
)  