class Stop:
    def __init__(self, _node, _time, _meal,_pickup=False):
        self.node = _node
        self.st = _time  # scheduled time
        self.meal = _meal
        self.pickup=_pickup

        self.bup = 0  # max time preceding stops can be advanced  [0..r]
        self.bdown = 0  # max time preceding stops can be delayed  [0..r]
        self.aup = 0  # max time following stops can be advanced  [r..d]
        self.adown = 0  # max time following stops can be delayed  [r..d]

    def getST(self):
        return self.st

    def getNode(self):
        return self.node

    def getBUP(self):
        return self.bup

    def getBDOWN(self):
        return self.bdown

    def getAUP(self):
        return self.aup

    def getADOWN(self):
        return self.adown


    def __str__(self):
        return str(self.node.coords)
