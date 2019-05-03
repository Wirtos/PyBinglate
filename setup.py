import setuptools

setuptools.setup(
    name="PyBinglate",
    version="0.2",
    author="Wirtos_new",
    author_email="Wirtos.new@gmail.com",
    description="Bing translator client for python",
    url="https://wirtos.github.io/PyBinglate/",
    packages=setuptools.find_packages(),
    project_urls={
        "Source Code": "https://github.com/Wirtos/PyBinglate",
    },
    install_requires=['requests'],
    keywords="bing translator translation microsoft",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
