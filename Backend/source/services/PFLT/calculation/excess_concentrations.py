import pandas as pd
import numpy as np
import pathlib
from datetime import datetime
from models import db, ConcentrationTest, Fund, FundConcentrationTest


class Obligor_Limit_Excess_GJ_GZ:
    def __init__(self):
        pass

    def Obligor_No_GX_new(self):
        # =IF(C11="","",IF(ISERROR(MATCH(C11,C10:C$10,0)),MAX(GO10:GO$10)+1,INDEX(GO10:GO$10,MATCH(C11,C10:C$10,0))))

        # def is_matched(row_index, loan_list_df):
        #     lookup_value = loan_list_df.loc[row_index, "Obligor"]
        #     if lookup_value in loan_list_df["Obligor"][0:row_index]:
        #         return False
        #     else:
        #         return True

        # # Function to process each row based on previous rows
        # def process_row(row_index, loan_list_df):

        #     if is_matched(row_index, loan_list_df):
        #         return loan_list_df["Obligor No GJ"][0 : row_index-1].max() + 1
        #     else:
        #         lookup_array = loan_list_df.loc[0 : row_index - 1, "Obligor"].tolist()
        #         looup_index = lookup_array.index(loan_list_df.loc[row_index-1, "Obligor"])
        #         return loan_list_df["Obligor No GJ"][0:row_index-1].iloc[looup_index-1]

        # loan_list_df = self.file_df["Loan List"]
        # loan_list_df["Obligor No GX"] = np.nan
        # loan_list_df.loc[0, "Obligor No GX"] = 1  # First row is always 1
        # # Apply the function to each row from the second row onward
        # for i in range(1, len(loan_list_df)):
        #     if (
        #         pd.isna(loan_list_df.loc[i, "Obligor"])
        #         or loan_list_df.loc[i, "Obligor"] == ""
        #     ):
        #         loan_list_df.loc[i, "Obligor No GX"] = ""
        #     else:
        #         loan_list_df.loc[i, "Obligor No GX"] = process_row(i, loan_list_df)

        loan_list_df = self.file_df["Loan List"]
        loan_list_df["Obligor No GX"] = loan_list_df["Obligor No GJ"]

    def Obligor_Loan_Balance_GY_new(self):
        # =IF(COUNTIF($A$10:A10,A10)<=1,SUMIF($A$10:$A$400,A10,$FG$10:$FG$400),0)

        def calculate_obligor_loan_balance_GY_new(row, df):
            idx = row.name

            # count_occurrences = df.loc[:idx, 'Obligor Name'].eq(row['Obligor Name']).sum()
            count_occurrences = (
                df["Obligor Name"][0 : idx + 1].tolist().count(row["Obligor Name"])
            )
            if count_occurrences <= 1:
                sum_matching_values = df.loc[
                    df["Obligor Name"] == row["Obligor Name"], "Obligor FE"
                ].sum()
                return sum_matching_values
            else:
                return 0

        loan_list_df = self.file_df["Loan List"]
        # Apply the function to create the 'Obligor Loan Balance' column
        loan_list_df["Obligor Loan Balance GY"] = loan_list_df.apply(
            lambda row: calculate_obligor_loan_balance_GY_new(row, loan_list_df), axis=1
        )

    def Obligor_Order_GZ_new(self):
        # =GZ10+1
        loan_list_df = self.file_df["Loan List"]
        loan_list_df["Obligor Order GZ"] = loan_list_df.reset_index(drop=True).index + 1

    def Obligor_Loan_Balance_HA(self):
        # =LARGE($GY$10:$GY$400,GZ10)

        loan_list_df = self.file_df["Loan List"]
        loan_list_df["Obligor Loan Balance HA"] = loan_list_df[
            "Obligor Order GZ"
        ].apply(
            lambda row: self.get_nth_largest(
                loan_list_df["Obligor Loan Balance GY"], row
            )
        )

    def Excess_HC_new(self):
        # =IF(GZ10<6,MAX(0,$HC$2/5),0)

        def calculate_value(gz_value, HC2):
            if gz_value < 6:
                return max(0, HC2 / 5)
            else:
                return 0

        loan_list_df = self.file_df["Loan List"]
        # borrowing_base_df = self.file_df["Borrowing Base"]
        # concentration_test_df = self.file_df["Concentration Test"]

        borrowing_base_value = loan_list_df[
            "Concentration Test Balance - OPB + Eligible Unfunded"
        ].sum()

        try:
            conc_test_fund_map = (
                db.session.query(FundConcentrationTest.limit_percentage)
                .join(Fund)
                .join(ConcentrationTest)
                .filter(Fund.id == 2)
                .filter(ConcentrationTest.test_name == "Top 5 Obligors (Aggregate)")
                .first()
            )
            limit_percent = conc_test_fund_map.limit_percentage
        except Exception as e:
            print(f"Error calculating limit percentage: {e}")
            limit_percent = 0.3
        limit = limit_percent * borrowing_base_value
        HC2 = max(0, loan_list_df["Obligor Loan Balance HA"][0:8].sum() - limit)
        loan_list_df["Excess HC"] = loan_list_df["Obligor Order GZ"].apply(
            lambda row: calculate_value(row, HC2)
        )

    def Obligor_No_HD_new(self):
        # {=IF(HA10=0,0,LARGE(IF($GY$10:$GY$400=HA10,$GX$10:$GX$400,0),COUNTIF($HA$10:$HA$400,HA10)-COUNTIF(HA$9:HA9,HA10)))}

        loan_list_df = self.file_df["Loan List"]

        def calculate_obligor_no_hd(row, df):
            # Current row index
            idx = row.name
            # Check if GM is 0
            if (
                row["Obligor Loan Balance HA"] == 0
                or pd.isna(row["Obligor Loan Balance HA"])
                or row["Obligor Loan Balance HA"] != row["Obligor Loan Balance HA"]
            ):
                return 0

            # Filter values where GK matches GM
            filtered_values = df.loc[
                df["Obligor Loan Balance GY"] == row["Obligor Loan Balance HA"],
                "Obligor No GX",
            ]
            if len(filtered_values) == 0:
                return 0

            # Calculate the rank position
            rank_position = (
                df["Obligor Loan Balance HA"].eq(row["Obligor Loan Balance HA"]).sum()
                - df.loc[: idx - 1, "Obligor Loan Balance HA"]
                .eq(row["Obligor Loan Balance HA"])
                .sum()
            )
            # Get the Nth largest value
            return (
                filtered_values.nlargest(rank_position).iloc[-1]
                if rank_position <= len(filtered_values)
                else 0
            )

        # Apply the function to create the 'Obligor No' column in GP
        loan_list_df["Obligor No HD"] = loan_list_df.apply(
            lambda row: calculate_obligor_no_hd(row, loan_list_df), axis=1
        )

    def Haircut_HE(self):
        # =IF(HA10=0,0,HC10/HA10)
        loan_list_df = self.file_df["Loan List"]

        def calculate_Haircut_he(row, df):
            if row["Obligor Loan Balance HA"] == 0:
                return 0
            else:
                return row["Excess HC"] / row["Obligor Loan Balance HA"]

        loan_list_df["Haircut HE"] = loan_list_df.apply(
            lambda row: calculate_Haircut_he(row, loan_list_df), axis=1
        )

    def Obligor_No_GJ(self):
        """
        generate column `Obligor No` from `Loan List`
        Formula:
        =IF(C13="","",IF(ISERROR(MATCH(C13,C$10:C12,0)),MAX(GJ$10:GJ12)+1,INDEX(GJ$10:GJ12,MATCH(C13,C$10:C12,0))))
        """
        loan_list_df = self.file_df["Loan List"]
        loan_list_df.loc[0, "Obligor No GJ"] = 1
        for i in range(1, len(loan_list_df)):
            if loan_list_df.loc[i, "Obligor"] == "":
                loan_list_df.loc[i, "Obligor No GJ"] = ""
            else:
                # Check if the "Obligor" already exists in the previous rows
                if (
                    loan_list_df.loc[i, "Obligor"]
                    in loan_list_df.loc[: i - 1, "Obligor"].values
                ):
                    # If exists, assign the corresponding Obligor No GJ value
                    loan_list_df.loc[i, "Obligor No GJ"] = (
                        loan_list_df.loc[: i - 1, :]
                        .loc[
                            loan_list_df.loc[: i - 1, "Obligor"]
                            == loan_list_df.loc[i, "Obligor"],
                            "Obligor No GJ",
                        ]
                        .values[0]
                    )
                else:
                    # If not, assign the next maximum Obligor No GJ value plus 1
                    loan_list_df.loc[i, "Obligor No GJ"] = (
                        loan_list_df.loc[: i - 1, "Obligor No GJ"].max() + 1
                    )

    def Obligor_Loan_Balance_GK(self):
        """
        generate column `Obligor Loan Balance` from `Loan List`
        Formula:
        =IF(COUNTIF($A$10:A10,A10)<=1,SUMIF($A$10:$A$113,A10,$FE$10:$FE$113),0)
        """
        loan_list_df = self.file_df["Loan List"]

        def calculate_obligor_loan_balance(row, df):
            # Current row index
            idx = row.name

            # Count the occurrences of the current value in 'A' up to the current row
            count_occurrences = (
                df.loc[:idx, "Obligor Name"].eq(row["Obligor Name"]).sum()
            )

            if count_occurrences <= 1:
                # If this is the first occurrence, calculate the sum of 'FE' for all matching 'A' values
                sum_matching_values = df.loc[
                    df["Obligor Name"] == row["Obligor Name"], "Obligor FE"
                ].sum()
                return sum_matching_values
            else:
                # If this is not the first occurrence, return 0
                return 0

        # Apply the function to create the 'Obligor Loan Balance' column
        loan_list_df["Obligor Loan Balance GK"] = loan_list_df.apply(
            lambda row: calculate_obligor_loan_balance(row, loan_list_df), axis=1
        )

    def Obligor_Order(self):
        # rule =GL10+1
        loan_list_df = self.file_df["Loan List"]
        loan_list_df["Obligor Order"] = loan_list_df.reset_index(drop=True).index + 1

    def get_nth_largest(self, values, n):
        sorted_values = sorted(values, reverse=True)
        return sorted_values[n - 1]

    def Obligor_Loan_Balance_GM(self):
        # Obligor Loan Balance =LARGE($GK$10:$GK$113,GL10)

        loan_list_df = self.file_df["Loan List"]
        loan_list_df["Obligor Loan Balance GM"] = loan_list_df["Obligor Order"].apply(
            lambda row: self.get_nth_largest(
                loan_list_df["Obligor Loan Balance GK"], row
            )
        )

    def Limit(self):
        # =IF(GQ10>GQ$6,0,IF(GQ10<=GQ$2,GS$2,IF(AND(GQ10<=$GQ$3,GQ10>$GQ$2),GS$3,GS$4)))
        loan_list_df = self.file_df["Loan List"]
        no_of_obligor_row2 = self.No_of_Obligor_GL2
        no_of_obligor_row3 = self.No_of_Obligor_GL3
        limit_dollar2 = self.total_Concentration_Test_Balance_OPB_Eligible_Unfunded * self.Limit_percent_GM2
        limit_dollar3 = self.total_Concentration_Test_Balance_OPB_Eligible_Unfunded * self.Limit_percent_GM3
        limit_dollar4 = self.total_Concentration_Test_Balance_OPB_Eligible_Unfunded * self.Limit_percent_GM4
        count = loan_list_df[loan_list_df["Obligor Loan Balance GK"] > 0].shape[0]

        loan_list_df["Limit"] = loan_list_df.apply(
            lambda row: (
                0 if row["Obligor Order"] > count
                    else (
                        limit_dollar2
                            if row["Obligor Order"] <= no_of_obligor_row2
                            else (
                                limit_dollar3
                                    if row["Obligor Order"] <= no_of_obligor_row3
                                    else (
                                        limit_dollar4
                                    )
                            )
                    )
            ), axis=1)

    def Excess_GO(self):
        # Excess =MAX(0,GM10-GN10)
        loan_list_df = self.file_df["Loan List"]
        loan_list_df["Excess_GO"] = loan_list_df.apply(
            lambda row: max(0, row["Obligor Loan Balance GM"] - row["Limit"]), axis=1
        )

    def Obligor_No_GP(self):
        loan_list_df = self.file_df["Loan List"]

        def calculate_obligor_no_gp(row, df):
            # Current row index
            idx = row.name
            # Check if GM is 0
            if (
                row["Obligor Loan Balance GM"] == 0
                or pd.isna(row["Obligor Loan Balance GM"])
                or row["Obligor Loan Balance GM"] != row["Obligor Loan Balance GM"]
            ):
                return 0

            # Filter values where GK matches GM
            filtered_values = df.loc[
                df["Obligor Loan Balance GK"] == row["Obligor Loan Balance GM"],
                "Obligor No GJ",
            ]
            if len(filtered_values) == 0:
                return 0

            # Calculate the rank position
            rank_position = (
                df["Obligor Loan Balance GM"].eq(row["Obligor Loan Balance GM"]).sum()
                - df.loc[: idx - 1, "Obligor Loan Balance GM"]
                .eq(row["Obligor Loan Balance GM"])
                .sum()
            )
            # Get the Nth largest value
            return (
                filtered_values.nlargest(rank_position).iloc[-1]
                if rank_position <= len(filtered_values)
                else 0
            )

        # Apply the function to create the 'Obligor No' column in GP
        loan_list_df["Obligor No GP"] = loan_list_df.apply(
            lambda row: calculate_obligor_no_gp(row, loan_list_df), axis=1
        )

    def Haircut_GQ(self):
        # rule =IF(GM10=0,0,GO10/GM10)
        loan_list_df = self.file_df["Loan List"]
        loan_list_df["Haircut GQ"] = loan_list_df.apply(
            lambda row: (
                0
                if pd.isna(row["Obligor Loan Balance GM"])
                or row["Obligor Loan Balance GM"] == 0
                else row["Excess_GO"] / row["Obligor Loan Balance GM"]
            ),
            axis=1,
        )

    def Obligor_GJ_GQ(self):
        self.Obligor_No_GJ()  # Column GJ
        self.Obligor_Loan_Balance_GK()  # column GK
        self.Obligor_Order()  # Column GL
        self.Obligor_Loan_Balance_GM()  # column GM
        self.Limit()  # Column GN
        self.Excess_GO()  # column GO
        self.Obligor_No_GP()  # column GP
        self.Haircut_GQ()  # column GQ

    def Obligor_new_GX_new_HE(self):
        self.Obligor_No_GX_new()
        self.Obligor_Loan_Balance_GY_new()
        self.Obligor_Order_GZ_new()
        self.Obligor_Loan_Balance_HA()
        self.Excess_HC_new()
        self.Obligor_No_HD_new()
        self.Haircut_HE()

    def Industry_No_FZ(self):
        # Industry No =IF(HN10="","",HN10)
        loan_list_df = self.file_df["Loan List"]
        loan_list_df["Industry No FZ"] = loan_list_df.apply(
            lambda row: (
                "" if row["Lookups'!F2:F3 No"] == "" else row["Lookups'!F2:F3 No"]
            ),
            axis=1,
        )

    def Lookups_F2_F3_Loan_Balance(self):
        # 'Lookups'!F2:F3 Loan Balance =IF(SUM(IF(HN$9:HN9=HN10,1,0))>0,0,SUMIF($HN$10:$HN$113,HN10,$FG$10:$FG$113))
        loan_list_df = self.file_df["Loan List"]

        def calculate_loan_balance(row, df):
            # Current row index
            idx = row.name
            # Check if HN10 has appeared before in HN column
            previous_occurrences = (
                df.loc[: idx - 1, "Lookups'!F2:F3 No"]
                .eq(row["Lookups'!F2:F3 No"])
                .sum()
            )
            if previous_occurrences > 0:
                return 0
            # Sum the FG values where HN matches the current row's HN
            sum_matching_values = df.loc[
                df["Lookups'!F2:F3 No"] == row["Lookups'!F2:F3 No"],
                "Obligor FE Net Loan Balance",
            ].sum()
            return sum_matching_values

        # Apply the function to create the 'Loan Balance' column in 'Lookups'
        loan_list_df["'Lookups'!F2:F3 Loan Balance"] = loan_list_df.apply(
            lambda row: calculate_loan_balance(row, loan_list_df), axis=1
        )

    def Industry_Loan_Balance(self):
        # Industry Loan Balance =GA10
        loan_list_df = self.file_df["Loan List"]
        loan_list_df["Industry Loan Balance"] = loan_list_df[
            "'Lookups'!F2:F3 Loan Balance"
        ]

    def Industry_Order(self):
        loan_list_df = self.file_df["Loan List"]
        loan_list_df["Industry Order"] = loan_list_df.reset_index(drop=True).index + 1

    def Outstanding_Loan_Balance(self):
        loan_list_df = self.file_df["Loan List"]

        def calculate_outstanding_loan_balance(row, loan_list_df):
            # Get the rank position from GC
            rank_position = row["Industry Order"]

            # Use nlargest to get the Nth largest value in GB
            result = (
                loan_list_df["Industry Loan Balance"].nlargest(rank_position).iloc[-1]
                if rank_position <= len(loan_list_df["Industry Loan Balance"])
                else 0
            )

            return result

        # Apply the function to create the 'Outstanding Loan Balance' column
        loan_list_df["Outstanding Loan Balance"] = loan_list_df.apply(
            lambda row: calculate_outstanding_loan_balance(row, loan_list_df), axis=1
        )

    def Limit_GE(self):
        loan_list_df = self.file_df["Loan List"]
        Industry_Loan_Balance_Count = len(
            loan_list_df[loan_list_df["'Lookups'!F2:F3 Loan Balance"] > 0]
        )

        ge2 = (
            self.total_Concentration_Test_Balance_OPB_Eligible_Unfunded
            * self.GD_Limit_NoOfIndustry_1
        )
        ge3 = (
            self.total_Concentration_Test_Balance_OPB_Eligible_Unfunded
            * self.GD_Limit_NoOfIndustry_2_and_3
        )
        ge4 = (
            self.total_Concentration_Test_Balance_OPB_Eligible_Unfunded
            * self.GD_Limit_NoOfIndustry_Other
        )

        def calculate_limit(row, gc6, gc2, ge2, ge3, ge4):
            # Check if GC > GC$6
            if row["Industry Order"] > gc6:
                return 0
            # Check if GC = GC$2
            if row["Industry Order"] == gc2:
                return ge2
            # Check if GC < 4
            if row["Industry Order"] < 4:
                return ge3
            # Default case
            return ge4

        # Apply the function to create the 'Limit' column
        loan_list_df["Limit GE"] = loan_list_df.apply(
            lambda row: calculate_limit(
                row,
                Industry_Loan_Balance_Count,
                self.No_of_Industry_GC_row1,
                ge2,
                ge3,
                ge4,
            ),
            axis=1,
        )

    def Excess_GF(self):
        # Excess =MAX(0,GD11-GE11)
        loan_list_df = self.file_df["Loan List"]
        loan_list_df["Excess_GF"] = loan_list_df.apply(
            lambda row: max(0, row["Outstanding Loan Balance"] - row["Limit GE"]),
            axis=1,
        )

    def Industry_No_Matched(self):
        loan_list_df = self.file_df["Loan List"]

        def calculate_industry_no_gg(row, df):
            # Current row index
            idx = row.name
            # Check if GD is 0
            if row["Outstanding Loan Balance"] == 0:
                return 0
            # Filter values where GA matches GD
            filtered_values = df.loc[
                df["'Lookups'!F2:F3 Loan Balance"] == row["Outstanding Loan Balance"],
                "Industry No FZ",
            ]

            if len(filtered_values) == 0:
                return 0
            # Calculate the rank position
            rank_position = (
                df["Outstanding Loan Balance"].eq(row["Outstanding Loan Balance"]).sum()
                - df.loc[: idx - 1, "Outstanding Loan Balance"]
                .eq(row["Outstanding Loan Balance"])
                .sum()
            )

            # Get the Nth largest value
            return (
                filtered_values.nlargest(rank_position).iloc[-1]
                if rank_position <= len(filtered_values)
                else 0
            )

        # Apply the function to create the 'Industry No (Matched)' column in GG
        loan_list_df["Industry No (Matched)"] = loan_list_df.apply(
            lambda row: calculate_industry_no_gg(row, loan_list_df), axis=1
        )

    def Haircut_GH(self):
        loan_list_df = self.file_df["Loan List"]
        loan_list_df["Haircut GH"] = 0
        loan_list_df.loc[
            loan_list_df["Outstanding Loan Balance"] == 0, "Haircut GH"
        ] = 0
        loan_list_df.loc[
            loan_list_df["Outstanding Loan Balance"] != 0, "Haircut GH"
        ] = (loan_list_df["Excess_GF"] / loan_list_df["Outstanding Loan Balance"])

    def Industry_FZ_GH(self):
        self.Industry_No_FZ()  # column FZ
        self.Lookups_F2_F3_Loan_Balance()  # column GA
        self.Industry_Loan_Balance()  # column GB
        self.Industry_Order()  # column GC
        self.Outstanding_Loan_Balance()  # column GD
        self.Limit_GE()  # column GE
        self.Excess_GF()  # column GF
        self.Industry_No_Matched()  # column GG
        self.Haircut_GH()  # column GH

    def Excess_Concentration_Amount_Dynamic(self):
        loan_list_df = self.file_df["Loan List"]
        loan_list_df["Excess Concentration Amount (Dynamic)"] = (
            loan_list_df[
                "Aggregate Collateral Balance (Post Eligibility; Including Eligible Unfunded)"
            ]
            - loan_list_df["Excess Concentration Test"]
        )

    def Applicable_Excess_Concentration_Amount_Last_Day_of_Reinvestment_Period(self):
        loan_list_df = self.file_df["Loan List"]
        loan_list_df[
            "Excess Concentration Amount (HARD CODE on Last Day of Reinvestment Period)"
        ] = loan_list_df[
            "Excess Concentration Amount (HARD CODE on Last Day of Reinvestment Period)"
        ].fillna(
            0
        )
        loan_list_df[
            "Applicable Excess Concentration Amount (Last Day of Reinvestment Period)"
        ] = loan_list_df.apply(
            lambda row: min(
                row[
                    "Excess Concentration Amount (HARD CODE on Last Day of Reinvestment Period)"
                ],
                row[
                    "Aggregate Collateral Balance (Post Eligibility; Including Haircut Ineligible; Excluding Unfunded)"
                ],
            ),
            axis=1,
        )

    def Obligor_No_GW(self):
        loan_list_df = self.file_df["Loan List"]
        loan_list_df["Obligor No GW"] = loan_list_df.reset_index(drop=True).index + 1
        loan_list_df["Obligor No GW"] = loan_list_df.apply(
            lambda row: (
                row["Obligor No GW"]
                if row["Obligor No GW"] in loan_list_df["Obligor"]
                else ""
            ),
            axis=1,
        )

    def Obligor_Loan_Balance_GX(self):
        loan_list_df = self.file_df["Loan List"]

        # Create a dictionary to store aggregate collateral sums by Obligor
        aggregate_collateral = loan_list_df.groupby("Obligor")[
            "Aggregate Collateral Balance (Post Eligibility; Including Eligible Unfunded)"
        ].sum()

        # Map the aggregated values to the 'Obligor No GW' column
        loan_list_df["Obligor Loan Balance_GX"] = (
            loan_list_df["Obligor No GW"].map(aggregate_collateral).fillna(0)
        )

        # Ensure to keep the DataFrame in the original object
        self.file_df["Loan List"] = loan_list_df

    def Aggregate_Collateral_Balance_Pre_Eligibility_Excluding_Unfunded_Excluding_Principal_Acct(
        self,
    ):
        # Warning : Already calculated
        # Aggregate Collateral Balance (Pre-Eligibility; Excluding Unfunded; Excluding Principal Acct) =MIN(HA10:HE10)
        loan_list_df = self.file_df["Loan List"]
        # loan_list_df['Aggregate Collateral Balance (Pre-Eligibility; Excluding Unfunded; Excluding Principal Acct)'] = loan_list_df[['Outstanding Principal Balance', 'Defaulted Collateral Loan Balance', 'Discount Loan Balance', 'Credit Improved Balance', 'Haircut Ineligible']].min()
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

    def Calculate_GS_GZ(self):
        self.Excess_Concentration_Amount_Dynamic()  # column GS
        self.Applicable_Excess_Concentration_Amount_Last_Day_of_Reinvestment_Period()  # column GU
        self.Obligor_No_GW()  # column GW
        self.Obligor_Loan_Balance_GX()  # column GX
        self.Aggregate_Collateral_Balance_Pre_Eligibility_Excluding_Unfunded_Excluding_Principal_Acct()  # column GZ


