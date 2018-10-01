# Dillon Vuong 82352779 ICS32 Project 5
import pygame
import random
import columns
class ColumnsGame:
    def __init__(self):
        self._running = True
        self._state = columns.ColumnsState(13,6)
        self._state._board = self._state.empty_game_board()
        FRAME_RATE = 30
    def run(self) -> None:
        pygame.init()

        self._resize_surface((600,600))

        clock = pygame.time.Clock()
        
        while self._running:
            clock.tick(FRAME_RATE)
            self._handle_events()
            self._redraw()

            self._handle_commands(command)
    
    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._end_game()
            elif event.type == pygame.VIDEORESIZE:
                self._resize_surface(event.size)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._on_mouse_button(event.pos)
                
    def _handle_commands(self, command: str):
        if command == '':
            self._state.remove_matches(self._state._board)
            if self._state.Faller == None:
                self._state.convert_matches_to_matched(self._state._board)
            if self._state.Faller != None:
                self._state.falling(self._state.Faller)
                self._display()
                if self._state.check_game_over(self._state.Faller):
                    print('GAME OVER')
                    self._end_game()
            else:
                self._display()
        elif command[0] == 'F':
            print(self._random_faller())
##                self._state.intialize_Faller(command[1:].split())
            
        elif command[0] == 'R':
            if self._state.Faller != None:
                self._state.rotate(self._state.Faller)
            self._display()
        elif command[0] == '>':
            if self._state.Faller != None:
                self._state.move_horizontally(command[0],self._state.Faller)
            self._display()
        elif command[0] == '<':
            if self._state.Faller != None:
                self._state.move_horizontally(command[0],self._state.Faller)
            self._display()
        elif command[0] == 'Q':
            self._end_game()
        elif command[0] == 'C':
            self._state.remove_matches(self._state._board)


    def _redraw(self) -> None:
        surface = pygame.display.get_surface()

        surface.fill(pygame.Color(255, 255, 0))
        self._draw_spots()

        pygame.display.flip()

    def _resize_surface(self, size: (int, int)) -> None:
        pygame.display.set_mode(size, pygame.RESIZABLE)
    
                
    def _random_faller(self) -> list:
        column = random.randrange(0,5)
        Gem1 = random.randrange(1,8)
        Gem2 = random.randrange(1,8)
        Gem3 = random.randrange(1,8)
        Faller = [column, Gem1, Gem2, Gem3]
        return Faller
        



    def _end_game(self) -> None:
        self._running = False

if __name__ == '__main__':
    ColumnsGame().run()
