from pathlib import Path

class DefaultConfig:
    def __init__(self):
        self.WORKSPACE = Path('workspace')

config = DefaultConfig()
