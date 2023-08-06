from __future__ import division

import random
import logging
import string

import pygame

from trosnoth.const import ZONE_CAP_DISTANCE
from trosnoth.utils import math

log = logging.getLogger('zone')


class ZoneDef(object):
    '''Stores static information about the zone.

    Attributes:
        adjacentZones - mapping from adjacent ZoneDef objects to collection of
            map blocks joining the zones.
        id - the zone id
        initialOwnerIndex - the team that initially owned this zone,
            represented as a number (0 for neutral, 1 or 2 for a team).
        pos - the coordinates of this zone in the map
    '''

    def __init__(self, id, initialOwnerIndex, xCoord, yCoord):
        self.id = id
        self.initialOwnerIndex = initialOwnerIndex
        self.pos = xCoord, yCoord

        primes, index = divmod(id, 26)
        self.label = string.uppercase[index] + "'" * primes

        self.cached_adjacentZones = set()
        self.cached_unblockedNeighbours = set()
        self.cache_serial = 0

    def __str__(self):
        if self.id is None:
            return 'Z---'
        return 'Z%3d' % self.id

    def randomPosition(self):
        '''
        Returns a random position in this zone.
        '''
        from trosnoth.model.map import MapLayout

        # Place a random point within a rectangle of the same area as the zone
        rect = pygame.Rect((0, 0), (0, 0))
        rect.width = MapLayout.zoneBodyWidth + MapLayout.zoneInterfaceWidth
        rect.height = MapLayout.halfZoneHeight * 2
        rect.centery = self.pos[1]
        rect.right = self.pos[0] + MapLayout.zoneBodyWidth * 0.5

        x = random.randrange(rect.left, rect.left + rect.width)
        y = random.randrange(rect.top, rect.top + rect.height)

        # Check for points outside the zone, and shift them
        rect.width = MapLayout.zoneInterfaceWidth
        if rect.collidepoint((x, y)):
            gradient = MapLayout.halfZoneHeight / MapLayout.zoneInterfaceWidth
            if (x - rect.left) * gradient > abs(self.pos[1] - y):
                x += MapLayout.zoneInterfaceWidth + MapLayout.zoneBodyWidth
                if y < self.pos[1]:
                    y += MapLayout.halfZoneHeight
                else:
                    y -= MapLayout.halfZoneHeight

        return (x, y)


