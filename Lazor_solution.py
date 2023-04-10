#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import random

class Game:

    '''
    The game class allows us to easily read in the information from the .bff files and to extract all useful and required
    information to solve the game state. This will tell us the grid state, what we have at our disposal, and the required
    locations that need to be met.
    '''

    def __init__(self, file):

        '''
        This function initializes the .bff file that we want to read.
        **Parameters**
            file : *str* 
                The name of file containing laser puzzle information for each level.
        '''
        self.fptr = open(file, 'r').read()


    def database(self):

        '''
        This function uses the activated .bff file and extracts out all the useful/required information to create our database.

        **Returns**
            grid : *list,list,str* 
                Nested list of strings that visualizes/contextualizes the base game state.
            laser_start : *list,tuple* 
                List of tuples containing the starting position of the laser(s).
            laser_path : *list,tuples* 
                List of tuples containing the direction of the laser(s).
            targets : *list,tuples* 
                List of tuples containing the position of the targets.
            blocks : *dict* 
                A dictionary with the types of blocks as keys and the number of blocks as values.
        '''
        # Setting up the empty set to establish the raw data taken from the activated file
        all_input_data = self.fptr.split('\n')
        raw_data = []
            
        for line in all_input_data:
            if '#' not in line and line != '':
                raw_data.append(line)
        
        # Needing to set the two variables for the grid start and stop locations to avoid any variable issues
        grid_start = None
        grid_stop = None

        # Searching through the dataset and taking the current position and setting our variable to this value
        # This allows us to itterate through the data between these two points in the future to collect our grid
        for i, line in enumerate(raw_data):
            if line == 'GRID START':
                grid_start = i
            elif line == 'GRID STOP':
                grid_stop = i
            if grid_start is not None and grid_stop is not None:
                break

        # Grid raw being set to the previously set range for grid start and grid stop
        grid_raw = raw_data[grid_start+1:grid_stop]

        self.grid = []
        
        
        # Appending this data information to the grid within the class and removing the unnecessary information if added
        # We ignore ' ' characters to make sure that the final grid is only the map of the puzzle
        for row in grid_raw:
            row_list = [char for char in list(row.strip()) if char != ' '] 
            self.grid.append(row_list)

        for line in reversed(grid_raw):
            if line in raw_data:
                raw_data.remove(line)

        # Establishing the origin and the direction of the laser to be used in future locations
        # We need this data to be able to solve the puzzles
        self.laser_start=[]
        self.laser_path=[]

        # Extracting the data and appending the tuple to our empty set
        # We search for the section of the .bff that includes information about laser 'L'
        # Depending on the length, we can know if it's the origin or the direction
        for line in raw_data:
            laser_direction = []
            laser_origin = []
            if 'L' in line:
                line = line.lstrip("L").split()
                if len(line) == 4 :
                    for i in range(len(line)):
                        if i < 2 :
                            laser_origin.append(int(line[i]))
                        else :
                            laser_direction.append(int(line[i]))
                    self.laser_start.append(tuple(laser_origin))
                    self.laser_path.append(tuple(laser_direction))
                else :
                    print("Encountering error!")


        # Establishing the targets to be used in future locations
        self.targets = []

        # Extracting the data related to the required points that the laser must cross through in solution
        # Looking for the part of the .bff file that includes 'P' referring to the points
        # We want the expected length of the tuples to get the coordinates, otherwise it's some sort of problem
        for line in raw_data:
            points_set = []
            if line.startswith('P') == True:
                line = line.lstrip("P").split()
                if len(line) == 2:
                    for i in range(len(line)):
                        points_set.append(int(line[i]))
                    self.targets.append(tuple(points_set))
                else :
                    print("Encountering error!")

        # Establishing a dictionary to include the information about inventory of blocks
        # This is honestly the easiest out of the information because the blocks are labeled by their letters
        self.blocks = {}

        # We search the .bff file for information about each letter and include that integer available in our inventory dictionary
        # Otherwise, they are set to 0 to not run in to any confusion
        for line in raw_data:
            if line[0] in ['A', 'B', 'C']:
                key, value = line.strip().split()
                self.blocks[key] = int(value)
        if 'A' not in self.blocks:
            self.blocks['A'] = 0
        if 'B' not in self.blocks:
            self.blocks['B'] = 0
        if 'C' not in self.blocks:
            self.blocks['C'] = 0    
        
    def print_game_state(self):
        
        '''
        This function can be used to print the current game state with all the available information.
        This is exclusively used a visual representation to see that the game file has been inputted properly into the code
        and the data is being read correctly.
        '''
        print("Current game state:")
        print("Grid:")
        for row in self.grid:
            print(' '.join(row))
        print("Laser start positions: {}".format(self.laser_start))
        print("Laser paths: {}".format(self.laser_path))
        print("Targets: {}".format(self.targets))
        print("Blocks: {}".format(self.blocks))        

