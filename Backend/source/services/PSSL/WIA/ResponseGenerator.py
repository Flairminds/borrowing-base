from source.utility.Util import float_to_numerized
from source.services.concTestService.concTestService import ConcentraionTestFormatter

class PsslWiaResponseGenerator:
    def __init__(self, initial_xl_df_map, calculated_xl_df_map):
        self.initial_xl_df_map = initial_xl_df_map
        self.calculated_xl_df_map = calculated_xl_df_map

    def get_card_data(self):
        initial_availability_df = self.initial_xl_df_map['Availability']
        calc_availability_df = self.calculated_xl_df_map['Availability']

        initial_pro_forma_advances_outstanding = initial_availability_df.loc[initial_availability_df["Terms"] == "Pro Forma Advances Outstanding", "Values"].values[0]
        initial_borrowing_base = initial_availability_df.loc[initial_availability_df["Terms"] == "Borrowing Base", "Values"].values[0]

        calc_pro_forma_advances_outstanding = calc_availability_df.loc[calc_availability_df["Terms"] == "Pro Forma Advances Outstanding", "Values"].values[0]
        calc_borrowing_base = calc_availability_df.loc[calc_availability_df["Terms"] == "Borrowing Base", "Values"].values[0]

        ordered_card_names = [
            "Borrowing Base",
            "Pro Forma Advances Outstanding"
        ]
        card_data = {
            "Borrowing Base": [{
                "changeInValue": calc_borrowing_base != initial_borrowing_base,
                "data": "$" + float_to_numerized(calc_borrowing_base),
                "prevValue": "$" +float_to_numerized(initial_borrowing_base),
                "percentageChange": '{:.2%}'.format((calc_borrowing_base - initial_borrowing_base) / initial_borrowing_base),
            }],
            "Pro Forma Advances Outstanding": [{
                "changeInValue": calc_pro_forma_advances_outstanding != initial_pro_forma_advances_outstanding,
                "data": "$" + float_to_numerized(calc_pro_forma_advances_outstanding),
                "prevValue": "$" +float_to_numerized(initial_pro_forma_advances_outstanding),
                "percentageChange": '{:.2%}'.format((calc_pro_forma_advances_outstanding - initial_borrowing_base) / initial_pro_forma_advances_outstanding),
            }],
            "ordered_card_names": ordered_card_names
        }
        return card_data
    
    def get_segmentation_overview_data(self):
        initial_portfolio_df = self.initial_xl_df_map['Portfolio']
        calc_portfolio_df = self.calculated_xl_df_map['Portfolio']

        initial_portfolio_df = initial_portfolio_df[['Approved Industry', 'Adjusted Borrowing Value']]
        calc_portfolio_df = calc_portfolio_df[['Approved Industry', 'Adjusted Borrowing Value']]

        initial_portfolio_df.rename(columns={"Approved Industry": "name", "Adjusted Borrowing Value": "Borrowing Base"}, inplace=True)
        calc_portfolio_df.rename(columns={"Approved Industry": "name", "Adjusted Borrowing Value": "Borrowing Base"}, inplace=True)

        initial_segmentation_bb_sum = (initial_portfolio_df.groupby("name")["Borrowing Base"].sum().reset_index())
        initial_segmentation_bb_sum = initial_segmentation_bb_sum.sort_values("Borrowing Base",ascending=False)

        calculated_segmentation_bb_sum = (calc_portfolio_df.groupby("name")["Borrowing Base"].sum().reset_index())
        calculated_segmentation_bb_sum = calculated_segmentation_bb_sum.sort_values("Borrowing Base", ascending=False)

        initial_segmentation_bb_sum["% of Borrowing Base"] = initial_segmentation_bb_sum["Borrowing Base"] /initial_segmentation_bb_sum["Borrowing Base"].sum()

        calculated_segmentation_bb_sum["% of Borrowing Base"] = calculated_segmentation_bb_sum["Borrowing Base"] / calculated_segmentation_bb_sum["Borrowing Base"].sum()

        merged_segmentation_bb_df = calculated_segmentation_bb_sum.merge(initial_segmentation_bb_sum, on="name",how="left")

        merged_segmentation_bb_df.rename(columns={
                "Borrowing Base_x": "Updated Borrowing Base",
                "Borrowing Base_y": "Borrowing Base",
                "% of Borrowing Base_x": "Updated % of Borrowing Base",
                "% of Borrowing Base_y": "initial % of Borrowing Base",
            }, inplace=True)
        
        cols_to_fillna = [
            "Updated Borrowing Base",
            "Updated % of Borrowing Base",
            "Borrowing Base",
            "initial % of Borrowing Base",
        ]

        merged_segmentation_bb_df[cols_to_fillna] = merged_segmentation_bb_df[cols_to_fillna].fillna(0)

        unadjusted_percent_of_bb = [
            {
                "data": "{:.2f}%".format(
                    merged_segmentation_bb_df["Updated % of Borrowing Base"][i] * 100
                ),
                "prevValue": "{:.2f}%".format(
                    merged_segmentation_bb_df["initial % of Borrowing Base"][i] * 100
                ),
                "percentageChange": "{:.2f}%".format(
                    (
                        (
                            (
                                merged_segmentation_bb_df["Updated % of Borrowing Base"][i]
                                - merged_segmentation_bb_df["initial % of Borrowing Base"][
                                    i
                                ]
                            )
                            / merged_segmentation_bb_df["initial % of Borrowing Base"][i]
                        )
                        * 100
                    )
                    if merged_segmentation_bb_df["initial % of Borrowing Base"][i] != 0
                    else 0
                ),
            }
            for i in range(len(merged_segmentation_bb_df))
        ]

        borrowing_base = [
            {
                "data": "$" + float_to_numerized(merged_segmentation_bb_df["Updated Borrowing Base"][i]),
                "percentageChange": "{:.2f}%".format(
                    (
                        (
                            (
                                merged_segmentation_bb_df["Updated Borrowing Base"][i]
                                - merged_segmentation_bb_df["Borrowing Base"][i]
                            )
                            / merged_segmentation_bb_df["Borrowing Base"][i]
                        )
                        * 100
                    )
                    if merged_segmentation_bb_df["Borrowing Base"][i] != 0
                    else 0
                ),
                "prevValue": "$"
                + float_to_numerized(merged_segmentation_bb_df["Borrowing Base"][i]),
            }
            for i in range(len(merged_segmentation_bb_df))
        ]

        industries = [
            {"data": merged_segmentation_bb_df["name"][i], "changeInValue": True}
            for i in range(len(merged_segmentation_bb_df))
        ]

        total = {
            "data": {
                "Industry": "Total",
                "% Borrowing Base": "{:.2f}%".format(merged_segmentation_bb_df["Updated % of Borrowing Base"].sum() * 100),
                "Borrowing Base": "$" + float_to_numerized(merged_segmentation_bb_df["Updated Borrowing Base"].sum()),
            }
        }

        columns = [{"data": ["Industry", "Borrowing Base", "% Borrowing Base"]}]

        segmentation_overview_data = {
            "Industry": industries,
            "Borrowing Base": borrowing_base,
            "% Borrowing Base": unadjusted_percent_of_bb,
            "Total": total,
            "columns": columns,
        }
        return segmentation_overview_data
        
        
    def get_seg_graph_data(self):
        initial_portfolio_df = self.initial_xl_df_map['Portfolio']
        calc_portfolio_df = self.calculated_xl_df_map['Portfolio']

        initial_portfolio_df = initial_portfolio_df[['Approved Industry', 'Adjusted Borrowing Value']]
        calc_portfolio_df = calc_portfolio_df[['Approved Industry', 'Adjusted Borrowing Value']]

        initial_portfolio_df.rename(columns={"Approved Industry": "name", "Adjusted Borrowing Value": "Borrowing Base"}, inplace=True)
        calc_portfolio_df.rename(columns={"Approved Industry": "name", "Adjusted Borrowing Value": "Borrowing Base"}, inplace=True)

        initial_segmentation_bb_sum = (initial_portfolio_df.groupby("name")["Borrowing Base"].sum().reset_index())
        initial_segmentation_bb_sum = initial_segmentation_bb_sum.sort_values("Borrowing Base",ascending=False)

        calculated_segmentation_bb_sum = (calc_portfolio_df.groupby("name")["Borrowing Base"].sum().reset_index())
        calculated_segmentation_bb_sum = calculated_segmentation_bb_sum.sort_values("Borrowing Base", ascending=False)

        calculated_segmentation_bb_sum = (calculated_segmentation_bb_sum.groupby("name")["Borrowing Base"].sum().reset_index())
        calculated_segmentation_bb_sum = calculated_segmentation_bb_sum.sort_values("Borrowing Base", ascending=False)

        merged_segmentation_bb_df = calculated_segmentation_bb_sum.merge(initial_segmentation_bb_sum, on="name",how="left")

        merged_segmentation_bb_df.rename(columns={
                "Borrowing Base_x": "Updated Borrowing Base",
                "Borrowing Base_y": "Borrowing Base",
            }, inplace=True)

        merged_segmentation_bb_df[["Updated Borrowing Base", "Borrowing Base"]] = (merged_segmentation_bb_df[["Updated Borrowing Base", "Borrowing Base"]].fillna(0))
        chart_data = merged_segmentation_bb_df.to_dict(orient="records")
        segmentation_graph_data = {
            "segmentation_chart_data": chart_data,
            "x_axis": ["Updated Borrowing Base", "Borrowing Base"],
            "y_axis": "name",
        }
        return segmentation_graph_data

    def get_security_bb_sum(self, security_bb):
        security_bb = security_bb[['Loan Type', 'Adjusted Borrowing Value']]
        security_bb.rename(columns={'Loan Type': "Security", 'Adjusted Borrowing Value': "Borrowing Base"}, inplace=True)
        security_bb_sum = (security_bb.groupby("Security")["Borrowing Base"].sum().reset_index())
        security_bb_sum = security_bb_sum.sort_values("Borrowing Base", ascending=False)
        return security_bb_sum

    def get_security_data(self):
        initial_portfolio_df = self.initial_xl_df_map['Portfolio']
        calc_portfolio_df = self.calculated_xl_df_map['Portfolio']

        initial_security_bb_sum = self.get_security_bb_sum(initial_portfolio_df)
        calculated_security_bb_sum = self.get_security_bb_sum(calc_portfolio_df)

        initial_security_bb_sum["% of Borrowing Base"] = (initial_security_bb_sum["Borrowing Base"] /initial_security_bb_sum["Borrowing Base"].sum())

        calculated_security_bb_sum["% of Borrowing Base"] = (calculated_security_bb_sum["Borrowing Base"] /calculated_security_bb_sum["Borrowing Base"].sum())

        merged_security_bb_df = calculated_security_bb_sum.merge(initial_security_bb_sum, on="Security", how="left")

        merged_security_bb_df.rename(
            columns={
                "Borrowing Base_x": "Updated Borrowing Base",
                "Borrowing Base_y": "Borrowing Base",
                "% of Borrowing Base_x": "Updated % of Borrowing Base",
                "% of Borrowing Base_y": "initial % of Borrowing Base",
            }, inplace=True)
        
        cols_to_fillna = [
            "Updated Borrowing Base",
            "Updated % of Borrowing Base",
            "Borrowing Base",
            "initial % of Borrowing Base",
        ]

        merged_security_bb_df[cols_to_fillna] = merged_security_bb_df[cols_to_fillna].fillna(0)

        percent_of_borrowing_base = [
            {
                "data": "{:.2f}%".format(
                    merged_security_bb_df["Updated % of Borrowing Base"][i] * 100
                ),
                "prevValue": "{:.2f}%".format(
                    merged_security_bb_df["initial % of Borrowing Base"][i] * 100
                ),
                "percentageChange": "{:.2f}%".format(
                    (
                        (
                            (
                                merged_security_bb_df["Updated % of Borrowing Base"][i]
                                - merged_security_bb_df["initial % of Borrowing Base"][i]
                            )
                            / merged_security_bb_df["initial % of Borrowing Base"][i]
                        )
                        * 100
                    )
                    if merged_security_bb_df["initial % of Borrowing Base"][i] != 0
                    else 0
                ),
            }
            for i in range(len(merged_security_bb_df))
        ]

        borrowing_base = [
            {
                "data": "$"
                +float_to_numerized(merged_security_bb_df["Updated Borrowing Base"][i]),
                "percentageChange": "{:.2f}%".format(
                    (
                        (
                            (
                                merged_security_bb_df["Updated Borrowing Base"][i]
                                - merged_security_bb_df["Borrowing Base"][i]
                            )
                            / merged_security_bb_df["Borrowing Base"][i]
                        )
                        * 100
                    )
                    if merged_security_bb_df["Borrowing Base"][i] != 0
                    else 0
                ),
                "prevValue": "$"
                + float_to_numerized(merged_security_bb_df["Borrowing Base"][i]),
            }
            for i in range(len(merged_security_bb_df))
        ]

        secuity = [
            {"data": merged_security_bb_df["Security"][i], "changeInValue": True}
            for i in range(len(merged_security_bb_df))
        ]

        total = {
            "data": {
                "Security": "Total",
                "% Borrowing Base": "{:.2f}%".format(
                    merged_security_bb_df["Updated % of Borrowing Base"].sum()
                ),
                "Borrowing Base": "$"
                + float_to_numerized(merged_security_bb_df["Updated Borrowing Base"].sum()),
            }
        }

        columns = [{"data": ["Security", "Borrowing Base", "% Borrowing Base"]}]

        security_data = {
            "% Borrowing Base": percent_of_borrowing_base,
            "Borrowing Base": borrowing_base,
            "Security": secuity,
            "Total": total,
            "columns": columns,
        }
        return security_data
    
    def get_security_graph_data(self):
        initial_portfolio_df = self.initial_xl_df_map['Portfolio']
        calc_portfolio_df = self.calculated_xl_df_map['Portfolio']

        initial_portfolio_df = initial_portfolio_df[['Loan Type', 'Adjusted Borrowing Value']]
        calc_portfolio_df = calc_portfolio_df[['Loan Type', 'Adjusted Borrowing Value']]

        initial_portfolio_df.rename(columns={'Loan Type': "Security", 'Adjusted Borrowing Value': "Borrowing Base"}, inplace=True)
        
        calc_portfolio_df.rename(columns={'Loan Type': "Security", 'Adjusted Borrowing Value': "Borrowing Base"}, inplace=True)

        initial_security_bb_sum = (initial_portfolio_df.groupby("Security")["Borrowing Base"].sum().reset_index())
        initial_security_bb_sum = initial_security_bb_sum.sort_values("Borrowing Base", ascending=False)

        calc_security_bb_sum = (initial_portfolio_df.groupby("Security")["Borrowing Base"].sum().reset_index())
        calc_security_bb_sum = initial_security_bb_sum.sort_values("Borrowing Base", ascending=False)

        merged_security_bb_df = calc_security_bb_sum.merge(initial_security_bb_sum, on="Security", how="left")

        merged_security_bb_df.rename(
            columns={
                "Borrowing Base_x": "Updated Borrowing Base",
                "Borrowing Base_y": "Borrowing Base",
            }, inplace=True)

        merged_security_bb_df[["Updated Borrowing Base", "Borrowing Base"]] = (merged_security_bb_df[["Updated Borrowing Base", "Borrowing Base"]].fillna(0))

        chart_data = merged_security_bb_df.to_dict(orient="records")
        security_graph_data = {
            "security_chart_data": chart_data,
            "x_axis": ["Updated Borrowing Base", "Borrowing Base"],
            "y_axis": "Loan Type",
        }
        return security_graph_data
    
    def get_concentration_test_data(self):
        concentration_test_df = self.initial_xl_df_map['Concentration Test']
        concentraion_test_formatter = ConcentraionTestFormatter(concentration_test_df)
        concentration_test_data = (
            concentraion_test_formatter.convert_to_std_table_format()
        )
        return concentration_test_data
    
    def get_principal_obligation_data(self):
        exchange_rates_df = self.initial_xl_df_map['Exchange Rates']
        principal_obligation_data = {
            "columns": [{"data": ["Currency", "Exchange Rates"]}],
            "Currency": [{"data": currency} for currency in exchange_rates_df["Currency"].tolist()],
            "Exchange Rates": [{"data": rate} for rate in exchange_rates_df["Exchange Rate"].tolist()],
        }
        return principal_obligation_data

    def generate_response(self):
        card_data = self.get_card_data()
        seg_overview_data = self.get_segmentation_overview_data()
        seg_graph_data = self.get_seg_graph_data()
        security_data = self.get_security_data()
        security_graph_data = self.get_security_graph_data()
        concentration_test_data = self.get_concentration_test_data()
        principle_obligation_data = self.get_principal_obligation_data()

        response_data = {
            "card_data": card_data,
            "concentration_test_data": concentration_test_data,
            "principal_obligation_data": principle_obligation_data,
            "security_chart_data": security_graph_data,
            "segmentation_chart_data": seg_graph_data,
            "security_data": security_data,
            "segmentation_overview_data": seg_overview_data,
        }
        return response_data

    

        
        
    
    def get_request(self):
        return self.request