from setuptools import setup

setup(name='sillymap',
        version='0.0.1',
        description='A silly implementation of a short read mapper for the course DD3436.',
        url='http://github.com/alneberg/sillymap',
        author='Johannes Alneberg',
        author_email='alneberg@kth.se',
        license='MIT',
        packages=['sillymap'],
        zip_safe=False,
        scripts=['bin/sillymap']
   )
