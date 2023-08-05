from setuptools import setup
setup(
    name='scalepy',
    description='Provies renaming utility for Nikon output files.',
    version='1.0',
    url='https://github.com/ChrisoftheBoyerClan/scale.py',
    author='Christopher Boyer',
    author_email='ChrisoftheBoyerClan@gmail.com',
    entry_points={ 'console_scripts': [ 'scalepy=scalepy.scale:scale', ], },
    packages=['scalepy'],
    license='MIT',
    keywords='scale image resize'
)
