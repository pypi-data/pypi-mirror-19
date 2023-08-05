from setuptools import setup

setup(
    name='symboldoc',
    version='0.0.1',
    author='Felipe Martin',
    author_email='me@fmartingr.com',
    url='https://github.com/fmartingr/symboldoc',
    description='Create docstrings based on module symbols',
    keywords='ast abstract syntax tree method class symbol docstring',
    license='MIT',
    py_modules=['symboldoc'],
    entry_points={
        'console_scripts': [
            'symboldoc=symboldoc:cli',
        ],
    },
    classifiers=[],
)
