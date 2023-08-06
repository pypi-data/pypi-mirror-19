from .app import App as _App


class UserGame(_App):
    '''
    An object based on the relationship between a user and a game. A subclass of :class:`steamfront.app.App`. Should not be called manually.

    :param dict appdata: The app data that came from the API through the user.
    :param steamfront.user.User user: The user to whom the app belongs.
    :ivar player_id: A `str` containing the player's ID.
    :ivar play_time: An `int` containing how many hours the user has played the game for.
    :ivar player: The :class:`steamfront.user.User` to whom the app belongs.
    :ivar lazy: A `bool` representing whether or not the object has all of its aspects from :class:`steamfront.app.App`.
    '''

    def __init__(self, appdata:dict, user, lazy=True):

        self.appid = str(appdata['appid'])
        self.play_time = appdata['playtime_forever']
        self.player_id = user.id64
        self.player = user

        if lazy == False:
            super().__init__(self.appid)
        self.lazy = lazy

    def unlazy(self):
        '''
        To get all of the game attributes of a game, this must be called.
        '''

        self.lazy = False 
        super().__init__(self.appid)
