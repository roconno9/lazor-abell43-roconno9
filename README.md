# Lazor Project for EN.540.635 at Johns Hopkins University
Contributors: Andrew Bell (abell43@jhu.edu) &amp; Ryan O'Connor (roconno9@jhu.edu)

### 1. Assignment Description
This code is meant to be able to automatically solve boards from the "Lazors" game found on Android and iPhone. This game has a large variety of boards that require the user to position additional blocks from their inventory to influence the path of a predetermined starting position laser through required intercept locations throughout the board space. To influence the laser, three block types are available in the game:
* Reflect = Bounces the laser off of it
* Opaque = Blocks the laser completely
* Refract = Bounces the laser off of it and passes the laser through it

With these tools, this project's code is meant to be able to read in boards using .bff files that give the starting layout of each level, the required intercept points, the inventory of blocks that are available to solve the level, and then solve! While the solution method is open to the student interpretation, some general rules that had to be followed are:
1.  You must read in the Lazor board via a text file with a specific format (.bff).
2.  You must use a class object to describe the blocks within the game.
3.  You must have an output file that shows the valid solution. Output file format is open to student selection, but must be easy to understand.
4.  The code should not be slow. Test boards (found in bff files folder) are expected to solved in less than 2 minutes each.
5.  Your boards should allow for all three types of blocks. You must also account for boards with fixed blocks as a starting position

The rest of the project code was up to students to figure out, and come up with possible solutions found fit based on their coding knowledge. This is only one possible solution to the Lazors game problem.

### 2. Solution Methodology
The input file (.bff) must be read by the code to extract all useful information. The starting layout of the board is the first requirement with the board being found between "GRID START" and "GRID STOP" with the characters correlating to the type by:
* x = no block allowed
* o = blocks allowed
* A = fixed reflect block
* B = fixed opaque block
* C = fixed refract block

Then the inventory of blocks that are able to be used, the laser positions, and the required intercept locations with the characters correlating as:
* A then the number of available of Reflect Blocks (if none available .bff file with not contain an 'A')
* B then the number of available of Opaque Blocks (if none available .bff file with not contain an 'B')
* C then the number of available of Refract Blocks (if none available .bff file with not contain an 'C')
* L then the traits for the lasers (can have multiple)
* P then the locatios for the points that must be intercepted (can have multiple)

The Lazors solver will place the available blocks and check to see how that influences the board state until a correct solution is found.

### 3. Code Functioning
To run the code, you can simply change the final_solution_generator function where the puzzle file name is located.
