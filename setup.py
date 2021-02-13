import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='huetui',
    version='1.0',
    author="channel-42",
    license='MIT',
    author_email="info@devls.de",
    description="A TUI for Philips Hue",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/channel-42/hue-tui",
    scripts=['huetui'],
    install_requires=['py-cui', 'hue-snek-channel42', 'Pillow', 'colormath',
                      'colorthief'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
)
