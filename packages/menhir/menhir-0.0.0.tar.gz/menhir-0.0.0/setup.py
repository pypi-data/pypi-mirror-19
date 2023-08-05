from setuptools import setup, find_packages


with open('requirements.txt') as f:
    requirements = f.read().split()

with open('requirements-tests.txt') as f:
    test_requirements = f.read().split()

setup(
    author='Hugo Duncan',
    author_email='hugo@hugoduncan.org',
    name='menhir',
    description="A build tool for monolithic repositories",
    packages=find_packages(
        exclude=['tests'],
    ),
    install_requires=requirements,
    tests_require=test_requirements,
    include_package_data=True,
    url='https://github.com/dialoguemd/menhir',
    license='MIT',
    entry_points={
        'console_scripts': [
            'menhir = menhir.script:main',
        ]
    }
)
