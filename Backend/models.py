from datetime import datetime, timezone
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Identity
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class BaseDataFile(db.Model):
    id = db.Column(
        db.Integer, Identity(start=1, cycle=True), primary_key=True, autoincrement=True
    )
    user_id = db.Column(db.Integer)
    file_name = db.Column(db.String)
    closing_date = db.Column(db.Date)
    fund_type = db.Column(db.String)
    # file_data = db.Column(db.JSON, nullable=False)
    # response = db.Column(db.JSON)

    file_data = db.Column(db.PickleType, nullable=False)
    response = db.Column(db.PickleType)
    intermediate_calculation = db.Column(db.PickleType)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    included_excluded_assets_map = db.Column(db.JSON, nullable=False)

    # one to many relationship with WhatIfAnalysis
    what_if_analyses = relationship("WhatIfAnalysis", back_populates="base_data_file")

    # One to many relationship with ModifiedBaseDataFile
    modified_base_data_files = relationship(
        "ModifiedBaseDataFile", back_populates="base_data_file"
    )


class WhatIfAnalysis(db.Model):
    id = db.Column(
        db.Integer, Identity(start=1, cycle=True), primary_key=True, autoincrement=True
    )
    base_data_file_id = db.Column(
        db.Integer, db.ForeignKey("base_data_file.id"), nullable=False
    )
    simulation_name = db.Column(db.String, nullable=False)
    initial_data = db.Column(db.PickleType, nullable=False)
    updated_data = db.Column(db.PickleType, nullable=False)
    intermediate_metrics_data = db.Column(db.PickleType, nullable=False)
    response = db.Column(db.PickleType, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    note = db.Column(db.String)
    is_saved = db.Column(db.Boolean, default=False)
    simulation_type = db.Column(db.String, nullable=False)

    # many to one relationship with BaseDataFile
    base_data_file = db.relationship("BaseDataFile", back_populates="what_if_analyses")


class WiaRefSheets(db.Model):
    id = db.Column(
        db.Integer, Identity(start=1, cycle=True), primary_key=True, autoincrement=True
    )
    user_id = db.Column(db.Integer, nullable=False)
    ref_file_name = db.Column(db.String, nullable=False)
    sheet_data = db.Column(db.PickleType, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))


class UserConfig(db.Model):
    id = db.Column(
        db.Integer, Identity(start=1, cycle=True), primary_key=True, autoincrement=True
    )
    user_id = db.Column(db.Integer, nullable=False)

    assets_selection_columns = db.Column(
        db.JSON,
        default=json.dumps(
            [
                "Investment Name",
                "Investment Investment Type",
                "Investment Par",
                "Investment Industry",
                "Investment Closing Date",
            ]
        ),
    )

    response_format = db.Column(db.String, default="numerize")


class ModifiedBaseDataFile(db.Model):
    id = db.Column(
        db.Integer, Identity(start=1, cycle=True), primary_key=True, autoincrement=True
    )
    base_data_file_id = db.Column(
        db.Integer, db.ForeignKey("base_data_file.id"), nullable=False
    )
    simulation_name = db.Column(db.String, nullable=False)
    initial_data = db.Column(db.PickleType, nullable=False)
    modified_data = db.Column(db.PickleType, nullable=False)
    changes = db.Column(db.JSON)
    intermediate_metrics_data = db.Column(db.PickleType)
    response = db.Column(db.PickleType)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    note = db.Column(db.String)
    simulation_type = db.Column(db.String, default="Update asset")
    is_saved = db.Column(db.Boolean, default=False)

    # Many to one relationship with BaseDataFile
    base_data_file = db.relationship(
        "BaseDataFile", back_populates="modified_base_data_files"
    )


class FundConcentrationTest(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fund_id = db.Column(db.Integer, db.ForeignKey("fund.id"), nullable=False)
    test_id = db.Column(
        db.Integer, db.ForeignKey("concentration_test.id"), nullable=False
    )
    limit_percentage = db.Column(db.Float, nullable=False)
    show_on_dashboard = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    modified_at = db.Column(db.DateTime(timezone=True))

    # Relationships
    fund = db.relationship("Fund", back_populates="concentration_tests")
    concentration_test = db.relationship("ConcentrationTest", back_populates="funds")


class ConcentrationTest(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    test_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    mathematical_formula = db.Column(db.String(255))
    columns = db.Column(db.JSON, nullable=True)
    ct_code = db.Column(db.String(15), unique=True)
    unit = db.Column(db.String(15), server_default='percentage')
    data_type = db.Column(db.String(15), server_default='integer')
    default_value = db.Column(db.Integer, server_default=db.text("0"))
    eligible_funds = db.Column(db.ARRAY(db.String))
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    modified_at = db.Column(db.DateTime(timezone=True))

    # Many-to-many relationship
    funds = db.relationship(
        "FundConcentrationTest", back_populates="concentration_test"
    )


class Fund(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fund_name = db.Column(db.String(100), nullable=False)

    # Many-to-many relationship
    concentration_tests = db.relationship(
        "FundConcentrationTest", back_populates="fund"
    )


class SourceFiles(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    file_name = db.Column(db.String(100), nullable=False)
    extension = db.Column(db.String(100), nullable=False)
    report_date = db.Column(db.DateTime(timezone=True))
    file_url = db.Column(db.String(200), nullable=False)
    file_size = db.Column(db.Float, nullable=False)
    company_id = db.Column(db.Integer, nullable=False)
    fund_type = db.Column(db.String(100), nullable=False)
    is_validated = db.Column(db.Boolean, default=False)
    is_extracted = db.Column(db.Boolean, default=False)
    uploaded_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    modified_at = db.Column(db.DateTime(timezone=True))
    uploaded_by = db.Column(db.Integer, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False)
    file_type = db.Column(db.String(100))

class HaircutConfig(db.Model):
    hc_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fund_type = db.Column(db.String(15), nullable=False)
    company_id = db.Column(db.Integer, nullable=False)
    haircut_level = db.Column(db.String(127), nullable=False)
    obligor_tier = db.Column(db.String(127), nullable=False)
    position = db.Column(db.String(127), nullable=False)
    value = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    created_by = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    modified_by = db.Column(db.Integer, nullable=True)
    modified_at = db.Column(db.DateTime(timezone=True))

class IndustryList(db.Model):
    il_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fund_type = db.Column(db.String(15), nullable=False)
    company_id = db.Column(db.Integer, nullable=False)
    industry_no = db.Column(db.Integer, nullable=False)
    industry_name = db.Column(db.String(255), nullable=False)
    industry_code = db.Column(db.String(127), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    created_by = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    modified_by = db.Column(db.Integer, nullable=True)
    modified_at = db.Column(db.DateTime(timezone=True))

class Companies(db.Model):
    company_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_name = db.Column(db.String(255), nullable=False)
    admin_id = db.Column(db.Integer, nullable=True)
    created_by = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    modified_by = db.Column(db.Integer, nullable=True)
    modified_at = db.Column(db.DateTime(timezone=True))

class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String, nullable=False)
    display_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String, nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.company_id"), nullable=False)
    created_by = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    modified_by = db.Column(db.Integer, nullable=True)
    modified_at = db.Column(db.DateTime(timezone=True))