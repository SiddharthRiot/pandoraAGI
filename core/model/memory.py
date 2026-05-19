import json
import os
from datetime import datetime


class Memory:
    def __init__(self, memory_file: str = "memory.json"):
        self.memory_file = memory_file
        self.conversations = []
        self._load()

    def _load(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file, "r") as f:
                self.conversations = json.load(f)
            print(f"[PandoraAGI] Memory loaded — {len(self.conversations)} conversations")
        else:
            print("[PandoraAGI] No memory found — starting fresh")

    def _save(self):
        with open(self.memory_file, "w") as f:
            json.dump(self.conversations, f, indent=2)

    def add(self, role: str, content: str):
        entry = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        self.conversations.append(entry)
        self._save()

    def get_context(self, last_n: int = 10) -> list:
        recent = self.conversations[-last_n:]
        return [{"role": c["role"], "content": c["content"]} for c in recent]

    def clear(self):
        self.conversations = []
        self._save()
        print("[PandoraAGI] Memory cleared")

    def stats(self) -> dict:
        return {
            "total_conversations": len(self.conversations),
            "memory_file": self.memory_file
        }