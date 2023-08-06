from setuptools import setup, find_packages

install_requires = [
    'boto3==1.4.2'
]

setup(
    name='BlueLeader',
    version='0.3',
    description='An automated Webpack deployment tool for S3 & CloudFront',
    author='Morgan McDermott',
    author_email='morganmcdermott@gmail.com',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'BlueLeader = blueleader.deploy:main',
        ]
    },
)
