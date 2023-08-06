import logging

from twisted.internet import defer

from trosnoth.const import GAME_FULL_REASON, UNAUTHORISED_REASON
from trosnoth.levels.base import Level, playLevel
from trosnoth.model.map import ZoneLayout, ZoneStep

log = logging.getLogger(__name__)


class DemoLevel(Level):
    '''
    Demonstrates a resync at game start, which shouldn't occur.
    '''

    world = None

    def setupMap(self, world):
        self.world = world

        zones = ZoneLayout()
        world.setLayout(zones.createMapLayout(world.layoutDatabase))

    @defer.inlineCallbacks
    def start(self):
        from twisted.internet import reactor

        # NOTE: without this yield line it syncs just fine.
        d = defer.Deferred()
        reactor.callLater(0, d.callback, None)
        # yield d

        humans = yield self.waitForHumans(self.world, 1)
        self.world.magicallyMovePlayer(
            humans[0], self.world.getZone(0).defn.pos, alive=True)


if __name__ == '__main__':
    playLevel(DemoLevel())
