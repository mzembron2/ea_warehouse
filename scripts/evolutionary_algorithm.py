from warehouse import Warehouse 
from evaluator import Evaluator
import numpy as np
import random
import copy
import os

FREE_CELL_VALUE = -1
DIRNAME = os.path.dirname(__file__)
FILENAME_BLOCKS = os.path.join(DIRNAME, '../data/blocks.csv')

class EvolutionaryAlgotihm():
    
    def __init__(self, population_size = 4):
        self.warehouse = Warehouse(10,10)
        self.warehouse.get_blocks_from_csv(FILENAME_BLOCKS)
        self.population_size = population_size
        self.generate_population()
        self.evaluator = Evaluator()
        self.largest_profit = 0
        self.best_warehouse = None
    
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
    def crossover(self, first_warehouse, second_warehouse) -> Warehouse:

        #TO DO po zmianie 
        # first_warehouse = self.current_population[first_warehouse_index]
        # second_warehouse = self.current_population[second_warehouse_index]

        border = self.create_crossover_border()
        # print("-- border: ", border, " --")
        # left_warehouse, uniq_left = self.delete_divided_blocks(first_warehouse, border, 'left')
        # right_warehouse, uniq_right = self.delete_divided_blocks(second_warehouse, border, 'right')

        left_warehouse = self.delete_divided_blocks(first_warehouse, border, 'left')
        right_warehouse = self.delete_divided_blocks(second_warehouse, border, 'right')
        # for u_l in uniq_left:
        blocks_in_left_warehouse = copy.deepcopy(left_warehouse.blocks_in_warehouse)
        for block_id in blocks_in_left_warehouse:
            if block_id in right_warehouse.blocks_in_warehouse:
                random_result = random.choice([True, False])
                if(random_result):
                    right_warehouse.remove_block(block_id)
                    # uniq_right = uniq_right[uniq_right!=u_l]
                else:
                    left_warehouse.remove_block(block_id)
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

    def evaluate_function(self, wh: Warehouse):
        
        # wh = self.current_population[warehouse_index].warehouse_matrix
        # count_blocks_area = np.count_nonzero(wh >= 0)
        # count_warehouse_size = wh.size - np.count_nonzero(wh == -2)
        return self.evaluator.calculate_profit(wh)

    def tournament_selection(self, number_of_blocks_to_pick=2):
        probability_distribution= [self.evaluate_function(x) for x in self.current_population]
        draw = np.random.choice(self.current_population, number_of_blocks_to_pick, probability_distribution)
        return draw

    def run(self, pc= 0.5):
        stop = False

        # self.generate_population()
        t= 0
        while (not stop):
            O = []
            for i in range (len(self.current_population)):
                a= random.randint(0, 100)/100
                if (a<pc):
                    wh1, wh2 = self.tournament_selection()
                    wh = self.crossover(wh1, wh2)
                # else:
                #     wh= self.tournament_selection(1)[0]
                    self.current_population[i]= wh
                self.mutation(i)
                child = self.current_population[i]
                child_profit = self.evaluate_function(child)
                if(child_profit > self.largest_profit):
                    self.largest_profit = child_profit
                    print("-- current best profit: ", child_profit, " --")
                    self.best_warehouse = copy.deepcopy(child)
            t= t + 1
            if (t>2000):
                stop= True
        print([self.evaluate_function(x) for x in self.current_population])
        for wh in self.current_population:
            print(wh.warehouse_matrix)
            print("-------------------------------------")
        print("-- Largest porfit: ", self.largest_profit, " --" )
        print(self.best_warehouse.warehouse_matrix)

