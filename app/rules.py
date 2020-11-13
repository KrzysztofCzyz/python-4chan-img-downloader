import re


class Rule:

    def __init__(self):
        self.passed = 0

    def check(self, thread):
        pass


class MatchRule(Rule):

    def __init__(self, arg):
        super().__init__()
        self.regexp = re.compile(arg, re.IGNORECASE)

    def check(self, thread):
        sub = thread.get('sub', '')
        com = thread.get('com', '')

        if self.regexp.match(sub) or self.regexp.match(com):
            print("Rule passed with sub and com:", sub, com)
            self.passed += 1
            return True
        else:
            return False


class ImageCountRule(Rule):

    def __init__(self, arg):
        super().__init__()
        self.num = int(arg)

    def check(self, thread):
        images = thread.get('images')
        result = images > self.num
        if result:
            self.passed += 1
            print(f"Rule passed with number {images}")
            return True
        return False
