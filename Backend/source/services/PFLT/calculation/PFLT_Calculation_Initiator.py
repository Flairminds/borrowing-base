import pandas as pd
import pathlib
from source.services.PFLT.calculation.second_level_formulas import (
    SecondLevelCalculations as SLC,
)
from source.services.PFLT.calculation.borrowing_base_sheet import (
    PFLT_BorrowingBase_calculation as PBC,
)
from source.services.PFLT.calculation.concentration_test_sheet import (
    PFLT_ConcentrationTest_calculation as PCTC,
)


class PFLTCalculationInitiator(SLC, PBC, PCTC):
    """
    Calculation Initiator class. Calculates all the columns in `Loan List` sheet.
    .*args:
        - file_df : Dictionary of DataFrames (Validated Base data )
    """

    def __init__(self):
        SLC.__init__(self)
        PBC.__init__(self)
        PCTC.__init__(self)

    def obligors(self):
        loan_list_df = self.file_df["Loan List"]
        print("Original Loan List DataFrame:")
        # print(loan_list_df.columns)

        obligor_col = "Obligor Name"
        new_values = []
        obligor_count = {}
        current_obligor = 1

        for index, row in loan_list_df.iterrows():
            obligor_name = row[obligor_col]

            if obligor_name in obligor_count:
                new_values.append(obligor_count[obligor_name])
            else:
                obligor_count[obligor_name] = current_obligor
                new_values.append(current_obligor)
                current_obligor += 1

        loan_list_df["Obligor"] = new_values

        print("Updated Loan List DataFrame with Obligor column:")
        # print(loan_list_df)

    def Convertible_to_Equity(self):
        loan_list_df = self.file_df["Loan List"]
        convertible_col = "Convertible to Equity (Y/N)"

        # Create a new column based on the rule =IF(BK11="Yes",1,0)
        loan_list_df["Convertible to Equity"] = loan_list_df[convertible_col].apply(
            lambda x: 1 if x == "Yes" else 0
        )

    def Equity_Security(self):
        loan_list_df = self.file_df["Loan List"]
        equity_security_col = "Equity Security (Y/N)"

        # Create a new column based on the rule =IF(BL11="Yes",1,0)
        loan_list_df["Equity Security"] = loan_list_df[equity_security_col].apply(
            lambda x: 1 if x == "Yes" else 0
        )

    def Subject_to_Offer_or_Redemption(self):
        loan_list_df = self.file_df["Loan List"]
        redemption_col = (
            "At Acquisition - Subject to offer or called for redemption (Y/N)"
        )

        # Create a new column based on the rule =IF(BM14="Yes",1,0)
        loan_list_df["Subject to Offer or Redemption"] = loan_list_df[
            redemption_col
        ].apply(lambda x: 1 if x == "Yes" else 0)

    def Margin_Stock(self):
        loan_list_df = self.file_df["Loan List"]
        margin_stock_col = "Margin Stock (Y/N)"

        # Create a new column based on the rule =IF(BN13="Yes",1,0)
        loan_list_df["Margin Stock"] = loan_list_df[margin_stock_col].apply(
            lambda x: 1 if x == "Yes" else 0
        )

    def Subject_to_withholding_tax(self):
        loan_list_df = self.file_df["Loan List"]

        # Create a new column based on the rule =IF(BO="Yes",1,0)
        loan_list_df["Subject to withholding tax"] = loan_list_df[
            "Subject to withholding tax (Y/N)"
        ].apply(lambda x: 1 if x == "Yes" else 0)

    def At_Acquisition_Defaulted_Collateral_Loan(self):
        loan_list_df = self.file_df["Loan List"]
        loan_list_df["At Acquisition - Defaulted Collateral Loan CK"] = loan_list_df[
            "At Acquisition - Defaulted Collateral Loan"
        ].apply(lambda x: 1 if x == "Yes" else 0)

    def Non_Cash_PIK(self):
        # Assuming the columns are in the "Loan List" sheet
        loan_list_df = self.file_df["Loan List"]
        non_cash_pik_col = "Non-Cash PIK (Y/N)"
        pik_fixed_rate_col = "PIK / PIK'able For Fixed Rate Loans"
        pik_floating_rate_col = "PIK / PIK'able For Floating Rate Loans"
        spread_col = "Spread incl. PIK and PIK'able"

        # Create a new column based on the rule =IF(OR(BQ13="Yes",AND(OR(BA13>0,AZ13>0),(AV13-AZ13-BA13)<2.5%)),1,0)
        loan_list_df["Non-Cash PIK"] = loan_list_df.apply(
            lambda row: (
                1
                if (
                    row[non_cash_pik_col] == "Yes"
                    or (
                        (row[pik_fixed_rate_col] > 0 or row[pik_floating_rate_col] > 0)
                        and (
                            row[spread_col]
                            - row[pik_floating_rate_col]
                            - row[pik_fixed_rate_col]
                        )
                        < 0.025
                    )
                )
                else 0
            ),
            axis=1,
        )

    def Zero_Coupon_Obligation(self):
        loan_list_df = self.file_df["Loan List"]
        loan_list_df["Zero Coupon Obligation"] = loan_list_df[
            "Zero Coupon Obligation (Y/N)"
        ].apply(lambda x: 1 if x == "Yes" else 0)

    def Covenant_Lite(self):
        loan_list_df = self.file_df["Loan List"]

        # Create a new column based on the rule =IF(AND(BS10="Yes",BT10="No"),1,0)
        loan_list_df["Covenant Lite"] = loan_list_df.apply(
            lambda row: (
                1
                if (
                    row["Covenant Lite (Y/N)"] == "Yes"
                    and row["Eligible Covenant Lite (Y/N)"] == "No"
                )
                else 0
            ),
            axis=1,
        )

    def Structured_Finance_Obligation(self):
        loan_list_df = self.file_df["Loan List"]

        loan_list_df["Structured Finance Obligation"] = loan_list_df[
            "Structured Finance Obligation, finance lease or chattel paper (Y/N)"
        ].apply(lambda x: 1 if x == "Yes" else 0)

    def Interest_Paid_Semi_Annually(self):
        loan_list_df = self.file_df["Loan List"]

        # Create a new column based on the rule =IF(OR(BB11<>"Monthly",BB11<>"Quarterly",BB11<>"Semi-Annually"),0,1)
        loan_list_df["Interest Paid Semi Annually"] = loan_list_df.apply(
            lambda row: (
                0
                if row["Interest Paid"] in ["Monthly", "Quarterly", "Semi-Annually"]
                else 1
            ),
            axis=1,
        )

    def Material_Non_Credit_Related_Risk(self):
        loan_list_df = self.file_df["Loan List"]

        # Create a new column based on the rule =IF(BV11="Yes",1,0)
        loan_list_df["Material Non-Credit Related Risk"] = loan_list_df[
            "Material Non-Credit Related Risk (Y/N)"
        ].apply(lambda x: 1 if x == "Yes" else 0)

    def Interest_Only_Security(self):
        loan_list_df = self.file_df["Loan List"]

        # Create a new column based on the rule =IF(BW11="Yes",1,0)
        loan_list_df["Interest Only Security"] = loan_list_df[
            "Interest Only Security (Y/N)"
        ].apply(lambda x: 1 if x == "Yes" else 0)

    def Satisfies_all_Other_Eligibility_Criteria(self):
        loan_list_df = self.file_df["Loan List"]

        # Create a new column based on the rule =IF(BY11="No",1,0)
        loan_list_df["Satisfies all Other Eligibility Criteria"] = loan_list_df[
            "Satisfies all Other Eligibility Criteria (Y/N)"
        ].apply(lambda x: 1 if x == "No" else 0)

    def Foreign_Currency_Variability_Factor(self):
        loan_list_df = self.file_df["Loan List"]

        # Create a new column based on the rule =IF(BD10="EUR",33%,IF(BD10="CAD",38%,IF(BD10="GBP",51%,IF(BD10="AUD",61%,0))))
        loan_list_df["Foreign Currency Variability Factor"] = loan_list_df[
            "Currency (USD / CAD / AUD / EUR)"
        ].apply(
            lambda x: (
                0.33
                if x == "EUR"
                else (
                    0.38
                    if x == "CAD"
                    else 0.51 if x == "GBP" else 0.61 if x == "AUD" else 0
                )
            )
        )

    def PFLTBB_calculation_First_Level_Formulas(self):
        try:

            # Call all functions sequentially
            # self.Loan_Number()
            self.obligors()
            self.Convertible_to_Equity()
            self.Equity_Security()
            self.Subject_to_Offer_or_Redemption()
            self.Margin_Stock()
            self.Subject_to_withholding_tax()
            self.At_Acquisition_Defaulted_Collateral_Loan()
            self.Zero_Coupon_Obligation()
            self.Covenant_Lite()
            self.Structured_Finance_Obligation()
            self.Interest_Paid_Semi_Annually()
            self.Material_Non_Credit_Related_Risk()
            # self.Real_Estate_Construction_or_Project_Finance_Loan()
            self.Interest_Only_Security()
            self.Satisfies_all_Other_Eligibility_Criteria()
            self.Foreign_Currency_Variability_Factor()

            # test add
            self.Specified_Term_SOFR = 0.0532981
            self.Loan_Number()
            self.Cash_Spread_On_Floating_Rate_Loans()  # column BB new
            self.Cash_Spread_On_Fixed_Rate_Loans()  # column BC new
            # calculate all other columns
            self.PFLTBB_calculation_Second_Level_Formulas()

            # calculate borrowing base sheet
            self.Borrowing_Base_Sheet()

            # calculate borrowing base sheet
            self.Concentration_Sheet_Sheet()
            # self.Obligor_new_GX_new_HE()
        except Exception as e:
            print(f"error on line {e.__traceback__.tb_lineno} inside {__file__}")


# file_path = pathlib.Path("PFLT Sub - Borrowing Base - 06.26.24 PF Truist Base.xlsx")
# with file_path.open(mode="rb") as file_obj:
#     file_df = pd.read_excel(file_obj, sheet_name=None)

# Fl = PFLTCalculationInitiator(file_df)
# Fl.PFLTBB_calculation_First_Level_Formulas()
# # Write the final DataFrame back to an Excel file
# output_file_path = "PFLT_Loan_List_Output.xlsx"
# # loan_list_df.to_excel(output_file_path, index=False)
# with pd.ExcelWriter(output_file_path) as writer:
#     for sheet, dataframe in Fl.file_df.items():
#         dataframe.to_excel(writer, sheet_name=sheet, index=False)
