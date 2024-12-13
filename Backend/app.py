from flask import (
    Flask,
    request,
    jsonify,
    render_template,
    send_from_directory,
    session,
    send_file,
    make_response,
)
import sys
import pathlib
import os


# source_dir = pathlib.Path().absolute() / "source"
# sys.path.append(str(source_dir))

# source_dir = pathlib.Path().absolute() / "source/PFLT_Borrowing_Base"
# sys.path.append(str(source_dir))

from flask_cors import CORS
import pandas as pd
from pandas import ExcelWriter
import math
from source.functionsCall import *
from source.Borrowing_base_calculation_API import *
from source.WIA_API import *
import pathlib
import numpy as np
import json
import locale
from flask_session import Session
from datetime import timedelta, date

# from std_file_formater import find_file_format_change, rename_columns#, rename_sheets
# from Standard_File_Formater import validate_file
from Exceptions.StdFileFormatException import StdFileFormatException
from source.intermediate_metrics_formulas import formula_info
from source.response import *
from session_files import *
from source.concentration_test import (
    get_data_concentration_test,
    change_haircut_number,
    lock_concentration_test_data,
)
import source.modify_sheet  # import validate_request, update_value_sheet
import source.modified_dfs_calculation  # from modified_dfs_calculation import calculate_borrowing_base
import source.concentration_test_application as concentration_test_application

import os
from flask_migrate import Migrate
from models import *
from urllib.parse import quote_plus
import pickle
from dotenv import load_dotenv
from io import BytesIO
from numerize import numerize

# Blueprint imports
from source.routes.dashboardRoute import dashboard_blueprint
from source.routes.fundSetupRoute import fundSetup_blueprint
from source.routes.wiaRoute import wia_blueprint

BASE_DIR = pathlib.Path().absolute()
os.chdir(BASE_DIR)

app = Flask(__name__, template_folder="dist", static_folder="dist/assets")
CORS(app, origins="*", supports_credentials=True)  # Allow requests from all origins
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "None"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=12)
Session(app)

# Database configurations
load_dotenv()
username = os.getenv("DATABASE_USERNAME")
password = quote_plus(os.getenv("DATABASE_PASSWORD"))
database_name = os.getenv("DATABASE_NAME")
database_host_name = os.getenv("DATABASE_HOST_NAME")
database_port = os.getenv("DATABASE_PORT")

app.secret_key = "srpilusm"
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql://{username}:{password}@{database_host_name}:{database_port}/{database_name}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
migrate = Migrate(app, db)


# blueprint registration
app.register_blueprint(dashboard_blueprint, url_prefix="/api/dashboard")
app.register_blueprint(fundSetup_blueprint, url_prefix="/api/fund_setup")
app.register_blueprint(wia_blueprint, url_prefix="/api/wia")


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/lib/<path:filename>")
def base_static(filename):
    return send_from_directory(app.root_path + "/lib/", filename)


# @app.route("/api/landing_page", methods=["POST"])
# def landing_page():
#     return (
#         landing_page_function()
#     )  # Assuming landing_page_function() is defined in an imported module


# @app.route("/api/validate_file", methods=["POST"])
# def validate():
#     return (
#         validate_function()
#     )  # Assuming validate_function() is defined in an imported module


# @app.route("/api/calculate", methods=["POST", "DELETE"])
# def calculate():
#     return (
#         calculate_function()
#     )  # Assuming calculate_function() is defined in an imported module


@app.route("/api/get_WIA_assets", methods=["POST"])
def get_WIA_assets():
    return (
        get_WIA_assets_function()
    )  # Assuming get_WIA_assets_function() is defined in an imported module


@app.route("/api/changeEBITDA", methods=["POST"])
def change_ebitda():
    return (
        change_ebitda_function()
    )  # Assuming change_ebitda_function() is defined in an imported module


# @app.route("/api/get_table_from_card", methods=["POST"])
# def get_table_from_card():
#     return (
#         get_table_from_card_function()
#     )  # Assuming get_table_from_card_function() is defined in an imported module


# @app.route("/api/changeasset", methods=["POST"])
# def change_asset():
#     return (
#         change_asset_function()
#     )  # Assuming change_asset_function() is defined in an imported module


@app.route("/api/get_selected_WIA_asstes", methods=["POST"])
def get_selected_WIA_asstes():
    return (
        get_selected_WIA_asstes_function()
    )  # Assuming get_selected_WIA_asstes_function() is defined in an imported module


