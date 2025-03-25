# LLaMA Tamil Classifier  

## Installation  

### Create and Activate a Virtual Environment  

#### Conda  
```bash
conda create -n llama_tamil python=3.11 -y
conda activate llama_tamil
```
#### venv

python -m venv llama_tamil
source llama_tamil/bin/activate  # macOS/Linux
llama_tamil\Scripts\activate     # Windows

#### Install the Package

pip install git+https://github.com/rsaldanha2019/llama_tamil_classifier.git

#### Usage
### Run the GUI

llama-gui

### Run the CLI

llama-cli "எனக்கு தமிழ் பிடிக்கும்"

#### Example CLI Output

Topic: Movies, Language  
Sentiment: Positive  
Reason: The text expresses a liking towards Tamil movies or language.  

#### Development Setup

git clone https://github.com/rsaldanha2019/llama_tamil_classifier.git
cd llama_tamil_classifier
pip install -e .

#### Uninstallation

pip uninstall llama_tamil_classifier

