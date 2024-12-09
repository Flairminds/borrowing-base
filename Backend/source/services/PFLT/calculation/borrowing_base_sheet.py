import pathlib
import pandas as pd
import numpy as np
from source.services.PFLT.calculation.Cash_and_credit import CashAndCredit as CC


class PFLT_BorrowingBase_calculation(CC):
    def __init__(self):
        self.Facility_Amount_less_value = (
            300000000 + 66000000 + 20000000 + 50000000 + 175000000
        )

        self.input_J13 = (
            self.file_df["Exchange Rates"]
            .loc[self.file_df["Exchange Rates"]["Currency"] == "CAD", "Exchange Rate"]
            .values[0]
        )
        self.input_J15 = (
            self.file_df["Exchange Rates"]
            .loc[self.file_df["Exchange Rates"]["Currency"] == "EUR", "Exchange Rate"]
            .values[0]
        )
        self.input_J14 = (
            self.file_df["Exchange Rates"]
            .loc[self.file_df["Exchange Rates"]["Currency"] == "AUD", "Exchange Rate"]
            .values[0]
        )
        super().__init__()

    def B_Cash_on_deposit_in_Principal_Collection_Subaccount(self):
        # Cash on deposit in Principal Collection Subaccount =+O51+O59*Inputs!J13+'Borrowing Base'!O67*Inputs!J15+'Borrowing Base'!O75*Inputs!J14
        # cash_on_deposit = (
        #     self.BB_O51 +
        #     self.BB_O59 * self.input_J13 +
        #     self.BB_O67 * self.input_J15 +
        #     self.BB_O75 * self.input_J14
        # )
        # self.file_df["Borrowing Base"]["(B) Cash on deposit in Principal Collection Subaccount"] = cash_on_deposit
        # -----------------------------------------
        Cash_Balance_Projections_df = self.file_df["Cash Balance Projections"]
        Cash_Balance_Projections_df["Cash On Deposite"] = (
            Cash_Balance_Projections_df["Cash - Net of UnSettled Trades"]
            * Cash_Balance_Projections_df["Exchange Rates"]
        )
        self.file_df["Borrowing Base"][
            "(B) Cash on deposit in Principal Collection Subaccount"
        ] = Cash_Balance_Projections_df["Cash On Deposite"].sum()

    # Define functions for calculations
    def CONCENTRATION_TEST_AMOUNT(self):
        concentration_test_amount = self.file_df["Loan List"][
            "Concentration Test Balance - OPB + Eligible Unfunded"
        ].sum()
        return concentration_test_amount

    def i_Aggregate_Principal_Balance_of_all_Collateral_Loans_other_than_Defaulted_Restructured_Haircut_Ineligible_and_Discount(
        self,
    ):
        loan_list_df = self.file_df["Loan List"]
        return loan_list_df.loc[
            loan_list_df["Loan Eligibility Flag"].fillna(0).replace("", 0) > 0,
            "Outstanding Principal Balance",
        ].sum()

    def ii_Defaulted_Collateral_Loan_Balance(self):
        return self.file_df["Loan List"]["Defaulted Test"].sum()

    def iii_The_aggregate_purchase_price_of_all_Discount_Loans_that_are_Eligible_Collateral_Loans_and_not_Defaulted_Haircut_or_Restructured(
        self,
    ):
        return self.file_df["Loan List"]["Discount Test"].sum()

    def iv_The_aggregate_Unfunded_Commitments_of_all_Delayed_Drawdown_and_Revolvers_that_are_Eligible_Loans(
        self,
    ):
        return self.file_df["Loan List"]["Total Unfunded"].sum()

    def v_The_Credit_Improved_Loan_Balance(self):
        return self.file_df["Loan List"]["Credit Improved Test"].sum()

    def vi_The_Haircut_Collateral_Loan_Balance(self):
        return self.file_df["Loan List"]["Haircut Test"].sum()

    def Date_of_determination(self):
        inputs_df = self.file_df["Inputs"]
        datermination_date = inputs_df.loc[
            inputs_df["INPUTS"] == "Determination Date", "Values"
        ].values[0]
        self.file_df["Borrowing Base"]["Date of determination:"] = datermination_date

    def Aggregate_Collateral_Balance_without_duplication_sum_of_i_vi(self):
        self.file_df["Borrowing Base"][
            "Aggregate Collateral Balance (without duplication) sum of (i)-(vi)"
        ] = self.file_df["Borrowing Base"][
            [
                "(i) Aggregate Principal Balance of all Collateral Loans (other than Defaulted, Restructured, Haircut Ineligible, and Discount)",
                "(ii) Defaulted Collateral Loan Balance",
                "(iii) The aggregate purchase price of all Discount Loans that are Eligible Collateral Loans and not Defaulted, Haircut or Restructured",
                "(iv) The aggregate Unfunded Commitments of all Delayed Drawdown and Revolvers that are Eligible Loans",
                "(v) The Credit Improved Loan Balance",
                "(vi) The Haircut Collateral Loan Balance",
            ]
        ].sum(
            axis=1
        )

    def Excess_Concentration_Amount(self):
        self.file_df["Borrowing Base"]["Excess Concentration Amount"] = self.file_df[
            "Loan List"
        ]["Excess Concentration Amount (Dynamic)"].sum()

    def BORROWING_BASE_A_minus_B_minus_A_iv(self):
        self.file_df["Borrowing Base"][
            "BORROWING BASE - (A) minus (B) minus (A)(iv)"
        ] = (
            self.file_df["Borrowing Base"][
                "Aggregate Collateral Balance (without duplication) sum of (i)-(vi)"
            ]
            - self.file_df["Borrowing Base"]["Excess Concentration Amount"]
            - self.file_df["Borrowing Base"][
                "(iv) The aggregate Unfunded Commitments of all Delayed Drawdown and Revolvers that are Eligible Loans"
            ]
        )

    def Facility_Amountless(self):
        # to call
        # Facility Amount, less =300000000+66000000+20000000+50000000+175000000
        self.Facility_Amount_less_value = (
            300000000 + 66000000 + 20000000 + 50000000 + 175000000
        )
        self.file_df["Borrowing Base"][
            "Facility Amount, less"
        ] = self.Facility_Amount_less_value

    def Revolving_Exposure_Plus(self):
        self.file_df["Borrowing Base"]["(A) Revolving Exposure, plus"] = self.file_df[
            "Loan List"
        ]["Eligible Unfunded"].sum()

    def x_Borrowing_Base_multipled_by(self):
        self.file_df["Borrowing Base"]["(x) Borrowing Base, multipled by"] = (
            self.file_df["Borrowing Base"][
                "BORROWING BASE - (A) minus (B) minus (A)(iv)"
            ]
        )

    def y_Weighted_Average_Advance_Rate_minus(self):
        loan_list_df = self.file_df["Loan List"]

        # Mask for Net Loan Balance FW > 0
        mask = loan_list_df["Net Loan Balance FW"] > 0

        # Calculate the weighted sum (SUMPRODUCT equivalent)
        weighted_sum = (
            loan_list_df.loc[mask, "Net Loan Balance FW"]
            * loan_list_df.loc[mask, "Advance Rate"]
        ).sum()

        # Calculate the total weight (SUMPRODUCT equivalent for FW)
        total_weight = loan_list_df.loc[mask, "Net Loan Balance FW"].sum()

        # Compute the weighted average advance rate
        result = np.where(total_weight != 0, weighted_sum / total_weight, "N/A")

        # Assign the result to the appropriate column in the borrowing base DataFrame
        self.file_df["Borrowing Base"][
            "(y) Weighted Average Advance Rate, minus"
        ] = result

    def Foreign_Currency_Variability_Reserve_minus(self):
        self.file_df["Borrowing Base"][
            "Foreign Currency Variability Reserve, minus"
        ] = self.file_df["Loan List"]["Foreign Currency Variability Reserve"].sum()

    def Revolving_Exposure_plus(self):
        self.file_df["Borrowing Base"]["(B) Revolving Exposure, plus"] = self.file_df[
            "Loan List"
        ]["Eligible Unfunded"].sum()

    def Total_Of_Above_5(self):
        # Convert columns to numeric, coercing errors to NaN (not a number)
        self.file_df["Borrowing Base"]["(x) Borrowing Base, multipled by"] = (
            pd.to_numeric(
                self.file_df["Borrowing Base"]["(x) Borrowing Base, multipled by"],
                errors="coerce",
            )
        )
        self.file_df["Borrowing Base"]["(y) Weighted Average Advance Rate, minus"] = (
            pd.to_numeric(
                self.file_df["Borrowing Base"][
                    "(y) Weighted Average Advance Rate, minus"
                ],
                errors="coerce",
            )
        )
        self.file_df["Borrowing Base"][
            "Foreign Currency Variability Reserve, minus"
        ] = pd.to_numeric(
            self.file_df["Borrowing Base"][
                "Foreign Currency Variability Reserve, minus"
            ],
            errors="coerce",
        )
        self.file_df["Borrowing Base"]["(B) Revolving Exposure, plus"] = pd.to_numeric(
            self.file_df["Borrowing Base"]["(B) Revolving Exposure, plus"],
            errors="coerce",
        )
        self.file_df["Borrowing Base"][
            "(B) Cash on deposit in Principal Collection Subaccount"
        ] = pd.to_numeric(
            self.file_df["Borrowing Base"][
                "(B) Cash on deposit in Principal Collection Subaccount"
            ],
            errors="coerce",
        )
        self.file_df["Borrowing Base"][
            "(B) Amount on deposit in the Revolving Reserve Account"
        ] = pd.to_numeric(
            self.file_df["Borrowing Base"][
                "(B) Amount on deposit in the Revolving Reserve Account"
            ],
            errors="coerce",
        )

        # Calculate the result
        self.file_df["Borrowing Base"]["(B) Total Of Above 5"] = (
            (
                self.file_df["Borrowing Base"]["(x) Borrowing Base, multipled by"]
                * self.file_df["Borrowing Base"][
                    "(y) Weighted Average Advance Rate, minus"
                ]
            )
            - self.file_df["Borrowing Base"][
                "Foreign Currency Variability Reserve, minus"
            ]
            - self.file_df["Borrowing Base"]["(B) Revolving Exposure, plus"]
            + self.file_df["Borrowing Base"][
                "(B) Cash on deposit in Principal Collection Subaccount"
            ]
            + self.file_df["Borrowing Base"][
                "(B) Amount on deposit in the Revolving Reserve Account"
            ]
        )

    def Aggregate_Collateral_Balance_minus(self):
        self.file_df["Borrowing Base"]["Aggregate Collateral Balance, minus"] = (
            self.file_df["Borrowing Base"][
                "Aggregate Collateral Balance (without duplication) sum of (i)-(vi)"
            ]
            - self.file_df["Borrowing Base"][
                "(iv) The aggregate Unfunded Commitments of all Delayed Drawdown and Revolvers that are Eligible Loans"
            ]
        )

    def Minimum_Equity_Amount_plus(self):
        # Extract the GX column (Obligor Loan Balance_GX) from the "Loan List" sheet
        obligor_loan_balance_gx = self.file_df["Loan List"][
            "Obligor Loan Balance_GX"
        ].values

        # Sort the values in descending order and select the top 3 largest values
        top_3_largest = np.sort(obligor_loan_balance_gx)[-3:]

        # Calculate the sum of the top 3 largest values
        sum_top_3_largest = np.sum(top_3_largest)

        # Access the 'Minimum Equity Amount Floor' value from the 'Inputs' sheet
        input_value = (
            self.file_df["Inputs"]
            .loc[
                self.file_df["Inputs"]["INPUTS"] == "Minimum Equity Amount Floor",
                "Values",
            ]
            .values[0]
        )

        # Calculate the final value by taking the max between input_value and sum_top_3_largest
        borrowing_base_value = max(input_value, sum_top_3_largest)

        # Assign the result to the appropriate column in the borrowing base DataFrame
        self.file_df["Borrowing Base"][
            "Minimum Equity Amount, plus"
        ] = borrowing_base_value

    def C_Cash_on_deposit_in_Principal_Collection_Subaccount(self):
        self.file_df["Borrowing Base"][
            "(C) Cash on deposit in Principal Collection Subaccount"
        ] = self.file_df["Borrowing Base"][
            "(B) Cash on deposit in Principal Collection Subaccount"
        ]

    def MAXIMUM_AVAILABLE_AMOUNT_Least_of_A_B_and_C(self):
        self.file_df["Borrowing Base"][
            "MAXIMUM AVAILABLE AMOUNT - Least of (A), (B) and (C)"
        ] = (
            self.file_df["Borrowing Base"][
                ["(A) Total of above 3", "(B) Total Of Above 5", "(C) Total of above 3"]
            ]
        ).min(
            axis=1
        )

    def Advances_Outstanding_at_beginning_of_the_Interest_Accrual_Period(self):
        # result = self.BB_O13 + self.BB_O9 * self.input_J14 + self.BB_O17 * self.input_J13 + self.BB_O21 * self.input_J15
        # self.file_df["Borrowing Base"]["Advances Outstanding at beginning of the Interest Accrual Period"] = result

        # --------------
        Credit_Balance_Projection_df = self.file_df["Credit Balance Projection"]
        Credit_Balance_Projection_df["Advance Outstanding"] = (
            Credit_Balance_Projection_df["Current Credit Facility Balance"]
            * Credit_Balance_Projection_df["Exchange Rates"]
        )
        self.file_df["Borrowing Base"][
            "Advances Outstanding at beginning of the Interest Accrual Period"
        ] = Credit_Balance_Projection_df["Advance Outstanding"].sum()
        Credit_Balance_Projection_df.drop(["Advance Outstanding"], axis=1, inplace=True)

    def Advances_Repayments_during_the_period_through_and_including_TEXT(self):
        # Advances/(Repayments) during the period through and including & TEXT =+O14+O10*Inputs!J14+'Borrowing Base'!O18*Inputs!J13+'Borrowing Base'!O22*Inputs!J15
        # result = self.BB_O14 + self.BB_O10 * self.input_J14 + self.BB_O18 * self.input_J13 + self.BB_O22 * self.input_J15
        # self.file_df["Borrowing Base"]["Advances/(Repayments) during the period through and including & TEXT"] = result
        # -----------------------------
        Cash_Balance_Projections_df = self.file_df["Cash Balance Projections"]
        Cash_Balance_Projections_df["Repayments"] = (
            Cash_Balance_Projections_df["Borrowing"]
            * Cash_Balance_Projections_df["Exchange Rates"]
        )
        self.file_df["Borrowing Base"][
            "Advances/(Repayments) during the period through and including & TEXT"
        ] = Cash_Balance_Projections_df["Repayments"].sum()

    def cash_balance_projection_calculation(self):
        Cash_Balance_Projections_df = self.file_df["Cash Balance Projections"]
        Cash_Balance_Projections_df = Cash_Balance_Projections_df.fillna(0)
        Cash_Balance_Projections_df["Cash - Budgeted & PostBorrowing"] = (
            Cash_Balance_Projections_df["Cash - Current & PreBorrowing"]
            + Cash_Balance_Projections_df["Borrowing"]
        )
        # considering Additional Expences 1, Additional Expences 2, Additional Expences 3 will always be there in base data file
        # Cash_Balance_Projections_df["Cash - Net of UnSettled Trades"] = [1,2,3,4]
        Cash_Balance_Projections_df["Cash - Net of UnSettled Trades"] = (
            Cash_Balance_Projections_df["Cash - Budgeted & PostBorrowing"]
            + Cash_Balance_Projections_df["Additional Expences 1"]
            + Cash_Balance_Projections_df["Additional Expences 2"]
            + Cash_Balance_Projections_df["Additional Expences 3"]
        )

        self.file_df["Cash Balance Projections"] = Cash_Balance_Projections_df

    def Credit_Balance_Projection(self):
        Cash_Balance_Projections_df = self.file_df["Cash Balance Projections"]
        Credit_Balance_Projection = self.file_df["Credit Balance Projection"]
        Credit_Balance_Projection["Exchange Rates"] = Cash_Balance_Projections_df[
            "Exchange Rates"
        ]
        Credit_Balance_Projection["Borrowing"] = Cash_Balance_Projections_df[
            "Borrowing"
        ]
        Credit_Balance_Projection["Projected Credit Facility Balance"] = (
            Credit_Balance_Projection["Current Credit Facility Balance"]
            + Credit_Balance_Projection["Borrowing"]
        )

        self.file_df["Credit Balance Projection"] = Credit_Balance_Projection

    def Borrowing_Base_Sheet(self):
        # Create a DataFrame to store results

        self.cash_balance_projection_calculation()
        self.Credit_Balance_Projection()

        bb_df_creation = pd.DataFrame(
            {
                "Concentration Test Amount": [self.CONCENTRATION_TEST_AMOUNT()],
                "(i) Aggregate Principal Balance of all Collateral Loans (other than Defaulted, Restructured, Haircut Ineligible, and Discount)": [
                    self.i_Aggregate_Principal_Balance_of_all_Collateral_Loans_other_than_Defaulted_Restructured_Haircut_Ineligible_and_Discount()
                ],
                "(ii) Defaulted Collateral Loan Balance": [
                    self.ii_Defaulted_Collateral_Loan_Balance()
                ],
                "(iii) The aggregate purchase price of all Discount Loans that are Eligible Collateral Loans and not Defaulted, Haircut or Restructured": [
                    self.iii_The_aggregate_purchase_price_of_all_Discount_Loans_that_are_Eligible_Collateral_Loans_and_not_Defaulted_Haircut_or_Restructured()
                ],
                "(iv) The aggregate Unfunded Commitments of all Delayed Drawdown and Revolvers that are Eligible Loans": [
                    self.iv_The_aggregate_Unfunded_Commitments_of_all_Delayed_Drawdown_and_Revolvers_that_are_Eligible_Loans()
                ],
                "(v) The Credit Improved Loan Balance": [
                    self.v_The_Credit_Improved_Loan_Balance()
                ],
                "(vi) The Haircut Collateral Loan Balance": [
                    self.vi_The_Haircut_Collateral_Loan_Balance()
                ],
            }
        )
        self.file_df["Borrowing Base"] = bb_df_creation
        self.Date_of_determination()
        self.Aggregate_Collateral_Balance_without_duplication_sum_of_i_vi()
        self.Excess_Concentration_Amount()
        self.BORROWING_BASE_A_minus_B_minus_A_iv()
        self.Facility_Amountless()
        self.Revolving_Exposure_Plus()
        self.file_df["Borrowing Base"][
            "(A) Amount on deposit in the Revolving Reserve Account"
        ] = [0]
        self.file_df["Borrowing Base"]["(A) Total of above 3"] = (
            self.file_df["Borrowing Base"]["Facility Amount, less"]
            - self.file_df["Borrowing Base"]["(A) Revolving Exposure, plus"]
            + self.file_df["Borrowing Base"][
                "(A) Amount on deposit in the Revolving Reserve Account"
            ]
        )
        self.x_Borrowing_Base_multipled_by()
        self.y_Weighted_Average_Advance_Rate_minus()
        self.Foreign_Currency_Variability_Reserve_minus()
        self.Revolving_Exposure_plus()
        self.B_Cash_on_deposit_in_Principal_Collection_Subaccount()
        self.file_df["Borrowing Base"][
            "(B) Amount on deposit in the Revolving Reserve Account"
        ] = self.file_df["Borrowing Base"][
            "(A) Amount on deposit in the Revolving Reserve Account"
        ]
        self.Total_Of_Above_5()
        self.Aggregate_Collateral_Balance_minus()
        self.Minimum_Equity_Amount_plus()
        self.C_Cash_on_deposit_in_Principal_Collection_Subaccount()
        self.file_df["Borrowing Base"]["(C) Total of above 3"] = (
            self.file_df["Borrowing Base"]["Aggregate Collateral Balance, minus"]
            - self.file_df["Borrowing Base"]["Minimum Equity Amount, plus"]
            + self.file_df["Borrowing Base"][
                "(C) Cash on deposit in Principal Collection Subaccount"
            ]
        )
        self.MAXIMUM_AVAILABLE_AMOUNT_Least_of_A_B_and_C()
        self.Advances_Outstanding_at_beginning_of_the_Interest_Accrual_Period()
        self.Advances_Repayments_during_the_period_through_and_including_TEXT()
        self.file_df["Borrowing Base"]["Advances Outstanding as of & TEXT"] = (
            self.file_df["Borrowing Base"][
                "Advances Outstanding at beginning of the Interest Accrual Period"
            ]
            + self.file_df["Borrowing Base"][
                "Advances/(Repayments) during the period through and including & TEXT"
            ]
        )
        self.file_df["Borrowing Base"]["(A) Maximum Available Amount"] = self.file_df[
            "Borrowing Base"
        ]["MAXIMUM AVAILABLE AMOUNT - Least of (A), (B) and (C)"]
        self.file_df["Borrowing Base"]["(B) Advances"] = self.file_df["Borrowing Base"][
            "Advances Outstanding as of & TEXT"
        ]
        self.file_df["Borrowing Base"]["AVAILABILITY - (a) minus (b)"] = (
            self.file_df["Borrowing Base"]["(A) Maximum Available Amount"]
            - self.file_df["Borrowing Base"]["(B) Advances"]
        )
        self.file_df["Borrowing Base"] = self.file_df["Borrowing Base"].T.reset_index()
        self.file_df["Borrowing Base"].columns = ["Terms", "Values"]

    # Add the new sheet to the Excel file
    # with pd.ExcelWriter(file_path, engine='openpyxl', mode='a') as writer:
    #     Borrowing Base.to_excel(writer, sheet_name="Borrowing Base", index=False)
