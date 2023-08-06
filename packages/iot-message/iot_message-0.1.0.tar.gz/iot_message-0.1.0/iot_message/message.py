#!/usr/bin/python3
import os
import subprocess
import iot_message.abstract.message_interface as message_interface
import json

__author__ = 'Bartosz Kościów'


class Message(message_interface.Message):
    """Class Message"""
    protocol = "iot:1"

    def __init__(self, node, chip_id=None):
        self._node = node
        if chip_id is None:
            self._chip_id = self._get_id()
        else:
            self._chip_id = chip_id

    @property
    def node(self):
        """
        Return node name
        :return string
        """
        return self._node

    @property
    def chip_id(self):
        """
        Return chip id
        :return string
        """
        return self._chip_id

    def _get_id(self):
        """:return string"""
        if 'nt' in os.name:
            return subprocess.getoutput('wmic csproduct get uuid')
        else:
            return subprocess.getoutput('cat /var/lib/dbus/machine-id')

    def prepare_message(self, data=None):
        """
        Return message as dict
        :return dict
        """
        message = {
            'protocol': self.protocol,
            'node': self._node,
            'chip_id': self._chip_id,
            'event': '',
            'parameters': {},
            'response': '',
            'targets': [
                'ALL'
            ]
        }
        if type(data) is dict:
            for k, v in data.items():
                if k in message:
                    message[k] = v

        return message

    def decode_message(self, message):
        """
        Decode json string to dict. Validate against node name(targets) and protocol version
        :return dict | None
        """
        try:
            message = json.loads(message)
            if not self._validate_message(message):
                message = None
        except ValueError:
            message = None

        return message

    def _validate_message(self, message):
        """:return boolean"""
        if 'protocol' not in message or 'targets' not in message or \
                type(message['targets']) is not list:
            return False

        if message['protocol'] != self.protocol:
            return False

        if self.node not in message['targets'] and 'ALL' not in message['targets']:
            return False

        return True