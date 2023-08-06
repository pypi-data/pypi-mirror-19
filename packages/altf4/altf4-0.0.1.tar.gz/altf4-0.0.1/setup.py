from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='altf4',
    version='0.0.1',
    description='Automatic Loadtesting Framework 4',
    long_description=readme(),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Testing :: Traffic Generation',
    ],
    url='https://github.com/fabeschan/altf4',
    author='Fabian Chan',
    author_email='fabeschan@gmail.com',
    license='MIT',
    packages=['altf4'],
    install_requires=[
        'gevent',
    ],
    test_suite='nose.collector',
    tests_require=['nose'],
    zip_safe=False
)