class ExcessConcentrations(Obligor_Limit_Excess_GJ_GZ):
    def __init__(self):
        super().__init__()

        # self.total_Concentration_Test_Balance_OPB_Eligible_Unfunded = self.file_df["Loan List"]["Concentration Test Balance - OPB + Eligible Unfunded"].sum()
        self.Limit_percent_DL = 0.15
        self.Limit_percent_DO = 0.10
        self.Limit_percent_DR = 0.05
        self.Limit_percent_DU = 0.15
        self.Limit_percent_DX = 0.10
        self.Limit_percent_EA = 0.15
        self.Limit_percent_ED = 0.10
        self.Limit_percent_EG = 0.25
        self.Limit_percent_EJ = 0.10
        self.Limit_percent_EM = 0.03
        self.Limit_percent_EP = 0.15
        self.Limit_percent_ES = 0.05
        self.Limit_percent_EV = 0.15
        self.Limit_percent_EY = 0.10
        self.Limit_percent_FB = 0.15
        self.percent_FK2 = 0.05
        self.percent_FN2 = 0.20
        self.percent_FQ2 = 0.20
        self.conc_limit_tier1_row1_location = (1, 1)
        self.conc_limit_tier1_row3_location = (3, 1)
        self.conc_limit_tier1_row2_location = (2, 1)
        self.conc_limit_tier2_row1_location = (1, 2)
        self.conc_limit_tier2_row2_location = (2, 2)
        self.conc_limit_tier2_row3_location = (3, 2)
        self.conc_limit_tier3_row1_location = (1, 3)
        self.conc_limit_tier3_row2_location = (2, 3)
        self.conc_limit_tier3_row3_location = (3, 3)

    def Second_Lien_and_Split_Lien(self):
        # Implement the calculations
        # rule =IF(OR(Y10="Second Lien",Y10="Split Lien"),DE10,0)
        loan_list_df = self.file_df["Loan List"]
        loan_list_df["Second Lien and Split Lien"] = loan_list_df.apply(
            lambda row: (
                row[
                    "Aggregate Collateral Balance (Post Eligibility; Including Eligible Unfunded)"
                ]
                if row[
                    "Lien Type (First Lien / Split First Lien / Split Lien / Second Lien / Tier 1 Split Lien / Tier 2 Split Lien)"
                ]
                == "Second Lien"
                or row[
                    "Lien Type (First Lien / Split First Lien / Split Lien / Second Lien / Tier 1 Split Lien / Tier 2 Split Lien)"
                ]
                == "Split Lien"
                else 0
            ),
            axis=1,
        )

    def Second_Lien(self):
        # rule =IF(Y10="Second Lien",DN10,0)
        loan_list_df = self.file_df["Loan List"]
        loan_list_df["Second Lien"] = loan_list_df.apply(
            lambda row: (
                row["Second Lien and Split Lien Net Loan Balance"]
                if row[
                    "Lien Type (First Lien / Split First Lien / Split Lien / Second Lien / Tier 1 Split Lien / Tier 2 Split Lien)"
                ]
                == "Second Lien"
                else 0
            ),
            axis=1,
        )

    def Net_Loan_Balance_DQ(self):
        loan_list_df = self.file_df["Loan List"]

        # Calculate the Net Loan Balance = DN - DP

        loan_list_df["Second Lien Net Loan Balance"] = loan_list_df.apply(
            lambda row: row["Second Lien and Split Lien Net Loan Balance"]
            - row["Second Lien Excess"],
            axis=1,
        )

    def DIP_Collateral_Loans(self):
        # rule =IF(BF10="Yes",DQ10,0)
        loan_list_df = self.file_df["Loan List"]
        loan_list_df["DIP Collateral Loans"] = loan_list_df.apply(
            lambda row: (
                row["Net Loan Balance"] if row["DIP Loan (Y/N)"] == "Yes" else 0
            ),
            axis=1,
        )

    def Eligible_Foreign_Country(self):
        # rule =IF(OR(BE10="Canada",BE10="United Kingdom",BE10="Australia",BE10="Netherlands Antilles",BE10="Bermuda",BE10="Cayman Islands",BE10="British Virgin Islands",
        # BE10="Channel Islands",BE10="Isle of Man",BE10="Australia",BE10="Netherlands",BE10="Germany",BE10="Sweden",BE10="Switzerland",BE10="Austria",BE10="Belgium",
        # BE10="Denmark",BE10="Finland",BE10="Iceland",BE10="Ireland",BE10="Lichtenstein",BE10="Luxemborg",BE10="Norway"),DT10,0)

        loan_list_df = self.file_df["Loan List"]

        country_list = [
            "Canada",
            "United Kingdom",
            "Norway",
            "Netherlands",
            "Netherlands Antilles",
            "Australia",
            "Bermuda",
            "Cayman Islands",
            "British Virgin Islands",
            "Channel Islands",
            "Luxemborg",
            "Lichtenstein",
            "Ireland",
            "Iceland",
            "Finland",
            "Denmark",
            "Belgium",
            "Austria",
            "Germany",
            "Sweden",
            "Switzerland",
            "Isle of Man",
        ]

        loan_list_df["Eligible Foreign Country"] = loan_list_df.apply(
            lambda row: (
                row["DIP Collateral Loans Net Loan Balance"]
                if row["Obligor Country"] in country_list
                else 0
            ),
            axis=1,
        )

    def Excess(self, excess_col, calculation_col, limit_percent):
        """
        generate the column `Excess` from `Loan List`
        Formula:
        =DL10*DL$6

        """
        loan_list_df = self.file_df["Loan List"]

        Limit = (
            limit_percent * self.total_Concentration_Test_Balance_OPB_Eligible_Unfunded
        )
        Total_Second_Lien_and_Split_Lien = loan_list_df[calculation_col].sum()
        Excess = max(0, Total_Second_Lien_and_Split_Lien - Limit)
        Haircut = (
            0
            if Total_Second_Lien_and_Split_Lien < 0.01
            else Excess / Total_Second_Lien_and_Split_Lien
        )

        loan_list_df[excess_col] = loan_list_df[calculation_col] * Haircut

    def Net_Loan_Balance(
        self,
        current_net_loan_balance_column,
        current_excess_column,
        prev_net_loan_balance_column,
    ):
        loan_list_df = self.file_df["Loan List"]
        # Calculate the Net Loan Balance = DQ - DS
        loan_list_df[current_net_loan_balance_column] = (
            loan_list_df[prev_net_loan_balance_column]
            - loan_list_df[current_excess_column]
        )

    def top_5_Obligor(self):
        # =FL10
        # old FJ
        loan_list_df = self.file_df["Loan List"]

        loan_list_df["Top 5 Obligors"] = loan_list_df[
            "Obligor Industry FH Net Loan Balance"
        ]

    def top_5_obligors_excess(self):
        # =IF(FL10=0,0,VLOOKUP(C10,$HD$10:$HE$400,2,FALSE)*FL10)

        def calculate_excess_fn(row, loan_list_df):

            if row["Obligor Industry FH Net Loan Balance"] == 0:

                return 0
            else:
                lookup_value = loan_list_df.loc[
                    loan_list_df["Obligor No HD"] == row["Obligor"], "Haircut HE"
                ]

                # Check if the lookup returned any results
                if lookup_value.empty:
                    return 0
                else:
                    # Multiply the 'Haircut HD' value by 'Top 5 Obligors'
                    return lookup_value.values[0] * row["Top 5 Obligors"]

        loan_list_df = self.file_df["Loan List"]

        loan_list_df["Top 5 Obligors Excess"] = loan_list_df.apply(
            lambda row: calculate_excess_fn(row, loan_list_df), axis=1
        )

    def Partial_PIK_Loan(self):
        # rule =IF(BG10="Yes",DW10,0)
        loan_list_df = self.file_df["Loan List"]
        loan_list_df["Partial PIK Loan"] = loan_list_df.apply(
            lambda row: (
                row["Eligible Foreign Country Net Loan Balance"]
                if row["Partial PIK Loan (Y/N)"] == "Yes"
                else 0
            ),
            axis=1,
        )

    def Revolving_Delayed_Drawdown(self):
        # rule =IF(OR(Z10="Delayed Draw",Z10="Revolver"),DZ10,0)
        loan_list_df = self.file_df["Loan List"]
        loan_list_df["Revolving / Delayed Drawdown"] = loan_list_df.apply(
            lambda row: (
                row["Partial PIK Loan Net Loan Balance"]
                if row["Loan Type (Term / Delayed Draw / Revolver)"] == "Delayed Draw"
                or row["Loan Type (Term / Delayed Draw / Revolver)"] == "Revolver"
                else 0
            ),
            axis=1,
        )

    def Discount_Loans(self):
        # rule =IF(S10="Yes",EC10,0)
        loan_list_df = self.file_df["Loan List"]
        loan_list_df["Discount Loans"] = loan_list_df.apply(
            lambda row: (
                row["Revolving / Delayed Drawdown Net Loan Balance"]
                if row["Discount Collateral Loan (Y/N)"] == "Yes"
                else 0
            ),
            axis=1,
        )

    def Credit_Improved_Loans(self):
        # rule =IF(Q10="Yes",EF10,0)
        loan_list_df = self.file_df["Loan List"]
        loan_list_df["Credit Improved Loans"] = loan_list_df.apply(
            lambda row: (
                row["Discount Loans Net Loan Balance"]
                if row["Credit Improved Loan (Y/N)"] == "Yes"
                else 0
            ),
            axis=1,
        )

    def Less_than_Quarterly_Pay(self):
        # rule =IF(BB10="Semi-Annually",EI10,0)
        loan_list_df = self.file_df["Loan List"]
        loan_list_df["Less Than Quarterly Pay"] = loan_list_df.apply(
            lambda row: (
                row["Credit Improved Loans Net Loan Balance"]
                if row["Interest Paid"] == "Semi-Annually"
                else 0
            ),
            axis=1,
        )

    def Warrants_to_Purchase_Equity_Securities(self):
        # Warrants to Purchase Equity Securities =IF(BH11="Yes",EL11,0)
        loan_list_df = self.file_df["Loan List"]
        loan_list_df["Warrants to Purchase Equity Securities"] = loan_list_df.apply(
            lambda row: (
                row["Less Than Quarterly Pay Net Loan Balance"]
                if row["Warrants to Purchase Equity (Y/N)"] == "Yes"
                else 0
            ),
            axis=1,
        )

    def LBO_Loan_with_Equity_to_Cap_lessthan_25(self):
        # LBO Loan with Equity to Cap <25% =IF(BI10="Yes",EO10,0)
        loan_list_df = self.file_df["Loan List"]
        loan_list_df["LBO Loan with Equity to Cap <25%"] = loan_list_df.apply(
            lambda row: (
                row["Net Loan Balance"] if row["LBO Loan (Y/N)"] == "Yes" else 0
            ),
            axis=1,
        )

    def Participation_Interests(self):
        # rule =IF(BJ10="Yes",ER10,0)
        loan_list_df = self.file_df["Loan List"]
        loan_list_df["Participation Interests"] = loan_list_df.apply(
            lambda row: (
                row["LBO Loan with Equity to Cap <25% Net Loan Balance"]
                if row["Parti-cipation (Y/N)"] == "Yes"
                else 0
            ),
            axis=1,
        )

    def Eligible_Covenant_Lite_Loans(self):
        # rule =IF(BT10="Yes",EU10,0)
        loan_list_df = self.file_df["Loan List"]
        loan_list_df["Eligible Covenant Lite Loans"] = loan_list_df.apply(
            lambda row: (
                row["Participation Interests Net Loan Balance"]
                if row["Eligible Covenant Lite (Y/N)"] == "Yes"
                else 0
            ),
            axis=1,
        )

    def Fixed_Rate_Loan(self):
        # rule =IF(AR10="Yes",EX10,0)
        loan_list_df = self.file_df["Loan List"]
        loan_list_df["Fixed Rate Loan"] = loan_list_df.apply(
            lambda row: (
                row["Eligible Covenant Lite Loans Net Loan Balance"]
                if row["Fixed Rate (Y/N)"] == "Yes"
                else 0
            ),
            axis=1,
        )

    def Agreed_Foreign_Currency(self):
        # Agreed Foreign Currency =IF(OR(BD10="EUR",BD10="AUD",BD10="CAD",BD10="GBP"),FA10,0)
        loan_list_df = self.file_df["Loan List"]
        loan_list_df["Agreed Foreign Currency"] = loan_list_df.apply(
            lambda row: (
                row["Fixed Rate Loan Net Loan Balance"]
                if row["Currency (USD / CAD / AUD / EUR)"]
                in ["EUR", "AUD", "CAD", "GBP"]
                else 0
            ),
            axis=1,
        )

    def Obligor_FE(self):
        # rule =FD10
        loan_list_df = self.file_df["Loan List"]

        loan_list_df["Obligor FE"] = loan_list_df[
            "Agreed Foreign Currency Net Loan Balance"
        ]

    def Excess_FF(self):
        loan_list_df = self.file_df["Loan List"]

        def calculate_excess(row, df):
            # If FD is 0, return 0

            if row["Agreed Foreign Currency Net Loan Balance"] == 0:

                return 0
            # VLOOKUP equivalent: find the matching value in GP and return the corresponding value in GQ
            vlookup_value = df.loc[
                df["Obligor No GP"] == row["Obligor"], "Haircut GQ"
            ].values

            if len(vlookup_value) == 0:
                return 0

            # Multiply the lookup value by FD

            return vlookup_value[0] * row["Agreed Foreign Currency Net Loan Balance"]

        # Apply the function to create the 'Excess' column
        loan_list_df["Obligor FE Excess"] = loan_list_df.apply(
            lambda row: calculate_excess(row, loan_list_df), axis=1
        )

    def Obligor_Industry_FH(self):
        # rule =FG10
        loan_list_df = self.file_df["Loan List"]

        loan_list_df["Obligor Industry FH"] = loan_list_df[
            "Obligor FE Net Loan Balance"
        ]

    def LTM_EBITDA_greater_than_equal_5000000_but_less_than_7500000(self):
        # rule =IF(SUM(CW10:DA10)>0,0,IF(AND(AL10>=5000000,AL10<7500000),FJ10,0))
        loan_list_df = self.file_df["Loan List"]

        loan_list_df["LTM EBITDA >= 5,000,000 but < 7,500,000"] = loan_list_df.apply(
            lambda row: (
                0
                if (
                    row["EBITDA Requirement Ongoing"]
                    + row["Leverage 10% Haircut"]
                    + row["Leverage 20% Haircut"]
                    + row["Leverage 35% Haircut"]
                    + row["Leverage - Final Haircut - 50%"]
                )
                > 0
                else (
                    row["Obligor Industry FH Net Loan Balance"]
                    if 5000000 <= row["Current TTM EBITDA"] < 7500000
                    else 0
                )
            ),
            axis=1,
        )

    def Excess_Haircut_to_1_Recovery_Rate_FL(self):
        loan_list_df = self.file_df["Loan List"]

        # Calculate FK3 as percent_FK2 multiplied by total concentration test balance
        FK3 = (
            self.percent_FK2
            * self.total_Concentration_Test_Balance_OPB_Eligible_Unfunded
        )
        sum_FK4 = loan_list_df["LTM EBITDA >= 5,000,000 but < 7,500,000"].sum()
        max_FK5 = max(0, sum_FK4 - FK3)

        # New rule implementation =IF(FK4<0.01,0,FK5/FK4)
        FK6 = 0 if sum_FK4 < 0.01 else max_FK5 / sum_FK4

        # Apply to 'Excess; Haircut to 1-Recovery Rate'
        loan_list_df["Excess; Haircut to 1-Recovery Rate FL"] = loan_list_df.apply(
            lambda row: (
                0
                if row["Loan Number"] == ""
                else row["LTM EBITDA >= 5,000,000 but < 7,500,000"]
                * FK6
                * (1 - row["Applicable Recovery Rate"])
            ),
            axis=1,
        )

    def LTM_EBITDA_less_than_15000000(self):
        # rule =IF(SUM(CW10:DA10)>0,0,IF(AL10<15000000,FM10,0))
        loan_list_df = self.file_df["Loan List"]
        loan_list_df["LTM EBITDA < 15,000,000"] = loan_list_df.apply(
            lambda row: (
                0
                if (
                    row["EBITDA Requirement Ongoing"]
                    + row["Leverage 10% Haircut"]
                    + row["Leverage 20% Haircut"]
                    + row["Leverage 35% Haircut"]
                    + row["Leverage - Final Haircut - 50%"]
                )
                > 0
                else (
                    row["Net Loan Balance FM"]
                    if row["Current TTM EBITDA"] < 15000000
                    else 0
                )
            ),
            axis=1,
        )

    def LTM_Snr_Debt_EBITDA(self):
        # LTM Snr Debt / EBITDA =IF(SUM(CW10:DA10)>0,0,IF(OR(AND(X10="No",AN10="Tier 1",AI10>$AG$3),AND(X10="No",AN10="Tier 2",AI10>$AH$3),AND(X10="No",AN10="Tier 3",AI10>$AI$3)),FP10,0))
        loan_list_df = self.file_df["Loan List"]
        haircut_df = self.file_df["Haircut"]
        loan_list_df["LTM Snr Debt / EBITDA"] = loan_list_df.apply(
            lambda row: (
                0
                if row[
                    [
                        "EBITDA Requirement Ongoing",
                        "Leverage 10% Haircut",
                        "Leverage 20% Haircut",
                        "Leverage 35% Haircut",
                        "Leverage - Final Haircut - 50%",
                    ]
                ].sum()
                > 0
                else (
                    row["Net Loan Balance FP"]
                    if (
                        (
                            row["Stretch Senior Loan (Y/N)"] == "No"
                            and row["Tier 1 / Tier 2 Obligor"] == "Tier 1"
                            and row["Current Senior Debt/EBITDA"]
                            > haircut_df.iat[self.conc_limit_tier1_row1_location]
                        )
                        or (
                            row["Stretch Senior Loan (Y/N)"] == "No"
                            and row["Tier 1 / Tier 2 Obligor"] == "Tier 2"
                            and row["Current Senior Debt/EBITDA"]
                            > haircut_df.iat[self.conc_limit_tier2_row1_location]
                        )
                        or (
                            row["Stretch Senior Loan (Y/N)"] == "No"
                            and row["Tier 1 / Tier 2 Obligor"] == "Tier 3"
                            and row["Current Senior Debt/EBITDA"]
                            > haircut_df.iat[self.conc_limit_tier3_row1_location]
                        )
                    )
                    else 0
                )
            ),
            axis=1,
        )

    def Excess_Haircut_to_1_Recovery_Rate_FO(self):
        loan_list_df = self.file_df["Loan List"]

        # Calculate FK3 as percent_FK2 multiplied by total concentration test balance
        FN3 = (
            self.percent_FN2
            * self.total_Concentration_Test_Balance_OPB_Eligible_Unfunded
        )
        sum_FN4 = loan_list_df["LTM EBITDA >= 5,000,000 but < 7,500,000"].sum()
        max_FK5 = max(0, sum_FN4 - FN3)

        # New rule implementation =IF(FK4<0.01,0,FK5/FK4)
        FN6 = 0 if sum_FN4 < 0.01 else max_FK5 / sum_FN4

        # Apply to 'Excess; Haircut to 1-Recovery Rate'
        loan_list_df["Excess; Haircut to 1-Recovery Rate FO"] = loan_list_df.apply(
            lambda row: (
                0
                if row["Loan Number"] == ""
                else row["LTM EBITDA < 15,000,000"]
                * FN6
                * (1 - row["Applicable Recovery Rate"])
            ),
            axis=1,
        )

    def LTM_Total_Debt_EBITDA(self):
        # rule =IF(SUM(CW10:DA10)>0,0,IF(OR(AND(X10="No",AN10="Tier 1",AJ10>$AG$4),AND(X10="No",AN10="Tier 2",AJ10>$AH$4),AND(X10="No",AN10="Tier 3",AJ10>$AI$4)),FP10,0))
        loan_list_df = self.file_df["Loan List"]
        # Load dataframes
        haircut_df = self.file_df["Haircut"]

        loan_list_df["LTM Total Debt / EBITDA"] = loan_list_df.apply(
            lambda row: (
                0
                if (
                    row["EBITDA Requirement Ongoing"]
                    + row["Leverage 10% Haircut"]
                    + row["Leverage 20% Haircut"]
                    + row["Leverage 35% Haircut"]
                    + row["Leverage - Final Haircut - 50%"]
                )
                > 0
                else (
                    row["Net Loan Balance FP"]
                    if (
                        (
                            row["Stretch Senior Loan (Y/N)"] == "No"
                            and row["Tier 1 / Tier 2 Obligor"] == "Tier 1"
                            and row["Current Total Debt/EBITDA"]
                            > haircut_df.iat[self.conc_limit_tier1_row2_location]
                        )
                        or (
                            row["Stretch Senior Loan (Y/N)"] == "No"
                            and row["Tier 1 / Tier 2 Obligor"] == "Tier 2"
                            and row["Current Total Debt/EBITDA"]
                            > haircut_df.iat[self.conc_limit_tier2_row2_location]
                        )
                        or (
                            row["Stretch Senior Loan (Y/N)"] == "No"
                            and row["Tier 1 / Tier 2 Obligor"] == "Tier 3"
                            and row["Current Total Debt/EBITDA"]
                            > haircut_df.iat[self.conc_limit_tier3_row2_location]
                        )
                    )
                    else 0
                )
            ),
            axis=1,
        )

    def Stretch_Senior_LTM_Total_Debt_EBITDA(self):
        # rule =IF(SUM(CW10:DA10)>0,0,IF(OR(AND(X10="Yes",AN10="Tier 1",AJ10>$AG$5),AND(X10="Yes",AN10="Tier 2",AJ10>$AH$5),AND(X10="Yes",AN10="Tier 3",AJ10>$AI$5)),FP10,0))
        loan_list_df = self.file_df["Loan List"]
        # Load dataframes
        haircut_df = self.file_df["Haircut"]
        loan_list_df["Stretch Senior LTM Total Debt / EBITDA"] = loan_list_df.apply(
            lambda row: (
                0
                if (
                    row["EBITDA Requirement Ongoing"]
                    + row["Leverage 10% Haircut"]
                    + row["Leverage 20% Haircut"]
                    + row["Leverage 35% Haircut"]
                    + row["Leverage - Final Haircut - 50%"]
                )
                > 0
                else (
                    row["Net Loan Balance FP"]
                    if (
                        (
                            row["Stretch Senior Loan (Y/N)"] == "Yes"
                            and row["Tier 1 / Tier 2 Obligor"] == "Tier 1"
                            and row["Current Total Debt/EBITDA"]
                            > haircut_df.iat[self.conc_limit_tier1_row3_location]
                        )
                        or (
                            row["Stretch Senior Loan (Y/N)"] == "Yes"
                            and row["Tier 1 / Tier 2 Obligor"] == "Tier 2"
                            and row["Current Total Debt/EBITDA"]
                            > haircut_df.iat[self.conc_limit_tier2_row3_location]
                        )
                        or (
                            row["Stretch Senior Loan (Y/N)"] == "Yes"
                            and row["Tier 1 / Tier 2 Obligor"] == "Tier 3"
                            and row["Current Total Debt/EBITDA"]
                            > haircut_df.iat[self.conc_limit_tier3_row3_location]
                        )
                    )
                    else 0
                )
            ),
            axis=1,
        )

    def Exceeds_Leverage_Limitation(self):
        # Exceeds Leverage Limitation =IF(SUM(FQ10:FS10)>0,FP10,0)
        loan_list_df = self.file_df["Loan List"]
        loan_list_df["Exceeds Leverage Limitation"] = loan_list_df.apply(
            lambda row: (
                row["Net Loan Balance FP"]
                if row[
                    [
                        "LTM Snr Debt / EBITDA",
                        "LTM Total Debt / EBITDA",
                        "Stretch Senior LTM Total Debt / EBITDA",
                    ]
                ].sum()
                > 0
                else 0
            ),
            axis=1,
        )

    def Excess_Haircut_to_1_Min_90percent_and_Market_Value(self):
        loan_list_df = self.file_df["Loan List"]
        FQ3 = (
            self.percent_FQ2
            * self.total_Concentration_Test_Balance_OPB_Eligible_Unfunded
        )
        sum_FQ4 = loan_list_df["Exceeds Leverage Limitation"].sum()
        sum_FR4 = loan_list_df["LTM Total Debt / EBITDA"].sum()
        sum_FS4 = loan_list_df["Stretch Senior LTM Total Debt / EBITDA"].sum()
        sum_FT4 = loan_list_df["Exceeds Leverage Limitation"].sum()
        max_FQ5 = max(0, sum_FT4 - FQ3)
        FQ6_percent = (
            0 if (sum_FQ4 + sum_FR4 + sum_FS4 + sum_FT4) < 0.01 else (max_FQ5 / sum_FT4)
        )
        # rule =IF(B10="",0,FT10*FQ$6*(1-MIN(90%,T10)))
        loan_list_df["Excess; Haircut to 1-Min(90% and Market Value)"] = (
            loan_list_df.apply(
                lambda row: (
                    0
                    if row["Loan Number"] == ""
                    else row["Exceeds Leverage Limitation"]
                    * FQ6_percent
                    * (1 - min(0.9, row["Market Value"]))
                ),
                axis=1,
            )
        )

    def Excess_FI(self):
        loan_list_df = self.file_df["Loan List"]
        lookup_df = (
            loan_list_df[["Industry No (Matched)", "Haircut GH"]]
            .dropna()
            .set_index("Industry No (Matched)")
        )

        def calculate_excess(row, lookup_df):

            if (
                pd.isna(row["Lookups'!F2:F3 No"])
                or row["Obligor FE Net Loan Balance"] < 0.01
            ):

                return 0
            else:
                lookup_value = lookup_df.get(row["Lookups'!F2:F3 No"], np.nan)
                return (
                    lookup_value * row["Obligor FE Net Loan Balance"]
                    if pd.notna(lookup_value)
                    else 0
                )

        # Apply the function to each row

        loan_list_df["Obligor Industry FH Excess"] = loan_list_df.apply(
            lambda row: calculate_excess(row, lookup_df), axis=1
        )

    def Net_Loan_Balance_FW(self):
        # Net Loan Balance FW =IF(AND(N10="No",DG10=0),FV10,IF(AND(N10="No",DG10<>0,K10=0),0,IF(AND(N10="No",DG10<>0,K10>0,J10<>K10),MAX(0,M10-(DF10-FV10)),DE10)))
        loan_list_df = self.file_df["Loan List"]
        loan_list_df["Net Loan Balance FW"] = loan_list_df.apply(
            lambda row: (
                row["Excess Concentration Test"]
                if (
                    row["Defaulted Collateral Loan / Material Mod (Y/N)"] == "No"
                    and row["Revolving Exposure"] == 0
                )
                else (
                    0
                    if (
                        row["Defaulted Collateral Loan / Material Mod (Y/N)"] == "No"
                        and row["Revolving Exposure"] != 0
                        and row["Eligible Outstanding Principal Balance (USD)"] == 0
                    )
                    else (
                        max(
                            0,
                            row["Outstanding Principal Balance (USD)"]
                            - (
                                row[
                                    "Concentration Test Balance - OPB + Eligible Unfunded"
                                ]
                                - row["Excess Concentration Test"]
                            ),
                        )
                        if (
                            row["Defaulted Collateral Loan / Material Mod (Y/N)"]
                            == "No"
                            and row["Revolving Exposure"] != 0
                            and row["Eligible Outstanding Principal Balance (USD)"] > 0
                            and row["Total Commitment (USD)"]
                            != row["Eligible Outstanding Principal Balance (USD)"]
                        )
                        else row[
                            "Aggregate Collateral Balance (Post Eligibility; Including Eligible Unfunded)"
                        ]
                    )
                )
            ),
            axis=1,
        )

    def Borrowing_Base(self):
        # Borrowing Base =+FW10*V10
        loan_list_df = self.file_df["Loan List"]
        loan_list_df["Borrowing Base"] = (
            loan_list_df["Net Loan Balance FW"] * loan_list_df["Advance Rate"]
        )

    def Calculate_Excess_Concentrations(self):
        # try:
        # Perform calculations
        self.Second_Lien_and_Split_Lien()  # column DL
        self.Excess(
            "Second Lien and Split Lien Excess",
            "Second Lien and Split Lien",
            self.Limit_percent_DL,
        )  # column DM
        self.Net_Loan_Balance(
            "Second Lien and Split Lien Net Loan Balance",
            "Second Lien and Split Lien Excess",
            "Aggregate Collateral Balance (Post Eligibility; Including Eligible Unfunded)",
        )  # column DN

        self.Second_Lien()  # column DO

        self.Excess(
            "Second Lien Excess", "Second Lien", self.Limit_percent_DO
        )  # column DP
        self.Net_Loan_Balance(
            "Second Lien Net Loan Balance",
            "Second Lien Excess",
            "Second Lien and Split Lien Net Loan Balance",
        )  # column DQ

        self.DIP_Collateral_Loans()  # column DR
        self.Excess(
            "DIP Collateral Loans Excess", "DIP Collateral Loans", self.Limit_percent_DR
        )  # column DS
        self.Net_Loan_Balance(
            "DIP Collateral Loans Net Loan Balance",
            "DIP Collateral Loans Excess",
            "Second Lien Net Loan Balance",
        )  # column DT

        self.Eligible_Foreign_Country()  # column DU
        self.Excess(
            "Eligible Foreign Country Excess",
            "Eligible Foreign Country",
            self.Limit_percent_DU,
        )  # column DV
        self.Net_Loan_Balance(
            "Eligible Foreign Country Net Loan Balance",
            "Eligible Foreign Country Excess",
            "DIP Collateral Loans Net Loan Balance",
        )  # column DW

        self.Partial_PIK_Loan()  # column DX
        self.Excess(
            "Partial PIK Loan Excess", "Partial PIK Loan", self.Limit_percent_DX
        )  # column DY
        self.Net_Loan_Balance(
            "Partial PIK Loan Net Loan Balance",
            "Partial PIK Loan Excess",
            "Eligible Foreign Country Net Loan Balance",
        )  # column DZ

        self.Revolving_Delayed_Drawdown()  # column EA
        self.Excess(
            "Revolving / Delayed Drawdown Excess",
            "Revolving / Delayed Drawdown",
            self.Limit_percent_EA,
        )  # column EB
        self.Net_Loan_Balance(
            "Revolving / Delayed Drawdown Net Loan Balance",
            "Revolving / Delayed Drawdown Excess",
            "Partial PIK Loan Net Loan Balance",
        )  # column EC

        self.Discount_Loans()  # column ED
        self.Excess(
            "Discount Loans Excess", "Discount Loans", self.Limit_percent_ED
        )  # column EE
        self.Net_Loan_Balance(
            "Discount Loans Net Loan Balance",
            "Discount Loans Excess",
            "Revolving / Delayed Drawdown Net Loan Balance",
        )  # column EF

        self.Credit_Improved_Loans()  # column EG
        self.Excess(
            "Credit Improved Loans Excess",
            "Credit Improved Loans",
            self.Limit_percent_EG,
        )  # column EH
        self.Net_Loan_Balance(
            "Credit Improved Loans Net Loan Balance",
            "Credit Improved Loans Excess",
            "Discount Loans Net Loan Balance",
        )  # column EI

        self.Less_than_Quarterly_Pay()  # column EJ
        self.Excess(
            "Less Than Quarterly Pay Excess",
            "Less Than Quarterly Pay",
            self.Limit_percent_EJ,
        )  # column EK
        self.Net_Loan_Balance(
            "Less Than Quarterly Pay Net Loan Balance",
            "Less Than Quarterly Pay Excess",
            "Credit Improved Loans Net Loan Balance",
        )  # column EL

        self.Warrants_to_Purchase_Equity_Securities()  # column EM
        self.Excess(
            "Warrants to Purchase Equity Securities Excess",
            "Warrants to Purchase Equity Securities",
            self.Limit_percent_EM,
        )  # column EN
        self.Net_Loan_Balance(
            "Warrants to Purchase Equity Securities Net Loan Balance",
            "Warrants to Purchase Equity Securities Excess",
            "Less Than Quarterly Pay Net Loan Balance",
        )  # column EO

        self.LBO_Loan_with_Equity_to_Cap_lessthan_25()  # column EP
        self.Excess(
            "LBO Loan with Equity to Cap <25% Excess",
            "LBO Loan with Equity to Cap <25%",
            self.Limit_percent_EP,
        )  # column EQ
        self.Net_Loan_Balance(
            "LBO Loan with Equity to Cap <25% Net Loan Balance",
            "LBO Loan with Equity to Cap <25% Excess",
            "Warrants to Purchase Equity Securities Net Loan Balance",
        )  # column ER

        self.Participation_Interests()  # column ES
        self.Excess(
            "Participation Interests Excess",
            "Participation Interests",
            self.Limit_percent_ES,
        )  # column ET
        self.Net_Loan_Balance(
            "Participation Interests Net Loan Balance",
            "Participation Interests Excess",
            "LBO Loan with Equity to Cap <25% Net Loan Balance",
        )  # column EU

        self.Eligible_Covenant_Lite_Loans()  # column EV
        self.Excess(
            "Eligible Covenant Lite Loans Excess",
            "Eligible Covenant Lite Loans",
            self.Limit_percent_EV,
        )  # column EW
        self.Net_Loan_Balance(
            "Eligible Covenant Lite Loans Net Loan Balance",
            "Eligible Covenant Lite Loans Excess",
            "Participation Interests Net Loan Balance",
        )  # column EX

        self.Fixed_Rate_Loan()  # column EY
        self.Excess(
            "Fixed Rate Loan Excess", "Fixed Rate Loan", self.Limit_percent_EY
        )  # column EZ
        self.Net_Loan_Balance(
            "Fixed Rate Loan Net Loan Balance",
            "Fixed Rate Loan Excess",
            "Eligible Covenant Lite Loans Net Loan Balance",
        )  # column FA

        self.Agreed_Foreign_Currency()  # column FB
        self.Excess(
            "Agreed Foreign Currency Excess",
            "Agreed Foreign Currency",
            self.Limit_percent_FB,
        )  # column FC
        self.Net_Loan_Balance(
            "Agreed Foreign Currency Net Loan Balance",
            "Agreed Foreign Currency Excess",
            "Fixed Rate Loan Net Loan Balance",
        )  # column FD

        self.Obligor_FE()  # column FE
        self.Obligor_GJ_GQ()  # column GJ to GQ
        self.Obligor_new_GX_new_HE()
        self.Excess_FF()  # column FF
        self.Net_Loan_Balance(
            "Obligor FE Net Loan Balance",
            "Obligor FE Excess",
            "Agreed Foreign Currency Net Loan Balance",
        )  # column FG

        self.Industry_FZ_GH()  # column FZ to GH

        self.Obligor_Industry_FH()  # column FH
        self.Excess_FI()  # column FI
        self.Net_Loan_Balance(
            "Obligor Industry FH Net Loan Balance",
            "Obligor Industry FH Excess",
            "Obligor FE Net Loan Balance",
        )  # column FJ

        # top 5 obligors FM
        self.top_5_Obligor()
        # excess FN
        self.top_5_obligors_excess()
        # net loan balance FO

        self.Net_Loan_Balance(
            "Top 5 Obligors Net Loan Balance",
            "Top 5 Obligors Excess",
            "Obligor Industry FH Net Loan Balance",
        )

        self.LTM_EBITDA_greater_than_equal_5000000_but_less_than_7500000()  # column FK
        self.Excess_Haircut_to_1_Recovery_Rate_FL()  # column FL
        self.Net_Loan_Balance(
            "Net Loan Balance FM",
            "Excess; Haircut to 1-Recovery Rate FL",
            "Top 5 Obligors Net Loan Balance",
        )  # column FM

        self.LTM_EBITDA_less_than_15000000()  # column FN
        self.Excess_Haircut_to_1_Recovery_Rate_FO()  # column FO
        self.Net_Loan_Balance(
            "Net Loan Balance FP",
            "Excess; Haircut to 1-Recovery Rate FO",
            "Net Loan Balance FM",
        )  # column FP

        self.LTM_Snr_Debt_EBITDA()  # column FQ
        self.LTM_Total_Debt_EBITDA()  # column FR
        self.Stretch_Senior_LTM_Total_Debt_EBITDA()  # column FS
        self.Exceeds_Leverage_Limitation()  # column FT
        self.Excess_Haircut_to_1_Min_90percent_and_Market_Value()  # column FU
        self.Net_Loan_Balance(
            "Excess Concentration Test",
            "Excess; Haircut to 1-Min(90% and Market Value)",
            "Net Loan Balance FP",
        )  # column FV
        self.Net_Loan_Balance_FW()  # column FW
        self.Borrowing_Base()  # column FX

        self.Calculate_GS_GZ()  # column GS to GZ

    # except Exception as e:
    #     print(f"Error occurred while reading the file: {e}")
    #     return None


# file_path = pathlib.Path("PFLT_Sub_Borrowing_Base_Second_Level_Formulas.xlsx")
# file_obj = file_path.open(mode="rb")
# file_df = pd.read_excel(file_obj, sheet_name=None)

# slc = ExcessConcentrations(file_df)
# slc.Calculate_Excess_Concentrations()

# output_file_path = "PFLT_Sub_Borrowing_Base_ExcessConcentrations_Formulas.xlsx"
# with pd.ExcelWriter(output_file_path) as writer:
#     for sheet, dataframe in slc.self.file_df.items():
#         dataframe.to_excel(writer, sheet_name=sheet, index=False)
