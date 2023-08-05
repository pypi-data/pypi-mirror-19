import setuptools


def readme():
    with open('README.rst') as f:
        return f.read()

setuptools.setup(
    name='brutalelk',
    version='0.1',
    description='Talk to Brutal Elk and take off your pink sunglasses',
    url='http://github.com/pannkotsky/brutalelk',
    author='Valerii Kovalchuk',
    author_email='kovvalole@gmail.com',
    license='MIT',
    packages=['brutalelk'],
    install_requires=[
        'slackclient',
    ],
    scripts=['cmd/elk'],
    zip_safe=False
)
