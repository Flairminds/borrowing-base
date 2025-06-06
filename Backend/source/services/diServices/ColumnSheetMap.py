from enum import Enum

borrower_stats = {
    "Current Metrics": (0, 9, 52),
    "At Close Metrics": (0, 52, 79),
    "Fund": (1, 2, 9),
    "Capital Structure": (1, 9, 23),
    "Reporting": (1, 23, 32),
    "For PSCF-Lev & PSSL": (1, 32, 33),
    "L3M / Quarterly": (1, 33, 37),
    "YTD": (1, 37, 41),
    "Current Leverage Stats Output": (1, 41, 52),
    "Comps Other Inputs / Leverage Calcs": (1, 52, 58),
    "Comps - At Close Metrics (Hardcode at close)": (1, 58, 72),
    "Pricing": (1, 72, 79)
}

security_stats = {
    "Banks": (0, 3, 9),
    "Security Information": (0, 10, 30),
    "PCOF Specific Metrics": (0, 31, 39),
    "Current": (0, 75, 81),
    "At Close": (0, 81, 91),
    "L3M / Quarterly": (0, 91, 95),
    "YTD": (0, 95, 99)
}

SOI_Mapping = {
    # "General": (0, 1, 5),
    "For Dropdown": (0, 6, 7)
}

PSSL_II_Borrowing_base = {
    "Initial Debt in $ and Multiple": (0, 48, 53),
    "Current Debt in $ and Multiple": (0, 53, 58),
    "Current Unrestricted": (-1, 53, 54),
    "Rating": (0, 31, 33),
    "Initial EBITDA": (0, 35, 41),
    "Current EBITDA": (0, 41, 47),
    "VALUE ADJUSTMENT EVENT": (0, 60, 70),
    "Initial Unrestricted": (-1, 48, 49),
    "Initial Senior": (-1, 49, 50),
    "Initial Total": (-1, 50, 51),
    "Current Senior": (-1, 54, 55),
    "Current Total": (-1, 55, 56),
    "Upfront Approval": (-1, 14, 15),
    "Eligible": (-1, 19, 20),
    "DIP": (-1, 22, 23),
    "Approved Country": (-1, 24, 25),
    "Approved": (-1, 25, 26),
    "GICS": (-1, 27, 28),
    "Fixed": (-1, 28, 29),
    "Interest Paid": (-1, 29, 30),
    "Paid Less than": (-1, 30, 31),
    "Rated": (-1, 33, 34),
    "Two Market ": (-1, 34, 35),
    "Initial Date of TTM": (-1, 35, 36),
    "Initial Initial EBITDA": (-1, 37, 38),
    "Initial Adjusted TTM": (-1, 38, 39),
    "Current Date of TTM": (-1, 41, 42),
    "Current Current Ebitda": (-1, 43, 44),
    "Current Adjusted TTM": (-1, 44, 45),
    "Obligor Payment": (-1, 60, 61),
    "Exercise of Rights and": (-1, 61, 62),
    "(a) Reduces/waives": (-1, 62, 63),
    "(b) Extends Maturity/": (-1, 63, 64),
    "(c) Waives": (-1, 64, 65),
    "(d) Subordinates": (-1, 65, 66),
    "(e) Releases": (-1, 66, 67),
    "(f) Amends": (-1, 67, 68),
    "(f) Failure to Deliver": (-1, 69, 70),
    "(e) Obligor Insolvency": (-1, 68, 69),
    "Loan": (-1, 3, 4),
    "RCF Exposure": (-1, 12, 13),
    "RCF Commitment": (-1, 13, 14),
    "Borrower Outstanding Principal": (-1, 4, 5),
    "Borrower Facility": (-1, 5, 6)
}

PCOF_III_BB = {}

PCOF_IV = {}

MARKET_BOOK = {}

master_rating = {
    "Ratings Data (Borrower)": (0, 3, 16),
    "Borrower Name": (0, 1, 2),
    "Moody's": (0, 3, 5),
    "S&P": (0, 6, 10),
    "Fitch": (0, 11, 13),
    "Date Estimates": (0, 14, 16)
}

sheet_column_mapper = {
    "Borrower Stats": borrower_stats,
    "Securities Stats": security_stats,
    "US Bank Holdings": {},
    "Client Holdings": {},
    "SOI Mapping": SOI_Mapping,
    "PFLT Borrowing Base": {},
    "PCOF III Borrrowing Base": PCOF_III_BB,
    "PCOF IV": PCOF_IV,
    "MarketBook": MARKET_BOOK,
    # "Sheet1": {},
    "Market and Book Value": {},
    "PSSL II Borrowing Base": PSSL_II_Borrowing_base,
    "Master Ratings": master_rating
}

FUND_SHEETS = {
    'cashfile': ["US Bank Holdings", "Client Holdings"],
    'master_comp': ["Borrower Stats", "Securities Stats", "SOI Mapping", "PFLT Borrowing Base", "PCOF III Borrrowing Base", "PCOF IV"],
    # "market_book": ["Sheet1"],
    "market_book": ["Market and Book Value"]
}

def get_file_sheets(fund, file_type):
    return FUND_SHEETS.get(file_type)

class ExtractionStatusMaster(Enum):
    COMPLETED = 'Completed'
    FAILED = 'Failed'
    PARTIALLY_COMPLETED = 'Partially Completed'
    IN_PROGRESS = 'In Progress'