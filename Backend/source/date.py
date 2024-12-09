from datetime import datetime
from config import Config


class Date():
    FORMAT = None
    def __init__(self, date) -> None:
        if isinstance(date, datetime):
            self.date = date
        elif isinstance(date, str):
            self.date = datetime.strptime(date, '%Y-%m-%d')
        self.fmt = Date.get_format()
    
    def __str__(self) -> str:
        return self.date.strftime(Date.get_format())
    
    @classmethod
    def get_format(cls) -> str:
        if Date.FORMAT:
             return Date.FORMAT
        symmap = {
            'YY' : '%y',
            'YYYY' : '%Y',
            'MM' : '%m',
            'MMM' : '%b',
            'DD' : '%d'
        }
        ss = Config().dateformat
        for k in ['YYYY', 'YY', 'MMM', 'MM', 'DD' ]:
             ss = ss.replace(k, symmap[k])
        Date.FORMAT = ss
        return Date.FORMAT
        

if "__main__" == __name__:
     a = Date(datetime(2024, 7, 23))
     print(a)