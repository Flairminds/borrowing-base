import copy
import pathlib
import pandas as pd
from source.services.PFLT.calculation.PFLT_Calculation_Initiator import (
    PFLTCalculationInitiator,
)
from numerize import numerize
from source.concentration_test_application import ConcentraionTestFormatter


class PFLTBorrowingBase(PFLTCalculationInitiator):
    def __init__(self, file_df):
        self.file_df = file_df
        super().__init__()

    def calculate(self):
        self.PFLTBB_calculation_First_Level_Formulas()
        # self.file_df = pd.read_excel("PFLT_Loan_List_Output.xlsx", sheet_name=None)
        # return self.file_df

    def generate_response(self):
        try:
            card_data = self.card_data()
            segmentation = self.segmentation()
            # concentration = self.concentration_test_data()
            concentration = self.concentration_test_data_from_base_sheet()
            # security_data = self.security_data()
            security_data = self.security_data_from_base_sheet()
            # security_chart_data = self.security_chart_data()
            security_chart_data = self.security_chart_data_from_sheet()
            # principal_data = self.principal_obligation_data()
            principal_data = self.principal_obligation_data_from_sheet()
            # segmentation_chart_data = self.segmentation_chart_data()
            segmentation_chart_data = self.segmentation_chart_data_from_sheet()

            return {
                "card_data": card_data,
                "segmentation_overview_data": segmentation,
                "concentration_test_data": concentration,
                "security_data": security_data,
                "security_chart_data": security_chart_data,
                "principal_obligation_data": principal_data,
                "segmentation_chart_data": segmentation_chart_data,
            }
        except Exception as e:
            raise Exception(e)

    def card_data(self):
        borrowing_base_df = self.file_df["Borrowing Base"]
        borrowing_base = borrowing_base_df.loc[
            borrowing_base_df["Terms"]
            == "BORROWING BASE - (A) minus (B) minus (A)(iv)",
            "Values",
        ].values[0]
        max_available_amount = borrowing_base_df.loc[
            borrowing_base_df["Terms"]
            == "MAXIMUM AVAILABLE AMOUNT - Least of (A), (B) and (C)",
            "Values",
        ].values[0]
        advances_outstanding = borrowing_base_df.loc[
            borrowing_base_df["Terms"] == "Advances Outstanding as of & TEXT", "Values"
        ].values[0]
        availability_card = borrowing_base_df.loc[
            borrowing_base_df["Terms"] == "AVAILABILITY - (a) minus (b)", "Values"
        ].values[0]

        Credit_Balance_Projection_df = self.file_df["Credit Balance Projection"]

        Credit_Balance_Projection_df["Exchange Rates"] = pd.to_numeric(
            Credit_Balance_Projection_df["Exchange Rates"], errors="coerce"
        )
        Credit_Balance_Projection_df["Projected Credit Facility Balance"] = pd.to_numeric(
            Credit_Balance_Projection_df["Projected Credit Facility Balance"], errors="coerce"
        )

        total = (Credit_Balance_Projection_df["Exchange Rates"] * Credit_Balance_Projection_df["Projected Credit Facility Balance"]).sum()

        if not pd.notnull(total):
            total = 0

        # Creating the card data structure
        card_data = {
            "Borrowing Base": [{"data": f"${borrowing_base / 1e6:.2f}M"}],
            "Maximum Available Amount": [
                {"data": f"${max_available_amount / 1e6:.2f}M"}
            ],
            "Advance Outstandings": [{"data": f"${advances_outstanding / 1e6:.2f}M"}],
            "Availability": [{"data": f"${availability_card / 1e6:.2f}M"}],
            "Total Credit Facility Balance": [
                {
                    "data": "$"
                    + numerize.numerize(total)
                }
            ],
            "ordered_card_names": [
                "Borrowing Base",
                "Maximum Available Amount",
                "Advance Outstandings",
                "Availability",
                "Total Credit Facility Balance",
            ],
        }
        return card_data

    def segmentation(self):
        # Extract the necessary columns
        loan_list_df = self.file_df["Loan List"]
        obligor_industry = loan_list_df["Obligor Industry"]
        borrowing_base = loan_list_df["Borrowing Base"]

        # Calculate total borrowing base
        total_borrowing_base = borrowing_base.sum()

        # Group by industry and calculate unadjusted borrowing base and percentage of total BB
        industry_group = (
            loan_list_df.groupby("Obligor Industry")
            .agg({"Borrowing Base": "sum"})
            .reset_index()
        )

        # Calculate the percentage of total borrowing base
        industry_group["Unadjusted % of BB"] = (
            industry_group["Borrowing Base"] / total_borrowing_base * 100
        )

        industry_group = industry_group.sort_values("Borrowing Base", ascending=False)

        # Format the borrowing base and percentages
        industry_group["Borrowing Base"] = industry_group["Borrowing Base"].apply(
            lambda x: "$" + numerize.numerize(x)
        )
        industry_group["Unadjusted % of BB"] = industry_group[
            "Unadjusted % of BB"
        ].apply(lambda x: f"{x:.2f}%")

        # Build the segmentation overview data structure
        segmentation_overview_data = {
            "Industry": [
                {"data": industry} for industry in industry_group["Obligor Industry"]
            ],
            "Borrowing Base": [{"data": bb} for bb in industry_group["Borrowing Base"]],
            "% Borrowing Base": [
                {"data": pct} for pct in industry_group["Unadjusted % of BB"]
            ],
            "columns": [{"data": ["Industry", "Borrowing Base", "% Borrowing Base"]}],
            "Total": {
                "data": {
                    "Industry": "Total",
                    "% Borrowing Base": "100.00%",
                    "Borrowing Base": f"${total_borrowing_base / 1e6:.2f}M",
                }
            },
        }

        return segmentation_overview_data

    def concentration_test_data_from_base_sheet(self):
        concentration_test_df = self.file_df["Concentration Test"]
        concentraion_test_formatter = ConcentraionTestFormatter(concentration_test_df)
        concentration_test_data = (
            concentraion_test_formatter.convert_to_std_table_format()
        )
        # concentration_test_data = {
        #     column: [
        #         {
        #             "data": (
        #                 "{:.2f}%".format(round(cell * 100, 2))
        #                 if column == "Limit %"
        #                 else (
        #                     "$" + numerize.numerize(cell)
        #                     if type(cell) == int or type(cell) == float
        #                     else cell
        #                 )
        #             )
        #         }
        #         for cell in concentration_test_df[column]
        #     ]
        #     for column in concentration_test_df.columns.tolist()
        # }
        # concentration_test_data["columns"] = [
        #     {"data": concentration_test_df.columns.tolist()}
        # ]
        return concentration_test_data

    def security_data_from_base_sheet(self):
        loan_list_df = self.file_df["Loan List"]
        security_columns_list = [
            "Borrowing Base",
            "Loan Type (Term / Delayed Draw / Revolver)",
        ]
        security_df = loan_list_df[security_columns_list]
        Total = security_df["Borrowing Base"].sum()
        security_df["% Borrowing Base"] = security_df["Borrowing Base"] / Total

        security_df = (
            security_df.groupby("Loan Type (Term / Delayed Draw / Revolver)")
            .agg({"Borrowing Base": "sum", "% Borrowing Base": "sum"})
            .reset_index()
        )

        security_df = security_df.sort_values("Borrowing Base", ascending=False)
        total_bb = security_df["Borrowing Base"].sum()
        percent_bb_sum = security_df["% Borrowing Base"].sum()*100
        security_df = security_df.rename(
            columns={"Loan Type (Term / Delayed Draw / Revolver)": "Loan Type"}
        )

        security_data = {
            column: [
                {
                    "data": (
                        "{:.2f}%".format(round(cell * 100, 2))
                        if column == "% Borrowing Base"
                        else (
                            "$" + numerize.numerize(cell)
                            if type(cell) == int or type(cell) == float
                            else cell
                        )
                    )
                }
                for cell in security_df[column]
            ]
            for column in security_df.columns.tolist()
        }
        security_data["Total"] = {
            "data": {
                "Loan Type": "Total",
                "% Borrowing Base": str(percent_bb_sum) +"%",
                "Borrowing Base": f"${numerize.numerize(total_bb)}",
            }
        }
        security_data["columns"] = [{"data": security_df.columns.tolist()}]
        return security_data

    def principal_obligation_data(self):
        return {
            "Amount": [{"data": "$60M"}, {"data": "$0"}],
            "Currency": [{"data": "USD"}, {"data": "CAD"}],
            "Dollar equivalent": [{"data": "$60M"}, {"data": "$0"}],
            "Obligation": [{"data": "Loans (USD)"}, {"data": "Loans (CAD)"}],
            "Spot rate": [{"data": "100.00%"}, {"data": "0.00%"}],
            "columns": [
                {
                    "data": [
                        "Obligation",
                        "Currency",
                        "Amount",
                        "Spot rate",
                        "Dollar equivalent",
                    ]
                }
            ],
        }

    def principal_obligation_data_from_sheet(self):
        Credit_Balance_Projection_df = self.file_df["Credit Balance Projection"]
        principle_obligation_data = {
            column: [
                {
                    "data": (
                        "{:.2f}%".format(round(cell * 100, 2))
                        if column == "Exchange Rates"
                        else (
                            "$" + (numerize.numerize(cell) if pd.notnull(cell) else numerize.numerize(0))
                            if type(cell) == int or type(cell) == float
                            else cell
                        )
                    )
                }
                for cell in Credit_Balance_Projection_df[column]
            ]
            for column in Credit_Balance_Projection_df.columns.tolist()
        }
        principle_obligation_data["columns"] = [
            {"data": Credit_Balance_Projection_df.columns.tolist()}
        ]
        return principle_obligation_data

    def security_chart_data_from_sheet(self):
        loan_list_df = self.file_df["Loan List"]
        loan_list_dataframe = copy.deepcopy(loan_list_df)
        column_list = ["Borrowing Base", "Loan Type (Term / Delayed Draw / Revolver)"]
        security_df = loan_list_dataframe[column_list]
        security_df.rename(
            columns={"Loan Type (Term / Delayed Draw / Revolver)": "name"},
            inplace=True,
        )

        security_bb_sum = (
            security_df.groupby("name")["Borrowing Base"].sum().reset_index()
        )
        security_bb_sum = security_bb_sum.sort_values("Borrowing Base", ascending=False)

        # Convert the DataFrame to a list of dictionaries
        security_bb_dict = {
            "security_chart_data": security_bb_sum.to_dict(orient="records"),
            "x_axis": ["Borrowing Base"],
            "y_axis": "Loan Type",
        }
        return security_bb_dict

    def segmentation_chart_data_from_sheet(self):
        loan_list_df = self.file_df["Loan List"]
        loan_list_dataframe = copy.deepcopy(loan_list_df)
        column_list = ["Borrowing Base", "Obligor Industry"]
        segmentation_df = loan_list_dataframe[column_list]
        segmentation_df.rename(
            columns={"Obligor Industry": "name"},
            inplace=True,
        )

        industry_bb_sum = (
            segmentation_df.groupby("name")["Borrowing Base"].sum().reset_index()
        )
        industry_bb_sum = industry_bb_sum.sort_values("Borrowing Base", ascending=False)

        # Convert the DataFrame to a list of dictionaries
        industry_bb_dict = {
            "segmentation_chart_data": industry_bb_sum.to_dict(orient="records"),
            "y_axis": "Obligor Industry",
            "x_axis": ["Borrowing Base"],
        }
        return industry_bb_dict


# file_path = pathlib.Path("PFLT_Loan_List_Output.xlsx")
# with file_path.open(mode="rb") as file_obj:
#     file_df = pd.read_excel(file_obj, sheet_name=None)

# Fl = PFLTBorrowingBase(file_df)
# Fl.generate_response()
