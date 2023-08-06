
__author__ = 'Bartosz Kościów'

"""Interface foe message"""


class Message(object):
    """Required function for message"""
    def __init__(self, node, chip_id=None):
        raise NotImplementedError("init not implemented")

    def prepare_message(self, data=None):
        """prepares empty message adn merge it with data"""
        raise NotImplementedError("prepare_message not implemented")

    def decode_message(self, message):
        """from string decode to json, check protocol and targets"""
        raise NotImplementedError("decode_message not implemented")