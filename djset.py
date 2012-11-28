
class DjForest(object):

    def __init__(self, point):
        self.parent = self
        self.point = point
        self.rank = 0

    def Find(self):
        if self.parent != self:
            self.parent = self.parent.Find
        return self.parent