# @app.route("/api/get_assets_list", methods=["POST"])
# def get_asset_selection_table():
#     return (
#         get_asset_selection_table_function()
#     )  # Assuming get_asset_selection_table_function() is defined in an imported module


# @app.route("/api/get_files_list", methods=["POST"])
# def retrieve_data():
#     return (
#         retrieve_data_function()
#     )  # Assuming retrieve_data_function() is defined in an imported module


@app.route("/api/select_what_if_analysis", methods=["POST"])
def select_what_if_analysis():
    return (
        select_what_if_analysis_function()
    )  # Assuming select_what_if_analysis_function() is defined in an imported module


@app.route("/api/get_analysis_list", methods=["POST"])
def get_analysis_list():
    return (
        get_analysis_list_function()
    )  # Assuming get_analysis_list_function() is defined in an imported module


# @app.route("/api/calendar", methods=["POST"])
# def retrieve_borrowing_base_data_datewise():
#     return (
#         retrieve_borrowing_base_data_datewise_function()
#     )  # Assuming retrieve_borrowing_base_data_datewise_function() is defined in an imported module


# @app.route("/api/trend_graph", methods=["POST"])
# def trend_graph():
#     return (
#         trend_graph_function()
#     )  # Assuming trend_graph_function() is defined in an imported module


@app.route("/api/download_excel", methods=["POST"])
def download_excel():
    return (
        download_excel_function()
    )  # Assuming download_excel_function() is defined in an imported module


@app.route("/api/get_intermediate_metrics", methods=["POST"])
def get_intermediate_metrics():
    return (
        get_intermediate_metrics_function()
    )  # Assuming get_intermediate_metrics_function() is defined in an imported module


# @app.route("/api/add_asset_overview", methods=["POST"])
# def add_asset_overview():
#     return (
#         add_asset_overview_function()
#     )  # Assuming add_asset_overview_function() is defined in an imported module


@app.route("/api/save_assets_for_wia", methods=["POST"])
def save_assets_for_wia():
    return (
        save_assets_for_wia_function()
    )  # Assuming save_assets_for_wia_function() is defined in an imported module


@app.route("/api/set_user_config", methods=["POST"])
def set_user_config():
    return (
        set_user_config_function()
    )  # Assuming set_user_config_function() is defined in an imported module


@app.route("/api/get_columns_list", methods=["POST"])
def get_columns_list():
    return (
        get_columns_list_function()
    )  # Assuming get_columns_list_function() is defined in an imported module


@app.route("/api/get_previous_assets", methods=["POST"])
def get_previous_columns():
    return (
        get_previous_columns_function()
    )  # Assuming get_previous_columns_function() is defined in an imported module


@app.route("/api/download_excel_for_assets", methods=["POST"])
def download_excel_for_assets():
    return (
        download_excel_for_assets_function()
    )  # Assuming download_excel_for_assets_function() is defined in an imported module


@app.route("/api/get_mathematical_formula", methods=["POST"])
def get_mathematical_formula():
    return (
        get_mathematical_formula_function()
    )  # Assuming get_mathematical_formula_function() is defined in an imported module


@app.route("/api/get_concentration_data", methods=["POST"])
def get_concentration_data():
    return (
        get_concentration_data_function()
    )  # Assuming get_concentration_data_function() is defined in an imported module


@app.route("/api/concentration_data_analysis", methods=["POST"])
def concentration_data_analysis():
    return (
        concentration_data_analysis_function()
    )  # Assuming concentration_data_analysis_function() is defined in an imported module


@app.route("/api/lock_concentration_test", methods=["POST"])
def lock_concentration_test():
    return (
        lock_concentration_test_function()
    )  # Assuming lock_concentration_test_function() is defined in an imported module



@app.route("/api/calculate_bb_modified_sheets", methods=["POST"])
def calculate_bb_modified_sheets():
    return calculate_bb_modified_sheets_function()


@app.route("/api/save_what_if_analysis", methods=["POST"])
def save_what_if_analysis():
    return save_what_if_analysis_function()


# @app.route("/api/get_concentration_test_master_list", methods=["POST"])
# def get_concentration_test_master_list():
#     return concentration_test_application.get_concentration_test_master_list_function()


# @app.route("/api/change_conc_test_config", methods=["POST"])
# def change_conc_test_config():
#     return concentration_test_application.change_conc_test_config_function()


# @app.route('/api/apply_concentration_test', methods=['POST'])
# def apply_concentration_test():
#     return concentration_test_application.apply_concentration_test_function()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run("0.0.0.0", port=5000, debug=True)
