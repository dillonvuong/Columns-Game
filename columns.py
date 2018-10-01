# Dillon Vuong 82352779 ICS32 Project 5

NONE = [0,0]
Jewels = [1,2,3,4,5,6,7]

class ColumnsState:
    def __init__(self, rows: int, columns: int):
        self._columns = columns
        self._rows = rows
        self._board = None
        self._row_counter = 0
        self._column_position = 0 
        self._freeze_counter = -1
        self.Faller = None
        
    def columns(self) -> int:
        return self._columns

    def rows(self) -> int:
        return self._rows
    
    def board(self) -> [[str]]:
        return self._board
    
    def update(self,board:[[str]]) -> None:
        self._board = board
        self._columns = len(board)
        self._rows = len(board[0])

    def intialize_Faller(self, command:list):
        self.reset_counters()
        self.Faller = Faller(command)
        self.Faller.is_falling()
        self.falling(self.Faller)
        

    def falling(self, Faller: 'Faller Class') -> None:
        '''This function makes the Faller go down in the row if it is not blocked
           and also makes the Faller frozen if it has been landed for more than one turn.
        '''
        column = self._board[Faller.column() + self._column_position]
        Gems = Faller.faller()
        landed = self._landed(column,Faller,0)
        falling = Faller.falling
        Faller.change_coords(Faller.column()+ self._column_position,self._row_counter)
        
        if self._row_counter > 0:
            self._move_down_once(column)
        if self._row_counter == 0 and column[0] == NONE:
            column[0] = Gems[-1]
        elif self._row_counter == 1 and column[0] == NONE:
            column[0] = Gems[-2]    
        elif self._row_counter == 2 and column[0] == NONE:
            column[0] = Gems[-3]
        if falling:        
            self._row_counter += 1
            self._freeze_counter = -1
        if landed:
            self._freeze_counter += 1
            self._row_counter += 1
        self._frozen(Faller)
        if Faller.frozen:
            self.convert_matches_to_matched(self._board)
            
    def check_game_over(self,Faller) -> bool:
        'This function checks if the game is over.'
        if self._row_counter <= 3 and Faller.frozen:
            return True
        else:
            return False

    def rotate(self,Faller) -> None:
        'This function rotates the Faller in the board.'
        if not Faller.frozen:
            Faller.rotate()
            self._swap(Faller)
            
    def move_horizontally(self, command:str, Faller) -> None:
        'This function moves the Faller either left or right.'
        col = Faller.coordinate[0]
        row = Faller.coordinate[1]
        Gems = Faller.faller()
        board = self._board
        if not Faller.frozen:
            if command == '<':
                if board[col-1][row] == NONE and col-1 >= 0:
                    self._column_position -= 1
                    board[col-1][row] = Gems[2]
                    board[col][row] = NONE
                    if row > 0:
                        board[col-1][row-1] = Gems[1]
                        board[col][row-1] = NONE
                    if row > 1:
                        board[col-1][row-2] = Gems[0]
                        board[col][row-2] = NONE
                    Faller.change_coords(col-1,row)
                    if self._landed(self._board[col-1],Faller,1):
                        self._freeze_counter += 1
                    else:
                        Faller.is_falling()
                        self._freeze_counter = -1
                    
                else:
                    raise InvalidMoveError()

                    
            elif command == '>':
                if col+1 < self._columns:
                    if board[col+1][row] == NONE:
                        self._column_position += 1
                        board[col+1][row] = Gems[2]
                        board[col][row] = NONE
                        if row > 0:
                            board[col+1][row-1] = Gems[1]
                            board[col][row-1] = NONE
                        if row > 1:
                            board[col+1][row-2] = Gems[0]
                            board[col][row-2] = NONE
                        Faller.change_coords(col+1,row)
                        if self._landed(self._board[col+1],Faller,1):
                            self._freeze_counter += 1
                        else:
                            self._freeze_counter = -1
                    else:
                        raise InvalidMoveError()
                else:
                    raise InvalidMoveError()
            
            
    def _swap(self, Faller) -> None:
        'This functions swaps the position of the Faller and is used for rotation.'
        col = Faller.coordinate[0]
        row = Faller.coordinate[1]
        Gems = Faller.faller()
        board = self._board
        board[col][row] = Gems[2]
        if row > 0:
            board[col][row-1] = Gems[1]
        if row > 1:
            board[col][row-2] = Gems[0]
       

    def reset_counters(self) -> None:
        self._row_counter = 0
        self._counter2 = 1
        self._counter3 = 0
        self._freeze_counter = -1
        self._column_position = 0
        
    def _landed(self, column: list, Faller, delay: int) -> bool:
        'This function determines if the Faller is landed.'
        try:
            if not Faller.frozen:
                if column[self._row_counter+1-delay] != NONE:
                    Faller.is_landed()
                    return True
                else:
                    Faller.is_falling()
                    return False
            else:
                return False
        except IndexError:
            if not Faller.frozen:                    
                Faller.is_landed()
                return True
            else:
                return False
        
    def _frozen(self, Faller) -> bool:
        'This function determines if the Faller is frozen.'
        if self._freeze_counter > 0:
            Faller.is_frozen()
            return True
        else:
            return False

            
        
    def _move_down_once(self, column: list) -> list:
        'This function moves everything down in a column exactly one time.'
        for index in range(len(column)-2, -1, -1):
            if index != len(column)-1 and column[index] != NONE and column[index+1] == NONE:
                column[index+1] = column[index]
                column[index] = NONE
        return column

        
    def empty_game_board(self) -> [[str]]:
        'This function creates an empty game board.'
        board = []
        for col in range(self._columns):
            board.append([])
            for row in range(self._rows):
                board[-1].append(NONE)
        return board
    def transpose(self, state: '2D list') -> [[str]]:
        'This functions swaps the rows and columns in a 2D list.'
        counter = 0
        c = []
        for col in range(len(state[0])): 
            r = [] 
            for row in state:
                r.append(row[counter])
            c.append(r)
            counter += 1
        return c
    def remove_matches(self, board:[[str]]) -> None:
        '''
        Changes the cells in the given board that are in a
        'MATCHED' state to a NONE state.
        '''
        for col in range(self._columns):
            for row in range(self._rows):
                if board[col][row][1] == 'MATCHED':
                    board[col][row] = NONE
                    self.fall_down(board)
                    
    def fall_down(self,board:[[str]]) -> [[str]]:
        'Moves all floating gems down to the lowest unfilled row'
        boundary = len(board[0]) - 1 
        for column in board:
            for index in range(len(column)-2, -1, -1):
                if index != len(column)-1 and column[index] != NONE and column[index+1] == NONE:
                    counter = index
                    while counter != boundary and column[counter+1] == NONE:
                        counter += 1
                    column[counter] = column[index]
                    column[index] = NONE
        return board
    
    def convert_matches_to_matched(self,board: [[str]]) -> None:
        '''
        Changes the cells in the given board to a 'MATCHED'
        state if there is a match greater than 3.
        '''
        for col in range(self._columns):
            for row in range(self._rows):
                if self._number_of_matches_in_direction(self._board,col,row,1,-1) >= 3:
                    for index in range(self._number_of_matches_in_direction(self._board,col,row,1,-1)):
                        board[col+1*index][row-1*index][1] = 'MATCHED'
                if self._number_of_matches_in_direction(self._board,col,row,1,0) >= 3:
                    for index in range(self._number_of_matches_in_direction(self._board,col,row,1,0)):
                        board[col+1*index][row-0*index][1] = 'MATCHED'
                if self._number_of_matches_in_direction(self._board,col,row,1,1) >= 3:
                    for index in range(self._number_of_matches_in_direction(self._board,col,row,1,1)):
                        board[col+1*index][row+1*index][1] = 'MATCHED'
                if self._number_of_matches_in_direction(self._board,col,row,0,1) >= 3:
                    for index in range(self._number_of_matches_in_direction(self._board,col,row,0,1)):
                        board[col+0*index][row+1*index][1] = 'MATCHED'

    def _number_of_matches_in_direction(self,board: [[int]], col: int, row: int, coldelta: int, rowdelta: int) -> int:
        '''
        Returns the number of matches in a direction
        indicated by coldelta and rowdelta.
        '''
        start_cell = board[col][row][0]
        matches = 0
        if start_cell == 0:
            return matches
        
        else:
            while True:
                if  self._is_valid_column_number(col) \
                        and self._is_valid_row_number(row) \
                        and board[col][row][0] == start_cell:
                    matches += 1
                else:
                    break
                col += coldelta
                row += rowdelta
            return matches
        
    def _is_valid_column_number(self, column_number:int) -> bool:
        '''Returns True if the given column number is valid; returns False otherwise'''
        return 0 <= column_number < self._columns
    
    def _is_valid_row_number(self, row_number: int) -> bool:
        '''Returns True if the given row number is valid; returns False otherwise'''
        return 0 <= row_number < self._rows
            
        

