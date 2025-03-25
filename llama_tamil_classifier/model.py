import re
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from huggingface_hub import login

class LlamaClassifier:
    def __init__(self):
        login(token="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")
        MODEL_NAME = "meta-llama/Llama-3.2-3B-Instruct"
        
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        self.model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME
        ).to(self.device)

    def classify(self, text):
        prompt = (
            f"Analyze the given Tamil or code-mixed Tamil-English text.\n"
            f"Identify up to 5 most relevant topics from: Politics, Entertainment, Sports, Technology, General, Pricing, Performance, Storage, Display, and Electronics.\n"
            f"For each topic, classify the sentiment as Positive, Negative, or Neutral.\n"
            f"Extract specific words or phrases that indicate the topic and sentiment.\n"
            f"Provide a concise reason summarizing the classification.\n\n"
            f"Text: {text}\n\n"
            f"Strictly use this response format:\n"
            f"1. Topic: <Single Topic> | Sentiment: <Positive/Negative/Neutral> | Words: '<Relevant words/phrases>'\n"
            f"2. Topic: <Single Topic> | Sentiment: <Positive/Negative/Neutral> | Words: '<Relevant words/phrases>'\n"
            f"... up to 5 topics\n\n"
            f"Overall Topic: <Most dominant topic>\n"
            f"Overall Sentiment: <Positive/Negative/Neutral>\n"
            f"Reason: <Concise explanation>\n\n"
            f"Output:"
        )

        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024).to(self.device)

        output = self.model.generate(
            **inputs,
            max_new_tokens=200,  # Ensures concise output
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.2,
            eos_token_id=self.tokenizer.eos_token_id,
            pad_token_id=self.tokenizer.eos_token_id,
        )

        result = self.tokenizer.decode(output[0], skip_special_tokens=True).strip()

        # Extract the relevant classification result
        if "Output:" in result:
            result = result.split("Output:")[-1].strip()

        # Ensure truncation after "Reason:" to avoid extra text
        if "Reason:" in result:
            result = result.split("Reason:")[0] + "Reason: " + result.split("Reason:")[1].split("\n")[0]

        return f"Input Text: {text}\n" + result
