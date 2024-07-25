from setuptools import setup, find_packages

setup(
    name='simplonbd',
    version='0.1.0',
    packages=find_packages(exclude=["API", "BDD"]),
    install_requires=[
        # List your package dependencies here
    ],
    author='dai',
    author_email='dai.tensaout@gmail.com',
    description='package to integrate bdd simplon',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)