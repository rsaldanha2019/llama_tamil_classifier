from setuptools import setup, find_packages

# Read dependencies from requirements.txt
with open("requirements.txt", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="llama_tamil_classifier",
    version="0.1.0",
    author="Richard Saldanha",
    author_email="rsaldanha554@gmail.com",
    description="A Python package for Tamil topic & sentiment classification using LLaMA 3.2 3B",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/rsaldanha2019/llama_tamil_classifier",  # Update with your repo
    packages=find_packages(),
    install_requires=requirements,  # Uses requirements.txt
    entry_points={
        "console_scripts": [
            "llama-cli=llama_tamil_classifier.cli:main",  # CLI command
            "llama-gui=llama_tamil_classifier.gui:main",  # GUI command
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
)