class Board:

    '''
    The board class allows for random variations of the current board state to be produced while also having two distinct
    board types. One board that is used as an actual representation that is similar to what is given to us, and a second board
    of larger scale that can be used to see where the laser passes through since it would be happening in between 
    the other grid. This board class takes information from the game class to complete a lot of useful tasks and is what ultimately
    allows for board states to be randomly tested (with different blocks and outcomes).
    '''

    def __init__(self,grid,origin,path,sets):
        
        '''
        This function initializes the information taken from the game glass to establish a board state. 
        ** Parameters**
            grid: *list,list,str*
                Nested list of strings that visualizes/contextualizes the base game state.
            origin: *list,tuple* 
                List of tuples containing the starting position of the laser(s).
            path: *list,tuples* 
                List of tuples containing the direction of the laser(s)
            sets: *dict* 
                A dictionary with the types of blocks as keys and the number of blocks as values.
        '''
        self.grid = grid
        self.origin = origin
        self.path = path
        self.sets = sets


    def sample_function(self, grid):
        '''
        The sample function generates a list of all available positions to be able to place blocks down at.
        **Parameters**
            grid : *list,list,str*
                Nested list of strings that visualizes/contextualizes the base game state.
        **Returns**
            sample_space : *list,tuple*
                A list of tuples indicating the locations where inventory of blocks can be placed.
        '''

        # Setting an empty variable to not run in to any variable setting issues
        sample_space = []

        # Whatever the coordinates are within the grid, we look at open spot 'o' and say that it is an available spot
        # We then add that coordinate to our list to be able to use it later
        sample_space = [(i,j) for j in range(len(grid)) for i in range(len(grid[0])) if grid[j][i] == 'o']
        return sample_space

    def sample_board(self, sample_space, blocks, grid):

        '''
        The sample_board function generates a single permutation of how a set of 
        given blocks can be arranged on the game grid
        **Parameters**
            sample_space: *list,tuple* 
                A list of tuples indicating the locations where inventory of blocks can be placed. 
            blocks: * dict* 
                A dictionary with the types of blocks as keys and the number of blocks as values.
            grid: *list,list,str*
                Nested list of strings that visualizes/contextualizes the base game state.
        **Returns**
            grid: *list,list,str*
                Nested list of strings that visualizes/contextualizes a state of the game with added inventory blocks.
        '''

        # Obtaining the number of total blocks to sum and then select a random sample from this number to place on sample space
        # We want to place our inventory of blocks in a random way on board state
        block_counts = {'A': blocks['A'], 'B': blocks['B'], 'C': blocks['C']}
        options = random.sample(sample_space, sum(block_counts.values()))

        # We look at the options available at if we have a block type, we can place it
        # Place blocks until we are fully out of blocks and then break out of it
        for element in options:
            (i,j) = element
            for block_type in ['C', 'B', 'A']:
                if block_counts[block_type] > 0:
                    grid[j][i] = block_type
                    block_counts[block_type] -= 1
                    break
            else:
                print("Error: No available blocks.")
                break

        return grid

    def make_board(self,grid):
        
        '''
        We want to make the board into a mesh grid that allows for the laser to actually pass through relevant points.
        Looking at the board state normal grid for where to place blocks is great, but the laser needs to be able to pass
        through half way points to be able to hit the target goals. We can do this by creating a grid that has lines of open 
        spaces on either side of our actual normal lines (effectively doubling and making our grid space odd).
        **Parameters**
            grid: *list, list, str*
                Nested list of strings that visualizes/contextualizes the game state.
        **Returns**
            meshgrid: *list, list, str*
                Nested list of strings that visualizes/contextualizes the laser board state better.
        '''
        # We need to create a new nested list of strings that is doubled the size + 1
        # This math effectively does what is described in the description of this function
        # We loop through each list and then create the additional space
        meshgrid = [['o' for i in range(2*len(grid[0])+1)] for j in range(2*len(grid)+1)]
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                meshgrid[2*i+1][2*j+1] = grid[i][j]
        return meshgrid
    

