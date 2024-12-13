from datetime import datetime, timezone
import json
from flask import jsonify
import pandas as pd
import pickle
import numpy as np

from models import WhatIfAnalysis,  ModifiedBaseDataFile, BaseDataFile, db
from source.utility.ServiceResponse import ServiceResponse

from constants.error_constants import ErrorConstants
from source.services.PCOF.WIA.util import PCOF_WIA
from source.services.PFLT.WIA.util import PFLT_WIA
import app
from source.services.commons import commonServices

PCOF_FUND_WIA = PCOF_WIA()
PFLT_FUND_WIA = PFLT_WIA()


def get_asset_overview(excelfile):
    wia_ref_sheets_dict = pd.read_excel(excelfile, sheet_name=None)
    data = wia_ref_sheets_dict["Sheet1"]
    preview_table_data = {"sheet1": {"columns": [], "data": []}}
    # Add columns to the preview_table_data dynamically
    preview_table_data["sheet1"]["columns"] = [
        {"title": col, "key": col.replace(" ", "_")} for col in data.columns
    ]
    # Add data to the preview_table_data
    for _, row in data.iterrows():
        row_data = {}
        for col, value in row.items():
            if isinstance(value, datetime):  # Convert datetime to string
                if pd.isna(value):
                    value = None
                else:
                    value = value.strftime("%Y-%m-%d")
            row_data[col.replace(" ", "_")] = value
        preview_table_data["sheet1"]["data"].append(row_data)
    # Convert preview_table_data to JSON string and then parse it to a dictionary
    response_dict = json.loads(json.dumps(preview_table_data))
    return jsonify(response_dict), 200


def save_what_if_analysis(
    base_data_file_id,
    simulation_name,
    initial_data,
    updated_data,
    intermediate_metrics_data,
    response,
    note,
    simulation_type,
    is_saved=False,
):
    try:
        what_if_analysis = WhatIfAnalysis(
            base_data_file_id=base_data_file_id,
            simulation_name=simulation_name,
            response=pickle.dumps(response),
            note=note,
            initial_data=pickle.dumps(initial_data),
            updated_data=pickle.dumps(updated_data),
            intermediate_metrics_data=pickle.dumps(intermediate_metrics_data),
            simulation_type=simulation_type,
        )

        db.session.add(what_if_analysis)
        db.session.commit()
        db.session.refresh(what_if_analysis)
        return {"error": False, "what_if_analysis": what_if_analysis}
    except Exception as e:
        print(str(e))
        db.session.rollback()
        return {"error": True, "what_if_analysis": None}

def save_analysis(what_if_analysis_id, analysis_type, simulation_name, note):
    if analysis_type == "Update asset":
        what_if_analysis = ModifiedBaseDataFile.query.filter_by(id=what_if_analysis_id).first()
    else:
        what_if_analysis = WhatIfAnalysis.query.filter_by(id=what_if_analysis_id).first()

    if not simulation_name:
        simulation_name = what_if_analysis.simulation_name

    what_if_analysis.simulation_name = simulation_name
    what_if_analysis.note = note
    what_if_analysis.is_saved = True

    db.session.add(what_if_analysis)
    db.session.commit()

    response = {"data": "What if analysis saved successfully"}
    return ServiceResponse.success(data=response, message="What if analysis saved successfully")

def wia_library(user_id):
    what_if_data = (
            db.session.query(BaseDataFile, WhatIfAnalysis)
            .join(WhatIfAnalysis, WhatIfAnalysis.base_data_file_id == BaseDataFile.id)
            .filter(BaseDataFile.user_id == user_id, WhatIfAnalysis.is_saved == True)
            .all()
        )
    update_Asset_what_if_data = (
            db.session.query(BaseDataFile, ModifiedBaseDataFile)
            .join(
                ModifiedBaseDataFile,
                ModifiedBaseDataFile.base_data_file_id == BaseDataFile.id,
            )
            .filter(
                BaseDataFile.user_id == user_id, ModifiedBaseDataFile.is_saved == True
            )
            .all()
        )

    wia_library_list = []
    for base_data_file, what_if_entry in what_if_data:
        result_entry = {
            "base_file_name": base_data_file.file_name,  # Assuming file_name is the column name for the file name
            "name": what_if_entry.simulation_name,
            "note": what_if_entry.note if what_if_entry.note else "",
            "what_if_analysis_id": what_if_entry.id,
            "simulation_type": what_if_entry.simulation_type,
            "last_updated": (
                what_if_entry.updated_at.strftime("%m/%d/%Y")
                if what_if_entry.updated_at
                else ""
            ),
            "created_date": (
                what_if_entry.created_at.strftime("%m/%d/%Y %H:%M")
                if what_if_entry.created_at
                else ""
            ),  
        }
        wia_library_list.append(result_entry)

    for base_data_file, what_if_entry in update_Asset_what_if_data:
        result_entry = {
            "base_file_name": base_data_file.file_name, 
            "name": what_if_entry.simulation_name,
            "note": what_if_entry.note if what_if_entry.note else "",
            "what_if_analysis_id": what_if_entry.id,
            "simulation_type": what_if_entry.simulation_type,
            "last_updated": (
                what_if_entry.updated_at.strftime("%m/%d/%Y")
                if what_if_entry.updated_at
                else ""
            ),  
            "created_date": (
                what_if_entry.created_at.strftime("%m/%d/%Y %H:%M")
                if what_if_entry.created_at
                else ""
            ),  
        }
        wia_library_list.append(result_entry)

    return ServiceResponse.success(data=wia_library_list, message="Saved what if analysis list fetched successfully")

