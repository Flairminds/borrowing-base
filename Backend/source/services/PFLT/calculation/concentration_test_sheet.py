from itertools import zip_longest
import pandas as pd

from source.services.concTestService.concTestService import ConcentrationTestExecutor

class PFLT_ConcentrationTest_calculation:
    def Concentration_Sheet_Sheet(self):
        loan_list_df = self.file_df["Loan List"]
        borrowing_base_df = self.file_df["Borrowing Base"]
        
        calculated_df_map = {
            "Loan List": loan_list_df,
            "Borrowing Base": borrowing_base_df,
        }

        concentration_test_executor = ConcentrationTestExecutor(calculated_df_map, "PFLT")
        concentration_test_df = concentration_test_executor.executeConentrationTest()
        self.file_df["Concentration Test"] = concentration_test_df
