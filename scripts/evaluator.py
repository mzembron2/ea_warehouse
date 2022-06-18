from msilib import _directories
import numpy as np
from warehouse import Warehouse


PATH_WIDTH = 1
FREE_CELL_VALUE = -1

class Evaluator():
    def __init__(self, warehouse: Warehouse):
        self.warehouse = warehouse

    def has_access_to_path(self, block_index):
        current_block = self.warehouse.blocks_dict[block_index]
        assert(current_block.is_position_set())
        x_origin = current_block.x_origin
        y_origin = current_block.y_origin
        x_len = current_block.x_length
        y_len = current_block.y_length
        x_end = x_origin + x_len -1
        y_end = y_origin + y_len -1

        return (self.is_space_above_block(x_origin, y_origin, y_len) or
                self.is_space_below_block(x_end, y_origin, y_len) or
                self.is_space_on_left_from_block(x_origin, y_origin, x_len) or
                self.is_space_on_right_from_block(x_origin, y_end, x_len)) 

    def is_space_above_block(self, x_origin, y_origin, y_len):
        return self.warehouse.is_spot_available(x_origin - PATH_WIDTH,
             y_origin, PATH_WIDTH, y_len)

    def is_space_below_block(self, x_end, y_origin, y_len):
        return self.warehouse.is_spot_available(x_end + PATH_WIDTH,
             y_origin, PATH_WIDTH, y_len)

    def is_space_on_left_from_block(self, x_origin, y_origin, x_len):
        return self.warehouse.is_spot_available(x_origin, 
            y_origin - PATH_WIDTH, x_len, PATH_WIDTH)

    def is_space_on_right_from_block(self, x_origin, y_end, x_len):
        return self.warehouse.is_spot_available(x_origin, 
            y_end + PATH_WIDTH, x_len, PATH_WIDTH)

    # def update_space(self):
    #     start_x = 0
    #     start_y = 0 
    #     (rows, columns) = np.shape(self.warehouse.warehouse_matrix)
    #     path_access_mask = np.full((rows, columns), False,dtype=bool)
    #     for row in rows:
    #         for col in columns:





        


