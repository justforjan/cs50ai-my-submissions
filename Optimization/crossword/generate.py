import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """

        for word in self.crossword.words:
            for var in self.domains:
                if len(word) != var.length:
                    self.domains[var].remove(word)
        

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        
        overlapping = self.crossword.overlaps[x, y]

        revised = False
        
        for word_in_x in self.domains[x].copy():
            corresponds = False
            for word_in_y in self.domains[y]:
                if word_in_x[overlapping[0]] == word_in_y[overlapping[1]]:
                    corresponds = True
                    break
            
            if not corresponds:
                self.domains[x].remove(word_in_x)
                revised = True

        return revised
        

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """

        if arcs == None:
            queue = set([overlap for overlap in self.crossword.overlaps if self.crossword.overlaps[overlap] is not None])
        else:
            queue = arcs

        while len(queue) > 0:
            arc = queue.pop()
            if self.revise(arc[0], arc[1]):
                if len(self.domains[arc[0]]) == 0:
                    return False
                neighbors = self.crossword.neighbors(arc[0])
                for neighbor in neighbors:
                    queue.add((neighbor, arc[0]))
            
        
        return True
                
    
    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """

        assignments = list(assignment.keys()) # List of all keys in the assigment dict

        for var in self.domains:
            if var not in assignments:
                return False
            if assignment[var] is None:
                return False
            
        return True
    

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.

        - words fit in crossword
        - all words are distinct
        - no conflicting words

        """

        # Check distinct values
        assigned_values = [assignment[value] for value in assignment if assignment[value] is not None]
        if len(assigned_values) is not len(set(assigned_values)):
            return False
        

        # Check word length
        for var in assignment:
            # Make sure variables has already been assigned a word
            if assignment[var] is None:
                continue
            if len(assignment[var]) is not var.length:
                return False

        # Check overlapping letters
        assignments = list(assignment.keys()) # List of all keys in the assigment dict

        for overlap in self.crossword.overlaps:

            # if no overlap, skip
            if self.crossword.overlaps[overlap] is None:
                continue

            # variables
            v1 = overlap[0]
            v2 = overlap[1]

            # if on of the variables has not been assigned a value yet, skip
            # if assignment[v1] == None or assignment[v2] == None:
            #     continue
            if v1 not in assignments or v2 not in assignments:
                continue

            # now we need to check if v1 and v2 are consistent

            # overlapping letter
            i = self.crossword.overlaps[overlap][0] # ith letter of v1
            j = self.crossword.overlaps[overlap][1] # jth letter of v2

            if assignment[v1][i] is not assignment[v2][j]:
                return False
                    
        return True


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """


        potential_words = list(self.domains[var])

        assignments = list(assignment.keys()) # List of all keys in the assigment dict
        unassigned_vars = set([var for var in self.domains if var not in assignments])
        neighbors = self.crossword.neighbors(var)

        neighboring_unassigned_vars = unassigned_vars.intersection(neighbors)

        if neighboring_unassigned_vars == set():
            return list(self.domains[var])

        number_of_outruled_words = dict()
        

        for neighbor in neighboring_unassigned_vars:
            # get overlapping letters
            i_word = self.crossword.overlaps[var, neighbor][0]
            j_neighbor = self.crossword.overlaps[var, neighbor][1]


            for word in self.domains[var]:
                # initiate value at 0
                number_of_outruled_words[word] = 0


                for neighbor_word in self.domains[neighbor]:
                    if word[i_word] != neighbor_word[j_neighbor]:
                        number_of_outruled_words[word] += 1
        
        potential_words[:] = sorted(number_of_outruled_words, key=lambda x:number_of_outruled_words[x])

        return potential_words
    


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        # List of all unassigned variables
        unassigned_vars = [var for var in self.domains if var not in assignment]

        # Minimum domain length of unassigned variables
        min_domain_length = min([len(self.domains[var]) for var in unassigned_vars])

        # List of vars whose domain length equals the minimum domain length
        vars_with_smallest_domain = [var for var in unassigned_vars if len(self.domains[var]) == min_domain_length]

        # If only one item in list, return the item
        if len(vars_with_smallest_domain) == 1:
            return vars_with_smallest_domain[0]
        
        if len(vars_with_smallest_domain) == 0:
            raise Exception
        
        # Calculate maximum degree among left variables
        max_degree = max([len(self.crossword.neighbors(var)) for var in vars_with_smallest_domain])

        # List of variables with highest degree (most neighbors)
        var_with_highest_degree = [var for var in vars_with_smallest_domain if len(self.crossword.neighbors(var)) == max_degree]

        # Return any item
        return var_with_highest_degree[0]
        

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        '''
        function BACKTRACK(assignment, csp):
            if assignment complete: 
                return assignment
            var = SELECT-UNASSIGNED-VAR(assignment, csp)
            for value in DOMAIN-VALUES(var, assignment, csp):
                if value consistent with assignment:
                    add {var = value} to assignment
                    result = BACKTRACK(assignment, csp)
                    if result ≠ failure: 
                        return result
                remove {var = value} from assignment
            return failure
        '''


        if self.assignment_complete(assignment):
            return assignment
        
        var = self.select_unassigned_variable(assignment)
        
        for word in self.order_domain_values(var, assignment):

            assignment[var] = word

            # print(assignment)

            if self.consistent(assignment):
                # print("assignment successful")

                result = self.backtrack(assignment)

                if result:
                    return assignment

                # if self.consistent(result):
                #     return result
            
            assignment.pop(var)
            # print("assignment unsuccessful")
        
        return None

        

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
