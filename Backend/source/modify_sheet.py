import pickle
import pandas as pd
import numpy as np
import json
from datetime import datetime, timezone
import copy

from models import BaseDataFile, ModifiedBaseDataFile
from constants.error_constants import ErrorConstants
import app


def validate_update_value_request(data):
    base_data_file_id = data.get("base_data_file_id")
    if not base_data_file_id:
        return {"error_status": True, "message": "base_data_file_id is required"}

    sheet_name = data.get("sheet_name")
    if not sheet_name:
        return {"error_status": True, "message": ErrorConstants.SHEET_NAME_REQUIRED_MSG}

    base_data_file = BaseDataFile.query.filter_by(id=base_data_file_id).first()
    if not base_data_file:
        return {"error_status": True, "message": "No base_data_file found"}

    file_data = pickle.loads(base_data_file.file_data)
    if sheet_name not in file_data.keys():
        return {"error_status": True, "message": f"{sheet_name} sheet not found"}

    changes = data.get("changes")
    if not changes:
        return {"error_status": True, "message": "changes is required"}


def add_row_at_index(sheet_df, changes):
    rows_to_add = changes["rows_to_add"]
    for row_to_add in rows_to_add:
        row_index = row_to_add["row_index"]
        row = pd.DataFrame(
            {sheet_df.columns[0]: row_to_add["row_identifier"]}, index=[row_index]
        )
        sheet_df = pd.concat(
            [sheet_df.iloc[:row_index], row, sheet_df.iloc[row_index:]],
            ignore_index=True,
        )
    return sheet_df


def delete_rows(df, changes):
    rows_to_delete = changes["rows_to_delete"]
    for row_to_delete in rows_to_delete:
        df = df.drop(df[df[df.columns[0]] == row_to_delete["row_identifier"]].index)
    return df


def find_is_NaT(previous_value):
    try:
        if pd.isna(previous_value):
            return True
    except Exception as e:
        return False


def get_updated_value(updated_value):
    if isinstance(updated_value, str):
        try:
            if updated_value.endswith("%"):
                updated_value = updated_value[:-1]
                updated_value = float(updated_value) / 100
        except ValueError:
            pass
    return updated_value


def get_raw_value(updated_value, col_type):
    if col_type == np.float64:
        if updated_value != "":
            if type(updated_value) == str:
                updated_value = updated_value.replace(",", "")
                updated_value = float(updated_value)
        else:
            updated_value = None
    if col_type == np.int64:
        if updated_value != "":
            if type(updated_value) == str:
                updated_value = updated_value.replace(",", "")
                updated_value = int(updated_value)
        else:
            updated_value = None
    elif col_type == "<M8[ns]":  # Handling datetime
        if updated_value != "":
            if type(updated_value) != str:
                if find_is_NaT(updated_value):
                    updated_value = ""
                else:
                    updated_value = pd.to_datetime(
                        updated_value, errors="coerce"
                    ).strftime("%Y-%m-%d")
        else:
            updated_value = None
    if col_type == object:
        try:
            if not pd.isna(updated_value):
                if updated_value != "":
                    updated_value = float(updated_value.replace(",", ""))
                else:
                    updated_value = None
            else:
                updated_value = ""
        except ValueError:
            updated_value = updated_value
    return updated_value


def get_row_index(sheet_df, row_name):
    try:
        row_index = sheet_df[sheet_df[sheet_df.columns[0]] == row_name].index[0]
        return row_index
    except IndexError as ie:
        return -1


