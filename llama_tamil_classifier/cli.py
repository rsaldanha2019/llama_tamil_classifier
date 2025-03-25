import argparse
import sys
import os
# Allow relative imports when running as a script
from llama_tamil_classifier.model import LlamaClassifier  # Package execution
class LlamaClassifierCLI:
    def __init__(self):
        self.classifier = LlamaClassifier()

    def classify_text(self, text):
        """Classify the given Tamil or Code-Mixed text."""
        prediction = self.classifier.classify(text)
        print("\n=== Prediction ===")
        print(prediction)

def main():
    parser = argparse.ArgumentParser(description="LLaMA Tamil Topic & Sentiment Classifier")
    parser.add_argument("text", type=str, help="Enter Tamil or Code-Mixed text")
    args = parser.parse_args()

    classifier_app = LlamaClassifierCLI()
    classifier_app.classify_text(args.text)

if __name__ == "__main__":
    main()
