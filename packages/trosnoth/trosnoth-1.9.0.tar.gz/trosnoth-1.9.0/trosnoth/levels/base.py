import logging
from twisted.internet import defer

from trosnoth.const import GAME_FULL_REASON, PRIVATE_CHAT
from trosnoth.messages import ChatMsg
from trosnoth.messages import PlaySoundMsg
from trosnoth.model.map import ZoneLayout
from trosnoth.model.universe_base import NEUTRAL_TEAM_ID

log = logging.getLogger(__name__)


class Level(object):
    '''
    Base class for all standard and custom levels. A level provides
    server-only instructions about how a particular game is set up and
    operates.

    NOTE that clients know nothing about what level is being used, so any
    events that affect world state need to be carried out through the
    message-passing API in order that clients stay in sync with the server.
    '''
    spawnStars = False

    def setupMap(self, world):
        '''
        Called before the game starts, to set up the map. Must be overridden.
        '''
        raise NotImplementedError('{}.setupMap'.format(
            self.__class__.__name__))

    def tearDownLevel(self):
        '''
        Called when a new level is selected, or the server terminates. This
        could be used to tear down event handlers which have been set up.
        '''
        pass

    def start(self):
        '''
        Called when the game has just started. By this point the Game and
        World have been completely initialised. May be used to set up event
        handlers and bots.
        '''
        pass

    def findReasonPlayerCannotJoin(self, game, teamId, user, bot):
        '''
        Checks whether or not another player with the given details can join
        the game. By default, this will respect game.maxTotalPlayers, and
        game.maxPerTeam.

        @param game: the LocalGame object of the current game
        @param teamId: the id of the team that the player will join if
            permitted (calculated from call to getIdOfTeamToJoin().
        @param user: the authentication server user object if this game is
            being run on an authentication server, or None otherwise.
        @param bot: whether or not the requested join is from a bot.

        @return: None if the player can join the game, or a reason constant
            otherwise (e.g. GAME_FULL_REASON, or UNAUTHORISED_REASON).
        '''
        if len(game.world.players) >= game.maxTotalPlayers:
            return GAME_FULL_REASON

        teamPlayerCounts = game.world.getTeamPlayerCounts()
        if (teamId != NEUTRAL_TEAM_ID and
                teamPlayerCounts.get(teamId, 0) >= game.maxPerTeam):
            return GAME_FULL_REASON

        return None

    def getTeamToJoin(self, game, preferredTeam, user, bot):
        '''
        When a player asks to join a game, this method is called to decide
        which team to put them on, assuming that they are allowed to join.

        @param game: the LocalGame object of the current game
        @param preferredTeam: the team that the player would like to join if
            possible, or None if the player does not care
        @param user: the authentication server user object if this game is
            being run on an authentication server, or None otherwise.
        @param bot: whether or not the requested join is from a bot.

        @return: a team
        '''

        # Default team selection logic depends on game phase
        return game.world.state.getTeamToJoin(game.world, preferredTeam, bot)

    @defer.inlineCallbacks
    def addBot(self, game, team, nick, botName='puppet'):
        '''
        Utility function that adds a bot to the game, but bypasses the call
        to findReasonPlayerCannotJoin(), because it is this level that has
        requested the join. By default, creates a PuppetBot which does
        nothing until told.
        '''
        bot = yield game.addBot(botName, team=team, fromLevel=True, nick=nick)
        if bot.player is None:
            yield bot.onPlayerSet.wait()

        defer.returnValue(bot.ai)

    @defer.inlineCallbacks
    def waitForHumans(self, world, number):
        '''
        Utility function that waits until at least number human players have
        joined the game, then returns a collection of the human players in
        the game.
        '''
        while True:
            humans = [p for p in world.players if not p.bot]
            if len(humans) >= number:
                defer.returnValue(humans)

            yield world.onPlayerAdded.wait()

    def sendPrivateChat(self, fromPlayer, toPlayer, text):
        fromPlayer.agent.sendRequest(
            ChatMsg(PRIVATE_CHAT, toPlayer.id, text=text.encode()))

    def playSound(self, world, filename):
        '''
        Utility function to play a sound on all clients. The sound file must
        exist on the client system.
        '''
        world.sendServerCommand(PlaySoundMsg(filename.encode('utf-8')))


