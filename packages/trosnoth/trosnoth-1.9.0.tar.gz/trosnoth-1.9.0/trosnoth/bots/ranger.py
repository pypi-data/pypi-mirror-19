import logging
import random

from trosnoth.bots.goalsetter import (
    GoalSetterBot, Goal, RespawnNearZone, MessAroundInZone,
    ZoneMixin,
)
from trosnoth.model import upgrades

log = logging.getLogger(__name__)


class WinCurrentGame(Goal):
    def reevaluate(self):
        state = self.bot.world.state

        self.bot.setUpgradePolicy(None)
        if not state.inMatch:
            # Lobby or similar
            self.setSubGoal(RunAroundKillingHumans(self.bot, self))
        elif state.isTrosball():
            self.setSubGoal(ScoreTrosballPoint(self.bot, self))
        elif state.becomeNeutralWhenDie():
            # Rabbit hunt
            self.setSubGoal(HuntTheRabbits(self.bot, self))
        else:
            self.setSubGoal(WinStandardTrosnothGame(self.bot, self))


class ScoreTrosballPoint(Goal):
    def reevaluate(self):
        if not self.bot.world.state.isTrosball():
            self.returnToParent()
            return

        # TODO: trosball logic
        self.setSubGoal(RunAroundKillingThings(self.bot, self))


class RunAroundKillingThings(Goal):
    def start(self):
        self.worldState = self.bot.world.state
        self.bot.world.onGameOver.addListener(self.reevaluate)
        self.bot.world.onReset.addListener(self.reevaluate)
        self.nextCheck = None
        self.scheduleNextCheck()

    def stop(self):
        super(RunAroundKillingThings, self).stop()
        self.bot.world.onGameOver.removeListener(self.reevaluate)
        self.bot.world.onReset.removeListener(self.reevaluate)

    def scheduleNextCheck(self):
        self.cancelNextCheck()
        delay = 2.5 + random.random()
        self.nextCheck = self.bot.world.callLater(delay, self.reevaluate)

    def cancelNextCheck(self):
        if self.nextCheck:
            self.nextCheck.cancel()
            self.nextCheck = None

    def reevaluate(self):
        self.cancelNextCheck()

        if self.bot.world.state != self.worldState:
            self.returnToParent()
            return

        player = self.bot.player

        if player.dead:
            zone = self.selectZone()
            if zone is None:
                zone = player.getZone()
                if zone is None:
                    zone = random.choice(list(self.bot.world.zones))
            self.setSubGoal(RespawnNearZone(self.bot, self, zone))
            self.scheduleNextCheck()
            return

        if player.getZone() and self.zoneIsOk(player.getZone()):
            # There are enemies here
            self.setSubGoal(MessAroundInZone(self.bot, self))
            self.scheduleNextCheck()
            return

        zone = self.selectZone()
        if zone:
            self.bot.moveToOrb(zone)
        else:
            self.setSubGoal(MessAroundInZone(self.bot, self))
        self.scheduleNextCheck()

    def zoneIsOk(self, zone):
        return any(
            (not p.dead and not self.bot.player.isFriendsWith(p))
            for p in zone.players)

    def selectZone(self):
        options = []
        for zone in self.bot.world.zones:
            if self.zoneIsOk(zone):
                options.append(zone)
        if not options:
            return None
        return random.choice(options)


class RunAroundKillingHumans(RunAroundKillingThings):
    def zoneIsOk(self, zone):
        return any(
            (not p.dead and not self.bot.player.isFriendsWith(p) and not p.bot)
            for p in zone.players)


class HuntTheRabbits(RunAroundKillingThings):
    def zoneIsOk(self, zone):
        return any(
            (
                not p.dead and not self.bot.player.isFriendsWith(p)
                and p.team is not None)
            for p in zone.players)