def validate_get_sheet_data_request(data):
    base_data_file_id = data.get("base_data_file_id")
    sheet_name = data.get("sheet_name")

    if not base_data_file_id:
        return ServiceResponse.error(message="base_data_file_id is required")

    base_data_file = BaseDataFile.query.filter_by(id=base_data_file_id).first()
    if not base_data_file:
        return ServiceResponse.error(message="No base_data_file found")

    sheet_name = data.get("sheet_name")
    if not sheet_name:
        return ServiceResponse.error(message=ErrorConstants.SHEET_NAME_REQUIRED_MSG)
    
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

  

def validate_update_value_request(data): 
    base_data_file_id = data.get("base_data_file_id")
    if not base_data_file_id:
        return ServiceResponse.error(message="base_data_file_id is required")

    sheet_name = data.get("sheet_name")
    if not sheet_name:
        return ServiceResponse.error(message=ErrorConstants.SHEET_NAME_REQUIRED_MSG)

    base_data_file = BaseDataFile.query.filter_by(id=base_data_file_id).first()
    if not base_data_file:
        return ServiceResponse.error(message="No base_data_file found")

    file_data = pickle.loads(base_data_file.file_data)
    if sheet_name not in file_data.keys():
        return ServiceResponse.error(message=f"{sheet_name} sheet not found")

    changes = data.get("changes")
    if not changes:
        return ServiceResponse.error(message="Changes is required")
    

def save_updated_df(data, updated_df, initial_df):
    try:
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

        return ServiceResponse.success(
            data = {
                "modified_base_data_file_id": modified_base_data_file.id,
            }, 
            message = "Sheet updated successfully"
        )
    except Exception as e:
        return ServiceResponse.error()
    

def filter_assets(sheet_df, base_data_file, asset_column_name):
    included_assets = json.loads(base_data_file.included_excluded_assets_map)["included_assets"]

    selected_assets_mask = sheet_df[asset_column_name].isin(included_assets)
    return sheet_df[selected_assets_mask]

def get_file_data(data):
    base_data_file_id = data.get("base_data_file_id")
    sheet_name = data.get("sheet_name")
    # sheet_name = "Loan List"

    base_data_file = BaseDataFile.query.filter_by(id=base_data_file_id).first()

    file_data = pickle.loads(base_data_file.file_data)
    sheet_df = file_data[sheet_name]
    fund_type = base_data_file.fund_type

    if sheet_name == "PL BB Build":
        sheet_df = filter_assets(sheet_df, base_data_file, "Investment Name")

    if sheet_name == "Loan List":
        sheet_df = filter_assets(sheet_df, base_data_file, "Security Name")

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

    if fund_type == "PCOF":
        table_dict = PCOF_FUND_WIA.convert_to_table(sheet_df, sheet_name)

    if fund_type == "PFLT":
        table_dict = PFLT_FUND_WIA.convert_to_table(sheet_df, sheet_name)

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

def update_df(sheet_df, changes, sheet_name):
    values_to_update = changes["updated_assets"]
    for value_to_update in values_to_update:
        row_name = value_to_update["row_name"]

        col_name = value_to_update["column_name"]
        if col_name != sheet_df.columns[0]:
            row_index = commonServices.get_row_index(sheet_df, row_name)
            if row_index != -1:
                updated_value = value_to_update["updated_value"]
                updated_value = commonServices.get_updated_value(updated_value)

                col_type = sheet_df[col_name].dtype

                updated_value = commonServices.get_raw_value(updated_value, col_type)
                # print(col_type, col_name, updated_value)

                previous_value = sheet_df.loc[row_index, col_name]
                previous_value = commonServices.get_raw_value(previous_value, col_type)
                if commonServices.find_is_NaT(previous_value):
                    previous_value = ""
                value_to_update["previous_value"] = previous_value
                sheet_df.loc[row_index, col_name] = updated_value
    return sheet_df


def get_modified_data_file(modified_base_data_file_id):
    modified_base_data_file = ModifiedBaseDataFile.query.filter_by(id=modified_base_data_file_id).first()
    return modified_base_data_file