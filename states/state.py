# Thanks CDCodes (YT)

class State():
    def __init__(self, game):
        self._game = game
        self._prev_state = None
        # DEV
        # since we are keeping 
        # states in a dictionnay,
        # we need to have a way to know
        # when we re enter in it
        self._in_state = True

    def events(self):
        pass

    def update(self, actions):
        pass

    def draw(self, surface):
        pass

    def enter_state(self):
        if len(self._game.state_stack) >= 1 :
            self._prev_state = self._game.state_stack[-1]
            self._prev_state._in_state = False
        # DEV
        # We don't put self._in_state = True on purpose
        # Since we want to do it in the state update methode :
        # It allows us to trigger all sort of re_initialisation of the state
        # For example, we currently use it to cleanly update the game_inventory
        self._game.state_stack.append(self)

    def exit_state(self):
        self._in_state = False
        self._game.state_stack.pop()
        
    @property
    def game(self):
        return self._game