def update_df(sheet_df, changes, sheet_name):
    values_to_update = changes["updated_assets"]
    for value_to_update in values_to_update:
        row_name = value_to_update["row_name"]

        col_name = value_to_update["column_name"]
        if col_name != sheet_df.columns[0]:
            row_index = get_row_index(sheet_df, row_name)
            if row_index != -1:
                updated_value = value_to_update["updated_value"]
                updated_value = get_updated_value(updated_value)

                col_type = sheet_df[col_name].dtype

                updated_value = get_raw_value(updated_value, col_type)
                # print(col_type, col_name, updated_value)

                previous_value = sheet_df.loc[row_index, col_name]
                previous_value = get_raw_value(previous_value, col_type)
                if find_is_NaT(previous_value):
                    previous_value = ""
                value_to_update["previous_value"] = previous_value
                sheet_df.loc[row_index, col_name] = updated_value
    return sheet_df


def update_add_df(data):
    base_data_file_id = data.get("base_data_file_id")
    sheet_name = data.get("sheet_name")
    changes = data.get("changes")

    base_data_file = BaseDataFile.query.filter_by(id=base_data_file_id).first()
    xl_sheet_df_map = pickle.loads(base_data_file.file_data)

    sheet_df = xl_sheet_df_map[sheet_name]

    if sheet_name == "PL BB Build":
        original_PL_BB_Build = sheet_df

        included_assets = json.loads(base_data_file.included_excluded_assets_map)[
            "included_assets"
        ]
        selected_assets_mask = sheet_df["Investment Name"].isin(included_assets)
        sheet_df = sheet_df[selected_assets_mask]
        sheet_df = sheet_df.reset_index(drop=True)
        sheet_df = sheet_df[sheet_df["Is Eligible Issuer"] == "Yes"]

        if "Cash" not in included_assets:
            cash_row = original_PL_BB_Build[
                original_PL_BB_Build["Investment Name"] == "Cash"
            ]
            sheet_df = pd.concat([sheet_df, cash_row], ignore_index=True)
        else:
            cash_row = original_PL_BB_Build[
                original_PL_BB_Build["Investment Name"] == "Cash"
            ]
            if cash_row["Is Eligible Issuer"].tolist()[0] == "No":
                sheet_df = pd.concat([sheet_df, cash_row], ignore_index=True)

    df = sheet_df.copy()

    if data.get("what_if_analysis_id"):
        what_if_analysis_id = data.get("what_if_analysis_id")
        modified_base_data_file = ModifiedBaseDataFile.query.filter_by(
            id=what_if_analysis_id
        ).first()
        modified_data = pickle.loads(modified_base_data_file.modified_data)
        if sheet_name in list(modified_data.keys()):
            df = modified_data.get(sheet_name)

    initial_df = sheet_df.copy()

    # add new line in dataframe
    added_rows = changes.get("rows_to_add")
    if added_rows:
        df = add_row_at_index(df, changes)

    rows_to_delete = changes.get("rows_to_delete")
    if rows_to_delete:
        df = delete_rows(df, changes)

    updated_assets = changes.get("updated_assets")
    if updated_assets:
        df = update_df(df, changes, sheet_name)
    return df, initial_df


