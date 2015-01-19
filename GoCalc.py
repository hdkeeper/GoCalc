# coding utf-8

from exceptions import IndexError
from random import randint

BLACK = 1
WHITE = 2


class Place (object):
    color = None
    group = None
    turn = None

    def __init__(self, color, turn):
        self.color = color
        self.turn = turn

    def __str__(self):
        return ' '+{None:'.', BLACK:'X', WHITE:'O'}[self.color]


class Group (object):

    def __init__(self, color):
        self.color = color
        self.stoneCount = 0
        self.dameCount = None
        self.stoneCoords = set()
        self.dameCoords = set()

    def __str__(self):
        return ', '.join(str(p) for p in self.stoneCoords)


class Board (object):
    emptyPlace = Place( None, None)

    def __init__(self, **kwargs):
        self.size = 0
        self.turn = 0
        self.places = {}
        self.groups = []
        self.prevBoard = None
        self.nextBoards = []
        self.lastMove = None

        if 'size' in kwargs:
            self.size = kwargs['size']
            for x in range(1, self.size+1):
                for y in range(1, self.size+1):
                    self.places[(x,y)] = Board.emptyPlace

        elif 'board' in kwargs:
            self.prevBoard = kwargs['board']
            self.prevBoard.nextBoards.append(self)
            self.size = self.prevBoard.size
            self.turn = self.prevBoard.turn + 1
            for (pos, place) in self.prevBoard.places.iteritems():
                self.places[pos] = Place( place.color, place.turn)

    def __str__(self):
        return ''.join(
            ''.join(str(self.places[(x,y)]) for y in range(1, self.size+1)) + '\n'
            for x in range(1, self.size+1))
                    
    def makeMove(self, x, y, color):
        if x < 1 or y < 1 or x > self.size or y > self.size:
            raise IndexError('Offset %d, %d is out of range' % (x, y))

        if self.places[(x,y)].color is not None:
            raise Exception('Offset %d, %d is already occupied' % (x, y))

        newBoard = Board(board=self)
        newBoard._putStone(x, y, color)
        return newBoard

    def _putStone(self, x, y, color):
        self.places[(x,y)] = Place(color, self.turn)
        self.lastMove = (x, y)
        self._findGroups()
        self._countDame()
        self._removeDeadGroups()

    def _getAdjacentPositions(self, pos):
        x, y = pos
        if x > 1:
            yield (x-1, y)
        if y > 1:
            yield (x, y-1)
        if x < self.size:
            yield (x+1, y)
        if y < self.size:
            yield (x, y+1)
        
    def _findGroups(self):
        def addPosToGroup(pos, group):
            group.stoneCoords.add(pos)
            group.stoneCount += 1
            self.places[pos].group = group
            for p in self._getAdjacentPositions(pos):
                if self.places[p].color == group.color and self.places[p].group is None:
                    addPosToGroup( p, group)

        for (pos, place) in self.places.iteritems():
            if place.group is None and place.color is not None:
                newGroup = Group(place.color)
                addPosToGroup(pos, newGroup)
                self.groups.append(newGroup)
    
    def _countDame(self):
        for group in self.groups:
            for stonePos in group.stoneCoords:
                for p in self._getAdjacentPositions(stonePos):
                    if self.places[p].color is None:
                        group.dameCoords.add(p)

            group.dameCount = len(group.dameCoords)

    def _removeDeadGroups(self):
        recount = False
        for group in self.groups:
            if group.dameCount == 0:
                for pos in group.stoneCoords:
                    self.places[pos] = Board.emptyPlace
                recount = True

        self.groups = [g for g in self.groups if g.dameCount > 0]
        if recount:
            self._countDame()

                        






if __name__ == '__main__':
    first = Board( size=9)
    last = first.makeMove(1, 1, BLACK).makeMove(1, 2, WHITE).makeMove(2, 2, WHITE).makeMove(2, 1, WHITE)

    print last



