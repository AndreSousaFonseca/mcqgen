from setuptools import find_packages,setup


setup(
    name='mcqgenerator',
    version='0.0.1',
    author='andre fonseca',
    author_email='andreffonseca@msn.com',
    install_requires=['openai', 'langchain', 'streamlit', 'python-dotenv','PyPDF2', 'transformers'],
    packages=find_packages()
)
    
