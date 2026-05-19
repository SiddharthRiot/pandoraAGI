from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from .config import ModelConfig
from .memory import Memory


class LivingModel:
    def __init__(self, config: ModelConfig = None):
        self.config = config or ModelConfig()
        self.tokenizer = None
        self.model = None
        self.memory = Memory()

    def load(self):
        print(f"[PandoraAGI] Loading model: {self.config.model_name}")
        self.tokenizer = AutoTokenizer.from_pretrained(self.config.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.config.model_name,
            torch_dtype=torch.float32,
        )
        self.model.eval()
        print(f"[PandoraAGI] Model loaded. Version: {self.config.version}")

    def generate(self, prompt: str) -> str:
        if self.model is None:
            raise RuntimeError("Model not loaded. Call load() first.")

        self.memory.add("user", prompt)

        context = self.memory.get_context(last_n=10)
        conversation = ""
        for msg in context:
            if msg["role"] == "user":
                conversation += f"User: {msg['content']}\n"
            else:
                conversation += f"Assistant: {msg['content']}\n"
        conversation += "Assistant:"

        inputs = self.tokenizer(conversation, return_tensors="pt")
        input_length = inputs["input_ids"].shape[1]

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=self.config.max_new_tokens,
                temperature=self.config.temperature,
                top_p=self.config.top_p,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,
            )

        new_tokens = outputs[0][input_length:]
        response = self.tokenizer.decode(new_tokens, skip_special_tokens=True)

        self.memory.add("assistant", response)

        return response

    def log_lineage(self, entry: str):
        self.config.lineage.append(entry)
        print(f"[PandoraAGI] Lineage updated: {entry}")