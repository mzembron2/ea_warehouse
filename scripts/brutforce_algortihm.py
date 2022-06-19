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
        self.warehouse = Warehouse(3,3)
        self.warehouse.get_blocks_from_csv(FILENAME_BLOCKS)
        self.evaluator = Evaluator(self.warehouse)
        self.list_of_grids= []
        self.max_num = 1

    def getOccupiedArea(self, grid):
        return np.count_nonzero(grid >= 0)

    def solve(self):
        xmax, ymax = self.warehouse.warehouse_matrix.shape
        for y in range(ymax):
            for x in range(xmax):
                if self.warehouse.warehouse_matrix[x][y]==FREE_CELL_VALUE:
                    for n in self.warehouse.blocks_in_waiting_list:
                        x_len = self.warehouse.blocks_dict[n].x_length
                        y_len = self.warehouse.blocks_dict[n].y_length
                        if self.warehouse.is_spot_available(y, x, y_len, x_len):
                            self.warehouse.place_block(n, x, y)
                            if(self.evaluator.has_access_to_path(n)):
                                self.solve()
                            self.warehouse.remove_block(n)
                        # if (x_len!=y_len):
                        #     if self.warehouse.is_spot_available(y, x, x_len, y_len):
                        #         for i in range(x_len):
                        #             for j in range(y_len):
                        #                 grid[y+i][x+j]=n+1
                        #         if(checkContainerList(grid, len(grid)-1, len(grid)-1)):
                        #             solve()
                        #         for i in range(x_len):
                        #             for j in range(y_len):
                        #                 grid[y+i][x+j]=FREE_CELL_VALUE
    #                 return  
        grid = self.warehouse.warehouse_matrix   
        if self.getOccupiedArea(grid)== self.max_num:
            self.list_of_grids.append(copy.deepcopy(grid))
        elif self.getOccupiedArea(grid)>self.max_num:
            self.max_num=self.getOccupiedArea(grid)
            self.list_of_grids= []
            self.list_of_grids.append(copy.deepcopy(grid))


    def show(self):
        print(self.max_num)
        for grid in self.list_of_grids:
            print(np.matrix(grid))

        # def find_spot(self, block_index):
        #     x_len =self.warehouse 
        #     for x in range(self.warehouse.warehouse_matrix.size()[0]):
