from sqlalchemy import text
import itertools

from models import db, LoanTypeMaster, LoanTypeMapping
from source.utility.ServiceResponse import ServiceResponse
from source.utility.Util import create_lookup

def get_unmapped_loan_types(fund_name):

    engine = db.get_engine()
    with engine.connect() as connection:
        unmapped_loan_types = connection.execute(text(f'''
            select 
                ssch."Issue Name",
                min(ssch.source_file_id)
            from loan_type_master ltmaster,
            sf_sheet_client_holdings ssch
            left join loan_type_mapping ltm on ssch."Issue Name" = ltm.loan_type
            where ltm.master_loan_type_id is null and ltmaster.fund_type = '{fund_name}'
            group by ssch."Issue Name"
        ''')).fetchall()
    unmapped_loan_type_data = [{'unmapped_loan_type': unmapped_loan_type[0], 'source_file_id': unmapped_loan_type[1]} for unmapped_loan_type in unmapped_loan_types]
    return ServiceResponse.success(data=unmapped_loan_type_data, message="Unmapped Loan Types")

def get_mapped_loan_types(fund_name):
    engine = db.get_engine()
    with engine.connect() as connection:
        mapped_loan_types = connection.execute(text(f'''
            select 
                ltmapping.master_loan_type_id,
                ltmaster.loan_type as master_loan_type,
                ltmapping.loan_type
            from loan_type_mapping ltmapping join loan_type_master ltmaster on ltmapping.master_loan_type_id = ltmaster.id 
            where ltmaster.fund_type = '{fund_name}'
        ''')).fetchall()

    mapped_loan_type_data = [{
        'master_loan_type_id': mapped_loan_type[0],
        'master_loan_type': mapped_loan_type[1],
        'loan_type': mapped_loan_type[2]
    } for mapped_loan_type in mapped_loan_types]

    return ServiceResponse.success(data=mapped_loan_type_data, message="Mapped Loan Types")

def get_master_loan_types(fund_name):
    engine = db.get_engine()
    with engine.connect() as connection:
        master_loan_types = connection.execute(text(f'''
            select ltmaster.id, ltmaster.loan_type from loan_type_master ltmaster where ltmaster.fund_type = '{fund_name}'
        ''')).fetchall()
    
    master_loan_type_data = [{'master_loan_type_id': master_loan_type[0], 'master_loan_type': master_loan_type[1]} for master_loan_type in master_loan_types]
    
    return ServiceResponse.success(data=master_loan_type_data, message="Master Loan Types")

def map_loan_type(mappings):
    loan_type_mappings = []
    for mapping in mappings:
        master_loan_type_id = mapping.get('master_loan_type_id')
        loan_type = mapping.get('loan_type')

        loan_type_master = LoanTypeMaster.query.filter_by(id = master_loan_type_id).first()

        company_id = 1 # hardcoded for now
        created_by = 1 # hardcoded for now

        loan_type_lookup = create_lookup(loan_type)

        loan_type_mapping = LoanTypeMapping(company_id=company_id, created_by=created_by, master_loan_type_id=loan_type_master.id, loan_type=loan_type, loan_type_lookup=loan_type_lookup)
        loan_type_mappings.append(loan_type_mapping)

    db.session.add_all(loan_type_mappings)
    db.session.commit()
    
    return ServiceResponse.success(message="Loan Type mapped successfully")

def add_loan_type_master(fund_type, master_loan_type, discription):
    company_id = 1
    created_by = 1

    lookup = create_lookup(master_loan_type)

    loan_type_master = LoanTypeMaster(company_id=company_id, created_by=created_by, loan_type=master_loan_type, loan_type_lookup=lookup, description=discription, fund_type=fund_type)
    db.session.add(loan_type_master)
    db.session.commit()
 
    return ServiceResponse.success(message="Loan Type added successfully")