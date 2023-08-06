import random

from trosnoth.const import ZONE_CAP_DISTANCE
from trosnoth.model.universe_base import NEUTRAL_TEAM_ID, NO_PLAYER
from trosnoth.utils.utils import Static
from trosnoth.utils import math
from trosnoth.messages import TrosballTagMsg, GameOverMsg

gameStatesById = {}


def registerGameState(gameStateClass):
    '''
    Allows a game state to be used across the network
    '''
    gameStatesById[gameStateClass.id] = gameStateClass
    return gameStateClass


def preferredTeamOtherwiseSmallest(preferredTeam, universe):
    if preferredTeam is not None:
        return preferredTeam
    else:
        playerCounts = universe.getTeamPlayerCounts()

        minCount = len(universe.players) + 1
        minTeams = []
        for team in universe.teams:
            count = playerCounts.get(team.id, 0)
            if count < minCount:
                minCount = count
                minTeams = [team]
            elif count == minCount:
                minTeams.append(team)
        return random.choice(minTeams)


class GameStateBase(Static):

    startsNewMatch = False
    inMatch = True
    statsCount = False
    userTitle = ''
    userInfo = ()

    def applyTo(self, world):
        pass

    def canShoot(self):
        return True

    def becomeNeutralWhenDie(self):
        return False

    def getTeamToJoin(self, universe, preferredTeam, bot):
        if universe.botManager:
            return universe.botManager.getTeamToJoin(preferredTeam, bot)
        return preferredTeamOtherwiseSmallest(preferredTeam, universe)

    def canRename(self):
        return False

    def isStartingCountdown(self):
        return False

    def displayWinner(self):
        return False

    def getGameTimeMode(self):
        return 'running'

    def isTrosball(self):
        return False

    def getInProgressState(self):
        return InProgress

    def getFinishedMessage(self, world):
        return None

    def onBecomingCurrentState(self, universe):
        pass

    def isTimedGameState(self):
        return False

    def getInfo(self, world, player):
        '''
        Returns information to display to the user about this game state.
        '''
        return self.userTitle, self.userInfo


@registerGameState
class Lobby(GameStateBase):
    id = 'Lobby'
    inMatch = False

    userTitle = 'Lobby'
    userInfo = (
        '* Free for all',
        '* Select preferred options from top menu',
        '* A match will start when enough players select "ready"',
    )

    def applyTo(self, world):
        super(Lobby, self).applyTo(world)
        world.abilities.zoneCaps = False
        world.abilities.stars = False
        world.onChangeVoiceChatRooms([], [])

    def becomeNeutralWhenDie(self):
        return True

    def getTeamToJoin(self, universe, preferredTeam, bot):
        return None

    def canRename(self):
        return True

    def getGameTimeMode(self):
        return 'unstarted'

    def getInfo(self, world, player):
        '''
        Returns information to display to the user about this game state.
        '''
        if world.canVote():
            return self.userTitle, self.userInfo
        return 'Game Over', ('Use the menu in the bottom left to leave game',)


@registerGameState
class Starting(GameStateBase):
    id = 'Starting'
    startsNewMatch = True

    userTitle = 'Get Ready...'
    userInfo = (
        '* Game will begin soon',
        '* Capture or neutralise all enemy zones',
        '* To capture a zone, touch the orb',
        "* If a team's territory is split, the smaller section is neutralised",
    )

    def applyTo(self, world):
        super(Starting, self).applyTo(world)
        world.abilities.upgrades = False
        world.abilities.respawn = False
        world.abilities.leaveFriendlyZones = False
        world.abilities.zoneCaps = False
        world.abilities.stars = False
        world.onChangeVoiceChatRooms(world.teams, world.players)

    def isStartingCountdown(self):
        return True

    def getGameTimeMode(self):
        return 'unstarted'


class StartingSolo(Starting):
    def getInProgressState(self):
        return Solo


@registerGameState
class StartingTrosball(Starting):
    id = 'StartingTrosball'

    userInfo = (
        '* Game will begin soon',
        '* Score points by getting the trosball through the net',
        '* To throw the trosball, press the "use upgrade" key',
        '* The trosball explodes if held for too long',
    )

    def applyTo(self, world):
        super(StartingTrosball, self).applyTo(world)
        world.uiOptions.showNets = True
        world.uiOptions.shiftingFrontLine = True
        world.uiOptions.frontLineGetter = (
            lambda: world.getTrosballPosition()[0])
        world.onChangeVoiceChatRooms(world.teams, world.players)

    def isTrosball(self):
        return True

    def getInProgressState(self):
        return Trosball

    def onBecomingCurrentState(self, universe):
        universe.resetTrosballToCentreOfMap()


