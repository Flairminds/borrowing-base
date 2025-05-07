from numerize import numerize
import re

from source.concentration_test_application import ConcentraionTestFormatter
from source.utility.Util import currency_to_float_to_numerize_to_currency
class PsslResponseGenerator:

    def __init__(self, calculator_info):
        self.calculator_info = calculator_info

    def get_concentration_test_data(self):
        concentration_test_df = self.calculator_info.intermediate_calculation_dict['Concentration Test']
        concentraion_test_formatter = ConcentraionTestFormatter(concentration_test_df)
        concentration_test_data = (
            concentraion_test_formatter.convert_to_std_table_format()
        )
        return concentration_test_data

    def get_segmentation_overview_data(self):
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        # Approved Industry,
        # Adjusted Borrowing Value
        
        segmentation_overview_df = portfolio_df[['Approved Industry', 'Adjusted Borrowing Value']]
        segmentation_overview_df.rename(columns={"Approved Industry": "Industry", "Adjusted Borrowing Value": "Borrowing Base"}, inplace=True)
        segmentation_overview_df = segmentation_overview_df.groupby("Industry")["Borrowing Base"].sum().reset_index()
        total_bb = segmentation_overview_df["Borrowing Base"].sum()
        segmentation_overview_df["% Borrowing Base"] = segmentation_overview_df["Borrowing Base"] / total_bb
        segmentation_overview_df = segmentation_overview_df.sort_values("Borrowing Base", ascending=False)
        total_percent_bb = segmentation_overview_df["% Borrowing Base"].sum()

        segmentation_overview_data = {}
        columns = segmentation_overview_df.columns.tolist()
        for column in columns:
            segmentation_overview_data[column] = []

        for column in columns:
            print(column)
            for value in segmentation_overview_df[column].tolist():
                if column == "Borrowing Base":
                    value = numerize.numerize(value)
                if column == "% Borrowing Base":
                    value = "{:.2f}%".format(value * 100)
                    
                segmentation_overview_data[column].append({"data": value})
        
        segmentation_overview_data["Total"] = {"data": {
            "Borrowing Base": numerize.numerize(total_bb),
            "% Borrowing Base": "{:.2f}%".format(total_percent_bb * 100),
            "Industry": "Total"
        }}
        segmentation_overview_data["columns"] = [{"data": columns}]
        return segmentation_overview_data

    def get_seg_overview_graph_data(self):
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        segmentation_overview_df = portfolio_df[['Approved Industry', 'Adjusted Borrowing Value']]
        segmentation_overview_df.rename(columns={"Approved Industry": "name", "Adjusted Borrowing Value": "Borrowing Base"}, inplace=True)
        total_bb = segmentation_overview_df["Borrowing Base"].sum()
        segmentation_overview_df = segmentation_overview_df.groupby("name")["Borrowing Base"].sum().reset_index()
        segmentation_overview_df = segmentation_overview_df.sort_values("Borrowing Base", ascending=False)

        seg_overview_chart_data = [{"name": row["name"], "Borrowing Base": row["Borrowing Base"]} for index, row in segmentation_overview_df.iterrows()]

        seg_overview_graph_data = {
            "segmentation_chart_data": seg_overview_chart_data,
            "x_axis": ["Borrowing Base"],
            "y_axis": "Obligor Industry"
        }

        return seg_overview_graph_data
    
    def security_data(self):
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        security_df = portfolio_df[['Loan Type', 'Adjusted Borrowing Value']]
        security_df.rename(columns={"Adjusted Borrowing Value": "Borrowing Base"}, inplace=True)
        security_df = security_df.groupby("Loan Type")["Borrowing Base"].sum().reset_index()
        total_bb = security_df["Borrowing Base"].sum()
        security_df["% Borrowing Base"] = security_df["Borrowing Base"] / total_bb * 100
        security_df = security_df.sort_values("Borrowing Base", ascending=False)
        total_percent_bb = security_df["% Borrowing Base"].sum()

        security_data = {}
        columns = security_df.columns.tolist()
        for column in columns:
            security_data[column] = []

        for column in columns:
            for value in security_df[column].tolist():
                if column == "Borrowing Base":
                    value = numerize.numerize(value)
                if column == "% Borrowing Base":
                    value = "{:.2f}%".format(value)
                
                security_data[column].append({"data": [value]})
        
        security_data["Total"] = {"data": {
            "Borrowing Base": numerize.numerize(total_bb),
            "% Borrowing Base": "{:.2f}%".format(total_percent_bb * 100),
            "Loan Type": "Total"
        }}
        security_data["columns"] = [{"data": columns}]
        return security_data
    
    def get_security_graph_data(self):
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        security_df = portfolio_df[['Loan Type', 'Adjusted Borrowing Value']]
        security_df.rename(columns={"Adjusted Borrowing Value": "Borrowing Base"}, inplace=True)
        security_df = security_df.groupby("Loan Type")["Borrowing Base"].sum().reset_index()
        security_df = security_df.sort_values("Borrowing Base", ascending=False)

        security_chart_data = [{"name": row["Loan Type"], "Borrowing Base": row["Borrowing Base"]} for index, row in security_df.iterrows()]

        security_graph_data = {
            "security_chart_data": security_chart_data,
            "x_axis": ["Borrowing Base"],
            "y_axis": "Loan Type"
        }
        
        return security_graph_data

    def get_principal_obligation_data(self):
        exchange_rates_df = self.calculator_info.intermediate_calculation_dict['Exchange Rates']
        principal_obligation_data = {
            "columns": [{"data": ["Currency", "Exchange Rates"]}],
            "Currency": [{"data": currency} for currency in exchange_rates_df["Currency"].tolist()],
            "Exchange Rates": [{"data": rate} for rate in exchange_rates_df["Exchange Rate"].tolist()],
        }
        return principal_obligation_data
        
    def get_card_data(self):
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        total_bb = portfolio_df["Adjusted Borrowing Value"].sum()

        availability_df = self.calculator_info.intermediate_calculation_dict['Availability']
        current_advances_outstanding_data = availability_df.loc[availability_df["Terms"] == "Current Advances Outstanding", "Values"].values[0]


        ordered_card_names = ["Borrowing Base","Current Advances Outstanding"]
        card_data = {
            "Borrowing Base": [{"data": currency_to_float_to_numerize_to_currency(total_bb)}],
            "Current Advances Outstanding": [{"data": currency_to_float_to_numerize_to_currency(current_advances_outstanding_data)}],
            "ordered_card_names": ordered_card_names
        }
        return card_data


    def generate_response(self):
        
        response = {}
        response["base_data_file_id"] = self.calculator_info.base_data_file.id
        response["closing_date"] = self.calculator_info.base_data_file.closing_date
        response["file_name"] = self.calculator_info.base_data_file.file_name
        response["fund_name"] = self.calculator_info.base_data_file.fund_type

        segmentation_overview_data = self.get_segmentation_overview_data()
        response["segmentation_overview_data"] = segmentation_overview_data

        segmentation_graph_data = self.get_seg_overview_graph_data()
        response["segmentation_chart_data"] = segmentation_graph_data

        security_data = self.security_data()
        response["security_data"] = security_data

        security_chart_data = self.get_security_graph_data()
        response["security_chart_data"] = security_chart_data

        concentration_test_data = self.get_concentration_test_data()
        response["concentration_test_data"] = concentration_test_data

        principal_obligation_data = self.get_principal_obligation_data()
        response["principal_obligation_data"] = principal_obligation_data

        card_data = self.get_card_data()
        response["card_data"] = card_data
        
        return response