from setuptools import setup

import pyconfimporter

install_reqs = [
    'six>=1.3.0',
]

description = """\
Easy way to import an external Python module into an environment.
"""

setup(
    name='pyconfimporter',
    version=pyconfimporter.__version__,
    description=description,
    author='Ken Elkabany',
    author_email='ken@elkabany.com',
    url='https://github.com/braincore/pyconfimporter',
    install_requires=install_reqs,
    py_modules=['pyconfimporter'],
    license='MIT',
    platforms=['CPython 2.7', 'CPython 3.4', 'CPython 3.5'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        ],
    )
