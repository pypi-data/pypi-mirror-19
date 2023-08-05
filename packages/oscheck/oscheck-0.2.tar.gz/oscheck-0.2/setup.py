from setuptools import setup, find_packages

requires = []

test_requires = requires

setup(
    name='oscheck',
    version='0.2',
    packages=find_packages(),
    # url='https://github.com/a1fred/git-barry',
    license='MIT',
    author='a1fred',
    author_email='demalf@gmail.com',
    description='OS checker',
    install_requires=requires,
    tests_require=test_requires,
    test_suite="tests",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development',
    ],
)
