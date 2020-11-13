class Logger:

    def __init__(self, log):
        self.is_logging = log

    def log(self, msg):
        if self.is_logging:
            print(msg)
