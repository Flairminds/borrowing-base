from flask import jsonify
import pickle
from sqlalchemy import text

from models import Fund, ConcentrationTest, FundConcentrationTest, db, BaseDataFile
from source.config import Config
from datetime import datetime
from source.utility.ServiceResponse import ServiceResponse
from source.concentration_test_application import ConcentraionTestFormatter, ConcentrationTestExecutor


def get_concentration_tests(fund_name):
    fund = Fund.query.filter_by(fund_name=fund_name).first()
    fund_tests = (
        db.session.query(
            ConcentrationTest.id,
            ConcentrationTest.test_name,
            ConcentrationTest.description,
            ConcentrationTest.mathematical_formula,
            ConcentrationTest.columns,
            ConcentrationTest.unit,
            ConcentrationTest.data_type,
            FundConcentrationTest.limit_percentage,
            FundConcentrationTest.min_limit,
            FundConcentrationTest.show_on_dashboard,
            # FundConcentrationTest.id,
        )
        .join(FundConcentrationTest)
        .filter(FundConcentrationTest.fund_id == fund.id)
        .all()
    )

    test_list = []
    for test in fund_tests:
        limit_percentage = test.limit_percentage
        if test.unit == 'percentage':
            limit_percentage = test.limit_percentage * 100
        if limit_percentage == 0:
            limit_percentage = ""
        engine = db.get_engine()
        with engine.connect() as connection:
            applicable_funds_tuple = connection.execute(text(f"select f.fund_name from fund f join fund_concentration_test fct on f.id = fct.fund_id where fct.test_id = (select id from concentration_test ct where ct.test_name = '{test.test_name}')")).fetchall()

            applicable_funds = [fund_tuple[0] for fund_tuple in applicable_funds_tuple]
        test_list.append(
            {
                "test_id": test.id,
                "fund_id": fund.id,
                "test_name": test.test_name,
                "description": test.description,
                "mathematical_formula": test.mathematical_formula,
                "columns": test.columns,
                "unit": test.unit,
                "data_type": test.data_type,
                "limit_percentage": limit_percentage,
                "min_limit": test.min_limit,
                "show_on_dashboard": test.show_on_dashboard,
                "eligible_funds": applicable_funds,
            }
        )

    columns = [
        {"key": "test_name", "title": "Concentration Test"},
        {"key": "description", "title": "Description "},
        {"key": "mathematical_formula", "title": "Mathematical Formula"},
        {"key": "min_limit", "title": "min_limit"},
        {"key": "limit_percentage", "title": "Concentration Limit"},
        {"key": "eligible_funds", "title": "Applicable Funds"},
        {"key": "show_on_dashboard", "title": "Show On Dashboard"},
    ]

    return {
        "error_status": False,
        "success": True,
        "columns": columns,
        "data": test_list
    }


def update_limit(test_changes):
    try:
        changed_records = []
        for test in test_changes:
            test_id = test["test_id"]
            fund_id = test["fund_id"]
            limit_percentage = 0 if test.get("limit_percentage") == "" else test.get("limit_percentage")
            show_on_dashboard = test.get("show_on_dashboard")
            
            if limit_percentage is not None or show_on_dashboard is not None:
                fund_test = FundConcentrationTest.query.filter_by(fund_id=fund_id, test_id=test_id).first()
                # fund_tests = FundConcentrationTest.query.filter_by(test_id=fund_test.test_id)
                # for fund_type in fund_tests:
                if limit_percentage is not None:
                    val = float(limit_percentage)
                    concentration_test = ConcentrationTest.query.filter_by(id=test_id).first()
                    if concentration_test.data_type == 'integer' and not int(val) == val:
                        return ServiceResponse.error(message="Integer value expected for certain tests.", status_code=400)
                    
                    if concentration_test.unit == 'percentage':
                        val /= 100
                    fund_test.limit_percentage = val

                if show_on_dashboard is not None:
                    fund_test.show_on_dashboard = show_on_dashboard

                fund_test.modified_at = datetime.now()
                changed_records.append(fund_test)
        if len(changed_records) == 0:
            return ServiceResponse.success(message="No changes done in test config", data=[])
        db.session.add_all(changed_records)
        db.session.commit()
        return ServiceResponse.success(message="Concentration test config updated successfully", data=changed_records)

    except Exception as e:
        raise Exception(e)


def get_base_files(user_id, fund_id):
    try:
        fund_type_record = db.session.query(
                Fund.id,
                Fund.fund_name,
            ).filter(Fund.id == fund_id).first()
        base_data_files = (
            BaseDataFile.query.filter_by(user_id=user_id, fund_type=fund_type_record.fund_name)
            .order_by(BaseDataFile.closing_date.desc())
            .all()
        )
        # If no data found for the user_id, return an error response
        if not base_data_files:
            return ServiceResponse.error(message="No data found for the user_id", status_code=404)
        return ServiceResponse.success(data={"files": base_data_files})
    except Exception as e:
        raise Exception(e)

def is_pass(actual, limit, comparison_type):
    if comparison_type == 'LessEqual':
        return actual <= limit
    if comparison_type == 'Greater':
        return actual > limit
    if comparison_type == 'GreaterEqual':
        return actual >= limit
    if comparison_type == 'Equal':
        return actual == limit
    return False


def recalculate_bb(base_data_files, changed_records):
    try:
        test_ids = []
        fund_id = changed_records[0].fund_id
        for c in changed_records:
            test_ids.append(c.test_id)
        conc_tests = db.session.query(
                ConcentrationTest.id,
                ConcentrationTest.test_name,
                ConcentrationTest.unit,
                FundConcentrationTest.limit_percentage,
                FundConcentrationTest.id,
                ConcentrationTest.comparison_type,
                FundConcentrationTest.show_on_dashboard
            ).join(FundConcentrationTest).filter(ConcentrationTest.id.in_(test_ids), FundConcentrationTest.fund_id == fund_id).all()
        for file in base_data_files["data"]["files"]:
            try:
                response_data = pickle.loads(file.response)
                a = response_data["concentration_test_data"]
                index = 0
                concentration_tests = []
                for d in a["Concentration Test"]:
                    for temp in conc_tests:
                        # print(temp[1])
                        if temp[1] == d["data"]:
                            limit = temp[3]
                            show_on_dashboard = temp[6]
                              
                            actual = a["Actual"][index]["data"]
                            if temp[2] == "percentage":
                                a["Concentration Limit"][index]["data"] = str("%0.1f" % (temp[3] * 100)) + '%'
                                actual = float(actual.replace('%', '')) / 100
                            else:
                                a["Concentration Limit"][index]["data"] = temp[3]
                            
                            if is_pass(actual, limit, temp[5]):
                                a["Result"][index]["data"] = 'Pass'
                            else:
                                a["Result"][index]["data"] = 'Fail'
                            
                            # if show_on_dashboard:
                            #     concentration_tests.append({
                            #         'Concentration Test': a['Concentration Test'][index],
                            #         'Concentration Limit': a['Concentration Limit'][index],
                            #         'Actual': a['Actual'][index],
                            #         'Result': a['Result'][index],
                            #         'columns': a['columns'][index],
                            #     })
                    index += 1
                response_data["concentration_test_data"] = a
                pickled_response_data = pickle.dumps(response_data)
                file.response = pickled_response_data
                file.updated_at = datetime.now()
                db.session.add(file)
                db.session.commit()
            except Exception as e:
                continue
        return ServiceResponse.success()
    except Exception as e:
        print(str(e))
        return ServiceResponse.success()
