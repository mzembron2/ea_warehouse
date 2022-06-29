import numpy as np
import pandas as pd
from block import Block
import random
import copy

FREE_CELL_VALUE = -1
UNAVAILABLE_AREA_VALUE = -2

class Warehouse():
    def __init__(self, rows, columns):
        """ 
            Reperesentation of warehouse 

            warehouse_matrix - 2D array representation of warehouse using block indexies, and 
            special values defined above:

            * FREE_CELL_VALUE - free space in warehouse - counts as an possible element of path,
                                block can be placed there, 

            * UNAVAILABLE_AREA - area that is excluded from placing a block

            blocks_dict - dictionary containing all available blocks 

            All available blocks(not only in warehouse) are stored in dictionary - self.blocks_dict
            which connects the block instance with its index. 

            For convenience indexes of blocks are stored in the following lists 
            (indicating its placement):

                * self.blocks_in_warehouse
                * self.blocks_in_waiting_list

            Unavailable areas are treated as blocks (that occupy area, but cannot be moved) and 
            are stored in self.unavailable_area_list.
        """
        self.warehouse_matrix = np.full((rows, columns), FREE_CELL_VALUE,dtype=int)
        self.blocks_dict = {}
        self.unavailable_area_list = []
        self.blocks_in_warehouse = []
        self.blocks_in_waiting_list = []

    def get_blocks_from_csv(self, file_name):
        blocks = pd.read_csv(file_name)
        for index, row in blocks.iterrows():
            self.blocks_dict[index] = Block(int(row['x_length']), int(row['y_length']))
            self.blocks_in_waiting_list.append(index)

    def set_unavailable_area(self, x_origin, y_origin, x_len, y_len) -> bool:

        if(self.is_spot_available(x_origin, y_origin, x_len, y_len)):
            self.warehouse_matrix[x_origin:x_origin+x_len, y_origin:y_origin+y_len] = UNAVAILABLE_AREA_VALUE
            self.unavailable_area_list.append(Block(x_len, y_len, x_origin, y_origin))
            return True
        else:
            return False

    def place_block(self, index, x_origin, y_origin):
        current_block = self.blocks_dict[index]
        self.warehouse_matrix[x_origin:x_origin + current_block.x_length,
            y_origin:y_origin + current_block.y_length] = index

        self.blocks_dict[index].set_position(x_origin, y_origin)
        self.blocks_in_waiting_list.remove(index)
        self.blocks_in_warehouse.append(index)

    def rotate_block(self, index) -> bool:
        if(index in self.blocks_in_waiting_list):
            x_len_prev = copy.deepcopy(self.blocks_dict[index].x_length)
            y_len_prev = copy.deepcopy(self.blocks_dict[index].y_length)
            self.blocks_dict[index].x_length = y_len_prev
            self.blocks_dict[index].y_length = x_len_prev
            return True
        else:
            return False

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
        self.blocks_in_warehouse.remove(index)
        self.blocks_in_waiting_list.append(index)

    def is_spot_available(self, x, y, x_len, y_len) ->bool:
        indexes = np.unique(self.warehouse_matrix[x:x+x_len,y:y+y_len])
        max_x = self.warehouse_matrix.shape[0] - 1
        max_y = self.warehouse_matrix.shape[1] - 1
        
        if(indexes.size == 0):
            return False

        elif(indexes.size>1 or indexes[0] != FREE_CELL_VALUE 
            or x + x_len - 1> max_x or y + y_len - 1 > max_y
            or x < 0 or y < 0):
            return False

        else:
            return True

    def get_available_spots(self, index):
        current_block = self.blocks_dict[index]
        x_len = current_block.x_length
        y_len = current_block.y_length

        available_spots = []
        for x in range(self.warehouse_matrix.shape[0] - x_len + 1):
            for y in range(self.warehouse_matrix.shape[1] - y_len + 1):
                if(self.is_spot_available(x, y, x_len, y_len)):
                    available_spots.append((x,y))

        return available_spots
    
    def place_random_block(self) -> bool:
        placed = False
        available_blocks = copy.deepcopy(self.blocks_in_waiting_list)

        while(not placed):
            if(len(available_blocks) == 0):
                    return False

            random_block_index = random.choice(available_blocks)
            available_blocks.remove(random_block_index)
            available_spots = self.get_available_spots(random_block_index)

            if(len(available_spots) == 0):
                continue
            
            random_spot = random.choice(available_spots)
            self.place_block(random_block_index, random_spot[0], random_spot[1])
            placed = True
            return True 

    def rotate_random_block(self) -> bool:
        if(len(self.blocks_in_waiting_list) > 0):
            random_index = random.choice(self.blocks_in_waiting_list)
            self.rotate_block(random_index)
            return True
        else:
            return False
    def remove_random_block(self) -> bool:
        if(len(self.blocks_in_warehouse) == 0):
            return False
        else:
            random_block_index = random.choice(self.blocks_in_warehouse)
            self.remove_block(random_block_index)
            return True

    def random_operation(self):
        operations = [self.remove_random_block, self.place_random_block]
        output = False
        while(not output):
            random_operation = random.choice(operations)
            operations.remove(random_operation)
            output = random_operation()


            
    
        


    


