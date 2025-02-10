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

PCOF_III_BB = {}

PCOF_IV = {}

sheet_column_mapper = {
    "Borrower Stats": borrower_stats,
    "Securities Stats": security_stats,
    "US Bank Holdings": {},
    "Client Holdings": {},
    "SOI Mapping": SOI_Mapping,
    "PFLT Borrowing Base": {},
    "PCOF III Borrrowing Base": PCOF_III_BB,
    "PCOF IV": PCOF_IV
}

FUND_SHEETS = {
    'cashfile': ["US Bank Holdings", "Client Holdings"],
    'master_comp': ["Borrower Stats", "Securities Stats", "SOI Mapping", "PFLT Borrowing Base", "PCOF III Borrrowing Base", "PCOF IV"]
}

def get_file_sheets(fund, file_type):
    return FUND_SHEETS.get(file_type)

class ExtractionStatusMaster(Enum):
    COMPLETED = 'completed'
    FAILED = 'failed'
    PARTIALLY_COMPLETED = 'Partially Completed'
    IN_PROGRESS = 'In progress'