class Blocks:

    '''
    The blocks class establishes the properties of the three different block types. We want some of them to reflect, some
    of them to transmit, or to do neither depending on which of the three blocks we are dealing with.
    '''
    def __init__(self,x,y):
        '''
        This function initializes the location of the block type with x and y coordinates. 
        ** Parameters**
            x: *int*
                The row position within the nested lists.
            y: *int* 
                The column position within the nested lists.
        '''
        self.x = x
        self.y = y

    def prop(self, meshgrid):
        '''
        This function specifies the 'reflect' and 'transmit' properties as booleans
        **Parameter**
            meshgrid: *list, list, str*
                Nested list of strings that visualizes/contextualizes the laser board state better.
        **Returns**
            self.reflect: *boolean*
                Ability to reflect the laser or not based on the location on the board
            self.transmit: *boolean*
                Ability to transmit the laser or not based on the location on the board
        '''
        # Checks to see which block type we are dealing with by looking at the letter
        # Then we give it the appropriate qualities.
        if meshgrid[self.y][self.x] == 'A':
            self.reflect = True
            self.transmit = False
        elif meshgrid[self.y][self.x] == 'B':
            self.reflect = False
            self.transmit = False
        elif meshgrid[self.y][self.x] == 'C':
            self.reflect = True
            self.transmit = True
        else:
            self.reflect = False
            self.transmit = True
        return self.reflect, self.transmit


