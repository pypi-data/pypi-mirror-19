class Bin(object):
   """ Base class to represent how bins are created """
   pass


class Above(Bin):
   def bins(self, thresholds):
      lowerT = [-np.inf for i in range(0, len(thresholds))]
      upperT = thresholds
      return [lowerT, upperT]

   def compute(self, array):
      return 1


class Below(Bin):
   pass


class Within(Bin):
   pass
