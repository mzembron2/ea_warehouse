from warehouse import Warehouse
from evaluator import Evaluator
from evolutionary_algorithm import EvolutionaryAlgorithm
import numpy as np
import os

# path to data
DIRNAME = os.path.dirname(__file__)
FILENAME_BLOCKS = os.path.join(DIRNAME, '../data/blocks.csv')

if(__name__ == "__main__"):
    wh = Warehouse(14,7)
    wh.get_blocks_from_csv(FILENAME_BLOCKS)

    # uncomment proper section below 

    """ demonstartion of warehouse """

    # blocks_number = len(wh.blocks_dict)
    # print(wh.warehouse_matrix)
    # assert(wh.is_spot_available(1,1,1,1))
    # can_place_random = True

    # # fill warehouse with blocks in random order  
    # while(can_place_random):
    #     can_place_random = wh.place_random_block()
    #     print(wh.warehouse_matrix)

    # print(wh.warehouse_matrix)
    # print(wh.blocks_dict[0].x_origin, wh.blocks_dict[0].y_origin)
    # print(wh.is_spot_available(1,1,5,5))

    # print("All available spots for block with index 3: ",  wh.get_available_spots(3))

    # # remove random block from warehouse
    # wh.remove_random_block()
    # print(wh.warehouse_matrix)
    
    """ block rotation """

    # wh.place_block(6, 0, 0)
    # print(wh.warehouse_matrix)
    # wh.remove_block(6)
    # wh.rotate_block(6)
    # wh.place_block(6, 0, 0)
    # print(wh.warehouse_matrix)

    """ demonstration of ea"""
    ea = EvolutionaryAlgorithm()

    ## crossover
    # ea.mutation(0)
    ea.current_population[0].place_block(0,1,1)
    ea.current_population[0].place_block(1,2,4)
    ea.current_population[0].place_block(2,2,15)  
    # ea.mutation(1)
    ea.current_population[1].place_block(0,1,2)
    ea.current_population[1].place_block(1,2,8)
    ea.current_population[1].place_block(2,3,15) 


    wh1 = ea.current_population[0]
    wh2 = ea.current_population[1]
    print(wh1.warehouse_matrix)
    print(wh2.warehouse_matrix)
    print(ea._crossover(wh1,wh2).warehouse_matrix)


    ea._tournament_selection(2)
    # ea.run()
    


    """ demonstartion of evaluator """
    # wh.place_block(0,11,4)
    # wh.place_block(1, 11, 3 )
    # print(wh.warehouse_matrix)

    # current_block = wh.blocks_dict[0]
    # assert(current_block.is_position_set())
    # x_origin = current_block.x_origin
    # y_origin = current_block.y_origin
    # x_len = current_block.x_length
    # y_len = current_block.y_length
    # x_end = x_origin + x_len -1
    # y_end = y_origin + y_len -1

    # eval = Evaluator(wh)

    # print(eval.path_above_block(x_origin, y_origin, y_len))
    # print(eval.path_below_block(x_end, y_origin, y_len))
    # print(eval.path_on_left_from_block(x_origin, y_origin, x_len))
    # print(eval.path_on_right_from_block(x_origin, y_end, x_len))
    # print(eval.has_access_to_path(0))
