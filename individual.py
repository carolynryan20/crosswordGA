class Individual():

    def __init__(self, chromosome, countConflictFit, letterWeightFit):
        self.chromosome = chromosome
        self.countConflictFit = countConflictFit
        self.letterWeightFit = letterWeightFit
        self.dominatedByCount = 0
        self.dominateSet = []
        self.rank = None


    def __str__(self):
        return "(" + str(self.chromosome) + ", (" + str(self.countConflictFit) + ", " + str(self.letterWeightFit) + "))"


    def dominates(self, other):
        if (self.letterWeightFit > other.letterWeightFit and self.countConflictFit < other.countConflictFit):
            return True
        else:
            return False
