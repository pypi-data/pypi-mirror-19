from setuptools import setup, find_packages

install_requires = [
    'boto3==1.4.2'
]

setup(
    name='BlueLeader',
    version='0.32.5',
    description='An automated Webpack deployment tool for S3 & CloudFront',
    author='Morgan McDermott',
    author_email='morganmcdermott@gmail.com',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'BlueLeader = blueleader.deploy:main',
        ]
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ]
)
