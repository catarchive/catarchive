from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='catarchive',
    version='0.1.0',
    author='Cat Archive Project',
    author_email='theodorehenson@protonmail.com',
    description='Open-source, distributed, cat archive platform',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/catarchive/catarchive',
    packages=setuptools.find_packages(),
    install_requires=['requests', 'pillow', 'beautifulsoup4', 'torch', 'torchvision'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'catarchive = client:main',
        ],
    },
)