class DynamicZoneLogic(object):
    '''
    Contains all the methods for performing logic about whether zones are
    capturable and what happens if they are captured.

    This serves as a useful base class for both the in-game ZoneState class,
    and simulation classes used by bots to evaluate different options.
    '''

    def __init__(self, universe, zoneDef):
        self.defn = zoneDef
        self.id = zoneDef.id
        self.world = universe

        # Subclasses may initialise these differently
        self.owner = None
        self.dark = False
        self.players = set()
        self.turretedPlayer = None
        self.frozen = False

    def __str__(self):
        # Debug: uniquely identify this zone within the universe.
        if self.id is None:
            return 'Z---'
        return 'Z%3d' % self.id

    def getZoneFromDefn(self, zoneDef):
        '''
        Helper function for getAdjacentZones(), getUnblockedNeighbours(), and
        functions that rely on these. Should return the zone object that
        corresponds to the given ZoneDef.
        '''
        raise NotImplementedError('{}.getZoneFromDefn'.format(
            self.__class__.__name__))

    def isNeutral(self):
        return self.owner is None

    def isEnemyTeam(self, team):
        return team != self.owner and team is not None

    def isDark(self):
        return self.dark

    def makeDarkIfNeeded(self):
        '''This method should be called by an adjacent friendly zone that has
        been tagged and gained. It will check to see if it now has all
        surrounding orbs owned by the same team, in which case it will
        change its zone ownership.'''

        # If the zone is already owned, ignore it
        if not self.dark and self.owner is not None:
            for zone in self.getAdjacentZones():
                if self.isEnemyTeam(zone.owner):
                    break
            else:
                self.dark = True

    def playerIsWithinTaggingDistance(self, player):
        distance = math.distance(self.defn.pos, player.pos)
        return distance < ZONE_CAP_DISTANCE

    def getContiguousZones(self):
        '''
        Returns a set of all contiguous zones with orb owned by the same team
        as this zone.
        '''
        owner = self.owner
        sector = set()
        stack = [self]
        while stack:
            zone = stack.pop()
            if zone in sector:
                continue
            sector.add(zone)
            for adjacentZone in zone.getAdjacentZones():
                if adjacentZone.owner == owner:
                    stack.append(adjacentZone)
        return sector

    def playerWhoTaggedThisZone(self):
        '''
        Checks to see whether the zone has been tagged. If not, return None.
        If it has, return a tuple of the player and team who tagged it.
        If the zone has been rendered Neutral, this will be None, None
        '''
        teamsToPlayers = self.getCountedPlayersByTeam()
        teamsWhoCanTag = self.teamsAbleToTag()
        taggingPlayers = []

        if (len(teamsWhoCanTag) == 1 and list(teamsWhoCanTag)[0] ==
                self.owner):
            # No need to check again - we are already the owner
            return

        for team in teamsWhoCanTag:
            for player in teamsToPlayers[team]:
                if self.playerIsWithinTaggingDistance(player):
                    taggingPlayers.append(player)
                    # Only allow one player from each team to have tagged it.
                    break
        if len(taggingPlayers) == 2:
            # Both teams tagged - becomes neutral
            return (None, None)
        elif (len(taggingPlayers) == 1 and list(taggingPlayers)[0].team !=
                self.owner):
            return (taggingPlayers[0], taggingPlayers[0].team)
        else:
            return None

    def clearPlayers(self):
        self.players.clear()

    def addPlayer(self, player):
        self.players.add(player)

    def removePlayer(self, player):
        self.players.remove(player)

    def getCountedPlayersByTeam(self):
        result = dict((team, []) for team in self.world.teams)

        for player in self.players:
            if player.dead or player.turret:
                # Turreted players do not count as a player for the purpose
                # of reckoning whether an enemy can capture the orb
                continue
            if player.team is not None:
                result[player.team].append(player)
        return result

    def getPlayerCounts(self):
        '''
        Returns a list of (count, teams) ordered by count descending, where
        count is the number of counted (living non-turret) players in the zone
        and teams is the teams with that number of players. Excludes teams
        which do not own the zone and cannot capture it.
        '''
        teamsByCount = {}
        for team, players in self.getCountedPlayersByTeam().iteritems():
            if (
                    team != self.owner
                    and not self.adjacentToAnotherZoneOwnedBy(team)):
                # If the enemy team doesn't have an adjacent zone, they don't
                # count towards numerical advantage.
                continue
            teamsByCount.setdefault(len(players), []).append(team)

        return sorted(teamsByCount.iteritems(), reverse=True)

    def isCapturableBy(self, team):
        '''
        Returns True or False depending on whether this zone can be captured by
        the given team. This takes into account both the zone location and the
        number of players in the zone.
        '''
        return team != self.owner and team in self.teamsAbleToTag()

    def isBorderline(self):
        '''
        Returns a value indicating whether this is a borderline zone. A borderline
        zone is defined as a zone which cannot be tagged by any enemy team, but
        could be if there was one more enemy player in the zone.
        '''
        moreThanThreeDefenders = False

        playerCounts = self.getPlayerCounts()
        while playerCounts:
            count, teams = playerCounts.pop(0)
            if moreThanThreeDefenders and count < 3:
                return False

            if count == 0:
                if any(t != self.owner for t in teams):
                    # There is a team which could tag if it had one attacker
                    return True

            elif count < 3:
                if len(teams) == 1:
                    # If it's an attacking team it's capturable, if it's a
                    # defending team it's not borderline.
                    return False

                # If an attacking team had one more player they could capture
                return True

            elif count == 3:
                if moreThanThreeDefenders:
                    return True

                if len(teams) == 1:
                    # If it's an attacking team it's capturable, if it's a
                    # defending team it's not borderline.
                    return False

                # Team could capture if it had 4 attackers
                return True

            else:
                if any(t != self.owner for t in teams):
                    # Already capturable
                    return False

                moreThanThreeDefenders = True

        return False

    def getAdjacentZones(self):
        '''
        Iterates through ZoneStates adjacent to this one.
        '''
        for adjZoneDef in self.world.layout.getAdjacentZoneDefs(self.defn):
            yield self.world.zoneWithDef[adjZoneDef]

    def getUnblockedNeighbours(self):
        '''
        Iterates through ZoneStates adjacent to this one which are not blocked
        off.
        '''
        for adjZoneDef in self.world.layout.getUnblockedNeighbours(self.defn):
            yield self.world.zoneWithDef[adjZoneDef]

    def adjacentToAnotherZoneOwnedBy(self, team):
        '''
        Returns whether or not this zone is adjacent to a zone whose orb is
        owned by the given team.
        '''
        for adjZone in self.getAdjacentZones():
            if adjZone.owner == team:
                return True
        return False

    def teamsAbleToTag(self):
        '''
        Returns the set of teams who have enough players to tag a zone
        (ignoring current zone ownership). Teams must have:
         (a) strict numerical advantage in this zone; or
         (b) more than 3 players in this zone.
        This takes into account the fact that turrets do not count towards
        numerical advantage.
        '''
        result = set()

        playerCounts = self.getPlayerCounts()
        while playerCounts:
            count, teams = playerCounts.pop(0)
            if count <= 3:
                if not result and len(teams) == 1 and count > 0:
                    result.update(teams)
                break
            result.update(teams)
        return result

    def consequenceOfCapture(self):
        '''
        Uses the zone neutralisation logic to calculate how many zone points an
        enemy team would gain by capturing this zone. That is, 2 points for the
        zone itself, plus one for each zone neutralised in the process.
        '''
        if self.owner is None:
            # Always one point for capturing a neutral zone
            return 1

        seen = {self}
        explore = [z for z in self.getAdjacentZones() if z.owner == self.owner]
        sectors = []
        while explore:
            zone = explore.pop(0)
            if zone in seen:
                continue

            thisSector = [zone]
            score = 0
            while thisSector:
                score += 1
                zone = thisSector.pop(0)
                seen.add(zone)
                for z in zone.getAdjacentZones():
                    if z.owner == self.owner and z not in seen:
                        thisSector.append(z)
            sectors.append(score)

        if sectors:
            # Largest sector is not lost
            sectors.remove(max(sectors))

        # Two points for capture, plus one for each zone neutralised
        return 2 + sum(sectors)


