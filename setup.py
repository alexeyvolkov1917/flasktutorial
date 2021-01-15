from setuptools import find_packages,setup

setup(
    name='flaskr',
    version='1.0.0',
    packeges=find_packages(),
    include_packages_date=True,
    zip_safe=False,
    install_requires=['flask',],
)