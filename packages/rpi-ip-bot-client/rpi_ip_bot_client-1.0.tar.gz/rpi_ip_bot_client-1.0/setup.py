""" Package meta """

from setuptools import setup


def readme():
    """ Load the contents of README.rst """
    with open('README.rst') as readme_file:
        return readme_file.read()

setup(
    name='rpi_ip_bot_client',
    version='1.0',
    description='Command line tool to manage the client part of rpi_ip_bot service.',
    long_description=readme(),
    classifiers=['Topic :: Utilities'],
    keywords='ip telegram bot raspberry pi',
    url='https://github.com/eugene-babichenko/rpi_ip_bot_client',
    author='Yevhenii Babichenko',
    author_email='eugene.babichenko@gmail.com',
    license='MIT',
    packages=['rpi_ip_bot_client'],
    zip_safe=False,
    include_package_data=True,
    entry_points={
        'console_scripts': ['rpiipbot=rpi_ip_bot_client.command_line:main']
    },
    install_requires=['requests']
)
