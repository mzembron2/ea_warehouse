from turtle import pd
import numpy as np
import pandas as pd
import copy
import os

from warehouse import Warehouse
from evaluator import Evaluator

FREE_CELL_VALUE = -1
DIRNAME = os.path.dirname(__file__)
FILENAME_BLOCKS = os.path.join(DIRNAME, '../data/blocks.csv')

class Bruteforce():
    
    def __init__(self):
        self.warehouse = Warehouse(6,6)
        self.warehouse.get_blocks_from_csv(FILENAME_BLOCKS)
        self.evaluator = Evaluator(self.warehouse)
        self.list_of_grids= []
        self.const_block_dict = self.warehouse.blocks_dict
        self.const_block_waiting_list = self.warehouse.blocks_in_waiting_list
        self.max_num = 1

    def getOccupiedArea(self, grid):
        return np.count_nonzero(grid >= 0)

    def solve(self):
        xmax, ymax = self.warehouse.warehouse_matrix.shape
        for y in range(ymax):
            for x in range(xmax):
                if self.warehouse.warehouse_matrix[x][y]==FREE_CELL_VALUE:
                    for n in self.const_block_waiting_list:
                        x_len = self.const_block_dict[n].x_length
                        y_len = self.const_block_dict[n].y_length
                        if self.warehouse.is_spot_available(x, y, x_len, y_len):
                            self.warehouse.place_block(n, x, y)
                            if(self.evaluator.has_access_to_path(n)):
                                self.solve()
                            self.warehouse.remove_block(n)
                        if (x_len!=y_len):
                            self.warehouse.rotate_block(n)
                            x_len = self.const_block_dict[n].x_length
                            y_len = self.const_block_dict[n].y_length
                            if self.warehouse.is_spot_available(x, y, x_len, y_len):
                                self.warehouse.place_block(n, x, y)
                                if(self.evaluator.has_access_to_path(n)):
                                    self.solve()
                                self.warehouse.remove_block(n)
                            self.warehouse.rotate_block(n)
                    # return  
        some_val_to_compare= self.evaluator.calculate_profit(self.warehouse)
        if some_val_to_compare == self.max_num:
            self.list_of_grids.append(copy.deepcopy(self.warehouse.warehouse_matrix ))
        elif some_val_to_compare>self.max_num:
            self.max_num= some_val_to_compare
            self.list_of_grids= []
            self.list_of_grids.append(copy.deepcopy(self.warehouse.warehouse_matrix ))
        print(self.max_num)


    def show(self):
        print(self.max_num)
        print(self.list_of_grids)
        for grid in self.list_of_grids:
            print(np.matrix(grid))

        # def find_spot(self, block_index):
        #     x_len =self.warehouse 
        #     for x in range(self.warehouse.warehouse_matrix.size()[0]):
