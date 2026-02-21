"""
1st logger for to_do.py
"""

import logging
import os

def create_file_handler(log_file, level=logging.DEBUG):
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(level)
    return file_handler

def create_stream_handler(level=logging.WARNING):
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)
    return stream_handler

def set_formatter(handler, detailed=False):
    if detailed:
        log_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s - [Logged by: %(name)s]')
    else:
        log_format = logging.Formatter('%(levelname)s - %(message)s')
    handler.setFormatter(log_format)

def setup_logger(name, log_file="logs/log.log", level=logging.DEBUG, handlers=None):

    root = logging.getLogger()
    root.setLevel(level)

    if root.hasHandlers():
        root.handlers.clear()
    
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    if handlers is None:
        handlers = ['file', 'stream']

    for handler in handlers:
        if handler == 'file':
            file_handler = create_file_handler(log_file, level)
            set_formatter(file_handler, detailed=True)
            root.addHandler(file_handler)
        elif handler == 'stream':
            stream_handler = create_stream_handler()
            set_formatter(stream_handler, detailed=False)
            root.addHandler(stream_handler)     

    logger = logging.getLogger(name)   
    logger.setLevel(level)
    logger.propagate = True

    return logger    
