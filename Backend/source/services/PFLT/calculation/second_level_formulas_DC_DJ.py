import pandas as pd
import pathlib
from datetime import datetime
from source.services.PFLT.calculation.excess_concentrations import (
    ExcessConcentrations as EC,
)


class SecondLevelCalculations_DC_DJ(EC):
    def __init__(self):
        self.No_of_Obligor_GL2 = 3
        self.No_of_Obligor_GL3 = 5
        self.Limit_percent_GM2 = 0.067
        self.Limit_percent_GM3 = 0.060
        self.Limit_percent_GM4 = 0.05
        self.No_of_Industry_GC_row1 = 1
        self.GD_Limit_NoOfIndustry_1 = 0.25
        self.GD_Limit_NoOfIndustry_2_and_3 = 0.15
        self.GD_Limit_NoOfIndustry_Other = 0.15
        super().__init__()

    def Aggregate_Collateral_Balance_Post_Eligibility_Including_Haircut_Ineligible_Excluding_Unfunded(
        self,
    ):
        # rule =IF(OR(B10="",DB10>0),0,W10)
        loan_list_df = self.file_df["Loan List"]

        loan_list_df[
            "Aggregate Collateral Balance (Post Eligibility; Including Haircut Ineligible; Excluding Unfunded)"
        ] = loan_list_df.apply(
            lambda row: (
                0
                if pd.isna(row["Loan Number"])
                or row["Loan Number"] == ""
                or row["Total Ineligible (excl. EBITDA and Leverage Ongoing)"] > 0
                else row[
                    "Aggregate Collateral Balance (Pre-Eligibility; Excluding Unfunded; Excluding Principal Acct)"
                ]
            ),
            axis=1,
        )

    def Eligible_Unfunded(self):
        loan_list_df = self.file_df["Loan List"]

        # rule =IF(B10="",0,IF(COUNTIF(CC10:CV10,1)>0,0,L10-M10))
        cc_to_cv_columns = [
            "Purchased Below 85% of Par",
            "Eligible Currency",
            "Eligible Country",
            "Convertible to Equity",
            "Equity Security",
            "Subject to offer or called for redemption",
            "Margin Stock",
            "Subject to withholding tax",
            "At Acquisition - Defaulted Collateral Loan CK",
            "Non-cash PIK",
            "Zero Coupon Obligation",
            "Covenant Lite",
            "Structured Finance Obligation",
            "Remaining term > 7 yrs",
            "Interest Paid Semi Annually",
            "Material Non-Credit Related Risk",
            "Real Estate, Construction or Project Finance Loan",
            "Interest Only Security",
            "Satisfies all Other Eligibility Criteria",
            "EBITDA Requirement at Acquisition",
        ]

        loan_list_df["Eligible Unfunded"] = loan_list_df.apply(
            lambda row: (
                0
                if pd.isna(row["Loan Number"]) or row["Loan Number"] == ""
                else (
                    0
                    if (row[cc_to_cv_columns] == 1).any()
                    else row["Eligible Commitment (USD)"]
                    - row["Eligible Outstanding Principal Balance (USD)"]
                )
            ),
            axis=1,
        )

    def Aggregate_Collateral_Balance_Post_Eligibility_Including_Eligible_Unfunded(self):
        loan_list_df = self.file_df["Loan List"]

        # rule =DC10+IF(DB10>0,0,DD10)
        loan_list_df[
            "Aggregate Collateral Balance (Post Eligibility; Including Eligible Unfunded)"
        ] = loan_list_df.apply(
            lambda row: row[
                "Aggregate Collateral Balance (Post Eligibility; Including Haircut Ineligible; Excluding Unfunded)"
            ]
            + (
                0
                if row["Total Ineligible (excl. EBITDA and Leverage Ongoing)"] > 0
                else row["Eligible Unfunded"]
            ),
            axis=1,
        )

    def Concentration_Test_Balance_OPB__Eligible_Unfunded(self):
        # Concentration Test Balance - OPB + Eligible Unfunded =IF(B10="","",M10+DD10)
        loan_list_df = self.file_df["Loan List"]
        loan_list_df["Concentration Test Balance - OPB + Eligible Unfunded"] = (
            loan_list_df.apply(
                lambda row: (
                    ""
                    if row["Loan Number"] == ""
                    else row["Eligible Outstanding Principal Balance (USD)"]
                    + row["Eligible Unfunded"]
                ),
                axis=1,
            )
        )

    def Revolving_Exposure(self):
        # Revolving Exposure =IF(B10="",0,J10-K10)
        loan_list_df = self.file_df["Loan List"]

        # rule =IF(B10="",0,J10-K10)
        loan_list_df["Revolving Exposure"] = loan_list_df.apply(
            lambda row: (
                0
                if pd.isna(row["Loan Number"]) or row["Loan Number"] == ""
                else row["Total Commitment (USD)"]
                - row["Outstanding Principal Balance (USD)"]
            ),
            axis=1,
        )

    def Foreign_Currency_Loan_OC_Balance(self):
        """
        generate column `Foreign Currency Loan OC Balance` from `Loan List`
        Formula:
        =IF(OR(BD10="EUR",BD10="CAD",BD10="GBP",BD10="AUD"),(FV10*(1-V10))+(GS10)+IF(HJ10="",0,HJ10*(1-U10)),0)
        """
        loan_list_df = self.file_df["Loan List"]

        def calculate_foreign_currency_loan_oc_balance(row):
            if row["Currency (USD / CAD / AUD / EUR)"] in ["EUR", "CAD", "GBP", "AUD"]:
                part1 = row["Excess Concentration Test"] * (1 - row["Advance Rate"])
                part2 = row["Excess Concentration Amount (Dynamic)"]
                part3 = (
                    0
                    if pd.isna(row["Haircut Test"])
                    else row["Haircut Test"] * (1 - row["Applicable Recovery Rate"])
                )
                return part1 + part2 + part3
            else:
                return 0

        # Apply the function to each row
        loan_list_df["Foreign Currency Loan OC Balance"] = loan_list_df.apply(
            calculate_foreign_currency_loan_oc_balance, axis=1
        )

    def Foreign_Currency_Variability_Factor(self):
        """
        generation of column `Foreign Currency Variability Factor` from `Loan List`
        Formula:
        =IF(BD10="EUR",33%,IF(BD10="CAD",38%,IF(BD10="GBP",51%,IF(BD10="AUD",61%,0))))
        """
        loan_list_df = self.file_df["Loan List"]
        loan_list_df["Foreign Currency Variability Factor"] = loan_list_df[
            "Currency (USD / CAD / AUD / EUR)"
        ].apply(
            lambda x: (
                0.33
                if x == "EUR"
                else (
                    0.38
                    if x == "CAD"
                    else (0.51 if x == "GBP" else (0.61 if x == "AUD" else 0))
                )
            )
        )

    def Foreign_Currency_Variability_Reserve(self):
        # Foreign Currency Variability Reserve =DH10*DI10
        loan_list_df = self.file_df["Loan List"]
        loan_list_df["Foreign Currency Variability Reserve"] = (
            loan_list_df["Foreign Currency Loan OC Balance"]
            * loan_list_df["Foreign Currency Variability Factor"]
        )

    def Revolver(self):
        loan_list_df = self.file_df["Loan List"]
        loan_list_df["Revolver"] = loan_list_df.apply(lambda row: "Yes" if row["Loan Type (Term / Delayed Draw / Revolver)"] == "Revolver" else "No", axis=1)

    def ddtl(self):
        loan_list_df = self.file_df["Loan List"]
        loan_list_df["DDTL"] = loan_list_df.apply(lambda row: "Yes" if row["Loan Type (Term / Delayed Draw / Revolver)"] == "Delayed Draw" else "No", axis=1)

    def Paid_Less_than_Qtrly(self):
        loan_list_df = self.file_df["Loan List"]
        loan_list_df["Paid Less than Qtrly"] = loan_list_df.apply(
            lambda row: "Yes" if row["Interest Paid"] != "Semi-Annully" else "No", axis=1
        )

    def PFLTBB_calculation_Second_Level_Formulas_DC_to_DJ(self):
        # try:
        # Perform calculations
        self.Aggregate_Collateral_Balance_Post_Eligibility_Including_Haircut_Ineligible_Excluding_Unfunded()  # column DC
        self.Eligible_Unfunded()  # column DD
        self.Aggregate_Collateral_Balance_Post_Eligibility_Including_Eligible_Unfunded()  # column DE
        self.Concentration_Test_Balance_OPB__Eligible_Unfunded()  # column DF
        self.Revolving_Exposure()  # column DG

        # Calculate 'Borrowing Base'!$J$5  value
        self.total_Concentration_Test_Balance_OPB_Eligible_Unfunded = self.file_df[
            "Loan List"
        ]["Concentration Test Balance - OPB + Eligible Unfunded"].sum()
        # Calculate Excess Concentrations
        self.Calculate_Excess_Concentrations()

        self.Foreign_Currency_Loan_OC_Balance()  # column DH
        self.Foreign_Currency_Variability_Factor()  # column DI
        self.Foreign_Currency_Variability_Reserve()  # column DJ
        self.Revolver()
        self.ddtl()
        self.Paid_Less_than_Qtrly()

    # except Exception as e:
    #     print(f"Error occurred while reading the file: {e}")
    #     return None


# file_path = pathlib.Path("PFLT_Sub_Borrowing_Base_Second_Level_Formulas.xlsx")
# file_obj = file_path.open(mode="rb")
# file_df = pd.read_excel(file_obj, sheet_name=None)

# slc = SecondLevelCalculations_DC_DJ(file_df)
# slc.PFLTBB_calculation_Second_Level_Formulas_DC_to_DJ()

# output_file_path = "PFLT_Sub_Borrowing_Base_Second_Level_Formulas_DC-DJ.xlsx"
# with pd.ExcelWriter(output_file_path) as writer:
#     for sheet, dataframe in slc.self.file_df.items():
#         dataframe.to_excel(writer, sheet_name=sheet, index=False)
