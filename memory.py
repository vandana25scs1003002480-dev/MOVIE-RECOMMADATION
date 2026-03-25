# memory.py

class Memory:
    def __init__(self):
        self.history = []

    def add(self, role, message):
        self.history.append({"role": role, "message": message})

    def get_summary(self):
        """Returns last 10 messages as context."""
        return "\n".join([f"{h['role']}: {h['message']}" for h in self.history[-10:]])