class Laser:

    '''
    The laser class estblishes the properties of the laser including what direction the lasers are going, the starting locations
    of any of the lasers, and looking at what happens to it when we update it as we go with changing the locations of blocks
    on the state of the board. We need to be able to understand how different blocks effect the laser's properties and then
    update that within it.
    '''

    def __init__(self, start_point, path):
        
        '''
        This function initializes the starting location and the direction of the laser(s). 
        ** Parameters**
            start_point: *list,tuple*
                List of tuples containing the starting position of the laser(s).
            path: *list,tuples* 
                List of tuples containing the direction of the laser(s).
        '''
        self.source = start_point
        self.direction = path


    def laser_prediction(self, path, intercepts, grid, meshgrid, path_1, intercept_new):
        
        '''
        The laser prediction function attempts to see where the laser intersects with the new board state with the different
        blocks and then setting those. We will later use this information to predict where the laser is going for future 
        prediction techniques.
        **Parameters**
            path: *list,tuples* 
                List of tuples containing the direction of the laser(s).
            intercepts: *list,tuples* 
                List of tuples containing the positions the laser intercepts after any interactions with blocks
            grid: *list,list,str*
                Nested list of strings that visualizes/contextualizes the base game state.
            meshgrid: *list, list, str*
                Nested list of strings that visualizes/contextualizes the laser board state better.
            path_1: *list,tuples* 
                List of tuples containing the direction of the laser(s) after any changes.
        **Returns**
            path: *list,tuples* 
                List of tuples containing the direction of the laser(s).
            intercepts: *list,tuples* 
                List of tuples containing the positions the laser intercepts after any interactions with blocks
            path_1: *list,tuples* 
                List of tuples containing the direction of the laser(s) after any changes.
            intercept_new: *list,tuples* 
                List of tuples containing the positions the laser intercepts after any interactions with blocks.
        '''
        # Setting up all the necessary variables and empty lists to be able to set information accessibly later
        # We want to colect the direction and the starting position of the lasers
        # We also want to set variables for the max boundaries of the grid so we can ensure we are within the puzzle scheme
        nearby_list = []
        transition_list = []
        (path_x, path_y) = path[-1]
        (int_x, int_y) = intercepts[-1]
        n_direct = [(0, 1),(0, -1),(-1, 0),(1, 0)]
        x_max = 2 * len(grid[0]) + 1
        y_max = 2 * len(grid) + 1

        # Can simplify the return feature if we know we are at 0,0 within the puzzle scheme
        if (path_x, path_y) == (0, 0):
            return path, intercepts, path_1, intercept_new

        # Loop to unpack the maximum values for ex and ey to know where the laser is going
        for dx, dy in n_direct:
            ex, ey = int_x + dx, int_y + dy

            # Quick check to ensure we are within the range we want to be in
            if 0 < ex < x_max and 0 < ey < y_max:
                delta_x = ex - int_x
                delta_y = ey - int_y

                # If we run into a reflect block, we want to reflect the laser
                # We are checking if the meshgrid is an A just to show there would be other ways to check the block properties
                if meshgrid[ey][ex] == 'A':
                    new_path_x = path_x * (1 if delta_x == 0 else -1)
                    new_path_y = path_y * (1 if delta_y == 0 else -1)
                    nearby_list.append((new_path_x, new_path_y))

                # Now we are using the Blocks class and checking if it has False, False for the reflection and transmitting properties
                # It needs to check where it is on the board and then correctly update to where the next location will be
                elif Blocks(ex,ey).prop(meshgrid) == (False,False):
                    if delta_x == path_x or delta_y == path_y:
                        new_path_x, new_path_y = path_x, path_y
                    else:
                        new_path_x, new_path_y = path_x * 1, path_y * 1
                    nearby_list.append((new_path_x, new_path_y))

                # Now we are using the Blocks class and checking if it has True, True for the reflection and transmitting properties
                # It needs to check where it is on the board and then correctly update to where the next location will be
                elif Blocks(ex,ey).prop(meshgrid) == (True,True):
                    if delta_x == path_x or delta_y == path_y:
                        new_path_x = path_x * (1 if delta_x == 0 else -1)
                        new_path_y = path_y * (1 if delta_y == 0 else -1)
                        old_path_x, old_path_y = path_x, path_y
                        transition_list.append((old_path_x, old_path_y))
                        nearby_list.append((new_path_x, new_path_y))
                    else:
                        new_path_x, new_path_y = path_x * 1, path_y * 1
                        nearby_list.append((new_path_x, new_path_y))

        # Depending on what list we have added to, we want to append to the list for the new intercepted points
        # We do this for both coordinates as path and intercepts is useful/required information
        if nearby_list:
            path.append(nearby_list[-1])
        else:
            path.append((path_x, path_y))

        if transition_list:
            path_1.append(transition_list[-1])
            intercept_new.append((int_x, int_y))

        int_x += path[-1][0]
        int_y += path[-1][1]
        intercepts.append((int_x, int_y))

        return path, intercepts, path_1, intercept_new


    def trajectory(self, path, grid, meshgrid):
        
        '''
        The trajectory function attempts to predict the trajectory of the laser using the laser_prediction function for
        additional information.
        **Parameters**
            path: *list,tuples* 
                List of tuples containing the direction of the laser(s).
            grid: *list,list,str*
                Nested list of strings that visualizes/contextualizes the base game state.
            meshgrid: *list, list, str*
                Nested list of strings that visualizes/contextualizes the laser board state better.
        **Returns**
            final_intercept_list: *list,tuples*
                List of tuples containing the final positions the laser intercepts after any interactions with blocks.
            path: *list,tuples* 
                List of tuples containing the direction of the laser(s).
            intercept_new : *list,tuples* 
                List of tuples containing the positions the laser intercepts after any interactions with blocks.
        '''
        # Setting the variables to be able to see the intercepted points and the path of the laser
        # We want to take the source and direction from the initialization step and append to these variables
        intercepts = []
        path = []
        for i in range(len(self.source)):
            intercepts.append([self.source[i]])
            path.append([self.direction[i]])

        # Now, we want to update these with the changes that we get from placing things on the grid and updating the effect
        # it has on the laser_prediction function which is extremely useful for finding a possible solution
        path_1 = []
        intercept_new = []
        
        # We will loop through the length of our path and see what changes occur with blocks in the path or not
        for k in range(len(path)) :
            
            # If one of the intercepts is nearby a block, we want it to be able to change directions as intended
            # This is good to check initially as it influences the rest of the program
            if len(intercepts[k]) == 1:
                path[k], intercepts[k], path_1, intercept_new = self.laser_prediction(path[k], intercepts[k], grid, meshgrid, path_1, intercept_new)

            # Once we get past the start, we want to continue this trend until we reach the bounds of our puzzle
            # The bounds of the puzzle will indicate we can stop going
            while intercepts[k][-1][0] != 0 and intercepts[k][-1][0] < len(meshgrid[0])-1 and intercepts[k][-1][1] != 0 and intercepts[k][-1][1] < len(meshgrid)-1:
                if path[k][-1] != (0,0):
                    path[k], intercepts[k], path_1, intercept_new = self.laser_prediction(path[k], intercepts[k], grid, meshgrid, path_1, intercept_new)
                else:
                    break
                    
            # This check is what is going to be breaking the laser path into multiple in the situation that it runs into a
            # block that splits it. This will be important to find solutions as most of the time we will likely need to do this
            if len(path_1) != 0:
                path_0 = []
                intercept_0 = []
                (dx,dy) = path_1[-1]
                (cx, cy) = intercept_new[-1]
                nx = cx + dx
                ny = cy + dy
                intercept_new.append((nx,ny))
                while intercept_new[-1][0] != 0 and intercept_new[-1][0] < len(meshgrid[0])-1 and intercept_new[-1][1] != 0 and intercept_new[-1][1] < len(meshgrid)-1:
                    if path_1[-1] != (0,0):
                        path_1, intercept_new, path_0, intercept_0 = self.laser_prediction(path_1, intercept_new, grid, meshgrid, path_0, intercept_0)
                    else:
                        break
                        
        # Now that we are out of the path, we want to return to a final intercept list that isn't double counting
        # as we have multiple paths now possibly and don't want to be multi-counting them
        final_intercept_list = []
        for sublist in intercepts:
            for item in sublist:
                final_intercept_list.append(item)
        return final_intercept_list, path, intercept_new

    
