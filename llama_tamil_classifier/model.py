from transformers import AutoModelForCausalLM, AutoTokenizer
# from transformers import BitsAndBytesConfig
import torch
from huggingface_hub import login

class LlamaClassifier:
    def __init__(self):
        login(token="hf_key")
        MODEL_NAME = "meta-llama/Llama-3.2-3B-Instruct"
        # 4-bit quantization for memory efficiency
        # bnb_config = BitsAndBytesConfig(
        #     load_in_4bit=True,
        #     bnb_4bit_compute_dtype="bfloat16",  # Change from float16 to bfloat16
        #     bnb_4bit_use_double_quant=True,
        #     bnb_4bit_quant_type="nf4"  # Use NF4 quantization for better accuracy
        # )
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        self.model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, 
                                                        #   load_in_8bit=True, 
                                                          device_map="cpu",
                                                          ).to("cpu")


    def classify(self, text):
        prompt = (
            f"Analyze the given Tamil or code-mixed Tamil-English text.\n"
            f"- Identify the **main topic(s)** from categories like politics, entertainment, sports, technology, or general.\n"
            f"- Classify the **sentiment** as positive, negative, or neutral.\n"
            f"- Provide a **brief reason (1-2 lines)** justifying the classification.\n\n"
            f"Text: {text}\n\n"
            f"Response format strictly as follows:\n"
            f"Topic: <One or More Topics> or Unknown\n"
            f"Sentiment: <Positive/Negative/Neutral> or Unknown\n"
            f"Reason: <1-2 lines explaining why>\n\n"
            f"Output:"
        )

        inputs = self.tokenizer(prompt, return_tensors="pt").to("cpu")
        output = self.model.generate(**inputs, max_length=200)
        result = self.tokenizer.decode(output[0], skip_special_tokens=True)
        return result
