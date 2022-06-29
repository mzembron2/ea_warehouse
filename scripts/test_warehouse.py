from warehouse import Warehouse
from evaluator import Evaluator
import os

"""

script with unit tests  - run `pytest` in terminal (in scripts directory)

"""
DIRNAME = os.path.dirname(__file__)
FILENAME_BLOCKS_TEST = os.path.join(DIRNAME, '../data/blocks_test.csv')

def test_add_remove_block():
    wh = Warehouse(4,7)
    wh.get_blocks_from_csv(FILENAME_BLOCKS_TEST)
    blocks_number = len(wh.blocks_dict)
    TEST_BLOCK_INDEX = 0
    TEST_BLOCK_X_SIZE = wh.blocks_dict[0].x_length
    TEST_BLOCK_Y_SIZE = wh.blocks_dict[0].y_length
    assert(wh.is_spot_available(0,0,TEST_BLOCK_X_SIZE,TEST_BLOCK_Y_SIZE) == True)
    wh.place_block(0,0,0)
    assert(len(wh.blocks_in_warehouse) == 1)
    assert(len(wh.blocks_in_waiting_list) == blocks_number - 1)
    assert(wh.blocks_dict[0].x_origin == 0)
    assert(wh.blocks_dict[0].y_origin == 0)
    assert(wh.is_spot_available(0,0,2,2) == False)
    wh.remove_block(0)
    assert(len(wh.blocks_in_warehouse) == 0)
    assert(wh.blocks_dict[0].x_origin == None)
    assert(wh.blocks_dict[0].y_origin == None)

def test_evaluate_warehouse():
    wh = Warehouse(14,7)
    wh.get_blocks_from_csv(FILENAME_BLOCKS_TEST)
    
    wh.place_block(0,11,4)
    wh.place_block(1, 11, 3 )

    current_block = wh.blocks_dict[0]
    assert(current_block.is_position_set())
    x_origin = current_block.x_origin
    y_origin = current_block.y_origin
    x_len = current_block.x_length
    y_len = current_block.y_length
    x_end = x_origin + x_len -1
    y_end = y_origin + y_len -1

    eval = Evaluator()
    eval.warehouse = wh

    assert(eval._is_space_above_block(x_origin, y_origin, y_len))
    assert( not eval._is_space_below_block(x_end, y_origin, y_len))
    assert( not eval._is_space_on_left_from_block(x_origin, y_origin, x_len))
    assert( not eval._is_space_on_right_from_block(x_origin, y_end, x_len))
    assert(eval.has_access_to_path(0))