def puzzle_generator(mesh):
    
    '''
    The puzzle generator function inputs the solution mesh grid and outputs a readable .bff readable in a similar format
    to the one that we are given. It's easy enough to read to easily see if a solution has been given!
    **Parameters**
        mesh: *list, list, str*
            Nested list of strings that visualizes/contextualizes the final laser board state including positions 
            of blocks, and the points the laser passes.
    **Output**
        solution.bff: *file*
            A .bff file that contains the solution to the puzzle in a similar format to the given .bff files.
    '''
    # We want to set our solution set to nothing so we can fill it up with the actual solution
    # We also set the the width to get the solution to be the correct size of the board we want
    # Then we just write the solution into the file by writing it in
    # And then close up shop, and get out of the file type
    solution = []
    for j in range(1,len(mesh),2):
        for i in range(1, len(mesh[0]),2):
            solution.append(mesh[j][i])
    width = int((len(mesh[0])-1)/2)
    solution = [solution[x:x+width] for x in range(0, len(solution), width)]
    file = open('solution.bff', 'w')
    for i in solution:
        for j in i:
            file.write(j)
            file.write('\t')
        file.write('\n')
    file.close()
    print("Solution found!")
    
def final_solution_generator(puzzle, maxiter=50000):

    '''
    The final solution generator function is what we want to run to actually find the solution for the puzzle and then
    generate the solution file using the puzzle_generator function. This is where we can also set max iterations of the code
    to not let it run for that long.
    **Parameters**
        puzzle: *str*
            The puzzle file that will we are trying to find a solution for.
        maxiter: *int*
            The longest allowed of iteration steps we are willing to wait before breaking out of the code. A found solution
            will premptively break it out of the loop anyway.
    **Output**
        solution.bff: *file*
            A .bff file that contains the solution to the puzzle in a similar format to the given .bff files.
    '''
    # We want to loop through until we find a solution using the number of iterations we have previously allowed
    # Then we activate all of our classes to get all the required information that will be used by puzzle_generator
    # We specifically need to set the target points as part of the final set
    # This is what we are checking as if we can hit every target point within a current run by looking at the 
    # intercept_new list, then we have 'accidentally' found a solution and can break out of the loop
    # It's honestly a pretty cool way of doing this, even though it's extremely basic
    for i in range(maxiter):
        G = Game(puzzle)
        G.database()
        B = Board(G.grid,G.laser_start, G.laser_path,G.targets)
        mesh_board = B.sample_board(B.sample_function(G.grid), G.blocks, G.grid)
        mesh = B.make_board(mesh_board)
        L = Laser(G.laser_start,G.laser_path)
        intcp, pth, intercept_new = L.trajectory(G.laser_path,G.grid, mesh)
        final_set = G.targets
        total_intcp = intcp + list(intercept_new)
        if all(x in total_intcp for x in final_set):
            puzzle_generator(mesh)
            break
    if not all(x in total_intcp for x in final_set) == True:
        print('No solution found within range of iterations.')
        

if __name__ == '__main__':
    # Can test whichever of the test cases that needs to be tested
    final_solution_generator('mad_1.bff', 500000)
    #final_solution_generator('mad_4.bff', 500000)
    #final_solution_generator('mad_7.bff', 500000)
    #final_solution_generator('dark_1.bff', 500000)
    #final_solution_generator('numbered_6.bff', 500000)
    #final_solution_generator('showstopper_4.bff', 500000)
    #final_solution_generator('tiny_5.bff', 500000)
    #final_solution_generator('yarn_5.bff', 500000)

