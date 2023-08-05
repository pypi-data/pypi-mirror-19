#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 11:18:05 2016

@author: chernov
"""
import os
import sys
import asyncio

main_dir = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))
if not main_dir in sys.path: sys.path.append(main_dir)
del main_dir

import dfparser as env_parser

class DataforgeEnvelopeProtocol(asyncio.Protocol):
    """
      Base class for dataforge envelope protocol server.
      
      To define your message processing, redefine process_message()
      function
      
      To send message back to peer use function send_message()
      
    """
    def process_message(self, message):
        """
          Process handler for received messages. This function will be executed
          for every datafogre envelope formatted message extracted from socket.
          
          @message - Message container. Contains 3 fields:
            - header - binary message header
            - meta - parsed message metadata
            - data - message binary data
            
        """
        print("this is process_message() placeholder\n"
              "received message: ", message)
        self.send_message(message['meta'])
        
    def send_message(self, meta, data=b''):
        prep_message = env_parser.create_message(meta, data)
        self.transport.write(prep_message)
    
    def __init__(self, *args, **kwargs):
        super(DataforgeEnvelopeProtocol, self).__init__(*args, **kwargs)
        self.data = b''
    
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        self.data += data
        messages, self.data = env_parser.get_messages_from_stream(data)   
        
        for message in messages:
            self.process_message(message)

            
def def_callback(message, client_obj):
    print("default callback triggered: received message:", message)
    client_obj.transport.close()
            
    
class DataforgeEnvelopeEchoClient(DataforgeEnvelopeProtocol):
    """
      Echo client for dataforge protocol
      
      Class will pass command, then wait for answer and close socket
    """
    
    def __init__(self, loop, meta, data=b'', callback=def_callback,
                 timeout_sec=1):
        
        super(DataforgeEnvelopeEchoClient, self).__init__()
        self.meta = meta
        self.data = data
        self.loop = loop
        self.timeout_sec = timeout_sec
        self.callback = callback

    def connection_made(self, transport):
        super(DataforgeEnvelopeEchoClient, self).connection_made(transport)
        self.h_timeout = self.loop.call_later(self.timeout_sec, self.timeout)
        self.send_message(self.meta, self.data)
        
    def process_message(self, message):
        self.h_timeout.cancel()
        self.loop.call_soon_threadsafe(self.callback, message, self)
        
    def data_received(self, data):
        super(DataforgeEnvelopeEchoClient, self).data_received(data)

    def connection_lost(self, exc):
        self.loop.stop()
        
    def timeout(self):
        self.transport.close()