class ZoneState(DynamicZoneLogic):
    '''
    Represents information about the dynamic state of a given zone during a
    game.
    '''

    def __init__(self, universe, zoneDef):
        super(ZoneState, self).__init__(universe, zoneDef)

        universe.zoneWithDef[zoneDef] = self

        teamIndex = zoneDef.initialOwnerIndex
        if teamIndex is None:
            self.owner = None
            self.dark = False
        else:
            self.owner = universe.teams[teamIndex]
            self.dark = True

            # Tell the team object that it owns one more zone
            self.owner.zoneGained()

        self.previousOwner = self.owner

    def getZoneFromDefn(self, zoneDef):
        return self.world.zoneWithDef[zoneDef]

    def tag(self, player):
        '''This method should be called when the orb in this zone is tagged'''
        self.previousOwner = self.owner
        self.dark = False

        # Inform the team objects
        if self.owner:
            self.owner.zoneLost()
        if player is not None:
            team = player.team
            if team is not None:
                team.zoneGained()
            player.incrementStars()
        else:
            team = None

        self.owner = team
        for zone in self.getAdjacentZones():
            if zone.owner == team or self.isNeutral():
                # Allow the adjacent zone to check if it is entirely
                # surrounded by non-enemy zones
                zone.makeDarkIfNeeded()
        self.makeDarkIfNeeded()

    def updateByTrosballPosition(self, position):
        self.isDark = False
        if abs(position[0] - self.defn.pos[0]) < 1e-5:
            self.owner = None
        elif position[0] < self.defn.pos[0]:
            self.owner = self.world.teams[1]
        else:
            self.owner = self.world.teams[0]

    def setOwnership(self, team, dark):
        if self.owner is not None:
            self.owner.zoneLost()
        self.owner = team
        if team is not None:
            team.zoneGained()
        self.dark = dark

    @staticmethod
    def canTag(numTaggers, numDefenders):
        '''
        Deprecated, do not use.
        '''
        return numTaggers > numDefenders or numTaggers > 3
