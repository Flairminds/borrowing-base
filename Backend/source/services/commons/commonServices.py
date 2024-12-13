from models import BaseDataFile, WhatIfAnalysis, ModifiedBaseDataFile, db
from source.utility.ServiceResponse import ServiceResponse


def get_base_data_file(**kwargs):
    if "base_data_file_id" in kwargs.keys():
        base_data_file_id = kwargs["base_data_file_id"]
        base_data_file = BaseDataFile.query.filter_by(id=base_data_file_id).first()
    else:
        user_id = kwargs["user_id"]
        if "closing_date" not in kwargs.keys():
            base_data_file = (
                BaseDataFile.query.filter_by(user_id=user_id)
                .order_by(BaseDataFile.closing_date.desc())
                .first()
            )
        else:
            closing_date = kwargs["closing_date"]
            base_data_file = BaseDataFile.query.filter_by(
                closing_date=closing_date, user_id=user_id
            ).first()
    return base_data_file

def get_fundType_of_wia(what_if_analysis_id, what_if_analysis_type):

    if what_if_analysis_type == "Update asset":
        fund_type = (
            db.session
            .query(BaseDataFile.fund_type)
            .join(ModifiedBaseDataFile, ModifiedBaseDataFile.base_data_file_id == BaseDataFile.id)
            .filter(ModifiedBaseDataFile.id == what_if_analysis_id, ModifiedBaseDataFile.simulation_type == what_if_analysis_type)
            .first()
        )
    else:
        fund_type = (
            db.session
            .query(BaseDataFile.fund_type)
            .join(WhatIfAnalysis, WhatIfAnalysis.base_data_file_id == BaseDataFile.id)
            .filter(WhatIfAnalysis.id == what_if_analysis_id, WhatIfAnalysis.simulation_type == what_if_analysis_type)
            .first()
        )

    if not fund_type:
        return ServiceResponse.error(message="What if analysis with given data not found")
    
    fund_type = fund_type[0]

    return ServiceResponse.success(data=fund_type, message="Base data file fund for WIA fetched")