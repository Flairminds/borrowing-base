from sqlalchemy import text
import itertools

from models import db, LoanTypeMaster, LoanTypeMapping
from source.utility.ServiceResponse import ServiceResponse
from source.utility.Util import create_lookup

def get_loan_type_data():
    engine = db.get_engine()
    with engine.connect() as connection:
        unmapped_loan_types = connection.execute(text('''
            select distinct ssch."Issue Name" 
            from sf_sheet_client_holdings ssch 
            left join loan_type_master ltm on ssch."Issue Name" = ltm.loan_type 
            where ltm.loan_type IS NULL
        ''')).fetchall()

        mapped_loan_types = connection.execute(text('''
            select 
                ltmapping.id as mapping_id, 
                ltmapping.master_loan_type_id as master_loan_type_id, 
                ltmaster.loan_type as master_loan_type, 
                ltmapping.loan_type as mapped_loan_type 
                from loan_type_mapping ltmapping 
                join loan_type_master ltmaster on ltmapping.master_loan_type_id = ltmaster.id
        ''')).fetchall()
    
    unmapped_loan_types_list = list(itertools.chain(*unmapped_loan_types))

    mapped_loan_type_details = {}
    for mapped_loan_type_data in mapped_loan_types:
        master_loan_type = mapped_loan_type_data[2]
        mapped_loan_type = mapped_loan_type_data[3]

        if master_loan_type not in mapped_loan_type_details:
            mapped_loan_type_details[master_loan_type] = []

        mapped_loan_type_details[master_loan_type].append(mapped_loan_type)

    loan_types_data = {
        'unmapped_loan_type_data': unmapped_loan_types_list,
        'mapped_loan_type_data': mapped_loan_type_details,
        'mapped_loan_types' : list(mapped_loan_type_details.keys())
    }
        
    return ServiceResponse.success(data=loan_types_data, message="Unmapped Loan Types")


def map_loan_type(mappings):
    loan_type_mappings = []
    for mapping in mappings:
        master_loan_type = mapping.get('master_loan_type')
        loan_type = mapping.get('loan_type')

        loan_type_master = LoanTypeMaster.query.filter_by(loan_type = master_loan_type).first()

        company_id = 1 # hardcoded for now
        created_by = 1 # hardcoded for now

        loan_type_lookup = create_lookup(loan_type)

        loan_type_mapping = LoanTypeMapping(company_id=company_id, created_by=created_by, master_loan_type_id=loan_type_master.id, loan_type=loan_type, loan_type_lookup=loan_type_lookup)
        loan_type_mappings.append(loan_type_mapping)

    db.session.add_all(loan_type_mappings)
    db.session.commit()
    
    return ServiceResponse.success(message="Loan Type mapped successfully")