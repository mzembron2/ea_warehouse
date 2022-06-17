from turtle import pd
import numpy as np
import pandas as pd
from warehouse import Warehouse
import copy

class Bruteforce():
    
    def __init__(self, warehouse):
        self.warehouse = copy.deepcopy(warehouse)  
        