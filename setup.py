from setuptools import setup

setup(
    name="zerochain",
    version="0.0.1-beta",
    description="Python SDK for use on the ZeroChain network, allowing developers to leverage full power of the Zerochain network with Python",
    url="https://github.com/subaquatic-pierre/zerochain-sdk-py",
    author="Pierre du Toit",
    author_email="subaquatic-pierre@gmail.com",
    license="BSD 2-clause",
    packages=["zerochain"],
    install_requires=["reedsolo==1.5.4", "requests==2.26.0", "bip39==0.0.2"],
    classifiers=[
        "Development Status :: 1 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Topic :: Blockchain :: SDK",
    ],
)
