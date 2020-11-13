class LinkBuilder:

    def __init__(self):
        self.d = dict()

    def configure(self, config):
        self.d = config

    def build_thread_link(self, board, no):
        link = self.d.get('thread-link-parts')
        return f"{link[0]}{board}{link[1]}{no}{link[2]}"

    def build_board_link(self, board):
        link = self.d.get('board-link-parts')
        return f"{link[0]}{board}{link[1]}"

    def build_image_link(self, board, tim, ext):
        link = self.d.get('image-link-parts')
        return f"{link[0]}{board}{link[1]}{tim}{ext}"
