from models import BaseDataFile


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
