from setuptools import setup, find_packages

setup(
    name='tamperfree',
    version='0.1dev',
    packages=find_packages(exclude=('tests', 'tests.*')),
    author='Joakim Uddholm',
    author_email='joakim@uddholm.com',
    license='MIT',
    description='A tool to verify static content on Tor hidden services against tamper.',
    long_description=open('README.md').read(),
    install_requires=open('requirements.txt').read().split(),
    entry_points={
        'console_scripts': ['tamperfree = tamperfree.main:main']
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2.7',
    ]
)
