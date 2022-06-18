from warehouse import Warehouse 
import numpy as np
import random
import copy
import os

FREE_CELL_VALUE = -1
DIRNAME = os.path.dirname(__file__)
FILENAME_BLOCKS = os.path.join(DIRNAME, '../data/blocks.csv')

class EvolutionaryAlgotihm():
    
    def __init__(self, population_size = 4):
        self.warehouse = Warehouse(4,17)
        self.warehouse.get_blocks_from_csv(FILENAME_BLOCKS)
        self.population_size = population_size
        self.generate_population()
    
    def generate_population(self):
        self.current_population = [copy.deepcopy(self.warehouse)
             for i in range(self.population_size)]

    def mutation(self, block_index):
        if(len(self.current_population[block_index].blocks_in_warehouse) == 0):
            self.current_population[block_index].place_random_block()
        else:
            self.current_population[block_index].random_operation()

    def create_crossover_border(self):
        #TO DO po zmianie 
        return random.randint(0, self.warehouse.warehouse_matrix.shape[1] - 1) # chyba shape[1]-1

    def delete_divided_blocks(self, some_warehouse, border, side):
        left_warehouse_matrix = some_warehouse.warehouse_matrix[:,:border]
        right_warehouse_matrix = some_warehouse.warehouse_matrix[:,border:]

        uniq_left = np.unique(left_warehouse_matrix[left_warehouse_matrix!=FREE_CELL_VALUE])
        uniq_right = np.unique(right_warehouse_matrix[right_warehouse_matrix!=FREE_CELL_VALUE])

        if (side == "left"):
            for u_r in uniq_right:
                # if u_r in uniq_left:
                #     some_warehoue.remove_block(u_r)
                #     uniq_left = uniq_left[uniq_left!=u_r]

                ##!! usuwam wszystkie bloki z prawej strony - pozostawiam tylko lewe
                some_warehouse.remove_block(u_r)
                # uniq_left = uniq_left[uniq_left!=u_r]
            # return some_warehouse, uniq_left
            return some_warehouse
        else:
            for u_l in uniq_left:
                # if u_l in uniq_right:

                ## !! analogicznie jak wyzej 
                some_warehouse.remove_block(u_l)
                # uniq_right = uniq_right[uniq_right!=u_l]
            # return some_warehouse, uniq_right
            return some_warehouse
    def crossover(self, first_warehouse_index, second_warehouse_index) -> Warehouse:

        #TO DO po zmianie 
        first_warehouse = self.current_population[first_warehouse_index]
        second_warehouse = self.current_population[second_warehouse_index]

        border = self.create_crossover_border()
        print("-- border: ", border, " --")
        # left_warehouse, uniq_left = self.delete_divided_blocks(first_warehouse, border, 'left')
        # right_warehouse, uniq_right = self.delete_divided_blocks(second_warehouse, border, 'right')

        left_warehouse = self.delete_divided_blocks(first_warehouse, border, 'left')
        right_warehouse = self.delete_divided_blocks(second_warehouse, border, 'right')
        # for u_l in uniq_left:
        for u_l in left_warehouse.blocks_in_warehouse:
            if u_l in right_warehouse.blocks_in_warehouse:
                if(random.choice([True, False])):
                    right_warehouse.remove_block(u_l)
                    # uniq_right = uniq_right[uniq_right!=u_l]
                else:
                    left_warehouse.remove_block(u_l)
                    # uniq_left = uniq_left[uniq_left!=u_l]
        
        #TO DO po zmianie 
        # warehouse_to_return = np.full(self.warehouse.warehouse_matrix.shape, FREE_CELL_VALUE,dtype=int)
        # warehouse_to_return[:][:border] =  left_warehouse
        # warehouse_to_return[:][border:] = right_warehouse
        # return warehouse_to_return

        ##!! zwracam caly warehouse
        return self.create_child(left_warehouse, right_warehouse)

    def create_child(self, left_warehouse: Warehouse, right_warehouse: Warehouse) -> Warehouse:
        child = copy.deepcopy(self.warehouse)
        assert(len(child.blocks_in_warehouse) == 0)

        for block_index in left_warehouse.blocks_in_warehouse:
            x_origin = left_warehouse.blocks_dict[block_index].x_origin
            y_origin = left_warehouse.blocks_dict[block_index].y_origin
            child.place_block(block_index, x_origin, y_origin)

        for block_index in right_warehouse.blocks_in_warehouse:
            x_origin = right_warehouse.blocks_dict[block_index].x_origin
            y_origin = right_warehouse.blocks_dict[block_index].y_origin
            child.place_block(block_index, x_origin, y_origin)

        return child





