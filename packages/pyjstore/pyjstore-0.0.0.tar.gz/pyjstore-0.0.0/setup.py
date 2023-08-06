from setuptools import setup

package_name = "pyjstore"

packages = [package_name]

setup(
    name=package_name,
    version='0.0.0',
    description='client library for dynamodb as a json store',
    url='https://github.com/xitter/dynamo-store',
    author='Vijay Jain',
    author_email='mnnit.vijay@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords=['dynamo', 'json', 'dump'],
    packages=packages,
    install_requires=[
        'boto3>=1.4.3'
    ],
    extras_require={},
    package_data={},
    data_files=[],
    entry_points={},
)
