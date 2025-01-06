from models import ModifiedBaseDataFile, WhatIfAnalysis, db
from source.utility.ServiceResponse import ServiceResponse
from source.services.sheetUniques import sheet_uniques

import pickle
import numpy as np
import pandas as pd
from datetime import datetime
from numerize import numerize

PCOF_SPECIFIC_COLUMNS = [
    "Investment Name",
    "Issuer",
    "Financials LTM EBITDA ($MMs)",
    "Leverage Total Leverage",
    # "Borrowing Base",
]

PCOF_RENAMED_COLUMNS = {
    "Investment Name": "Investor Name",
    "Financials LTM EBITDA ($MMs)": "EBITDA",
    "Leverage Total Leverage": "Leverage",
}


PFLT_SPECIFIC_COLUMNS = [
    "Security Name",
    "Current TTM EBITDA",
    "Current Total Debt/EBITDA",
]

PFLT_RENAMED_COLUMNS = {
    "Security Name": "Investor Name",
    "Current TTM EBITDA": "EBITDA",
    "Current Total Debt/EBITDA": "Leverage",
}

class AssetProcessor:
    def __init__(self, what_if_analysis, fund_type):
        self.simulation_type = what_if_analysis.simulation_type

        match fund_type:
            case "PCOF":
                sheet_name = "PL BB Build"
                self.specific_columns = PCOF_SPECIFIC_COLUMNS
                self.renamed_columns = PCOF_RENAMED_COLUMNS
            case "PFLT":
                sheet_name = "Loan List"
                self.specific_columns = PFLT_SPECIFIC_COLUMNS
                self.renamed_columns = PFLT_RENAMED_COLUMNS

        if self.simulation_type == "add_asset":
            self.init_add_asset(what_if_analysis, sheet_name)
        elif (
            self.simulation_type == "change_Ebitda"
            or self.simulation_type == "change_Leverage"
        ):
            self.init_asset_inventory(what_if_analysis, sheet_name)
        else:
            self.init_update_asset_inventory(what_if_analysis)

    def init_add_asset(self, what_if_analysis, sheet_name):
        initial_sheet = pickle.loads(what_if_analysis.initial_data)[sheet_name]
        updated_sheet = pickle.loads(what_if_analysis.updated_data)[sheet_name]
        self.what_if_intermediate_metrics_output = updated_sheet
        self.base_data_intermediate_metrics_output = initial_sheet
        self.sheet_name = sheet_name
        # Ensure indices are aligned
        self.base_data_intermediate_metrics_output.reset_index(drop=True, inplace=True)
        self.what_if_intermediate_metrics_output.reset_index(drop=True, inplace=True)

        self.data = {
            self.sheet_name: {
                "columns": [],
                "data": [],
                "new_data": [],
                "simulation_type": self.simulation_type,
            }
        }

        self.prepare_columns()
        self.fill_missing_values()
        self.added_indices = self.identify_added_rows()
        self.process_rows()

    def init_asset_inventory(self, what_if_analysis, sheet_name):

        self.asset_inventory_initial_sheet = pickle.loads(
            what_if_analysis.initial_data
        )
        self.asset_inventory_updated_data = pickle.loads(what_if_analysis.updated_data)
        self.asset_inventory_updated_sheet = self.asset_inventory_updated_data[sheet_name]
        self.sheet_name = sheet_name
        self.data = {
            self.sheet_name: {
                "columns": [],
                "data": [],
                "new_data": [],
                "simulation_type": self.simulation_type,
            }
        }

        self.prepare_columns()
        self.fill_missing_values()
        self.process_rows()

        
    def init_update_asset_inventory(self, modified_base_data_file):
        modified_data = pickle.loads(modified_base_data_file.modified_data)
        initial_data = pickle.loads(modified_base_data_file.initial_data)

        self.data = {}
        for sheet in modified_data:
            self.sheet_name = sheet
            self.initial_df = initial_data[sheet]
            self.modified_df = modified_data[sheet]

            # self.data = {
            self.data[self.sheet_name] = {
                "columns": [],
                "data": [],
                "new_data": [],
                "simulation_type": self.simulation_type,
            }
            # }

            self.process_update_sheet_rows(sheet)

    def get_native_value(self, value, dtype):
        if isinstance(value, (np.integer, int)):
            if value != value:
                return ""
            if value == "":
                return value
            return numerize.numerize(int(value), 2)
        if isinstance(value, (np.floating, float)):
            if value != value:
                return ""
            if value == "":
                return "{:,.02}".format(value)
            return float(value)
        if dtype == "datetime64[ns]":
            if pd.isna(value):
                return ""
            if value == "":
                return ""
            return pd.to_datetime(value).strftime("%Y-%m-%d")
        if dtype == "object":
            if value != value:
                return ""
            return str(value)

    def process_update_sheet_rows(self, sheet_name):
        new_data = []
        for idx, row in self.modified_df.iterrows():
            row_data = {}
            unique_id = row[sheet_uniques[sheet_name]]
            if unique_id not in self.initial_df[sheet_uniques[sheet_name]].tolist():
                for col, current_value in row.items():
                    key = col.replace(" ", "_")
                    if col == sheet_uniques[sheet_name]:
                        self.data[sheet_name]["new_data"].append(current_value)

                    row_data[key] = {
                        "previous_value": "",
                        "current_value": self.get_native_value(
                            current_value, self.initial_df[col].dtype
                        ),  # format it accordingly
                        "changed": True,
                    }
            else:
                for col, current_value in row.items():
                    key = col.replace(" ", "_")
                    # previous_value = self.initial_df[col].values[0]
                    previous_value = self.initial_df[
                        self.initial_df[sheet_uniques[sheet_name]] == unique_id
                    ][col].values[0]

                    # Format the values accordingly as per the data type of the column
                    previous_value = self.get_native_value(
                        previous_value, self.initial_df[col].dtype
                    )
                    current_value = self.get_native_value(
                        current_value, self.initial_df[col].dtype
                    )

                    row_data[key] = {
                        "previous_value": previous_value,
                        "current_value": current_value,
                        "changed": bool(current_value != previous_value),
                    }
                    # previous_value = self.get_native_value(previous_value, self.initial_df[col].dtype)
                    # current_value = self.get_native_value(previous_value, self.initial_df[col].dtype)

                    # row_data[key] = {
                    #     "previous_value": previous_value,
                    #     "current_value": current_value,
                    #     "changed": bool(current_value != previous_value),
                    # }

            self.data[sheet_name]["data"].append(row_data)

        self.data[sheet_name]["columns"] = [
            {"key": column_name.replace(" ", "_"), "title": column_name}
            for column_name in self.modified_df.columns.tolist()
        ]

    def prepare_columns(self):
        if self.simulation_type == "add_asset":
            self.data[self.sheet_name]["columns"] = [
                {"title": col, "key": col.replace(" ", "_")}
                for col in self.base_data_intermediate_metrics_output.columns
            ]
        elif (
            self.simulation_type == "change_Ebitda"
            or self.simulation_type == "change_Leverage"
        ):
            columns = [
                {
                    "title": self.renamed_columns.get(col, col),
                    "key": self.renamed_columns.get(col, col).replace(" ", "_"),
                }
                for col in self.specific_columns
            ]
            self.data[self.sheet_name]["columns"] = columns
        else:
            self.data[self.sheet_name]["columns"] = [
                {"title": col, "key": col.replace(" ", "_")}
                for col in self.modified_df.columns
            ]

    def fill_missing_values(self):
        if self.simulation_type == "add_asset":
            self.what_if_intermediate_metrics_output.fillna("", inplace=True)
            self.base_data_intermediate_metrics_output.fillna("", inplace=True)
        else:
            self.asset_inventory_initial_sheet = (
                self.asset_inventory_initial_sheet[self.sheet_name][self.specific_columns]
                .rename(columns=self.renamed_columns)
                .fillna("")
            )
            self.asset_inventory_updated_sheet = (
                self.asset_inventory_updated_sheet[self.specific_columns]
                .rename(columns=self.renamed_columns)
                .fillna("")
            )

    def identify_added_rows(self):
        base_first_col_set = self.base_data_intermediate_metrics_output.iloc[:, 0]
        added_assets = []
        for i, asset in self.what_if_intermediate_metrics_output.iterrows():
            if not base_first_col_set.isin([asset.iloc[0]]).any().any():
                added_assets.append(asset.iloc[0])
        return added_assets

    def format_value(self, value, col):
        if pd.isna(value):
            return ""
        if isinstance(value, (int, float)):
            if col != "Adj. Advance Rate":
                return numerize.numerize(float(value), 2)
            else:
                return "{:,.01f}%".format(value * 100)
        elif isinstance(value, (datetime, pd.Timestamp)):
            return value.strftime("%Y-%m-%d")
        else:
            return str(value)

    def process_rows(self):
        if self.simulation_type == "add_asset":
            self.process_add_asset_rows()
        elif (
            self.simulation_type == "change_Ebitda"
            or self.simulation_type == "change_Leverage"
        ):
            self.process_asset_inventory_rows()
        # else:
        #     self.process_update_asset_inventory_rows()

    def process_add_asset_rows(self):
        for idx, row in self.what_if_intermediate_metrics_output.iterrows():
            row_data = {}
            for col, current_value in row.items():
                key = col.replace(" ", "_")
                formatted_current_value = self.format_value(current_value, col)
                if row.iloc[0] in self.added_indices:
                    row_data[key] = {
                        "previous_value": "",
                        "current_value": formatted_current_value,
                        "changed": True,
                    }
                else:
                    row_data[key] = {
                        "previous_value": "",
                        "current_value": formatted_current_value,
                        "changed": False,
                    }
            self.data[self.sheet_name]["data"].append(row_data)

        self.data[self.sheet_name]["new_data"] = self.added_indices

    def process_asset_inventory_rows(self):
        for index, row in self.asset_inventory_updated_sheet.iterrows():
            row_data = {}
            base_row = self.asset_inventory_initial_sheet[
                self.asset_inventory_initial_sheet["Investor Name"]
                == row["Investor Name"]
            ]

            if not base_row.empty:
                base_row = base_row.squeeze()
            else:
                base_row = None

            for col, value in row.items():
                key = col.replace(" ", "_")

                if base_row is not None:
                    base_value = base_row[col]
                    changed = bool(base_value != value)
                    percent_change = (
                        self.calculate_percent_change(base_value, value)
                        if changed
                        else ""
                    )
                    formatted_previous_value = self.format_value(base_value, col)
                else:
                    base_value = None
                    changed = False
                    percent_change = ""
                    formatted_previous_value = ""

                formatted_current_value = self.format_value(value, col)

                row_data[key] = {
                    "previous_value": formatted_previous_value,
                    "current_value": formatted_current_value,
                    "changed": changed,
                    "percent_change": percent_change,
                }

            self.data[self.sheet_name]["data"].append(row_data)

    def calculate_percent_change(self, old_value, new_value):
        if isinstance(old_value, (int, float)) and isinstance(new_value, (int, float)):
            if old_value == 0:
                return f"{new_value:.2f}%"
            percent_change = ((new_value - old_value) / abs(old_value)) * 100
            return f"{percent_change:.2f}%"
        else:
            return ""

    def get_response(self):
        return self.data


def get_asset_inventry(what_if_analysis_id, what_if_analysis_type, fund_type):
    if what_if_analysis_type == "Update asset":
        what_if_analysis = ModifiedBaseDataFile.query.filter_by(
            id=what_if_analysis_id
        ).first()
        # ServiceResponse.error(status_code=405, message="Asset inventory for update asset not available")
    else:
        what_if_analysis = WhatIfAnalysis.query.filter_by(
            id=what_if_analysis_id
        ).first()

    if not what_if_analysis:
        ServiceResponse.error(status_code=404, message="what if analysis not found")

    processor = AssetProcessor(what_if_analysis, fund_type)
    selected_WIA_asstes_table_data = processor.get_response()

    return ServiceResponse.success(data=selected_WIA_asstes_table_data,message="What if analysis found")

