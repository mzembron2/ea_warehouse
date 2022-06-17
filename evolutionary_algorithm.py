import pandas as pd
import numpy as np
from warehouse import Warehouse 

class EvolutionaryAlgotihm():
    
    def __init__(self):
        self.warehouse = Warehouse(4,7)
        self.warehouse.get_blocks_from_csv("blocks.csv")
    
    def mutation(self):
        if(len(self.warehouse.blocks_in_warehouse) == 0):
            self.warehouse.place_random_block()
        else:
            """ Rnadom: place, remove or exchange """
            pass
