from setuptools import find_packages,setup

setup(
    name = 'mcqgenerator',
    version = '0.0.1',
    author='Roofose Tomy',
    author_email='roofosetomy@gmail.com',
    packages=find_packages(),
    install_requires=["openai","langchain","streamlit","python-dotenv","PyPDF2"]
)