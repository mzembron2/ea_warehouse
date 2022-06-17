import numpy as np
import copy

list_of_grids= []
max_num = 1
grid = []
containers = []

def isPath(matrix, goal, i=0, j=0):
    n= len(matrix)
    visited = [[False for x in range (n)]
                      for y in range (n)]
    
    if (matrix[i][j] == 0 and not visited[i][j]):
        if (checkPath(matrix, i,j, visited, goal)):
            return True
    return False
 
def isSafe(i, j, matrix):
   
    if (i >= 0 and i < len(matrix) and
        j >= 0 and j < len(matrix[0])):
        return True
    return False
 
def checkPath(matrix, i, j, visited, goal):

    if (isSafe(i, j, matrix) and (matrix[i][j] ==0 or matrix[i][j] ==goal) and not visited[i][j]):
        visited[i][j] = True

        if (matrix[i][j] == goal):
            return True

        up = checkPath(matrix, i - 1,j, visited, goal)
        if (up):
            return True

        left = checkPath(matrix, i,j - 1, visited, goal)
        if (left):
            return True
 
        down = checkPath(matrix, i + 1, j, visited, goal)
        if (down):
            return True
 
        right = checkPath(matrix, i,j + 1, visited, goal)
        if (right):
            return True     
    return False

def checkContainerList(grid, x=0, y=0):
    list= getContainerList(grid)
    for l in list:
        if isPath(grid, l, x, y):
            continue
        else:
            return False
    return True

def placeContainer(grid, y, x, y_len, x_len):
    n= len(grid)
    if x+x_len> n or y+y_len> n:
        return False
    
    for i in range(y_len):
        for j in range(x_len):
            if grid[y+i][x+j]!=0:
                return False          
    return True

def placeContainer2(grid, y, x, y_len, x_len):
    #version with empty space around
    n= len(grid)
    if x+x_len> n or y+y_len> n:
        return False
    
    for i in range(y_len):
        for j in range(x_len):
            if grid[y+i][x+j]!=0:
                return False     
            
    flag= True
    if x+x_len+1 < n:
        for i in range(y_len):
            if grid[y+i][x+x_len+1]!=0:
                    flag = False 
    if x-1 >= 0:
        for i in range(y_len):
            if grid[y+i][x-1]!=0:
                    flag = False  
    if y-1 >= 0:
        for i in range(x_len):
            if grid[y-1][x+i]!=0:
                    flag = False  
    if y+y_len+1 < n:
        for i in range(x_len):
            if grid[y+y_len+1][x+i]!=0:
                    flag = False
    return flag

def getOccupiedArea(grid):
    num= 0
    forbidden = [0, -1]
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] not in forbidden:
                num= num +1
    return num

def getContainerList(grid):
    list= []
    forbidden = [0, -1]
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] not in forbidden:
                if grid[i][j] not in list:
                    list.append(grid[i][j])
    return list

def solve():
    global grid, list_of_grids, max_num
    global containers
    
    for y in range(len(grid)):
        for x in range(len(grid)):
            if grid[y][x]==0:
                for n in range(len(containers)):
                    if (n+1 not in getContainerList(grid)):
                        x_len = containers[n][0]
                        y_len = containers[n][1]
                        if placeContainer2(grid, y, x, y_len, x_len):
                            for i in range(y_len):
                                for j in range(x_len):
                                    grid[y+i][x+j]=n+1
                            if(checkContainerList(grid, len(grid)-1, len(grid)-1)):
                                solve()
                            for i in range(y_len):
                                for j in range(x_len):
                                    grid[y+i][x+j]=0
                        if (x_len!=y_len):
                            if placeContainer2(grid,y, x, x_len, y_len):
                                for i in range(x_len):
                                    for j in range(y_len):
                                        grid[y+i][x+j]=n+1
                                if(checkContainerList(grid, len(grid)-1, len(grid)-1)):
                                    solve()
                                for i in range(x_len):
                                    for j in range(y_len):
                                        grid[y+i][x+j]=0
#                 return
    
    if getOccupiedArea(grid)== max_num:
        list_of_grids.append(copy.deepcopy(grid))
    elif getOccupiedArea(grid)>max_num:
        max_num=getOccupiedArea(grid)
        list_of_grids= []
        list_of_grids.append(copy.deepcopy(grid))


if __name__ == "__main__":
       
    grid = [[0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]]
    # grid = [[0, 0, 0, 0],
    #         [0, 0, 0, 0],
    #         [0, 0, 0, 0],
    #         [0, 0, 0, 0]]
    # grid = [[0, 0, 0],
    #         [0, 0, 0],
    #         [0, 0, 0]]
    containers = [[1, 2], [3, 3], [3, 2], [2,2]]

    solve()
    print(max_num)
    for grid in list_of_grids:
        print(np.matrix(grid))