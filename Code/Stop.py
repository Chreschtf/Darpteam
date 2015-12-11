class Stop:
    def __init__(self,_node,_time,_meal=None,_pickup=False):
        self.node=_node
        self.st=_time   #scheduled time
        self.meal=_meal
        self.pickup=_pickup

    def getST(self):
        return self.st

    def getNode(self):
        return self.node