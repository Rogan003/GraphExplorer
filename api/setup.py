from setuptools import setup, find_packages

setup(
    name="graph_explorer_api",
    version="0.1",
    packages=find_packages(),
    install_requires=['Django>=2.1'],
    package_data={'api': ['static/*.css', 'templates/*.html']},
    zip_safe=False
)