def save_updated_df(data, updated_df, initial_df):
    db = app.db
    base_data_file_id = data.get("base_data_file_id")
    sheet_name = data.get("sheet_name")
    changes = data.get("changes")

    base_data_file = BaseDataFile.query.filter_by(id=base_data_file_id).first()
    xl_sheet_df_map = pickle.loads(base_data_file.file_data)

    # latest modified_base_data_file for same base_data_file which is not saved
    modified_base_data_file = ModifiedBaseDataFile.query.filter_by(
        base_data_file_id=base_data_file_id, is_saved=False
    ).first()

    if not modified_base_data_file:
        changes_to_save = {sheet_name: {}}
        changes_to_save[sheet_name]["updated_assets"] = changes.get("updated_assets")
        if changes.get("rows_to_add"):
            changes_to_save[sheet_name]["added_rows"] = [
                row["row_identifier"] for row in changes.get("rows_to_add")
            ]
        modified_xl_sheet_df_map = {}
        modified_xl_sheet_df_map[sheet_name] = updated_df
        modified_base_data_file = ModifiedBaseDataFile(
            base_data_file_id=base_data_file_id,
            changes=json.dumps(changes_to_save),
            modified_data=pickle.dumps(modified_xl_sheet_df_map),
            initial_data=pickle.dumps({sheet_name: initial_df}),
            simulation_name="update_asset",
        )
    else:
        what_if_analysis_id = data.get("what_if_analysis_id")
        if not what_if_analysis_id:
            changes_to_save = {sheet_name: {}}
            changes_to_save[sheet_name]["updated_assets"] = changes.get(
                "updated_assets"
            )
            if changes.get("rows_to_add"):
                changes_to_save[sheet_name]["added_rows"] = [
                    row["row_identifier"] for row in changes.get("rows_to_add")
                ]
            modified_xl_sheet_df_map = {}
            modified_xl_sheet_df_map[sheet_name] = updated_df
            modified_base_data_file = ModifiedBaseDataFile(
                base_data_file_id=base_data_file_id,
                changes=json.dumps(changes_to_save),
                modified_data=pickle.dumps(modified_xl_sheet_df_map),
                initial_data=pickle.dumps({sheet_name: initial_df}),
                simulation_name="update_asset",
            )
        if what_if_analysis_id:
            # changes_to_save = {sheet_name: {}}

            modified_base_data_file = ModifiedBaseDataFile.query.filter_by(
                id=what_if_analysis_id
            ).first()
            saved_changes = json.loads(modified_base_data_file.changes)
            # saved_changes[sheet_name] = changes
            if saved_changes.get(sheet_name) == None:
                saved_changes[sheet_name] = {}
            saved_changes[sheet_name]["updated_assets"] = changes["updated_assets"]
            if changes.get("rows_to_add"):
                if saved_changes.get(sheet_name):
                    added_rows = saved_changes[sheet_name].get("added_rows") or []
                    for row in changes["rows_to_add"]:
                        row_identifier = row["row_identifier"]
                        added_rows.append(row_identifier)
                    # added_rows.append(row["row_identifier"] for row in changes["rows_to_add"])
                    saved_changes[sheet_name]["added_rows"] = added_rows
                else:
                    saved_changes[sheet_name]["added_rows"] = [
                        row["row_identifier"] for row in changes["added_rows"]
                    ]
            if changes.get("rows_to_delete"):
                if saved_changes.get(sheet_name):
                    deleted_rows = saved_changes[sheet_name].get("deleted_rows") or []
                    for row_to_delete in changes["rows_to_delete"]:
                        deleted_rows.append(row_to_delete["row_identifier"])
                    saved_changes[sheet_name]["deleted_rows"] = deleted_rows
                    updated_assets = saved_changes[sheet_name].get("updated_assets")
                    if updated_assets:
                        updated_assets = [
                            updated_asset
                            for updated_asset in updated_assets
                            if updated_asset["row_name"] not in deleted_rows
                        ]
                        saved_changes[sheet_name]["updated_assets"] = updated_assets

            modified_base_data_file.changes = json.dumps(saved_changes)

            saved_modified_base_data_file = pickle.loads(
                modified_base_data_file.modified_data
            )
            saved_modified_base_data_file[sheet_name] = updated_df
            modified_base_data_file.modified_data = pickle.dumps(
                saved_modified_base_data_file
            )

            saved_initial_base_data_file = pickle.loads(
                modified_base_data_file.initial_data
            )
            saved_initial_base_data_file[sheet_name] = initial_df
            modified_base_data_file.initial_data = pickle.dumps(
                saved_initial_base_data_file
            )

            modified_base_data_file.updated_at = datetime.now(timezone.utc)

    db.session.add(modified_base_data_file)
    db.session.commit()
    db.session.refresh(modified_base_data_file)

    return {
        "error_status": False,
        "message": "Sheet updated successfully",
        "modified_base_data_file_id": modified_base_data_file.id,
    }


