class CashAndCredit:
    def __init__(self):
        self.BB_O9 = 0
        self.BB_O10 = 0
        self.BB_O11 = self.BB_O9 + self.BB_O10
        self.BB_O13 = 217400000
        self.BB_O33 = 55000000
        self.BB_O14 = self.BB_O33
        self.BB_O15 = self.BB_O13 + self.BB_O14
        self.BB_O17 = 2000000
        self.BB_O18 = 0
        self.BB_O19 = self.BB_O18 + self.BB_O17
        self.BB_O21 = 0
        self.BB_O22 = 0
        self.BB_O23 = self.BB_O21 + self.BB_O22
        self.BB_O25 = 273867600  # hardcoded for now. Need to calculate.
        self.BB_O26 = 0  # hardcoded for now. Need to calculate.
        self.BB_O28 = 44548929  # base
        self.BB_O29 = 1032843  # from J18 which is calculated

        self.BB_O32 = 8836419.56  # base
        self.BB_O34 = self.BB_O32 + self.BB_O33
        self.BB_O35 = -7960000  # base

        self.BB_O51 = 55876419  # sum(34: 50)
        self.BB_O54 = 274912.62  # base
        self.BB_O57 = 274912.62  # sum(54:56)
        self.BB_O59 = 274912.62  # sum(57:58)
        self.BB_O62 = 0  # base
        self.BB_O65 = 0  # sum(62:64)
        self.BB_O67 = 0  # sum(65:66)

        self.BB_O70 = 0  # base
        self.BB_O73 = 0  # sum(70:72)
        self.BB_O75 = 0  # sum(73:74)
