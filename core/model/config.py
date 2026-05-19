from dataclasses import dataclass

@dataclass
class ModelConfig:
    model_name: str = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    device: str = "cpu"
    max_new_tokens: int = 256
    temperature: float = 0.7
    top_p: float = 0.9
    version: str = "0.0.1"
    lineage: list = None

    def __post_init__(self):
        if self.lineage is None:
            self.lineage = []