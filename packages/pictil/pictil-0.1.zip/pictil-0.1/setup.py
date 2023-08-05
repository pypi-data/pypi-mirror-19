from setuptools import setup
setup(
    name='pictil',
    description='Rename Nikon camera files',
    version='0.1',
    url='https://github.com/ChrisoftheBoyerClan/pictil',
    author='Christopher Boyer',
    author_email='ChrisoftheBoyerClan@gmail.com',
    entry_points={ 'console_scripts': [ 'pictil=pictil:main', ], },
    packages=['pictil'],
    license='MIT',
    keywords='rename nikon pictures'
)
