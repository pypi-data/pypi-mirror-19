from setuptools import setup
setup(
    name='pictil',
    description='Provies renaming utility for Nikon output files.',
    version='1.0',
    url='https://github.com/ChrisoftheBoyerClan/pictil',
    author='Christopher Boyer',
    author_email='ChrisoftheBoyerClan@gmail.com',
    entry_points={ 'console_scripts': [ 'pictil=pictil.main:main', ], },
    packages=['pictil'],
    license='MIT',
    keywords='rename nikon pictures'
)
