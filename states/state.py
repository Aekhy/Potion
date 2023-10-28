# Thanks CDCodes (YT)

class State():
    def __init__(self, game):
        self._game = game
        self._prev_state = None

    def update(self, actions):
        pass

    def render(self, actions):
        pass

    def enter_state(self):
        if len(self.game.state_stack) > 1 :
            self._prev_state = self.game.state_stack[-1]
        self.game.state_stack.append(self)

    def exit_state(self):
        self.game.state_stack.pop()