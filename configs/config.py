from pathlib import Path

class DefaultConfig:
    def __init__(self):
        self.WORKSPACE = Path('workspace')
        self.TRAIN_PERCENT = 80
        self.TEST_PERCENT = 20

config = DefaultConfig()
