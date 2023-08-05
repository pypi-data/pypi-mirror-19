from setuptools import setup

setup(
    name='cdu',
    version='0.1.3',
    packages=['cdu'],
    description="Cloud Storage Disk Usage Analyzer",
    author="Adrian Mester",
    author_email="mesteradrian@gmail.com",
    url="https://github.com/ilogik/cdu",
    keywords=["aws", "s3", "boto"],
    entry_points={
        'console_scripts': [
            'cdu = cdu.__main__:main'
        ]
    },
    install_requires=[
        'boto3',
    ]
)
