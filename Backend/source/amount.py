from config import Config
from numerize import numerize
from currency import symbols

class Amount():
    TYPE = None
    CURRENCY = None
    DECIMALPLACES = 0
    def __init__(self, val) -> None:
        self.value = val
        Amount.displayformat()
    
    @classmethod
    def currency(cls):
        curname = Config().currency
        if curname in symbols:
            return symbols[curname]
        else:
            raise Exception(f"Unknown currency {curname}")
    
    @classmethod
    def displayformat(cls):
        if Amount.TYPE: #defaults are set already or not.
            return
        Amount.DECIMALPLACES = 0 if Config().amountdisplaystyle != "human-readable" else Config().decimalsinhrformat
        Amount.CURRENCY = Amount.currency()
        style  = Config().amountdisplaystyle
        if style == "comma-separated":
            digits = Config().amountdecimalplaces
            if digits == 0:
                Amount.TYPE = "A"
            elif digits == 2:
                Amount.TYPE = "B"
        elif style == "human-readable":
            Amount.TYPE = "C"
        
    def __str__(self) -> str:
        if Amount.TYPE == "A":
            return f"{Amount.CURRENCY}{self.value:,.0f}"
        elif Amount.TYPE == "B":
            return f"{Amount.CURRENCY}{self.value:,:.2f}"            
        elif Amount.TYPE == "C":
            return Amount.CURRENCY + numerize.numerize(self.value, Amount.DECIMALPLACES)
        else:
            raise Exception(f"Invalid type ('{Amount.TYPE}') of amount")
         

if __name__ == "__main__":
    a = Amount(2220)
    print(a)
