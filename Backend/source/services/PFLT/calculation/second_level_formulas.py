import numpy as np
import pandas as pd
import pathlib
from datetime import datetime
from source.services.PFLT.calculation.second_level_formulas_DC_DJ import (
    SecondLevelCalculations_DC_DJ as SL,
)


class SecondLevelCalculations(SL):

    def __init__(self):
        self.Specified_Term_SOFR = 0.0532981
        super().__init__()
        # second level static values
        print("in SecondLevelCalculations")
        # cell AZ4

    def Rem_Term_to_Maturity(self):
        loan_list_df = self.file_df["Loan List"]
        base_date = pd.Timestamp("2024-06-26")  # need to be chnaged will come from UI

        # Create a new column based on the rule =IF(C10="","",DAYS360("2024-06-26",AO10)/360)
        loan_list_df["Rem. Term to Maturity"] = loan_list_df.apply(
            lambda row: (
                ""
                if pd.isna(row["Obligor Name"])
                or row["Obligor Name"] != row["Obligor Name"]
                or row["Obligor Name"] == ""
                else pd.Timedelta(pd.Timestamp(row["Maturity Date"]) - base_date).days
                / 360
            ),
            axis=1,
        )

    def Remaining_Term_Greater_Than_7_Years(self):
        self.Rem_Term_to_Maturity()  # column AP

        loan_list_df = self.file_df["Loan List"]

        # Create a new column based on the rule =IF(AP10="",0,IF(AP10>7,1,0))
        loan_list_df["Remaining term > 7 yrs"] = loan_list_df[
            "Rem. Term to Maturity"
        ].apply(lambda x: 0 if pd.isna(x) or x == "" else (1 if x > 7 else 0))

    def Exchange_Rate(self):
        loan_list_df = self.file_df["Loan List"]

        # Static exchange rate data
        exchange_rates = {
            "USD": 1.000000,
            "CAD": 0.733800,
            "AUD": 0.665290,
            "EUR": 1.084800,
        }

        # Create a new column based on the rule =IF(B11="","",VLOOKUP(BD11,Inputs!$A$12:$J$15,10,FALSE))
        loan_list_df["Exchange Rate"] = loan_list_df.apply(
            lambda row: (
                ""
                if pd.isna(row["Loan Number"])
                or row["Loan Number"] != row["Loan Number"]
                or row["Loan Number"] == ""
                else exchange_rates.get(row["Currency (USD / CAD / AUD / EUR)"], 0)
            ),
            axis=1,
        )

    def Loan_Number(self):
        loan_list_df = self.file_df["Loan List"]

        # Create a new column based on the rule =IF(D11="","",B10+1)
        loan_list_df["Loan Number"] = loan_list_df.apply(
            lambda row: (
                ""
                if pd.isna(row["Obligor Name"])
                or row["Obligor Name"] != row["Obligor Name"]
                or row["Obligor Name"] == ""
                else (row.name + 1)
            ),
            axis=1,
        )
        # condition = pd.isna(loan_list_df['Obligor Name']) | loan_list_df['Obligor Name'] == ''
        # loan_list_df.loc[condition , "Loan Number"] = list(range(1, len(loan_list_df[condition])+1 ))

    def Total_Commitment_USD(self):
        loan_list_df = self.file_df["Loan List"]

        # Create a new column based on the rule =IF(B10="","",G10*I10)
        loan_list_df["Total Commitment (USD)"] = loan_list_df.apply(
            lambda row: (
                ""
                if pd.isna(row["Loan Number"])
                or row["Loan Number"] != row["Loan Number"]
                or row["Loan Number"] == ""
                else row["Total Commitment (Issue Currency)"] * row["Exchange Rate"]
            ),
            axis=1,
        )

    def EBITDA_Requirement_at_Acquisition(self):
        loan_list_df = self.file_df["Loan List"]

        # Create a new column based on the rule =IF(B10="",0,IF(AK10>=5000000,0,1))
        loan_list_df["EBITDA Requirement at Acquisition"] = loan_list_df.apply(
            lambda row: (
                0
                if pd.isna(row["Loan Number"])
                or row["Loan Number"] != row["Loan Number"]
                or row["Loan Number"] == ""
                else (0 if row["Initial TTM EBITDA"] >= 5000000 else 1)
            ),
            axis=1,
        )

    def Purchased_Below_85_percent_of_Par(self):
        loan_list_df = self.file_df["Loan List"]

        # Create a new column based on the rule =IF(AND(B10<>"",R10<=85%),1,0)
        loan_list_df["Purchased Below 85% of Par"] = loan_list_df.apply(
            lambda row: (
                1
                if (
                    pd.notna(row["Loan Number"])
                    and row["Loan Number"] != ""
                    and row["Purchase Price"] <= 0.85
                )
                else 0
            ),
            axis=1,
        )

    def Outstanding_Principal_Balance_USD(self):
        loan_list_df = self.file_df["Loan List"]

        # Create a new column based on the rule =IF(B10="","",H10*I10)
        loan_list_df["Outstanding Principal Balance (USD)"] = loan_list_df.apply(
            lambda row: (
                ""
                if pd.isna(row["Loan Number"])
                or row["Loan Number"] != row["Loan Number"]
                or row["Loan Number"] == ""
                else row["Outstanding Principal Balance (Issue Currency)"]
                * row["Exchange Rate"]
            ),
            axis=1,
        )

    def Eligible_Commitment_USD(self):
        loan_list_df = self.file_df["Loan List"]

        # Calculate Total_Commitment_USD Column J
        self.Total_Commitment_USD()

        cc_to_cv_columns = [
            "Purchased Below 85% of Par",
            "Eligible Currency",
            "Eligible Country",
            "Convertible to Equity",
            "Equity Security",
            "Subject to offer or called for redemption",
            "Margin Stock",
            "Subject to withholding tax",
            "At Acquisition - Defaulted Collateral Loan",
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

        # Calculate Eligible Commitment USD rule =IF(B10="","",IF(COUNTIF($CC10:$CV10,1)>0,0,J10))
        loan_list_df["Eligible Commitment (USD)"] = loan_list_df.apply(
            lambda row: (
                ""
                if pd.isna(row["Loan Number"]) or row["Loan Number"] == ""
                else (
                    0
                    if (row[cc_to_cv_columns] == 1).any()
                    else row["Total Commitment (USD)"]
                )
            ),
            axis=1,
        )

    def Eligible_Outstanding_Principal_Balance_USD(self):
        loan_list_df = self.file_df["Loan List"]
        # Calculate Outstanding Principal Balance USD column K
        self.Outstanding_Principal_Balance_USD()

        cc_to_cv_columns = [
            "Purchased Below 85% of Par",
            "Eligible Currency",
            "Eligible Country",
            "Convertible to Equity",
            "Equity Security",
            "Subject to offer or called for redemption",
            "Margin Stock",
            "Subject to withholding tax",
            "At Acquisition - Defaulted Collateral Loan",
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
        # Calculate Eligible Outstanding Principal Balance (USD) the rule =IF(B10="","",IF(COUNTIF($CC10:$CV10,1)>0,0,K10))
        loan_list_df["Eligible Outstanding Principal Balance (USD)"] = (
            loan_list_df.apply(
                lambda row: (
                    ""
                    if pd.isna(row["Loan Number"]) or row["Loan Number"] == ""
                    else (
                        0
                        if (row[cc_to_cv_columns] == 1).any()
                        else row["Outstanding Principal Balance (USD)"]
                    )
                ),
                axis=1,
            )
        )

    def Outstanding_Principal_Balance(self):
        loan_list_df = self.file_df["Loan List"]

        # Calculate HA using the rule =IF(B10="","",$M10)
        # where B is Loan Number and M is Eligible Outstanding Principal Balance (USD)
        loan_list_df["Outstanding Principal Balance"] = loan_list_df.apply(
            lambda row: (
                ""
                if pd.isna(row["Loan Number"])
                or row["Loan Number"] != row["Loan Number"]
                or row["Loan Number"] == ""
                else row["Eligible Outstanding Principal Balance (USD)"]
            ),
            axis=1,
        )

    def Initial_Haircut_Level(self):
        loan_list_df = self.file_df["Loan List"]

        def calculate_initial_haircut_level(row):
            if pd.isna(row["Loan Number"]) or row["Loan Number"] == "":
                return ""
            elif row[
                "Lien Type (First Lien / Split First Lien / Split Lien / Second Lien / Tier 1 Split Lien / Tier 2 Split Lien)"
            ] == "Second Lien" and (
                row["Leverage 10% Haircut"] == 1
                or row["Leverage 20% Haircut"] == 1
                or row["Leverage 35% Haircut"] == 1
            ):
                return 0.50
            elif row["Leverage 10% Haircut"] == 1:
                return 0.90
            elif row["Leverage 20% Haircut"] == 1:
                return 0.80
            elif row["Leverage 35% Haircut"] == 1:
                return 0.65
            else:
                return "No Initial Haircut"

        # Apply the function to each row
        loan_list_df["Initial Haircut Level"] = loan_list_df.apply(
            calculate_initial_haircut_level, axis=1
        )

    def Defaulted_Collateral_Loan_Balance(self):
        # rule =IF($N10="Yes",IF(P10>=6,0,MIN($T10*$M10,$U10*$M10)),"")
        loan_list_df = self.file_df["Loan List"]
        loan_list_df["Defaulted Collateral Loan Balance"] = loan_list_df.apply(
            lambda row: (
                ""
                if row["Defaulted Collateral Loan / Material Mod (Y/N)"] != "Yes"
                else (
                    0
                    if row["Months Since Default"] >= 6
                    else min(
                        row["Market Value"]
                        * row["Eligible Outstanding Principal Balance (USD)"],
                        row["Applicable Recovery Rate"]
                        * row["Eligible Outstanding Principal Balance (USD)"],
                    )
                )
            ),
            axis=1,
        )

    def Discount_Loan_Balance(self):
        # rule =IF(AND(N10="Yes",P10>=6),"",IF($S10="Yes",$R10*$M10,""))
        loan_list_df = self.file_df["Loan List"]
        loan_list_df["Discount Loan Balance"] = loan_list_df.apply(
            lambda row: (
                ""
                if (
                    row["Defaulted Collateral Loan / Material Mod (Y/N)"] == "Yes"
                    and row["Months Since Default"] >= 6
                )
                else (
                    row["Purchase Price"]
                    * row["Eligible Outstanding Principal Balance (USD)"]
                    if row["Discount Collateral Loan (Y/N)"] == "Yes"
                    else ""
                )
            ),
            axis=1,
        )

    def Credit_Improved_Balance(self):
        # rule =IF($Q10="Yes",MIN($M10,$T10*$M10),"")
        loan_list_df = self.file_df["Loan List"]
        loan_list_df["Credit Improved Balance"] = loan_list_df.apply(
            lambda row: (
                min(
                    row["Eligible Outstanding Principal Balance (USD)"],
                    row["Market Value"]
                    * row["Eligible Outstanding Principal Balance (USD)"],
                )
                if row["Credit Improved Loan (Y/N)"] == "Yes"
                else ""
            ),
            axis=1,
        )

    def Ineligibles(self):
        # rule =IF(DB10>0,DB10,"")
        loan_list_df = self.file_df["Loan List"]
        loan_list_df["Ineligibles"] = loan_list_df.apply(
            lambda row: (
                row["Total Ineligible (excl. EBITDA and Leverage Ongoing)"]
                if row["Total Ineligible (excl. EBITDA and Leverage Ongoing)"] > 0
                else ""
            ),
            axis=1,
        )

    def Total_Unfunded(self):
        # Total Unfunded =IF(B10="",0,$L10-$M10)
        loan_list_df = self.file_df["Loan List"]
        loan_list_df["Total Unfunded"] = loan_list_df.apply(
            lambda row: (
                0
                if row["Obligor Name"] == ""
                else row["Eligible Commitment (USD)"]
                - row["Eligible Outstanding Principal Balance (USD)"]
            ),
            axis=1,
        )

    def LookupsF2F3_No(self):
        # Lookups'!F2:F3 No =IF(C10="","",INDEX(Lookups!$E$2:$E$69,MATCH('Loan List'!BC10,Lookups!$F$2:$F$69,0)))
        loan_list_df = self.file_df["Loan List"]
        Industry_df = self.file_df["Industry"]

        def lookup_value(row, Industry_df):
            if row["Obligor"] == "":
                return ""
            else:
                match_row = Industry_df[
                    Industry_df["Industry"] == row["Obligor Industry"]
                ]
                if not match_row.empty:
                    return match_row["Industry No"].values[0]
                else:
                    return None

        # Apply the function to each row in the loan list DataFrame
        loan_list_df["Lookups'!F2:F3 No"] = loan_list_df.apply(
            lambda row: lookup_value(row, Industry_df), axis=1
        )

    def APB_Other_Than_Def_Inelib_Restructured_Haircut(self):
        # rule =IF(OR(SUM(HB10:HF10)>0,P10>=6),"",IF($B10="","",1))
        loan_list_df = self.file_df["Loan List"]

        loan_list_df["Loan Eligibility Flag"] = loan_list_df.apply(
            lambda row: (
                ""
                if (
                    row[
                        [
                            "Defaulted Collateral Loan Balance",
                            "Discount Loan Balance",
                            "Credit Improved Balance",
                            "Haircut Ineligible",
                            "Ineligibles",
                        ]
                    ]
                    .replace("", 0)
                    .sum()
                )
                > 0
                or row["Months Since Default"] >= 6
                else (1 if row["Loan Number"] != "" else "")
            ),
            axis=1,
        )

    def Discount_Test(self):
        # Discount Test =IF(AND($HC10<>0,OR(AND($HC10<>$HF10,HC10<>HE10,HC10<>HD10,HC10<>HB10,HC10<MIN(HD10:HF10)),SUM(HB10)+SUM(HD10:HF10)=0)),$HC10,0)
        loan_list_df = self.file_df["Loan List"]
        loan_list_df["Discount Test"] = loan_list_df.apply(
            lambda row: (
                row["Discount Loan Balance"]
                if (
                    row["Discount Loan Balance"] != 0
                    and (
                        (
                            row["Discount Loan Balance"] != row["Ineligibles"]
                            and row["Discount Loan Balance"]
                            != row["Haircut Ineligible"]
                            and row["Discount Loan Balance"]
                            != row["Credit Improved Balance"]
                            and row["Discount Loan Balance"]
                            != row["Defaulted Collateral Loan Balance"]
                            and row["Discount Loan Balance"]
                            < min(row["Credit Improved Balance"], row["Ineligibles"])
                        )
                        or (
                            row["Defaulted Collateral Loan Balance"]
                            + row[
                                [
                                    "Credit Improved Balance",
                                    "Haircut Ineligible",
                                    "Ineligibles",
                                ]
                            ].sum()
                            == 0
                        )
                    )
                )
                else 0
            ),
            axis=1,
        )

    def Ineligibles_Test(self):
        # Ineligibles Test =IF(AND($HF10<>0,OR(HF10<=MIN(HB10:HE10),SUM(HB10:HE10)=0)),$HF10,0)
        loan_list_df = self.file_df["Loan List"]

        # Ensure numeric conversion, coercing errors to NaN
        loan_list_df[
            [
                "Defaulted Collateral Loan Balance",
                "Discount Loan Balance",
                "Credit Improved Balance",
                "Haircut Ineligible",
                "Ineligibles",
            ]
        ] = loan_list_df[
            [
                "Defaulted Collateral Loan Balance",
                "Discount Loan Balance",
                "Credit Improved Balance",
                "Haircut Ineligible",
                "Ineligibles",
            ]
        ].apply(
            pd.to_numeric, errors="coerce"
        )

        loan_list_df["Ineligibles Test"] = loan_list_df.apply(
            lambda row: (
                row["Ineligibles"]
                if (
                    row["Ineligibles"] != 0
                    and (
                        row["Ineligibles"]
                        <= min(
                            row["Defaulted Collateral Loan Balance"],
                            row["Discount Loan Balance"],
                            row["Credit Improved Balance"],
                            row["Haircut Ineligible"],
                        )
                        or row[
                            [
                                "Defaulted Collateral Loan Balance",
                                "Discount Loan Balance",
                                "Credit Improved Balance",
                                "Haircut Ineligible",
                            ]
                        ].sum()
                        == 0
                    )
                )
                else 0
            ),
            axis=1,
        )

    def Credit_Improved_Test(self):
        loan_list_df = self.file_df["Loan List"]

        def calculate_credit_improved_test(row):
            if row["Credit Improved Balance"] != 0:
                # Evaluate the OR conditions
                condition1 = (
                    row["Credit Improved Balance"] != row["Ineligibles"]
                    and row["Credit Improved Balance"] != row["Haircut Ineligible"]
                    and (
                        row["Credit Improved Balance"] != row["Discount Loan Balance"]
                        and row["Credit Improved Balance"]
                        != row["Defaulted Collateral Loan Balance"]
                    )
                )
                condition2 = row["Credit Improved Balance"] < min(
                    row["Defaulted Collateral Loan Balance"],
                    row["Discount Loan Balance"],
                )
                condition3 = row["Credit Improved Balance"] < min(
                    row["Haircut Ineligible"], row["Ineligibles"]
                )
                condition4 = (
                    row["Defaulted Collateral Loan Balance"]
                    + row["Discount Loan Balance"]
                    + row["Haircut Ineligible"]
                    + row["Ineligibles"]
                ) == 0

                if condition1 or condition2 or condition3 or condition4:
                    return row["Credit Improved Balance"]
            return 0

        # Apply the function to each row
        loan_list_df["Credit Improved Test"] = loan_list_df.apply(
            calculate_credit_improved_test, axis=1
        )

    def Haircut_Test(self):
        # =IF(
        #   AND(
        #           $HE10<>0,
        #               OR(
        #                      AND(
        #                           $HE10<>$HF10,
        #                           $HE10<>$HD10,
        #                           $HE10<>$HC10,
        #                           $HE10<>$HB10,
        #                           $HE10<MIN($HB10:$HD10),$HE10<HF10),SUM($HB10:$HD10)
        # +SUM(HF10)=0),HM10<=0),$HE10,0)
        loan_list_df = self.file_df["Loan List"]

        loan_list_df["Haircut Test"] = loan_list_df.apply(
            lambda row: (
                row["Haircut Ineligible"]
                if (
                    row["Haircut Ineligible"] != 0
                    and (
                        (
                            row["Haircut Ineligible"] != row["Ineligibles"]
                            and row["Haircut Ineligible"]
                            != row["Credit Improved Balance"]
                            and row["Haircut Ineligible"]
                            != row["Discount Loan Balance"]
                            and row["Haircut Ineligible"]
                            != row["Defaulted Collateral Loan Balance"]
                            and row["Haircut Ineligible"]
                            < row[
                                [
                                    "Defaulted Collateral Loan Balance",
                                    "Discount Loan Balance",
                                    "Credit Improved Balance",
                                ]
                            ].min(skipna=True)
                            or row["Haircut Ineligible"] < (row["Ineligibles"] if pd.notna(row["Ineligibles"]) and row["Ineligibles"] != "" else 0)
                        )
                        or (
                            row[
                                [
                                    "Defaulted Collateral Loan Balance",
                                    "Discount Loan Balance",
                                    "Credit Improved Balance",
                                    "Ineligibles",
                                ]
                            ].sum()
                            == 0
                        )
                    )
                    and row["Defaulted Test"] <= 0.0
                )
                else 0
            ),
            axis=1,
        )

    def Defaulted_Test(self):
        # rule =IF(AND($HB10<>0,OR(HB10<=MIN(HC10:HF10),SUM(HC10:HF10)=0)),$HB10,0)
        loan_list_df = self.file_df["Loan List"]

        loan_list_df["Defaulted Test"] = loan_list_df.apply(
            lambda row: (
                row["Defaulted Collateral Loan Balance"]
                if (
                    row["Defaulted Collateral Loan Balance"] != 0
                    and (
                        row["Defaulted Collateral Loan Balance"]
                        <= row[
                            [
                                "Discount Loan Balance",
                                "Credit Improved Balance",
                                "Haircut Ineligible",
                                "Ineligibles",
                            ]
                        ].min(skipna=True)
                        or (
                            row[
                                [
                                    "Discount Loan Balance",
                                    "Ineligibles",
                                    "Credit Improved Balance",
                                    "Haircut Ineligible",
                                ]
                            ].sum()
                            == 0
                        )
                    )
                )
                else 0
            ),
            axis=1,
        )

    def Aggregate_Collateral_Balance_Pre_Eligibility_Excl_Unfunded_Excl_Principal_Acct(
        self,
    ):
        loan_list_df = self.file_df["Loan List"]

        self.LookupsF2F3_No()  # column HN
        self.Outstanding_Principal_Balance()  # Column HA
        self.Months_Since_Default()  # calculate Months Since Default column P
        self.Applicable_Recovery_Rate()  # calculate Applicable Recovery Rate column U
        self.Defaulted_Collateral_Loan_Balance()  # column HB
        self.Discount_Loan_Balance()  # column HC
        self.Credit_Improved_Balance()  # column HD
        self.Initial_Haircut_Level()  # column HQ
        self.Haircut_Ineligible()  # column HE

        # Calculate the column =IF($C10="","",MIN($HA10:$HE10))
        loan_list_df[
            [
                "Outstanding Principal Balance",
                "Defaulted Collateral Loan Balance",
                "Discount Loan Balance",
                "Credit Improved Balance",
                "Haircut Ineligible",
            ]
        ] = loan_list_df[
            [
                "Outstanding Principal Balance",
                "Defaulted Collateral Loan Balance",
                "Discount Loan Balance",
                "Credit Improved Balance",
                "Haircut Ineligible",
            ]
        ].apply(
            pd.to_numeric, errors="coerce"
        )
        loan_list_df[
            "Aggregate Collateral Balance (Pre-Eligibility; Excluding Unfunded; Excluding Principal Acct)"
        ] = loan_list_df.apply(
            lambda row: (
                ""
                if pd.isna(row["Obligor"])
                or row["Obligor"] != row["Obligor"]
                or row["Obligor"] == ""
                else row[
                    [
                        "Outstanding Principal Balance",
                        "Defaulted Collateral Loan Balance",
                        "Discount Loan Balance",
                        "Credit Improved Balance",
                        "Haircut Ineligible",
                    ]
                ]
                .replace("", None)
                .min(skipna=True)
            ),
            axis=1,
        )

        # loan_list_df = self.file_df["Loan List"]
        # loan_list_df['Aggregate Collateral Balance (Pre-Eligibility; Excluding Unfunded; Excluding Principal Acct)'] = loan_list_df[['Outstanding Principal Balance', 'Defaulted Collateral Loan Balance', 'Discount Loan Balance', 'Credit Improved Balance', 'Haircut Ineligible']].min()

        self.Total_Ineligible_excl_EBITDA_and_Leverage_Ongoing()  # Calculation for Total Ineligible excluding EBITDA and Leverage Ongoing (Column DB)
        self.Ineligibles()  # column HF
        self.Total_Unfunded()  # column HG
        self.APB_Other_Than_Def_Inelib_Restructured_Haircut()  # column HH
        self.Ineligibles_Test()  # column HI
        self.Defaulted_Test()  # column HM
        self.Haircut_Test()  # column HJ
        self.Credit_Improved_Test()  # column HK
        self.Discount_Test()  # column HL

    def Total_Ineligible_excl_EBITDA_and_Leverage_Ongoing(self):
        loan_list_df = self.file_df["Loan List"]

        # cc - cv
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
        loan_list_df["sum_cc_to_cv"] = loan_list_df[cc_to_cv_columns].sum(axis=1)

        # print(loan_list_df[cc_to_cv_columns].any())

        # Create a new column based on the rule =IF((SUM(CC10:CV10)=0),0,W10)
        loan_list_df["Total Ineligible (excl. EBITDA and Leverage Ongoing)"] = (
            loan_list_df.apply(
                lambda row: (
                    0
                    if row["sum_cc_to_cv"] == 0 or row["sum_cc_to_cv"] == 0.0
                    else row[
                        "Aggregate Collateral Balance (Pre-Eligibility; Excluding Unfunded; Excluding Principal Acct)"
                    ]
                ),
                axis=1,
            )
        )
        loan_list_df.drop(columns=["sum_cc_to_cv"], inplace=True)

    def Months_Since_Default(self):
        loan_list_df = self.file_df["Loan List"]

        # Static date for Borrowing Base
        borrowing_base_date = datetime.strptime("6/26/24", "%m/%d/%y")

        # Create a new column based on the rule =IF(B10="","",IF(OR(O10="N/A",O10=""),0,YEARFRAC('Borrowing Base'!$J$4,'Loan List'!O10)*12))
        loan_list_df["Months Since Default"] = loan_list_df.apply(
            lambda row: (
                0
                if pd.isna(row["Date of Default"])
                or row["Date of Default"] in ["N/A", ""]
                else (borrowing_base_date - row["Date of Default"]).days / 30
            ),
            axis=1,
        )

    # Function to calculate EBITDA Requirement Ongoing
    def EBITDA_Requirement_Ongoing(self):
        loan_list_df = self.file_df["Loan List"]

        # Create a new column based on the rule =IF(B10="",0,IF(AL10>=5000000,0,1))
        loan_list_df["EBITDA Requirement Ongoing"] = loan_list_df.apply(
            lambda row: (
                0
                if pd.isna(row["Loan Number"])
                or row["Loan Number"] != row["Loan Number"]
                or row["Loan Number"] == ""
                else (0 if row["Current TTM EBITDA"] >= 5000000 else 1)
            ),
            axis=1,
        )

    def Applicable_Recovery_Rate(self):
        loan_list_df = self.file_df["Loan List"]

        # Create a new column based on the rule =IF(B10="","",IF(OR(Y10="First Lien",Y10="Split First Lien",Y10="Split Lien"),50%,30%))
        loan_list_df["Applicable Recovery Rate"] = loan_list_df.apply(
            lambda row: (
                0
                if pd.isna(row["Loan Number"])
                or row["Loan Number"] != row["Loan Number"]
                or row["Loan Number"] == ""
                else (
                    0.50
                    if row[
                        "Lien Type (First Lien / Split First Lien / Split Lien / Second Lien / Tier 1 Split Lien / Tier 2 Split Lien)"
                    ]
                    in [
                        "First Lien",
                        "Split First Lien",
                        "Tier 1 Split Lien",
                        "Tier 2 Split Lien",
                    ]
                    else 0.30
                )
            ),
            axis=1,
        )

    def Tier_1_Tier_2_Obligor(self):
        loan_list_df = self.file_df["Loan List"]

        # Create a new column based on the rule =IF(C10="","",(IF(AK10>=50000000,"Tier 1",
        # (IF(OR(AK10>=20000000,AND(AK10>5000000,AC10>=1.25,AF10<=0.65)),"Tier 2","Tier 3")))))
        loan_list_df["Tier 1 / Tier 2 Obligor"] = loan_list_df.apply(
            lambda row: (
                ""
                if pd.isna(row["Obligor Name"])
                or row["Obligor Name"] != row["Obligor Name"]
                or row["Obligor Name"] == ""
                else (
                    "Tier 1"
                    if row["Initial TTM EBITDA"] >= 50000000
                    else (
                        "Tier 2"
                        if (
                            row["Initial TTM EBITDA"] >= 20000000
                            or (
                                row["Initial TTM EBITDA"] > 5000000
                                and row["Initial Fixed Charge Coverage Ratio"] >= 1.25
                                and row["Debt to Capitalization Ratio"] <= 0.65
                            )
                        )
                        else "Tier 3"
                    )
                )
            ),
            axis=1,
        )

    def Leverage_Final_Haircut_50_percent(self):
        """
        calculate the column Leverage Final Haircut 50% rule (DA in Loan List)
        Formula `=IF(B25="",0,IF(OR(AND(AN25="Tier 1",X25="No",OR(AI25>$AS$3,AJ25>$AS$4)),(AND(AN25="Tier 1",X25="Yes",AJ25>$AS$5)),(AND(AN25="Tier 2",X25="No",OR(AI25>$AT$3,AJ25>$AT$4))),(AND(AN25="Tier 2",X25="Yes",AJ25>$AT$5)),(AND(AN25="Tier 3",X25="No",OR(AI25>$AU$3,AJ25>$AU$4))),(AND(AN25="Tier 3",X25="Yes",AJ25>$AU$5))),1,0))`
        where B = Loan Number
        AN = Tier 1 / Tier 2 Obligor
        X = Stretch Senior Loan (Y/N)
        AI = Current Senior Debt/EBITDA
        AJ = Coupon (if Fixed)
        AT = Current Total Debt/EBITDA
        AU = Floor Obligation (Y/N)

        """
        # Level 4 - Max Eligibility - 50% Haircut
        #### (ROW_INDEX, COLUMN_INDEX)
        level4_tier1_row1_location = (1, 13)
        level4_tier1_row2_location = (2, 13)
        level4_tier1_row3_location = (3, 13)
        level4_tier2_row1_location = (1, 14)
        level4_tier2_row2_location = (2, 14)
        level4_tier2_row3_location = (3, 14)
        level4_tier3_row1_location = (1, 15)
        level4_tier3_row2_location = (2, 15)
        level4_tier3_row3_location = (3, 15)
        # Load dataframes
        loan_list_df = self.file_df["Loan List"]
        haircut_df = self.file_df["Haircut"]

        loan_list_df["Leverage - Final Haircut - 50%"] = loan_list_df.apply(
            lambda row: (
                0
                if pd.isna(row["Loan Number"])
                or row["Loan Number"] != row["Loan Number"]
                or row["Loan Number"] == ""
                else (
                    1
                    if (
                        row["Tier 1 / Tier 2 Obligor"] == "Tier 1"
                        and row["Stretch Senior Loan (Y/N)"] == "No"
                        and (
                            row["Current Senior Debt/EBITDA"]
                            > haircut_df.iat[level4_tier1_row1_location]
                            or row["Current Total Debt/EBITDA"]
                            > haircut_df.iat[level4_tier1_row2_location]
                        )
                    )
                    or (
                        row["Tier 1 / Tier 2 Obligor"] == "Tier 1"
                        and row["Stretch Senior Loan (Y/N)"] == "Yes"
                        and row["Current Total Debt/EBITDA"]
                        > haircut_df.iat[level4_tier1_row3_location]
                    )
                    or (
                        row["Tier 1 / Tier 2 Obligor"] == "Tier 2"
                        and row["Stretch Senior Loan (Y/N)"] == "No"
                        and (
                            row["Current Senior Debt/EBITDA"]
                            > haircut_df.iat[level4_tier2_row1_location]
                            or row["Current Total Debt/EBITDA"]
                            > haircut_df.iat[level4_tier2_row2_location]
                        )
                    )
                    or (
                        row["Tier 1 / Tier 2 Obligor"] == "Tier 2"
                        and row["Stretch Senior Loan (Y/N)"] == "Yes"
                        and row["Current Total Debt/EBITDA"]
                        > haircut_df.iat[level4_tier2_row3_location]
                    )
                    or (
                        row["Tier 1 / Tier 2 Obligor"] == "Tier 3"
                        and row["Stretch Senior Loan (Y/N)"] == "No"
                        and (
                            row["Current Senior Debt/EBITDA"]
                            > haircut_df.iat[level4_tier3_row1_location]
                            or row["Current Total Debt/EBITDA"]
                            > haircut_df.iat[level4_tier3_row2_location]
                        )
                    )
                    or (
                        row["Tier 1 / Tier 2 Obligor"] == "Tier 3"
                        and row["Stretch Senior Loan (Y/N)"] == "Yes"
                        and row["Current Total Debt/EBITDA"]
                        > haircut_df.iat[level4_tier3_row3_location]
                    )
                    else 0
                )
            ),
            axis=1,
        )

    def Haircut_Ineligible(self):
        loan_list_df = self.file_df["Loan List"]

        # Define a function to calculate the 'Haircut Ineligible' column
        def calculate_haircut_ineligible(row):
            if (
                row["Defaulted Collateral Loan / Material Mod (Y/N)"] == "Yes"
                and row["Months Since Default"] >= 6
            ):
                return ""
            elif (
                row["EBITDA Requirement Ongoing"] == 1
                or row["Leverage - Final Haircut - 50%"] == 1
            ):
                return min(
                    row["Market Value"]
                    * row["Eligible Outstanding Principal Balance (USD)"],
                    row["Applicable Recovery Rate"]
                    * row["Eligible Outstanding Principal Balance (USD)"],
                )
            elif (
                row["Leverage 10% Haircut"] == 1
                or row["Leverage 20% Haircut"] == 1
                or row["Leverage 35% Haircut"] == 1
            ):
                if row["Initial TTM EBITDA"] >= 5000000:
                    return min(
                        row["Market Value"]
                        * row["Eligible Outstanding Principal Balance (USD)"],
                        row["Initial Haircut Level"]
                        * row["Eligible Outstanding Principal Balance (USD)"],
                    )
                else:
                    return min(
                        row["Market Value"]
                        * row["Eligible Outstanding Principal Balance (USD)"],
                        row["Applicable Recovery Rate"]
                        * row["Eligible Outstanding Principal Balance (USD)"],
                    )
            else:
                return ""

        # Apply the function to each row
        loan_list_df["Haircut Ineligible"] = loan_list_df.apply(
            calculate_haircut_ineligible, axis=1
        )

    def Aggregate_Unfunded_Spread(self):
        loan_list_df = self.file_df["Loan List"]
        # loan_list_df = self.file_df["Loan List"]
        self.Exchange_Rate()  # Column I

        # Create column based on the rule =IF(B10="","",AY10*(L10-M10)*IF(DB10>0,0,1))
        # Calculate Purchased_Below_85_percent_of_Par Column CC
        self.Purchased_Below_85_percent_of_Par()

        # Calculation for Eligible Commitment USD (Column L)
        self.Eligible_Commitment_USD()

        # Calculation for Eligible Outstanding Principal Balance (USD) (Column M)
        self.Eligible_Outstanding_Principal_Balance_USD()

        # Calculate Aggregate Collateral Balance Pre Eligibility Excl Unfunded Excl Principal Acct
        self.Aggregate_Collateral_Balance_Pre_Eligibility_Excl_Unfunded_Excl_Principal_Acct()  # Column W

        # Calculation for Aggregate Unfunded Spread (Column CA)
        loan_list_df["Aggregate Unfunded Spread"] = loan_list_df.apply(
            lambda row: (
                ""
                if pd.isna(row["Loan Number"])
                or row["Loan Number"] != row["Loan Number"]
                or row["Loan Number"] == ""
                else row["For Revolvers/Delayed Draw, commitment or other unused fee"]
                * (
                    row["Eligible Commitment (USD)"]
                    - row["Eligible Outstanding Principal Balance (USD)"]
                )
                * (
                    0
                    if row["Total Ineligible (excl. EBITDA and Leverage Ongoing)"] > 0
                    else 1
                )
            ),
            axis=1,
        )

    def Greater_of_Base_Rate_and_Floor(self):
        loan_list_df = self.file_df["Loan List"]
        loan_list_df["Floor"] = (
            loan_list_df["Floor"].fillna(0.0).replace("", 0.0, inplace=True)
        )
        loan_list_df["Floor"].replace(to_replace=[None], value=0.0, inplace=True)
        loan_list_df["Base Rate"] = (
            loan_list_df["Base Rate"].fillna(0.0).replace("", 0.0, inplace=True)
        )
        loan_list_df["Base Rate"].replace(to_replace=[None], value=0.0, inplace=True)
        # # =IF(C11="","",MAX(AU11,AW11))
        loan_list_df["Greater of Base Rate and Floor"] = loan_list_df.apply(
            lambda row: (
                "" if row["Obligor"] == "" else max(row["Floor"], row["Base Rate"])
            ),
            axis=1,
        )

    def Aggregate_Funded_Spread(self):
        loan_list_df = self.file_df["Loan List"]
        # =IF(B10="","",IF(AT10="No",((AV10+AW10-AZ10-BA10)-$AZ$4),((AV10+AX10-AZ10-BA10)-$AZ$4))*IF(DB10>0,0,M10))

        self.Greater_of_Base_Rate_and_Floor()  # Column AX

        loan_list_df["Aggregate Funded Spread"] = loan_list_df.apply(
            lambda row: (
                ""
                if row["Loan Number"] == ""
                else (
                    (
                        (
                            row["Spread incl. PIK and PIK'able"]
                            + row["Base Rate"]
                            - row["PIK / PIK'able For Floating Rate Loans"]
                            - row["PIK / PIK'able For Fixed Rate Loans"]
                        )
                        - self.Specified_Term_SOFR
                    )
                    if row["Floor Obligation (Y/N)"] == "No"
                    else (
                        (
                            row["Spread incl. PIK and PIK'able"]
                            + row["Greater of Base Rate and Floor"]
                            - row["PIK / PIK'able For Floating Rate Loans"]
                            - row["PIK / PIK'able For Fixed Rate Loans"]
                        )
                        - self.Specified_Term_SOFR
                    )
                )
                * (
                    0
                    if row["Total Ineligible (excl. EBITDA and Leverage Ongoing)"] > 0
                    else row["Eligible Outstanding Principal Balance (USD)"]
                )
            ),
            axis=1,
        )

    def Discount_Collateral_Loan_Y_N(self):
        # Discount Collateral Loan (Y/N) = IF(B13="","",IF(R13<95%,"Yes","No"))
        loan_list_df = self.file_df["Loan List"]
        loan_list_df["Discount Collateral Loan (Y/N)"] = loan_list_df.apply(
            lambda row: (
                ""
                if row["Loan Number"] == ""
                else ("Yes" if row["Purchase Price"] < 0.95 else "No")
            ),
            axis=1,
        )

    def Avg_Life(self):
        loan_list_df = self.file_df["Loan List"]
        # Calculate Avg Life rule =IF(C10="","",AP10)
        loan_list_df["Avg Life"] = loan_list_df.apply(
            lambda row: "" if row["Obligor"] == "" else row["Rem. Term to Maturity"],
            axis=1,
        )

    def Cash_Spread_On_Floating_Rate_Loans(self):
        # =IF(B10="","",IF(AR10="No",AV10-AZ10,""))

        loan_list_df = self.file_df["Loan List"]
        loan_list_df["Cash Spread On Floating Rate Loans"] = loan_list_df.apply(
            lambda row: (
                ""
                if pd.isna(row["Loan Number"]) or row["Loan Number"] == ""
                else (
                    row["Spread incl. PIK and PIK'able"]
                    - row["PIK / PIK'able For Floating Rate Loans"]
                    if row["Fixed Rate (Y/N)"] == "No"
                    else ""
                )
            ),
            axis=1,
        )

    def Cash_Spread_On_Fixed_Rate_Loans(self):
        # =IF(B10="","",IF(AR10="Yes",AS10-BA10,""))

        loan_list_df = self.file_df["Loan List"]
        loan_list_df["Cash Spread On Fixed Rate Loans"] = loan_list_df.apply(
            lambda row: (
                ""
                if pd.isna(row["Loan Number"]) or row["Loan Number"] == ""
                else (
                    row["Coupon incl. PIK and PIK'able (if Fixed)"]
                    - row["PIK / PIK'able For Fixed Rate Loans"]
                    if row["Fixed Rate (Y/N)"] == "Yes"
                    else 0
                )
            ),
            axis=1,
        )

    def Partial_PIK_Loan_Y_N(self):
        # =IF(B10="","",IF(OR(AND(AZ10>0,BB10>=2.5%,BB10<4.5%),AND(BA10>0,BC10>=6%,BC10<8%)),"Yes","No"))

        loan_list_df = self.file_df["Loan List"]
        loan_list_df["Partial PIK Loan (Y/N)"] = loan_list_df.apply(
            lambda row: (
                ""
                if pd.isna(row["Loan Number"]) or row["Loan Number"] == ""
                else (
                    "Yes"
                    if (
                        row["PIK / PIK'able For Floating Rate Loans"] > 0
                        and row["Cash Spread On Floating Rate Loans"] >= 0.025
                        and row["Cash Spread On Floating Rate Loans"] < 0.045
                    )
                    or (
                        row["PIK / PIK'able For Fixed Rate Loans"] > 0.0
                        and row["Cash Spread On Fixed Rate Loans"] >= 0.06
                        and row["Cash Spread On Fixed Rate Loans"] < 0.08
                    )
                    else "No"
                )
            ),
            axis=1,
        )

    def Non_Cash_PIK_Loan_Y_N(self):
        # =IF(B10="","",IF(OR(AND(AZ10>0,BB10<2.5%),AND(BA10>0,BC10<6%)),"Yes","No"))

        loan_list_df = self.file_df["Loan List"]
        loan_list_df["Non-Cash PIK Loan (Y/N)"] = loan_list_df.apply(
            lambda row: (
                ""
                if pd.isna(row["Loan Number"]) or row["Loan Number"] == ""
                else (
                    "Yes"
                    if row["PIK / PIK'able For Floating Rate Loans"] > 0.0
                    and row["Cash Spread On Floating Rate Loans"] < 0.025
                    or row["PIK / PIK'able For Fixed Rate Loans"] > 0.0
                    and row["Cash Spread On Fixed Rate Loans"] < 0.06
                    else "No"
                )
            ),
            axis=1,
        )

    def Eligible_Country(self):
        loan_list_df = self.file_df["Loan List"]

        country_list = [
            "Norway",
            "Luxemborg",
            "Lichtenstein",
            "Ireland",
            "Iceland",
            "Finland",
            "Denmark",
            "Belgium",
            "Austria",
            "Switzerland",
            "Sweden",
            "Germany",
            "Netherlands",
            "Bermuda",
            "Cayman Islands",
            "British Virgin Islands",
            "Isle of Man",
            "Channel Islands",
            "United States",
            "Canada",
            "Australia",
            "United Kingdom",
            "Netherlands Antilles",
        ]

        # Calculate Eligible Country rule =IF(B11="",0,(IF(OR(BE11="United States",BE11="Canada",BE11="United Kingdom",BE11="Australia",BE11="Netherlands Antilles",BE11="Bermuda",BE11="Cayman Islands",BE11="British Virgin Islands",BE11="Channel Islands",BE11="Isle of Man",BE11="Australia",BE11="Netherlands",BE11="Germany",BE11="Sweden",BE11="Switzerland",BE11="Austria",BE11="Belgium",BE11="Denmark",
        # BE11="Finland",BE11="Iceland",BE11="Ireland",BE11="Lichtenstein",BE11="Luxemborg",BE11="Norway"),0,1)))
        loan_list_df["Eligible Country"] = loan_list_df.apply(
            lambda row: (
                0
                if row["Obligor"] == ""
                else (0 if row["Obligor Country"] in country_list else 1)
            ),
            axis=1,
        )

    def Eligible_Currency(self):
        #  Eligible Currency =IF(C12="",0,(IF(OR(BD12="USD",BD12="CAD",BD12="GBP",BD12="AUD",BD12="EUR"),0,1)))
        loan_list_df = self.file_df["Loan List"]
        loan_list_df["Eligible Currency"] = loan_list_df.apply(
            lambda row: (
                0
                if row["Obligor"] == ""
                else (
                    0
                    if row["Currency (USD / CAD / AUD / EUR)"]
                    in ["USD", "CAD", "GBP", "AUD", "EUR"]
                    else 1
                )
            ),
            axis=1,
        )

    def Equity_Security(self):
        loan_list_df = self.file_df["Loan List"]
        loan_list_df["Equity Security"] = loan_list_df.apply(
            lambda row: 1 if row["Equity Security (Y/N)"] == "Yes" else 0, axis=1
        )

    def Subject_to_offer_or_called_for_redemption(self):
        # Subject to offer or called for redemption =IF(BM14="Yes",1,0)
        loan_list_df = self.file_df["Loan List"]
        loan_list_df["Subject to offer or called for redemption"] = loan_list_df.apply(
            lambda row: (
                1
                if row[
                    "At Acquisition - Subject to offer or called for redemption (Y/N)"
                ]
                == "Yes"
                else 0
            ),
            axis=1,
        )

    def Margin_Stock(self):
        # Margin Stock = IF(BN14="Yes",1,0)
        loan_list_df = self.file_df["Loan List"]
        loan_list_df["Margin Stock"] = loan_list_df.apply(
            lambda row: 1 if row["Margin Stock (Y/N)"] == "Yes" else 0, axis=1
        )

    def Subject_To_Witholding_Tax(self):
        # Convertible to Equity =
        loan_list_df = self.file_df["Loan List"]
        loan_list_df["Subject to withholding tax"] = loan_list_df.apply(
            lambda row: 1 if row["Subject to withholding tax (Y/N)"] == "Yes" else 0,
            axis=1,
        )

    def Non_cash_PIK(self):
        loan_list_df = self.file_df["Loan List"]
        # Apply the rule =IF(OR(BQ10="Yes",AND(OR(BA10>0,AZ10>0),(AV10-AZ10-BA10)<2.5%)),1,0)
        loan_list_df["Non-cash PIK"] = loan_list_df.apply(
            lambda row: (1 if row["Non-Cash PIK Loan (Y/N)"] == "Yes" else 0),
            axis=1,
        )

    def At_Acquisition_Defaulted_Collateral_Loan(self):
        # At Acquisition - Defaulted Collateral Loan =IF(BP11="Yes",1,0)
        loan_list_df = self.file_df["Loan List"]
        loan_list_df["At Acquisition - Defaulted Collateral Loan CK"] = (
            loan_list_df.apply(
                lambda row: (
                    1
                    if (row["At Acquisition - Defaulted Collateral Loan"] == "Yes")
                    else 0
                ),
                axis=1,
            )
        )

    def Covenant_Lite(self):
        # Covenant Lite rule =IF(AND(BS10="Yes",BT10="No"),1,0)
        loan_list_df = self.file_df["Loan List"]
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
        # Structured_Finance_Obligation rule =IF(BU10="Yes",1,0)
        loan_list_df["Structured Finance Obligation"] = loan_list_df.apply(
            lambda row: (
                1
                if (
                    row[
                        "Structured Finance Obligation, finance lease or chattel paper (Y/N)"
                    ]
                    == "Yes"
                )
                else 0
            ),
            axis=1,
        )

    def Zero_Coupon_Obligation(self):
        """
        generation of column `Zero Coupon Obligation` from `Loan List` column CM
        Formula:
        =IF(BR10="Yes",1,0)
        """
        loan_list_df = self.file_df["Loan List"]
        loan_list_df["Zero Coupon Obligation"] = loan_list_df.apply(
            lambda row: 1 if row["Zero Coupon Obligation (Y/N)"] == "Yes" else 0, axis=1
        )

    def Interest_Paid_Semi_Annually(self):
        # Interest Paid Semi Annually rule =IF(OR(BB10<>"Monthly",BB10<>"Quarterly",BB10<>"Semi-Annually"),0,1)
        loan_list_df = self.file_df["Loan List"]
        loan_list_df["Interest Paid Semi-Annually"] = loan_list_df.apply(
            lambda row: (
                0
                if (
                    (row["Interest Paid"] != "Monthly")
                    or (row["Interest Paid"] != "Quarterly")
                    or (row["Interest Paid"] != "Semi-Annually")
                )
                else 1
            ),
            axis=1,
        )

    def Material_Non_Credit_Related_Risk(self):
        """
        generation of column `Material Non-Credit Related Risk` from `Loan List` column CM
        Formula:
        =IF(BV10="Yes",1,0)
        """
        loan_list_df = self.file_df["Loan List"]
        loan_list_df["Material Non-Credit Related Risk"] = loan_list_df.apply(
            lambda row: (
                1 if row["Material Non-Credit Related Risk (Y/N)"] == "Yes" else 0
            ),
            axis=1,
        )

    def Real_Estate_Construction_or_Project_Finance_Loan(self):
        # Real Estate, Construction or Project Finance Loan =IF(BW13="Yes",1,0)=IF(BW13="Yes",1,0)
        loan_list_df = self.file_df["Loan List"]
        loan_list_df["Real Estate, Construction or Project Finance Loan"] = (
            loan_list_df.apply(
                lambda row: (
                    1
                    if row[
                        "Primarily Secured by Real Estate, Construction Loan or Project Finance Loan (Y/N)"
                    ]
                    == "Yes"
                    else 0
                ),
                axis=1,
            )
        )

    def Interest_Only_Security(self):
        # Interest Only Security =IF(BX10="Yes",1,0)
        loan_list_df = self.file_df["Loan List"]
        loan_list_df["Interest Only Security"] = loan_list_df.apply(
            lambda row: 1 if row["Interest Only Security (Y/N)"] == "Yes" else 0, axis=1
        )

    def Satisfies_all_Other_Eligibility_Criteria(self):
        # Satisfies all Other Eligibility Criteria =IF(BY11="No",1,0)
        loan_list_df = self.file_df["Loan List"]
        loan_list_df["Satisfies all Other Eligibility Criteria"] = loan_list_df.apply(
            lambda row: (
                1
                if row["Satisfies all Other Eligibility Criteria (Y/N)"] == "No"
                else 0
            ),
            axis=1,
        )

    def Leverage_35percent_Haircut(self):
        """
        generation of column `Leverage 35% Haircut` from `Loan List`
        Formula:
        =IF(DA10=1,0,IF(B10="",0,IF(OR(AND(AN10="Tier 1",X10="No",OR(AI10>$AP$3,AJ10>$AP$4)),(AND(AN10="Tier 1",X10="Yes",AJ10>$AP$5)),(AND(AN10="Tier 2",X10="No",OR(AI10>$AQ$3,AJ10>$AQ$4))),(AND(AN10="Tier 2",X10="Yes",AJ10>$AQ$5)),(AND(AN10="Tier 3",X10="No",OR(AI10>$AR$3,AJ10>$AR$4))),(AND(AN10="Tier 3",X10="Yes",AJ10>$AR$5))),1,0)))
        """ """"""

        # Level 3 - 35% Haircut
        #### (ROW_INDEX, COLUMN_INDEX)
        level3_tier1_row1_location = (1, 10)
        level3_tier1_row2_location = (2, 10)
        level3_tier1_row3_location = (3, 10)
        level3_tier2_row1_location = (1, 11)
        level3_tier2_row2_location = (2, 11)
        level3_tier2_row3_location = (3, 11)
        level3_tier3_row1_location = (1, 12)
        level3_tier3_row2_location = (2, 12)
        level3_tier3_row3_location = (3, 12)

        # Load dataframes
        loan_list_df = self.file_df["Loan List"]
        haircut_df = self.file_df["Haircut"]

        # Create the 'Leverage 35% Haircut' column based on the formula
        def calculate_leverage_haircut(row):
            if row["Leverage - Final Haircut - 50%"] == 1:
                return 0
            elif (
                pd.isna(row["Loan Number"])
                or row["Loan Number"] != row["Loan Number"]
                or row["Loan Number"] == ""
            ):
                return 0
            elif (
                (
                    row["Tier 1 / Tier 2 Obligor"] == "Tier 1"
                    and row["Stretch Senior Loan (Y/N)"] == "No"
                    and (
                        row["Current Senior Debt/EBITDA"]
                        > haircut_df.iat[level3_tier1_row1_location]
                        or row["Current Total Debt/EBITDA"]
                        > haircut_df.iat[level3_tier1_row2_location]
                    )
                )
                or (
                    row["Tier 1 / Tier 2 Obligor"] == "Tier 1"
                    and row["Stretch Senior Loan (Y/N)"] == "Yes"
                    and row["Current Total Debt/EBITDA"]
                    > haircut_df.iat[level3_tier1_row3_location]
                )
                or (
                    row["Tier 1 / Tier 2 Obligor"] == "Tier 2"
                    and row["Stretch Senior Loan (Y/N)"] == "No"
                    and (
                        row["Current Senior Debt/EBITDA"]
                        > haircut_df.iat[level3_tier2_row1_location]
                        or row["Current Total Debt/EBITDA"]
                        > haircut_df.iat[level3_tier2_row2_location]
                    )
                )
                or (
                    row["Tier 1 / Tier 2 Obligor"] == "Tier 2"
                    and row["Stretch Senior Loan (Y/N)"] == "Yes"
                    and row["Current Total Debt/EBITDA"]
                    > haircut_df.iat[level3_tier2_row3_location]
                )
                or (
                    row["Tier 1 / Tier 2 Obligor"] == "Tier 3"
                    and row["Stretch Senior Loan (Y/N)"] == "No"
                    and (
                        row["Current Senior Debt/EBITDA"]
                        > haircut_df.iat[level3_tier3_row1_location]
                        or row["Current Total Debt/EBITDA"]
                        > haircut_df.iat[level3_tier3_row2_location]
                    )
                )
                or (
                    row["Tier 1 / Tier 2 Obligor"] == "Tier 3"
                    and row["Stretch Senior Loan (Y/N)"] == "Yes"
                    and row["Current Total Debt/EBITDA"]
                    > haircut_df.iat[level3_tier3_row3_location]
                )
            ):
                return 1
            else:
                return 0

        # Apply the function to create the 'Leverage 35% Haircut' column
        loan_list_df["Leverage 35% Haircut"] = loan_list_df.apply(
            calculate_leverage_haircut, axis=1
        )

    def Leverage_20percent_Haircut(self):
        # =IF(OR(CZ10=1,DA10=1),0,IF(B10="",0,IF(OR(AND(AN10="Tier 1",X10="No",OR(AI10>$AM$3,AJ10>$AM$4)),(AND(AN10="Tier 1",X10="Yes",AJ10>$AM$5)),(AND(AN10="Tier 2",X10="No",OR(AI10>$AN$3,AJ10>$AN$4))),(AND(AN10="Tier 2",X10="Yes",AJ10>$AN$5)),(AND(AN10="Tier 3",X10="No",OR(AI10>$AO$3,AJ10>$AO$4))),(AND(AN10="Tier 3",X10="Yes",AJ10>$AO$5))),1,0)))
        #### (ROW_INDEX, COLUMN_INDEX)
        level2_tier1_row1_location = (1, 7)
        level2_tier1_row2_location = (2, 7)
        level2_tier1_row3_location = (3, 7)
        level2_tier2_row1_location = (1, 8)
        level2_tier2_row2_location = (2, 8)
        level2_tier2_row3_location = (3, 8)
        level2_tier3_row1_location = (1, 9)
        level2_tier3_row2_location = (2, 9)
        level2_tier3_row3_location = (3, 9)
        # Load dataframes
        loan_list_df = self.file_df["Loan List"]
        haircut_df = self.file_df["Haircut"]

        loan_list_df["Leverage 20% Haircut"] = loan_list_df.apply(
            lambda row: (
                0
                if (
                    row["Leverage 35% Haircut"] == 1
                    or row["Leverage - Final Haircut - 50%"] == 1
                )
                else (
                    0
                    if pd.isna(row["Loan Number"]) or row["Loan Number"] == ""
                    else (
                        1
                        if (
                            row["Tier 1 / Tier 2 Obligor"] == "Tier 1"
                            and row["Stretch Senior Loan (Y/N)"] == "No"
                            and (
                                row["Current Senior Debt/EBITDA"]
                                > haircut_df.iat[level2_tier1_row1_location]
                                or row["Current Total Debt/EBITDA"]
                                > haircut_df.iat[level2_tier1_row2_location]
                            )
                        )
                        or (
                            row["Tier 1 / Tier 2 Obligor"] == "Tier 1"
                            and row["Stretch Senior Loan (Y/N)"] == "Yes"
                            and row["Current Total Debt/EBITDA"]
                            > haircut_df.iat[level2_tier1_row3_location]
                        )
                        or (
                            row["Tier 1 / Tier 2 Obligor"] == "Tier 2"
                            and row["Stretch Senior Loan (Y/N)"] == "No"
                            and (
                                row["Current Senior Debt/EBITDA"]
                                > haircut_df.iat[level2_tier2_row1_location]
                                or row["Current Total Debt/EBITDA"]
                                > haircut_df.iat[level2_tier2_row2_location]
                            )
                        )
                        or (
                            row["Tier 1 / Tier 2 Obligor"] == "Tier 2"
                            and row["Stretch Senior Loan (Y/N)"] == "Yes"
                            and row["Current Total Debt/EBITDA"]
                            > haircut_df.iat[level2_tier2_row3_location]
                        )
                        or (
                            row["Tier 1 / Tier 2 Obligor"] == "Tier 3"
                            and row["Stretch Senior Loan (Y/N)"] == "No"
                            and (
                                row["Current Senior Debt/EBITDA"]
                                > haircut_df.iat[level2_tier3_row1_location]
                                or row["Current Total Debt/EBITDA"]
                                > haircut_df.iat[level2_tier3_row2_location]
                            )
                        )
                        or (
                            row["Tier 1 / Tier 2 Obligor"] == "Tier 3"
                            and row["Stretch Senior Loan (Y/N)"] == "Yes"
                            and row["Current Total Debt/EBITDA"]
                            > haircut_df.iat[level2_tier3_row3_location]
                        )
                        else 0
                    )
                )
            ),
            axis=1,
        )

    def Leverage_10_Haircut(self):
        # Leverage 10% Haircut =IF(OR(CY12=1,CZ12=1,DA12=1),0,IF(B12="",0,IF(OR(AND(AN12="Tier 1",X12="No",OR(AI12>$AJ$3,AJ12>$AJ$4)),(AND(AN12="Tier 1",X12="Yes",AJ12>$AJ$5)),(AND(AN12="Tier 2",X12="No",OR(AI12>$AK$3,AJ12>$AK$4))),(AND(AN12="Tier 2",X12="Yes",AJ12>$AK$5)),(AND(AN12="Tier 3",X12="No",OR(AI12>$AL$3,AJ12>$AL$4))),(AND(AN12="Tier 3",X12="Yes",AJ12>$AL$5))),1,0)))

        level1_tier1_row1_location = (1, 4)
        level1_tier1_row2_location = (2, 4)
        level1_tier1_row3_location = (3, 4)
        level1_tier2_row1_location = (1, 5)
        level1_tier2_row2_location = (2, 5)
        level1_tier2_row3_location = (3, 5)
        level1_tier3_row1_location = (1, 6)
        level1_tier3_row2_location = (2, 6)
        level1_tier3_row3_location = (3, 6)
        # Load dataframes
        loan_list_df = self.file_df["Loan List"]
        haircut_df = self.file_df["Haircut"]

        loan_list_df["Leverage 10% Haircut"] = loan_list_df.apply(
            lambda row: (
                0
                if (
                    row["Leverage 20% Haircut"] == 1
                    or row["Leverage 35% Haircut"] == 1
                    or row["Leverage - Final Haircut - 50%"] == 1
                )
                else (
                    0
                    if pd.isna(row["Loan Number"]) or row["Loan Number"] == ""
                    else (
                        1
                        if (
                            row["Tier 1 / Tier 2 Obligor"] == "Tier 1"
                            and row["Stretch Senior Loan (Y/N)"] == "No"
                            and (
                                row["Current Senior Debt/EBITDA"]
                                > haircut_df.iat[level1_tier1_row1_location]
                                or row["Current Total Debt/EBITDA"]
                                > haircut_df.iat[level1_tier1_row2_location]
                            )
                        )
                        or (
                            row["Tier 1 / Tier 2 Obligor"] == "Tier 1"
                            and row["Stretch Senior Loan (Y/N)"] == "Yes"
                            and row["Current Total Debt/EBITDA"]
                            > haircut_df.iat[level1_tier1_row3_location]
                        )
                        or (
                            row["Tier 1 / Tier 2 Obligor"] == "Tier 2"
                            and row["Stretch Senior Loan (Y/N)"] == "No"
                            and (
                                row["Current Senior Debt/EBITDA"]
                                > haircut_df.iat[level1_tier2_row1_location]
                                or row["Current Total Debt/EBITDA"]
                                > haircut_df.iat[level1_tier2_row2_location]
                            )
                        )
                        or (
                            row["Tier 1 / Tier 2 Obligor"] == "Tier 2"
                            and row["Stretch Senior Loan (Y/N)"] == "Yes"
                            and row["Current Total Debt/EBITDA"]
                            > haircut_df.iat[level1_tier2_row3_location]
                        )
                        or (
                            row["Tier 1 / Tier 2 Obligor"] == "Tier 3"
                            and row["Stretch Senior Loan (Y/N)"] == "No"
                            and (
                                row["Current Senior Debt/EBITDA"]
                                > haircut_df.iat[level1_tier3_row1_location]
                                or row["Current Total Debt/EBITDA"]
                                > haircut_df.iat[level1_tier3_row2_location]
                            )
                        )
                        or (
                            row["Tier 1 / Tier 2 Obligor"] == "Tier 3"
                            and row["Stretch Senior Loan (Y/N)"] == "Yes"
                            and row["Current Total Debt/EBITDA"]
                            > haircut_df.iat[level1_tier3_row3_location]
                        )
                        else 0
                    )
                )
            ),
            axis=1,
        )

    def Eligible_Criteria(self):
        self.Eligible_Currency()  # column CD
        self.Eligible_Country()  # column CE
        # self.Convertible_to_Equity() # column CF
        # self.Equity_Security()  # column CG
        self.Subject_to_offer_or_called_for_redemption()  # column CH
        self.Margin_Stock()  # column CI
        self.Subject_To_Witholding_Tax()  # column CJ
        self.At_Acquisition_Defaulted_Collateral_Loan()  # column CK - name chnaged to Defaulted Collateral Loan CK
        self.Non_cash_PIK()  # column CL
        self.Zero_Coupon_Obligation()  # column CM
        self.Covenant_Lite()  # column CN
        self.Structured_Finance_Obligation()  # Column CO
        self.Remaining_Term_Greater_Than_7_Years()  # column CP
        self.Interest_Paid_Semi_Annually()  # column CQ
        self.Material_Non_Credit_Related_Risk()  # column CR
        self.Real_Estate_Construction_or_Project_Finance_Loan()  # column CS
        self.Interest_Only_Security()  # column CT
        self.Satisfies_all_Other_Eligibility_Criteria()  # column CU
        self.EBITDA_Requirement_at_Acquisition()  # column CV
        self.EBITDA_Requirement_Ongoing()  # column CW
        self.Leverage_Final_Haircut_50_percent()  # column DA
        self.Leverage_35percent_Haircut()  # column CZ
        self.Leverage_20percent_Haircut()  # column CY
        self.Leverage_10_Haircut()  # colummn CX

    def Advance_Rate(self):
        """
        Calculation of Advance Rate column (V column from Loan List)
        Formula:
        =IF(B10="",0,IF(AND(OR(Y10="First Lien",Y10="Split First Lien"),OR(AN10="Tier 1",AN10="Tier 2")),
        IF(AND(X10="Yes",AG10>4.5),(((4.5/AG10)*70%)+(((AG10-4.5)/AG10)*35%)),70%),
        IF(AND(X10="Yes",AG10>4),(((4/AG10)*70%)+(((AG10-4)/AG10)*35%)),
        IF(OR(Y10="First Lien",Y10="Split First Lien"),70%,IF(Y10="Tier 1 Split Lien",53%,IF(Y10="Tier 2 Split Lien", 44%,35%)))))))
        """
        loan_list_df = self.file_df["Loan List"]

        def calculate_advance_rate(row):
            if pd.isna(row["Loan Number"]):
                return 0
            elif (
                row[
                    "Lien Type (First Lien / Split First Lien / Split Lien / Second Lien / Tier 1 Split Lien / Tier 2 Split Lien)"
                ]
                in ["First Lien", "Split First Lien"]
            ) and (row["Tier 1 / Tier 2 Obligor"] in ["Tier 1", "Tier 2"]):
                if (
                    row["Stretch Senior Loan (Y/N)"] == "Yes"
                    and row["Initial Senior Debt/EBITDA"] > 4.5
                ):
                    return ((4.5 / row["Initial Senior Debt/EBITDA"]) * 0.7) + (
                        (
                            (row["Initial Senior Debt/EBITDA"] - 4.5)
                            / row["Initial Senior Debt/EBITDA"]
                        )
                        * 0.35
                    )
                else:
                    return 0.7
            elif (
                row["Stretch Senior Loan (Y/N)"] == "Yes"
                and row["Initial Senior Debt/EBITDA"] > 4
            ):
                return ((4 / row["Initial Senior Debt/EBITDA"]) * 0.7) + (
                    (
                        (row["Initial Senior Debt/EBITDA"] - 4)
                        / row["Initial Senior Debt/EBITDA"]
                    )
                    * 0.35
                )
            elif row[
                "Lien Type (First Lien / Split First Lien / Split Lien / Second Lien / Tier 1 Split Lien / Tier 2 Split Lien)"
            ] in ["First Lien", "Split First Lien"]:
                return 0.7
            elif (
                row[
                    "Lien Type (First Lien / Split First Lien / Split Lien / Second Lien / Tier 1 Split Lien / Tier 2 Split Lien)"
                ]
                == "Tier 1 Split Lien"
            ):
                return 0.53
            elif (
                row[
                    "Lien Type (First Lien / Split First Lien / Split Lien / Second Lien / Tier 1 Split Lien / Tier 2 Split Lien)"
                ]
                == "Tier 2 Split Lien"
            ):
                return 0.44
            else:
                return 0.35

        loan_list_df["Advance Rate"] = loan_list_df.apply(
            calculate_advance_rate, axis=1
        )

    def PFLTBB_calculation_Second_Level_Formulas(self):

        # Perform calculations
        self.Tier_1_Tier_2_Obligor()  # Calculate Tier 1 Tier 2 Obligor column AN
        self.Advance_Rate()  # column V
        self.Partial_PIK_Loan_Y_N()  # column BI new
        self.Non_Cash_PIK_Loan_Y_N()  # column BJ new
        self.Eligible_Criteria()  # column CC - DA
        self.Discount_Collateral_Loan_Y_N()  # column S
        self.Aggregate_Unfunded_Spread()  # column CA
        self.Aggregate_Funded_Spread()  # column BZ
        self.Avg_Life()  # column AQ
        # calculate PFLTBB_calculation_Second_Level_Formulas_DC_to_DJ columns
        self.PFLTBB_calculation_Second_Level_Formulas_DC_to_DJ()


# file_path = pathlib.Path("PFLT_Sub_Borrowing_Base_First_Level_Formulas.xlsx")
# file_obj = file_path.open(mode="rb")

# file_df = pd.read_excel(file_obj, sheet_name=None)

# slc = SecondLevelCalculations(file_df)
# slc.PFLTBB_calculation_Second_Level_Formulas()
# output_file_path = "PFLT_Sub_Borrowing_Base_Second_Level_Formulas.xlsx"
# with pd.ExcelWriter(output_file_path) as writer:
#     for sheet, dataframe in slc.file_df.items():
#         dataframe.to_excel(writer, sheet_name=sheet, index=False)
