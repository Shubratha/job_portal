from setuptools import setup, find_packages
setup(
    name="cs-utils",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'djangorestframework==3.7.7',
        'requests==2.18.4'
    ],
    author="Pramod Lakshmanan",
    author_email="pramod@codekraft.in",
    description="Common utils needed for College Search project",
)
