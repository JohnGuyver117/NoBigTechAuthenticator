from setuptools import setup, find_packages

setup(
    name='nbtauth',
    version='0.1.0',
    author='J.P. Kloosterman',
    author_email='jg117@mget.nl',
    description='A secure, open source, multi-language OTP authenticator without big-tech dependencies.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/JohnGuyver117/nbtauth',
    packages=find_packages(),
    install_requires=[
        'customtkinter',
        'pyotp',
        'cryptography',
        'CTkMessagebox'
    ],
    entry_points={
        'console_scripts': [
            'nbtauth=nbtauth.nbtauth:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