class StandardLevel(Level):
    '''
    The base class used for levels with standard joining rules and win
    conditions.
    '''
    spawnStars = True

    def __init__(self, *args, **kwargs):
        super(StandardLevel, self).__init__(*args, **kwargs)

        self.world = None

    def setupMap(self, world):
        self.world = world


class StandardRandomLevel(StandardLevel):
    '''
    A standard Trosnoth level with no special events or triggers, played on
    a randomised map.
    '''

    def __init__(
            self, halfMapWidth=None, mapHeight=None, blockRatio=None,
            duration=None):
        super(StandardRandomLevel, self).__init__()

        self.halfMapWidth = halfMapWidth
        self.mapHeight = mapHeight
        self.blockRatio = blockRatio
        self.duration = None

    def setupMap(self, world):
        super(StandardRandomLevel, self).setupMap(world)

        self.ensureMapSizeIsNotNone()
        self.ensureBlockRatioIsNotNone()
        self.ensureDurationIsNotNone()

        zones = ZoneLayout.generate(
            self.halfMapWidth, self.mapHeight, self.blockRatio)
        layout = zones.createMapLayout(self.world.layoutDatabase)
        self.world.setLayout(layout)

        self.world.timer.setMatchDuration(self.duration)

    def ensureMapSizeIsNotNone(self):
        if self.halfMapWidth is not None and self.mapHeight is not None:
            return

        # Calculates a new map size based on what players vote for, with the
        # defaults (if most people select Auto) being determined by the size of
        # the teams.
        sizeCount = {}
        for player in self.world.players:
            if player.bot:
                continue
            size = player.preferredSize
            sizeCount[size] = sizeCount.get(size, 0) + 1

        if sizeCount:
            bestSize = max(sizeCount, key=sizeCount.get)
            if sizeCount.get((0, 0), 0) != sizeCount[bestSize]:
                self.halfMapWidth, self.mapHeight = bestSize
                return

        # Decide size based on player count.
        teamSize = sum(1 for p in self.world.players if not p.bot)

        if teamSize <= 3:
            self.halfMapWidth, self.mapHeight = (1, 1)
        elif teamSize <= 4:
            self.halfMapWidth, self.mapHeight = (5, 1)
        else:
            self.halfMapWidth, self.mapHeight = (3, 2)

        assert self.halfMapWidth is not None
        assert self.mapHeight is not None

    def ensureBlockRatioIsNotNone(self):
        '''
        By default, assume that larger maps want higher block ratios because a
        map that's too big with no obstacles results in chaos.
        '''
        if self.blockRatio is not None:
            return
        roughArea = (2 * self.halfMapWidth + 1) * (self.mapHeight + 0.5)
        self.blockRatio = max(0.3, 1 - 5. / roughArea)

        assert self.blockRatio is not None

    def ensureDurationIsNotNone(self):
        if self.duration is not None:
            return

        durationCount = {}
        for player in self.world.players:
            if player.bot:
                continue
            duration = player.preferredDuration
            durationCount[duration] = durationCount.get(duration, 0) + 1

        if durationCount:
            bestDuration = max(durationCount, key=durationCount.get)
            if durationCount.get(0, 0) != durationCount[bestDuration]:
                self.duration = bestDuration
                return

        # Decide default based on map size.
        if (self.halfMapWidth, self.mapHeight) == (3, 2):
            self.duration = 45 * 60
        elif (self.halfMapWidth, self.mapHeight) == (1, 1):
            self.duration = 10 * 60
        elif (self.halfMapWidth, self.mapHeight) == (5, 1):
            self.duration = 20 * 60
        else:
            self.duration = min(
                7200,
                2 * 60 * (self.halfMapWidth * 2 + 1) * (self.mapHeight * 1.5))

        assert self.duration is not None


class StandardLoadedLevel(StandardLevel):
    def __init__(self, mapLayout):
        super(StandardLoadedLevel, self).__init__()

        self.mapLayout = mapLayout

    def setupMap(self, world):
        super(StandardLoadedLevel, self).setupMap(world)
        self.world.setLayout(self.mapLayout)


def playLevel(level, withLogging=True, **kwargs):
    '''
    For testing new Levels - launches Trosnoth in single player mode with
    the given level.
    '''
    from trosnoth.run.solotest import Main

    if withLogging:
        from trosnoth.utils.utils import initLogging
        initLogging()

    Main(level=level, **kwargs).run_twisted()
