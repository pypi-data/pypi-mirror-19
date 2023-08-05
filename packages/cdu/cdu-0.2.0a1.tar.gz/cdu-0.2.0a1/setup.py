from setuptools import setup

setup(
    name='cdu',
    version='0.2.0a1',
    packages=['cdu'],
    description="Cloud Storage Disk Usage Analyzer",
    author="Adrian Mester",
    author_email="mesteradrian@gmail.com",
    url="https://github.com/ilogik/cdu",
    keywords=["aws", "s3", "boto"],
    entry_points={
        'console_scripts': [
            'cdu = cdu.main:main',
            'cdun = cdun.main:main',
        ]
    },
    install_requires=[
        'boto3',
        'six',
    ]
)
