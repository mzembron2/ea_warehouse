from warehouse import Warehouse 
from evaluator import Evaluator
import numpy as np
import random
import copy
import os

FREE_CELL_VALUE = -1
DIRNAME = os.path.dirname(__file__)
FILENAME_BLOCKS = os.path.join(DIRNAME, '../data/blocks.csv')
FILENAME_PERFORMANCE = os.path.join(DIRNAME, '../data/performance.txt')

class EvolutionaryAlgorithm():
    
    def __init__(self, population_size: int = 4, iterations_number: int  = 2000, use_crossover: bool = True,
                    warehouse: Warehouse = None, p_c = 0.5):

        """
            Implementation of evolutionary algorithm for optimization of
            occupated space in warehouse, with respect for path to each stored element.

            All blocks are defined in blocks.csv in data folder.

            Every time the algorithm is used, its performance(data useful for ECDF curve plotting,
            see performance_plotting.py) is saved to performance.txt.
            
            ---

            Parameters: 

            * population_size - amount of solutions(configurations of warehouses) generated independently 
                                in each iteration 

            * iterations_number - maximum iteration number - stopping condition of the algorithm

            * use_crossover - Boolean variable indicating, whether to use crossover during the evolution 
                                process

            * warehouse - warehouse class object defining specific size and configuration(unavailable areas) 
                                of the warehouse, which is being filled by the algorithm

            * p_c - the factor determining probability of crossover
            

            ---
            Referances:
            < https://en.wikipedia.org/wiki/Evolutionary_algorithm >

        """
        if(warehouse == None):
            self.warehouse = Warehouse(8,8)
        else:
            self.warehouse = warehouse
        self.warehouse.get_blocks_from_csv(FILENAME_BLOCKS)
        self.population_size = population_size
        self._generate_population()
        self.evaluator = Evaluator()
        self.largest_profit = 0
        self.p_c = p_c
        self.best_warehouse = None
        self.iterations_number = iterations_number
        self.use_crossover = use_crossover
        self.performance = []
    
    def run(self):
        self.performance.clear()
        iteration= 0
        while (iteration< self.iterations_number):

            next_population = copy.deepcopy(self.current_population)
            population_profits_list = [self._evaluate_function(x) for x in self.current_population]
            population_profit_ziped = zip(self.current_population, population_profits_list)

            best_wh_ziped= max(population_profit_ziped, key = lambda i : i[1])
            if(best_wh_ziped[1] > self.largest_profit):
                    self.largest_profit = best_wh_ziped[1]
                    print("-- current largest profit: ", best_wh_ziped[1], " --")
                    print(best_wh_ziped[0].warehouse_matrix)
                    self.best_warehouse = copy.deepcopy(best_wh_ziped[0])
                    self.performance.append((iteration,best_wh_ziped[1]))
            
            for element_index in range (len(self.current_population)):

                if(self.use_crossover):
                    a= random.randint(0, 100)/100
                    if (a<self.p_c):
                        wh1, wh2 = self._tournament_selection(probability_distribution=population_profits_list)
                        wh = self._crossover(wh1, wh2)
                        next_population[element_index]= wh

                else:
                    wh= self._tournament_selection(number_of_blocks_to_pick=1,
                        probability_distribution=population_profits_list)[0]
                    next_population[element_index]= wh
                self._mutation(next_population, element_index)


            self.current_population = copy.deepcopy(next_population)
            iteration+= 1
            print("iterations: %i/%i"%(iteration,self.iterations_number))
        print("-- Largest profit: ", self.largest_profit, " --" )
        print(self.best_warehouse.warehouse_matrix) 
        self._save_performance_to_txt()
        return self.best_warehouse

    def _generate_population(self):
        self.current_population = [copy.deepcopy(self.warehouse)
             for i in range(self.population_size)]

    def _mutation(self,population, block_index):
        if(len(population[block_index].blocks_in_warehouse) == 0):
            population[block_index].place_random_block()
            population[block_index].rotate_random_block()
        else:
            population[block_index].random_operation()
            population[block_index].rotate_random_block()

    def _create_crossover_border(self):
        return random.randint(0, self.warehouse.warehouse_matrix.shape[1] - 1) 

    def _delete_divided_blocks(self, some_warehouse, border, side):
        left_warehouse_matrix = some_warehouse.warehouse_matrix[:,:border]
        right_warehouse_matrix = some_warehouse.warehouse_matrix[:,border:]
        uniq_left = np.unique(left_warehouse_matrix[left_warehouse_matrix > FREE_CELL_VALUE])
        uniq_right = np.unique(right_warehouse_matrix[right_warehouse_matrix > FREE_CELL_VALUE])

        if (side == "left"):
            for u_r in uniq_right:
                some_warehouse.remove_block(u_r)
            return some_warehouse
        else:
            for u_l in uniq_left:
                some_warehouse.remove_block(u_l)
            return some_warehouse

    def _crossover(self, first_warehouse, second_warehouse) -> Warehouse:
        border = self._create_crossover_border()
        left_warehouse = self._delete_divided_blocks(first_warehouse, border, 'left')
        right_warehouse = self._delete_divided_blocks(second_warehouse, border, 'right')
        blocks_in_left_warehouse = copy.deepcopy(left_warehouse.blocks_in_warehouse)

        for block_id in blocks_in_left_warehouse:
            if block_id in right_warehouse.blocks_in_warehouse:
                random_result = random.choice([True, False])
                if(random_result):
                    right_warehouse.remove_block(block_id)
                else:
                    left_warehouse.remove_block(block_id)
        return self._create_child(left_warehouse, right_warehouse)

    def _create_child(self, left_warehouse: Warehouse, right_warehouse: Warehouse) -> Warehouse:
        child = copy.deepcopy(self.warehouse)
        assert(len(child.blocks_in_warehouse) == 0)

        for block_index in left_warehouse.blocks_in_warehouse:
            x_origin = left_warehouse.blocks_dict[block_index].x_origin
            y_origin = left_warehouse.blocks_dict[block_index].y_origin

            #Children can have blocks with different rotation
            x_len = child.blocks_dict[block_index].x_length
            y_len = child.blocks_dict[block_index].y_length
            if(child.is_spot_available(x_origin, y_origin, x_len, y_len)):
                child.place_block(block_index, x_origin, y_origin)

        for block_index in right_warehouse.blocks_in_warehouse:
            x_origin = right_warehouse.blocks_dict[block_index].x_origin
            y_origin = right_warehouse.blocks_dict[block_index].y_origin
            x_len = child.blocks_dict[block_index].x_length
            y_len = child.blocks_dict[block_index].y_length
            if(child.is_spot_available(x_origin, y_origin, x_len, y_len)):
                child.place_block(block_index, x_origin, y_origin)

        return child

    def _evaluate_function(self, wh: Warehouse):
        return self.evaluator.calculate_profit(wh)

    def _tournament_selection(self, number_of_blocks_to_pick=2, probability_distribution=None):
        if(probability_distribution ==None):
            probability_distribution= [self._evaluate_function(x) for x in self.current_population]
        draw = np.random.choice(self.current_population, number_of_blocks_to_pick, probability_distribution)
        return draw

    def _save_performance_to_txt(self):
        with open(FILENAME_PERFORMANCE, 'a') as f:
            f.write('Population size: %i, iterations: %i, crossover: %s, blocks num: %i, warehouse size: %ix%i\n'%
                (self.population_size, self.iterations_number, str(self.use_crossover),
                len(self.warehouse.blocks_dict), np.shape(self.warehouse.warehouse_matrix)[0],
                np.shape(self.warehouse.warehouse_matrix)[1]))
            for element in self.performance:
                f.write('%i %f\n' % (element[0], element[1]))