class WinStandardTrosnothGame(Goal):
    '''
    Win the current game of Trosnoth by capturing all the zones.
    '''

    def start(self):
        self.bot.setUpgradePolicy(upgrades.Shield, ownStars=False, delay=6)

        self.bot.world.onGameOver.addListener(self.reevaluate)
        self.bot.world.onReset.addListener(self.reevaluate)
        self.nextCheck = None
        self.scheduleNextCheck()

    def scheduleNextCheck(self):
        self.cancelNextCheck()
        delay = 2.5 + random.random()
        self.nextCheck = self.bot.world.callLater(delay, self.reevaluate)

    def cancelNextCheck(self):
        if self.nextCheck:
            self.nextCheck.cancel()
            self.nextCheck = None

    def stop(self):
        super(WinStandardTrosnothGame, self).stop()
        self.cancelNextCheck()
        self.bot.world.onGameOver.removeListener(self.reevaluate)
        self.bot.world.onReset.removeListener(self.reevaluate)

    def reevaluate(self, *args, **kwargs):
        '''
        Decide whether to stay in the current zone, or move to another.
        '''
        self.cancelNextCheck()

        state = self.bot.world.state
        if (not state.inMatch) or state.becomeNeutralWhenDie():
            self.returnToParent()
            self.scheduleNextCheck()
            return

        player = self.bot.player
        myZone = player.getZone()

        # 1. If we're defending a borderline zone, stay in the zone
        if myZone and myZone.owner == player.team and myZone.isBorderline():
            self.setSubGoal(DefendZone(self.bot, self, myZone))
            self.scheduleNextCheck()
            return

        # 2. If we're attacking a capturable zone, stay in the zone
        if (
                myZone and myZone.owner != player.team
                and myZone.isCapturableBy(player.team)):
            self.setSubGoal(CaptureZone(self.bot, self, myZone))
            self.scheduleNextCheck()
            return

        # 3. Score other zones based on how helpful it would be to be there and
        #    how likely we are to get there in time.

        if player.dead:
            zone = self.getMostUrgentZone()
        else:
            zone = self.getMostLikelyUrgentZone(myZone)

        if zone is None:
            self.returnToParent()
        elif zone.owner == player.team:
            self.setSubGoal(DefendZone(self.bot, self, zone))
        else:
            self.setSubGoal(CaptureZone(self.bot, self, zone))

        self.scheduleNextCheck()

    def getMostUrgentZone(self):
        bestScore = 0
        bestOptions = []

        for zone in self.bot.world.zones:
            utility = self.getZoneUtility(zone)

            if not [
                    z for z in zone.getAdjacentZones()
                    if z.owner == zone.owner]:
                # This is the last remaining zone
                awesomeness = 5
            else:
                awesomeness = zone.consequenceOfCapture()

            score = utility * awesomeness
            if score == bestScore:
                bestOptions.append(zone)
            elif score > bestScore:
                bestOptions = [zone]
                bestScore = score

        if not bestOptions:
            return None

        return random.choice(bestOptions)

    def getMostLikelyUrgentZone(self, myZone):
        bestScore = 0
        bestOptions = []
        seen = {myZone}
        pending = [(zone, 0.7) for zone in myZone.getUnblockedNeighbours()]
        while pending:
            zone, likelihood = pending.pop(0)
            seen.add(zone)

            utility = self.getZoneUtility(zone)

            if not [
                    z for z in zone.getAdjacentZones()
                    if z.owner == zone.owner]:
                # This is the last remaining zone
                awesomeness = 5
            else:
                awesomeness = zone.consequenceOfCapture()

            score = likelihood * utility * awesomeness
            if score == bestScore:
                bestOptions.append(zone)
            elif score > bestScore:
                bestOptions = [zone]
                bestScore = score

            likelihood *= 0.7
            for other in zone.getUnblockedNeighbours():
                if other not in seen:
                    pending.append((other, likelihood))

        if not bestOptions:
            return None

        return random.choice(bestOptions)

    def getZoneUtility(self, zone):
        player = self.bot.player

        # Count the number of friendly players and players on the most
        # likely enemy team to tag the zone.
        enemy = friendly = 0
        for count, teams in zone.getPlayerCounts():
            if player.team in teams and not friendly:
                friendly = count
            if [t for t in teams if t != player.team] and not enemy:
                enemy = count
            if friendly and enemy:
                break

        if zone.owner == player.team:
            defence = min(3, friendly)
            if enemy == 0:
                utility = 0
            elif enemy > defence:
                # There's a slim chance you could shoot them before they
                # capture the zone.
                utility = 0.2 ** (enemy - defence)
            elif enemy == defence:
                # Being here will stop it being tagged
                utility = 1
            else:
                # There's a slim chance the enemy might shoot them
                utility = 0.2 ** (friendly - enemy)
        elif not zone.adjacentToAnotherZoneOwnedBy(player.team):
            # Cannot capture, have no adjacent zones
            utility = 0
        else:
            defence = min(3, enemy)
            if friendly > defence:
                # Already capturable, but there's a slim chance teammates
                # might die.
                utility = 0.2 ** (friendly - defence)
            elif friendly == defence:
                # Being here will enable the zone tag
                utility = 1
            else:
                # There's a slim chance you could shoot them and capture
                utility = 0.2 ** (friendly - enemy)
        return utility


class CaptureZone(ZoneMixin, Goal):
    '''
    Respawns if necessary, moves to the given zone, messes around until it's
    capturable, and captures it. If the player dies, respawns and tries again.
    Returns if the zone is captured or becomes uncapturable by virtue of having
    no adjacent zones owned by the team.
    '''

    def __init__(self, bot, parent, zone):
        super(CaptureZone, self).__init__(bot, parent)
        self.zone = zone

    def reevaluate(self):
        player = self.bot.player
        if self.zone.owner == player.team:
            self.returnToParent()
            return

        if not self.zone.adjacentToAnotherZoneOwnedBy(player.team):
            self.returnToParent()
            return

        if player.dead:
            self.setSubGoal(RespawnNearZone(self.bot, self, self.zone))
            return

        playerZone = player.getZone()
        if (
                playerZone == self.zone
                and not self.zone.isCapturableBy(player.team)):
            self.setSubGoal(MessAroundInZone(self.bot, self))
        else:
            self.bot.moveToOrb(self.zone)


class DefendZone(ZoneMixin, Goal):
    '''
    Respawns if necessary, moves to the given zone and messes around there.
    If the player dies, respawns and continues. Returns if the zone is
    captured or neutralised.
    '''

    def __init__(self, bot, parent, zone):
        super(DefendZone, self).__init__(bot, parent)
        self.zone = zone

    def reevaluate(self):
        player = self.bot.player
        if self.zone.owner != player.team:
            self.returnToParent()
            return

        if player.dead:
            self.setSubGoal(RespawnNearZone(self.bot, self, self.zone))
            return

        playerZone = player.getZone()
        if playerZone == self.zone:
            self.setSubGoal(MessAroundInZone(self.bot, self))
        else:
            self.bot.moveToOrb(self.zone)


class RangerBot(GoalSetterBot):
    nick = 'RangerBot'
    playable = True

    MainGoalClass = WinCurrentGame


BotClass = RangerBot
