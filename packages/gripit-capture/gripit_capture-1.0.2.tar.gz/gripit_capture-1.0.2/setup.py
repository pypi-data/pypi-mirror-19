from setuptools import setup


setup(
    name='gripit_capture',
    version='1.0.2',
    description='A webcam extension package for GripIt App',
    url='http://github.com/agilefreaks',
    author='Agilefreaks',
    author_email='agilefreaks@agilefreaks.com',
    license='MIT',
    packages=[
        'webcam',
        'webcam.data',
        'webcam.jobs',
        'webcam.services'
    ],
    tests_require=['pytest', 'mock'],
    zip_safe=False
)
