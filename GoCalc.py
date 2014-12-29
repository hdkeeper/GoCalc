# coding utf-8

BLACK = 1
WHITE = 2


class Board (object):
    positions = {}
    groups = []
    prevBoard = None
    nextBoards = []


class Position (object):
    color = None
    group = None
    move = None
    positions = []


class Group (object):
    color = None
    stoneCount = 0
    dameCount = None
    positions = []


print('Hello World')
