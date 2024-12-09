from itertools import zip_longest
import pandas as pd

from source.concentration_test_application import ConcentrationTestExecutor


class PFLT_ConcentrationTest_calculation:
    def Concentration_Sheet_Sheet(self):
        loan_list_df = self.file_df["Loan List"]
        borrowing_base_df = self.file_df["Borrowing Base"]

        total_borrowing_base = borrowing_base_df.loc[
            borrowing_base_df["Terms"]
            == "BORROWING BASE - (A) minus (B) minus (A)(iv)",
            "Values",
        ].iloc[0]

        # concentration_test_df = pd.DataFrame()
        # concentration_tests = [
        #     "Second Lien and Split Lien",
        #     "Second Lien",
        #     "DIP Collateral Loans",
        #     "Eligible Foreign Country",
        #     "Partial PIK Loan",
        #     "Revolving / Delayed Drawdown",
        #     "Discount Loans",
        #     "Credit Improved Loans",
        #     "Less Than Quarterly Pay",
        #     "Warrants to Purchase Equity Securities",
        #     "LBO Loan with Equity to Cap <25%",
        #     "Participation Interests",
        #     "Eligible Covenant Lite Loans",
        #     "Fixed Rate Loan",
        #     "Agreed Foreign Currency",
        #     "LTM EBITDA < 15,000,000",
        #     "LTM EBITDA >= 5,000,000 but < 7,500,000",
        #     "LTM Snr Debt / EBITDA",
        # ]

        # # concentration_test_df = pd.DataFrame({'CONCENTRATION TEST': concentration_tests})

        # for column in concentration_tests:
        #     current = loan_list_df[column].sum()
        #     limit = 0.10 * total_borrowing_base

        #     row_data = {
        #         "CONCENTRATION TEST": [column],
        #         "Current": [current],
        #         "Limit": [limit],
        #         "Limit %": [0.10],
        #         "Excess": [max([0, current - limit])],
        #     }
        #     row_df = pd.DataFrame(row_data)
        #     concentration_test_df = pd.concat(
        #         [concentration_test_df, row_df], ignore_index=True
        #     )
        #     concentration_test_df.reset_index()

        # loan_list_data_for_concentration = {
        #     "Borrowing Base": [total_borrowing_base],
        #     "Obligor Industry": loan_list_df["Obligor Industry"].tolist(),

        # }

        # loan_list_df_for_concentration = pd.DataFrame(zip_longest(*loan_list_data_for_concentration.values(), fillvalue=None), columns=loan_list_data_for_concentration.keys())
        calculated_df_map = {
            "Loan List": loan_list_df,
            "Borrowing Base": borrowing_base_df,
        }

        concentrationrestExecutor = ConcentrationTestExecutor(calculated_df_map, "PFLT")
        concentration_test_df = concentrationrestExecutor.executeConentrationTest()
        self.file_df["Concentration Test"] = concentration_test_df
