import numpy as np

class Block():
    """

    Representation of block - an item that can be stored in a warehouse
    
    """

    def __init__(self, x_length, y_length, x_origin = None, y_origin = None):
        self.x_origin = x_origin
        self.y_origin =  y_origin
        self.x_length =  x_length
        self.y_length =  y_length

    def set_position(self, x_origin, y_origin):
        self.x_origin = x_origin
        self.y_origin =  y_origin
    
    def is_position_set(self):
        return ((self.x_origin is not None) and (self.y_origin is not None))