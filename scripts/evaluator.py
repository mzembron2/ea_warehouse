from warehouse import Warehouse
import numpy as np
import copy

PATH_WIDTH = 1
FREE_CELL_VALUE = -1
UNAVAILABLE_AREA = -2

class Evaluator():
    def __init__(self, warehouse: Warehouse = None):
        self.warehouse = warehouse

    def calculate_profit(self, warehouse: Warehouse):
        profit = 0
        self.warehouse = warehouse
        for block_index in warehouse.blocks_in_warehouse:
            block_profit = self.calculate_block_area(block_index) 
            if(not self.has_access_to_path(block_index)):
                block_profit = block_profit/2
            profit += block_profit

        return profit

    def calculate_block_area(self, block_index):
        current_block = self.warehouse.blocks_dict[block_index]
        x_len = current_block.x_length
        y_len = current_block.y_length
        return x_len*y_len


    def has_access_to_path(self, block_index):
        current_block = self.warehouse.blocks_dict[block_index]
        assert(current_block.is_position_set())
        x_origin = current_block.x_origin
        y_origin = current_block.y_origin
        x_len = current_block.x_length
        y_len = current_block.y_length
        x_end = x_origin + x_len -1
        y_end = y_origin + y_len -1

        return (self.is_path_above_block(x_origin, y_origin, y_len) or
                self.is_path_below_block(x_end, y_origin, y_len) or
                self.is_path_on_left_from_block(x_origin, y_origin, x_len) or
                self.is_path_on_right_from_block(x_origin, y_end, x_len)) 

    def is_path_above_block(self, x_origin, y_origin, y_len):
        return (self.is_space_above_block(x_origin, y_origin, y_len) and
        self.is_path(x_origin - PATH_WIDTH, y_origin))
    
    def is_path_below_block(self, x_end, y_origin, y_len):
        return (self.is_space_below_block(x_end, y_origin, y_len) and 
        self.is_path(x_end + PATH_WIDTH, y_origin))

    def is_path_on_left_from_block(self, x_origin, y_origin, x_len):
        return(self.is_space_on_left_from_block(x_origin, y_origin, x_len) and
        self.is_path(x_origin, y_origin - PATH_WIDTH))
    
    def is_path_on_right_from_block(self, x_origin, y_end, x_len):
        return(self.is_space_on_right_from_block(x_origin, y_end, x_len) and
        self.is_path(x_origin, y_end + PATH_WIDTH))

    def is_space_above_block(self, x_origin, y_origin, y_len):
        return self.warehouse.is_spot_available(x_origin - PATH_WIDTH,
             y_origin, PATH_WIDTH, y_len)

    def is_space_below_block(self, x_end, y_origin, y_len):
        return self.warehouse.is_spot_available(x_end + PATH_WIDTH,
             y_origin, PATH_WIDTH, y_len)

    def is_space_on_left_from_block(self, x_origin, y_origin, x_len):
        return self.warehouse.is_spot_available(x_origin, 
            y_origin - PATH_WIDTH, x_len, PATH_WIDTH)

    def is_space_on_right_from_block(self, x_origin, y_end, x_len):
        return self.warehouse.is_spot_available(x_origin, 
            y_end + PATH_WIDTH, x_len, PATH_WIDTH)


    def is_path(self, goal_x, goal_y, x_door = 0, y_door = 0) :
        
        arr = copy.deepcopy(self.warehouse.warehouse_matrix)
        # directions
        directions = [ [0, 1], [0, -1], [1, 0], [-1, 0]]
        # queue
        q = []

        if(arr[x_door][y_door] > FREE_CELL_VALUE):
            return False
        # insert the top right corner.
        q.append((x_door, y_door))
        
        # until queue is empty
        while(len(q) > 0) :
            p = q[0]
            q.pop(0)
            
            # mark as visited
            arr[p[0]][p[1]] = 1
            
            # destination is reached.
            if(p == (goal_x , goal_y )) :
                return True
                
            # check all four directions
            for i in range(4) :
            
                # using the direction array
                a = p[0] + directions[i][0]
                b = p[1] + directions[i][1]
                
                # not blocked and valid
                if(a >= 0 and b >= 0 and a <= goal_x and b <= goal_y and arr[a][b]  == FREE_CELL_VALUE) :           
                    q.append((a, b))
        return False

    # def update_space(self):
    #     start_x = 0
    #     start_y = 0 
    #     (rows, columns) = np.shape(self.warehouse.warehouse_matrix)
    #     path_access_mask = np.full((rows, columns), False,dtype=bool)
    #     for row in rows:
    #         for col in columns:
    
    # def is_path(self, i=0, j=0):
    #     matrix = self.warehouse.warehouse_matrix
    #     (rows, columns) = np.shape(self.warehouse.warehouse_matrix)
    #     visited = np.full((rows, columns), False ,dtype=bool)
        
    #     if (matrix[i][j] == FREE_CELL_VALUE and not visited[i][j]):
    #         if (self.check_path(matrix, i,j, visited, FREE_CELL_VALUE)):
    #             return True
    #     return False
    
    # def is_safe(self,i, j, matrix):
    #     if (i >= 0 and i < len(matrix) and j >= 0 and j < len(matrix[0])):
    #         return True
    #     return False
    
    # def check_path(self, matrix, i, j, visited, goal):

    #     if (self.is_safe(i, j, matrix) and (matrix[i][j] ==FREE_CELL_VALUE or matrix[i][j] ==goal) and not visited[i][j]):
    #         visited[i][j] = True

    #         if (matrix[i][j] == goal):
    #             return True

    #         up = self.check_path(matrix, i - 1,j, visited, goal)
    #         left = self.check_path(matrix, i,j - 1, visited, goal)
    #         down = self.check_path(matrix, i + 1, j, visited, goal)
    #         right = self.check_path(matrix, i,j + 1, visited, goal)
    #         return up or left or down or right
        
    #     return False





        


