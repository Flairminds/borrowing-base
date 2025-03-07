from sqlalchemy import text
import itertools

from models import db, LienTypeMaster, LienTypeMapping
from source.utility.ServiceResponse import ServiceResponse
from source.utility.Util import create_lookup

def get_unmapped_lien_types():

    engine = db.get_engine()
    with engine.connect() as connection:
        unmapped_lien_types = connection.execute(text('''
            select
                distinct ssss."[SI] Credit Facility Lien Type",
                min(ssss.source_file_id)
            from sf_sheet_securities_stats ssss
            left join lien_type_mapping ltmapping on ssss."[SI] Credit Facility Lien Type" = ltmapping.lien_type
            where ltmapping.lien_type is null
            group by ssss."[SI] Credit Facility Lien Type"
        ''')).fetchall()
    unmapped_lien_type_data = [{'unmapped_lien_type': unmapped_lien_type[0], 'source_file_id': unmapped_lien_type[1]} for unmapped_lien_type in unmapped_lien_types]
    return ServiceResponse.success(data=unmapped_lien_type_data, message="Unmapped lien Types")

def get_mapped_lien_types():
    engine = db.get_engine()
    with engine.connect() as connection:
        mapped_lien_types = connection.execute(text('''
            select 
	            ltmapping.master_lien_type_id,
	            ltmaster.lien_type as master_lien_type,
	            ltmapping.lien_type
            from lien_type_mapping ltmapping join lien_type_master ltmaster on ltmapping.master_lien_type_id = ltmaster.id
        ''')).fetchall()

    mapped_lien_type_data = [{
        'master_lien_type_id': mapped_lien_type[0],
        'master_lien_type': mapped_lien_type[1],
        'lien_type': mapped_lien_type[2]
    } for mapped_lien_type in mapped_lien_types]

    return ServiceResponse.success(data=mapped_lien_type_data, message="Mapped lien Types")

def get_master_lien_types():
    engine = db.get_engine()
    with engine.connect() as connection:
        master_lien_types = connection.execute(text('''
            select ltmaster.id, ltmaster.lien_type from lien_type_master ltmaster
        ''')).fetchall()
    
    master_lien_type_data = [{'master_lien_type_id': master_lien_type[0], 'master_lien_type': master_lien_type[1]} for master_lien_type in master_lien_types]
    
    return ServiceResponse.success(data=master_lien_type_data, message="Master lien Types")


def map_lien_type(mappings):
    lien_type_mappings = []
    for mapping in mappings:
        master_lien_type = mapping.get('master_lien_type')
        lien_type = mapping.get('lien_type')

        lien_type_master = LienTypeMaster.query.filter_by(lien_type = master_lien_type).first()

        company_id = 1 # hardcoded for now
        created_by = 1 # hardcoded for now

        lien_type_lookup = create_lookup(lien_type)

        lien_type_mapping = LienTypeMapping(company_id=company_id, created_by=created_by, master_lien_type_id=lien_type_master.id, lien_type=lien_type, lien_type_lookup=lien_type_lookup)
        lien_type_mappings.append(lien_type_mapping)

    db.session.add_all(lien_type_mappings)
    db.session.commit()
    
    return ServiceResponse.success(message="Lien Type mapped successfully")