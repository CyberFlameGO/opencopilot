from setuptools import setup

setup(
    name='opencopilot-ai',
    version='0.1.0',
    packages=["sdk", "backend"],
    license="MIT",
    description="OpenCopilot",
    author="OpenCopilot",
    author_email="kaspar@nftport.xyz",
    url="https://github.com/nftport/opencopilot",
    py_modules=['opencopilot'],
    install_requires=[
        'langchain==0.0.236',
        'omegaconf==2.3.0',
        'pypdf==3.14.0',
        'python-dotenv==1.0.0',
        'requests==2.31.0',
        'rich==12.6.0',
        'typer[all]==0.7.0',
        'unstructured==0.7.2',
    ],
    entry_points={
        'console_scripts': [
            'opencopilot = sdk.cli:app',
        ],
    },
)


