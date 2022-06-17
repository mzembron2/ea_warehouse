import numpy as np
import pandas as pd
from block import Block

FREE_CELL_VALUE = -1

class Warehouse():
    def __init__(self, rows, columns):
        """ 
            warehouse_matrix - representation of warehouse
            blocks_dict - dictionary containing all available blocks
        """
        self.warehouse_matrix = np.full((rows, columns), FREE_CELL_VALUE,dtype=int)
        self.blocks_dict = {}

    def get_blocks_from_csv(self, file_name):
        blocks = pd.read_csv(file_name)
        for index, row in blocks.iterrows():
            self.blocks_dict[index] = Block(int(row['x_length']), int(row['y_length']))

    def place_block(self, index, x_origin, y_origin):
        current_block = self.blocks_dict[index]
        self.warehouse_matrix[x_origin:x_origin + current_block.x_length,
            y_origin:y_origin + current_block.y_length] = index

        self.blocks_dict[index].set_position(x_origin, y_origin)

    def remove_block(self, index):
        current_block = self.blocks_dict[index]
        assert(current_block.is_position_set())
        x_origin = current_block.x_origin
        y_origin = current_block.y_origin
        x_len = current_block.x_length
        y_len = current_block.y_length

        self.warehouse_matrix[x_origin:x_origin + x_len,
            y_origin:y_origin + y_len] = FREE_CELL_VALUE
        self.blocks_dict[index].set_position(None, None)

    def is_spot_available(self, x, y, x_len, y_len):
        indexes = np.unique(self.warehouse_matrix[x:x+x_len,y:y+y_len])
        if(indexes.size>1 or indexes[0] != FREE_CELL_VALUE):
            return False
        else:
            return True

    def get_matrix(self):
        return self.warehouse_matrix

    


