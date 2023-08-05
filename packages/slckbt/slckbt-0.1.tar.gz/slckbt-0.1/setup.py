import setuptools


def readme():
    with open('README.rst') as f:
        return f.read()

setuptools.setup(
    name='slckbt',
    version='0.1',
    description='Basic chat bot for Slack',
    url='http://github.com/pannkotsky/slckbt',
    author='Valerii Kovalchuk',
    author_email='kovvalole@gmail.com',
    license='MIT',
    packages=['slckbt'],
    install_requires=[
        'slackclient',
    ],
    zip_safe=False
)
