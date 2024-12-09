from datetime import datetime, timezone
import json
from flask import jsonify
import pandas as pd
import pickle

from models import WhatIfAnalysis,  ModifiedBaseDataFile, BaseDataFile, db
from source.utility.ServiceResponse import ServiceResponse


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