def validate_get_sheet_data_request(data):
    base_data_file_id = data.get("base_data_file_id")
    sheet_name = data.get("sheet_name")

    if not base_data_file_id:
        return {"error_status": True, "message": "base_data_file_id is required"}

    base_data_file = BaseDataFile.query.filter_by(id=base_data_file_id).first()
    if not base_data_file:
        return {"error_status": True, "message": "No base_data_file found"}

    sheet_name = data.get("sheet_name")
    if not sheet_name:
        return {"error_status": True, "message": ErrorConstants.SHEET_NAME_REQUIRED_MSG}


percentage_map = {
    "PL BB Build": {
        "Rates Floating Cash Spread": {"is_conditional": False},
        "Rates Current LIBOR/Floor": {"is_conditional": False},
        "Leverage LTV Thru PCOF IV": {"is_conditional": False},
    },
    "PL BB Results": {
        "Concentration Limit": {
            "is_conditional": True,
            "percent_row_identifier": [
                "Max. Issuer Concentration (% BB)",
                "Max. Industry Concentration (Largest Industry, % BB)",
                "Max. Industry Concentration (2nd Largest Industry, % BB)",
                "Max. Industry Concentration (All Other Industries, % BB)",
                "Max. Contribution to BB with Maturity > 8 years",
                "Max. PIK, DIP",
                "Min. Cash, First Lien, and Cov-Lite",
                "Min. Senior Secured",
                "Min. Weighted Average Cash Fixed Coupon",
                "Min. Weighted Average Cash Floating Coupon",
                "Max. LTV Transactions",
                "Max. Third Party Finance Companies",
                "Max. Foreign Eligible Portfolio Investments",
                "Max. Affiliate Investments",
                "Max. Warehouse Assets",
                "Max. Preferred Stock",
            ],
        }
    },
    "Pricing": {"percent": {"is_conditional": False}},
    "Advance Rates": {"Advance Rate": {"is_conditional": False}},
    "Portfolio LeverageBorrowingBase": {
        "Unquoted": {
            "is_conditional": True,
            "percent_row_identifier": [
                "First Lien",
                "Warehouse First Lien",
                "Last Out",
                "Second Lien",
                "High Yield",
                "Mezzanine",
                "Cov-Lite",
                "PIK",
                "Preferred Stock",
                "Equity",
            ],
        },
        "Quoted": {
            "is_conditional": True,
            "percent_row_identifier": [
                "Cash",
                "Cash Equivalent",
                "LT US Debt",
                "First Lien",
                "Warehouse First Lien",
                "Last Out",
                "Second Lien",
                "High Yield",
                "Mezzanine",
                "Cov-Lite",
                "PIK",
                "Preferred Stock",
                "Equity",
            ],
        },
    },
    "Concentration Limits": {"Concentration Limit": {"is_conditional": False}},
    "Other Metrics": {
        "values": {
            "is_conditional": True,
            "percent_row_identifier": [
                "LTV",
                "Concentration Test Threshold 1",
                "Concentration Test Threshold 1",
                "Threshold 1 Advance Rate",
                "Threshold 2 Advance Rate",
            ],
        }
    },
}


