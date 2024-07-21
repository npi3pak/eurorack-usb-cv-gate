class Logger:
    DEBUG = 1
    INFO = 2
    ERROR = 3

    def __init__(self, level=DEBUG):
        self.level = level

    def debug(self, message):
        if self.level <= self.DEBUG:
            print(f"DEBUG: {message}")

    def info(self, message):
        if self.level <= self.INFO:
            print(f"INFO: {message}")

    def error(self, message):
        if self.level <= self.ERROR:
            print(f"ERROR: {message}")