@registerGameState
class Trosball(GameStateBase):
    id = 'Trosball'
    statsCount = True

    userTitle = 'Trosball'
    userInfo = (
        '* Score points by getting the trosball through the net',
        '* To throw the trosball, press the "use upgrade" key',
        '* The trosball explodes if held for too long',
    )

    def applyTo(self, world):
        super(Trosball, self).applyTo(world)
        world.abilities.zoneCaps = False
        world.abilities.stars = False

        world.uiOptions.showNets = True
        world.uiOptions.shiftingFrontLine = True
        world.uiOptions.frontLineGetter = (
            lambda: world.getTrosballPosition()[0])

    def isTrosball(self):
        return True

    def getFinishedMessage(self, world):
        if world.timer.hasTimeLimit() and world.timer.getTimeLeft() <= 0:
            teams = world.teamsWithHighestTrosballScore()
            teamId = NEUTRAL_TEAM_ID if len(teams) != 1 else teams[0].id
            return GameOverMsg(teamId, True)
        for team in world.teams:
            distance = math.distance(world.getTrosballPosition(),
                    world.getTrosballTargetZoneDefn(team).pos)
            if distance < ZONE_CAP_DISTANCE:
                playerId = (world.trosballPlayer.id if
                        world.trosballPlayer is not None else NO_PLAYER)
                return TrosballTagMsg(team.id, playerId)

    def isTimedGameState(self):
        return True

@registerGameState
class BetweenTrosballPoints(Trosball):
    id = 'BetweenTrosballPoints'
    statsCount = True

    def getFinishedMessage(self, world):
        return None


class StartingSoloTrosball(StartingTrosball):
    def getInProgressState(self):
        return SoloTrosball


class SoloTrosball(Trosball):
    def canRename(self):
        return True

    def isTimedGameState(self):
        return True


@registerGameState
class InProgress(GameStateBase):
    id = 'InProgress'
    statsCount = True

    userTitle = 'Trosnoth Match'
    userInfo = (
        '* Capture or neutralise all enemy zones',
        '* To capture a zone, touch the orb',
        "* If a team's territory is split, the smaller section is neutralised",
    )

    def getFinishedMessage(self, world):
        # Check first for timeout
        if world.timer.hasTimeLimit() and world.timer.getTimeLeft() <= 0:
            team = world.teamWithMoreZones()
            if team is not None:
                return GameOverMsg(team.id, True)
            else:
                return GameOverMsg(NEUTRAL_TEAM_ID, True)
        # Next check for an actual winning team
        else:
            team = world.teamWithAllZones()
            if team == 'Draw':
                return GameOverMsg(NEUTRAL_TEAM_ID, False)
            elif team is not None:
                return GameOverMsg(team.id, False)
            else:
                # No result yet
                pass
        return None

    def isTimedGameState(self):
        return True


@registerGameState
class Solo(InProgress):
    id = 'Solo'

    def canRename(self):
        return True

    def isTimedGameState(self):
        return True


@registerGameState
class Ended(GameStateBase):
    id = 'Ended'

    userTitle = 'Rabbit Hunt'

    def applyTo(self, world):
        super(Ended, self).applyTo(world)
        world.abilities.zoneCaps = False
        world.uiOptions.showWinner = True
        world.onChangeVoiceChatRooms([], [])

    def becomeNeutralWhenDie(self):
        return True

    def getTeamToJoin(self, universe, preferredTeam, bot):
        return None

    def getGameTimeMode(self):
        return 'ended'

    def getInfo(self, world, player):
        '''
        Returns information to display to the user about this game state.
        '''
        userInfo = []
        winner = world.getWinningTeam()
        if winner is None:
            userInfo.append('* The game was a draw')
        else:
            userInfo.append('* %s win!' % (winner.teamName,))

        if player is None or player.team is None:
            if world._onceOnly:
                userInfo.extend([
                    '* Players who survived are "rabbits"',
                    '* Try to shoot all the rabbits',
                ])
            else:
                userInfo.extend([
                    '* Players who survived are "rabbits"',
                    '* Try to shoot all the rabbits before the time runs out',
                ])
        elif world._onceOnly:
            userInfo.extend([
                '* Try to survive for as long as possible',
                '* Try to kill any surviving enemy rabbits',
                '* If you die, you will respawn as a rogue',
            ])
        else:
            userInfo.extend([
                '* Try to survive until the time runs out',
                '* Try to kill any surviving enemy rabbits',
                '* If you die, you will respawn as a rogue',
            ])
        return self.userTitle, userInfo


@registerGameState
class CustomLevel(GameStateBase):
    id = 'Custom'