def convert_to_table(df, sheet_name):
    table_dict = {sheet_name: {"columns": [], "data": []}}
    table_dict["sheets"] = [
        "PL BB Build",
        "Other Metrics",
        "Availability Borrower",
        "PL BB Results",
        "Subscription BB",
        "PL_BB_Results_Security",
        "Inputs Industries",
        "Pricing",
        "Portfolio LeverageBorrowingBase",
        "Obligors' Net Capital",
        "Advance Rates",
        "Concentration Limits",
        "Principle Obligations",
    ]
    table_dict[sheet_name]["columns"] = [
        {"label": column, "key": column.replace(" ", "_")} for column in df.columns
    ]

    for index, row in df.iterrows():
        row_data = {}

        for col, value in row.items():
            if df.dtypes[col] in ["datetime64[ns]"]:
                if value is pd.NaT:
                    row_data[col.replace(" ", "_")] = ""
                else:
                    # row_data[col.replace(' ', '_')] = value.strftime("%Y-%m-%d")
                    value = value.strftime("%Y-%m-%d")
                    row_data[col.replace(" ", "_")] = value  # .strftime("%Y-%m-%d")
            elif df.dtypes[col] in ["int64"]:
                if value != value:
                    row_data[col.replace(" ", "_")] = ""
                else:
                    if sheet_name in percentage_map.keys():
                        if col in percentage_map[sheet_name].keys():
                            if percentage_map[sheet_name][col]["is_conditional"]:
                                if (
                                    row[row[0]]
                                    in percentage_map[sheet_name][col][
                                        "percent_row_identifier"
                                    ]
                                ):
                                    value = "{:,.01f}%".format(value * 100)
                            else:
                                value = "{:,.01f}%".format(value * 100)
                        else:
                            value = "{:,.0f}".format(value)
                    row_data[col.replace(" ", "_")] = value  #'{:,}'.format(value)
            elif df.dtypes[col] in ["float64"]:
                if value != value:
                    row_data[col.replace(" ", "_")] = ""
                else:
                    if sheet_name in percentage_map.keys():
                        if col in percentage_map[sheet_name].keys():
                            if percentage_map[sheet_name][col]["is_conditional"]:
                                if (
                                    row[0]
                                    in percentage_map[sheet_name][col][
                                        "percent_row_identifier"
                                    ]
                                ):
                                    value = "{:,.01f}%".format(value * 100)
                            else:
                                value = "{:,.01f}%".format(value * 100)
                        else:
                            value = "{:,.0f}".format(value)
                    # row_data[col.replace(' ', '_')] = '{:.2f}%'.format(value)
                    row_data[col.replace(" ", "_")] = value
            else:
                if value != value:
                    row_data[col.replace(" ", "_")] = ""
                else:
                    row_data[col.replace(" ", "_")] = value

        table_dict[sheet_name]["data"].append(row_data)
    return table_dict


def validate_updated_dfs(updated_df, initial_df):
    error_list = []
    for column in initial_df.columns:
        if initial_df[column].dtype != update_df[column].dtype:
            error_list.append(
                f"Data type mismatch for column '{column}': initial data type is {initial_df[column].dtype}, updated data type is {update_df[column].dtype}"
            )

    return error_list


def get_file_data(data):
    base_data_file_id = data.get("base_data_file_id")
    sheet_name = data.get("sheet_name")

    base_data_file = BaseDataFile.query.filter_by(id=base_data_file_id).first()

    file_data = pickle.loads(base_data_file.file_data)
    sheet_df = file_data[sheet_name]

    if sheet_name == "PL BB Build":
        included_assets = json.loads(base_data_file.included_excluded_assets_map)[
            "included_assets"
        ]
        selected_assets_mask = sheet_df["Investment Name"].isin(included_assets)
        sheet_df = sheet_df[selected_assets_mask]

    what_if_analysis_id = data.get("what_if_analysis_id")
    if what_if_analysis_id:
        modified_base_data_file = ModifiedBaseDataFile.query.filter_by(
            id=what_if_analysis_id
        ).first()
        if modified_base_data_file:
            modified_sheet = pickle.loads(modified_base_data_file.modified_data)
            if sheet_name not in modified_sheet.keys():
                sheet_df = pickle.loads(base_data_file.file_data)[sheet_name]
            else:
                sheet_df = modified_sheet[sheet_name]

    table_dict = convert_to_table(sheet_df, sheet_name)
    changes = None
    if what_if_analysis_id:
        modified_base_data_file = ModifiedBaseDataFile.query.filter_by(
            id=what_if_analysis_id
        ).first()
        if sheet_name not in modified_sheet:
            changes = None
        else:
            changes = json.loads(modified_base_data_file.changes)[sheet_name][
                "updated_assets"
            ]

    return table_dict, changes
