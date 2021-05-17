


class Message:
    def __init__(self, from_, to, content, protocol):
        self.from_ = from_
        self.to = to
        self.content = content
        self.protocol = protocol

        self.is_send = False
