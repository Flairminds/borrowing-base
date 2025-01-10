from flask import jsonify
import pickle

from models import Fund, ConcentrationTest, FundConcentrationTest, db, BaseDataFile
from source.config import Config
from datetime import datetime
from source.utility.ServiceResponse import ServiceResponse


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
        if test.test_name not in [
            "Min. Eligible Issuers (#)",
            "8 or 9 Issuers?",
            "Max. Weighted Average Maturity (Years)",
            "Max. Weighted Average Leverage thru Borrower",
        ]:
            limit_percentage = test.limit_percentage * 100
        if limit_percentage == 0:
            limit_percentage = ""
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
                "show_on_dashboard": test.show_on_dashboard,
                "eligible_funds": list(
                    Config().data["fund_std_col_map"][test.test_name].keys()
                ),
            }
        )

    columns = [
        {"key": "test_name", "title": "Concentration Test"},
        {"key": "description", "title": "Description "},
        {"key": "mathematical_formula", "title": "Mathematical Formula"},
        # {"key": "columns", "title": "Columns"},
        {"key": "limit_percentage", "title": "Concentration Limit"},
        {"key": "eligible_funds", "title": "Applicable Funds"},
        {"key": "show_on_dashboard", "title": "Show On Dashboard"},
    ]

    return (
        jsonify(
            {
                "error_status": False,
                "columns": columns,
                "data": test_list,
            }
        ),
        200,
    )


def update_limit(test_changes):
    try:
        changed_records = []
        for test in test_changes:
            test_id = test["test_id"]
            fund_id = test["fund_id"]
            limit_percentage = test.get("limit_percentage")
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
            return ServiceResponse.success(message="No changes done in test config")
        db.session.add_all(changed_records)
        db.session.commit()
        return ServiceResponse.success(message="Concentration test config updated successfully", data=changed_records)

    except Exception as e:
        raise Exception(e)


def get_base_files(user_id):
    try:
        base_data_files = (
            BaseDataFile.query.filter_by(user_id=user_id)
            .order_by(BaseDataFile.closing_date.desc())
            .all()
        )
        # If no data found for the user_id, return an error response
        if not base_data_files:
            return ServiceResponse.error(message="No data found for the user_id", status_code=404)
        return ServiceResponse.success(data={"files": base_data_files})
    except Exception as e:
        raise Exception(e)


def recalculate_bb(base_data_files, changed_records):
    try:
        test_ids = []
        for c in changed_records:
            test_ids.append(c.test_id)
        conc_tests = db.session.query(
                ConcentrationTest.id,
                ConcentrationTest.test_name,
                ConcentrationTest.unit,
                FundConcentrationTest.limit_percentage,
                FundConcentrationTest.id
            ).join(FundConcentrationTest).filter(ConcentrationTest.id.in_(test_ids)).all()
        for file in base_data_files["data"]["files"]:
            try:
                response_data = pickle.loads(file.response)
                a = response_data["concentration_test_data"]
                index = 0
                for d in a["Concentration Test"]:
                    for temp in conc_tests:
                        print(temp[1])
                        if temp[1] == d["data"]:
                            limit = temp[3]
                            actual = a["Actual"][index]["data"]
                            if temp[2] == "percentage":
                                a["Concentration Limit"][index]["data"] = str("%0.1f" % (temp[3] * 100)) + '%'
                                actual = float(actual.replace('%', '')) / 100
                            else:
                                a["Concentration Limit"][index]["data"] = temp[3]
                            if limit < actual:
                                a["Result"][index]["data"] = 'Fail'
                            else:
                                a["Result"][index]["data"] = 'Pass'
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
