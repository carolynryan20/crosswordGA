class Individual():

    def __init__(self, chromosome, countConflictFit = 0, letterWeightFit = 0):
        self.chromosome = chromosome
        self.countConflictFit = countConflictFit
        self.letterWeightFit = letterWeightFit
        self.dominatedByCount = 0
        self.dominateSet = []
        self.rank = None
        self.sharedFit = 0


    def __str__(self):
        return "(" + str(self.chromosome) + ", (" + str(self.countConflictFit) + ", " + str(self.letterWeightFit) + "))"


    def dominates(self, other):
        if (self.letterWeightFit > other.letterWeightFit and self.countConflictFit < other.countConflictFit):
            return True
        else:
            return False


    #d(i,j) = scaleX( F_i (objective X) - F_j (objective X) ) + scaleY( F_i (objective Y) - F_j(objective Y) )

    # letter weight max: 2000
    # intersection: #intersections in current grid


