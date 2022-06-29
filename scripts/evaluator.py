from warehouse import Warehouse
import copy

PATH_WIDTH = 1
FREE_CELL_VALUE = -1
UNAVAILABLE_AREA_VALUE = -2

class Evaluator():

    """ 
        The class evaluates the sum score for provided warehouse configuration.

        The evaluator applies a penalty(defined during class construction) to 
        profit from the block.
    """
    def __init__(self, penalty = 2):
        self.penalty = penalty 

    def calculate_profit(self, warehouse: Warehouse):
        profit = 0
        self.warehouse = warehouse
        for block_index in warehouse.blocks_in_warehouse:
            block_profit = self._calculate_block_area(block_index)

            if(not self.has_access_to_path(block_index)):
                #applying penalty
                block_profit = block_profit/self.penalty
            profit += block_profit

        return profit

    def has_access_to_path(self, block_index):
        current_block = self.warehouse.blocks_dict[block_index]
        # assert(current_block.is_position_set())
        x_origin = current_block.x_origin
        y_origin = current_block.y_origin
        x_len = current_block.x_length
        y_len = current_block.y_length
        x_end = x_origin + x_len -1
        y_end = y_origin + y_len -1

        return (self._is_path_above_block(x_origin, y_origin, y_len) or
                self._is_path_below_block(x_end, y_origin, y_len) or
                self._is_path_on_left_from_block(x_origin, y_origin, x_len) or
                self._is_path_on_right_from_block(x_origin, y_end, x_len)) 

    def is_path(self, goal_x, goal_y, x_door = 0, y_door = 0) :
        
        """ 
            Path finding algorithm in 2D array. 

            x_door and y_door are coordinates of the beginning of the path.

            ---
            References:
            < https://www.geeksforgeeks.org/check-possible-path-2d-matrix/ >
        """

        CELL_VISITED = 1
        warehouse_representation_matrix = copy.deepcopy(self.warehouse.warehouse_matrix)
        # possible directions of the next element of path 
        directions = [ [0, 1], [0, -1], [1, 0], [-1, 0]]
        # queue
        q = []

        if(warehouse_representation_matrix[x_door][y_door] > FREE_CELL_VALUE):
            return False
        # insert the top right corner.
        q.append((x_door, y_door))
        
        # until queue is empty
        while(len(q) > 0) :
            p = q[0]
            q.pop(0)
            
            # mark as visited
            warehouse_representation_matrix[p[0]][p[1]] = CELL_VISITED
            
            # destination is reached.
            if(p == (goal_x , goal_y )) :
                return True
                
            # check all four directions
            for i in range(4) :
            
                # using the direction array
                a = p[0] + directions[i][0]
                b = p[1] + directions[i][1]
                
                # not blocked and valid
                if(a >= 0 and b >= 0 and a <= goal_x and b <= goal_y and
                    warehouse_representation_matrix[a][b]  == FREE_CELL_VALUE) :           
                    q.append((a, b))
        return False


    def _calculate_block_area(self, block_index):
        current_block = self.warehouse.blocks_dict[block_index]
        x_len = current_block.x_length
        y_len = current_block.y_length
        return x_len*y_len

    def _is_path_above_block(self, x_origin, y_origin, y_len):
        return (self._is_space_above_block(x_origin, y_origin, y_len) and
        self.is_path(x_origin - PATH_WIDTH, y_origin))
    
    def _is_path_below_block(self, x_end, y_origin, y_len):
        return (self._is_space_below_block(x_end, y_origin, y_len) and 
        self.is_path(x_end + PATH_WIDTH, y_origin))

    def _is_path_on_left_from_block(self, x_origin, y_origin, x_len):
        return(self._is_space_on_left_from_block(x_origin, y_origin, x_len) and
        self.is_path(x_origin, y_origin - PATH_WIDTH))
    
    def _is_path_on_right_from_block(self, x_origin, y_end, x_len):
        return(self._is_space_on_right_from_block(x_origin, y_end, x_len) and
        self.is_path(x_origin, y_end + PATH_WIDTH))

    def _is_space_above_block(self, x_origin, y_origin, y_len):
        return self.warehouse.is_spot_available(x_origin - PATH_WIDTH,
             y_origin, PATH_WIDTH, y_len)

    def _is_space_below_block(self, x_end, y_origin, y_len):
        return self.warehouse.is_spot_available(x_end + PATH_WIDTH,
             y_origin, PATH_WIDTH, y_len)

    def _is_space_on_left_from_block(self, x_origin, y_origin, x_len):
        return self.warehouse.is_spot_available(x_origin, 
            y_origin - PATH_WIDTH, x_len, PATH_WIDTH)

    def _is_space_on_right_from_block(self, x_origin, y_end, x_len):
        return self.warehouse.is_spot_available(x_origin, 
            y_end + PATH_WIDTH, x_len, PATH_WIDTH)





        