class Faller:
    def __init__(self, Gems: list):
        self._column = int(Gems[0]) - 1
        self.Gem1 = Gems[1]
        self.Gem2 = Gems[2]
        self.Gem3 = Gems[3]
        self.frozen = False
        self.falling = False
        self.landed = False
        self.state = 'FALLING'
        self.Gems = [[Gems[1],self.state],
                     [Gems[2],self.state],
                     [Gems[3],self.state]]        
        self.coordinate = [self._column,0]
        
    def faller(self) -> list:
        return self.Gems
    def change_coords(self, col: int, row:int):
        self.coordinate[0] = col
        self.coordinate[1] = row
    
    def column(self) -> int:
        return self._column
        
    def rotate(self) -> None:
        self.Gems = self.Gems[-1:] + self.Gems[:-1]

    def is_frozen(self) -> None:
        self.frozen = True
        self.landed = False
        self.falling = False
        self.state = 'FROZEN'
        for index in range(3):
            self.Gems[index][1] = self.state
        
    def is_falling(self) -> None:
        self.falling = True
        self.landed = False
        self.state = 'FALLING'
        for index in range(3):
            self.Gems[index][1] = self.state

    def is_landed(self) -> None:
        self.landed = True
        self.falling = False
        self.state = 'LANDED'
        for index in range(3):
            self.Gems[index][1] = self.state

class InvalidMoveError(Exception):
    '''Raised whenever an invalid move is made'''
    pass






        
