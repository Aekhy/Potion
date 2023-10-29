# Thanks CDCodes (YT)

class State():
    def __init__(self, game):
        self._game = game
        self._prev_state = None
        
    def events(self):
        pass

    def update(self, actions):
        pass

    def draw(self, surface):
        pass

    def enter_state(self):
        if len(self._game.state_stack) >= 1 :
            self._prev_state = self._game.state_stack[-1]
        self._game.state_stack.append(self)

    def exit_state(self):
        self._game.state_stack.pop()