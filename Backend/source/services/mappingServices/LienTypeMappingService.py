from sqlalchemy import text
import itertools

from models import db, LienTypeMaster, LienTypeMapping
from source.utility.ServiceResponse import ServiceResponse
from source.utility.Util import create_lookup

def get_lien_type_data():
    engine = db.get_engine()
    with engine.connect() as connection:
        unmapped_lien_types = connection.execute(text('''
            select 
	            distinct  ssss."[SI] Credit Facility Lien Type"
	        from sf_sheet_securities_stats ssss 
	            left join lien_type_master ltm on ssss."[SI] Credit Facility Lien Type" = ltm.lien_type 
            where ltm.lien_type is NULL
        ''')).fetchall()

        mapped_lien_types = connection.execute(text('''
            select 
	            ltmapping.id as mapping_id, 
	            ltmapping.master_lien_type_id as master_lien_type_id, 
	            ltmaster.lien_type as master_lien_type, 
	            ltmapping.lien_type as mapped_lien_type 
            from lien_type_mapping ltmapping 
            join lien_type_master ltmaster on ltmapping.master_lien_type_id = ltmaster.id
        ''')).fetchall()
    
    unmapped_lien_types_list = list(itertools.chain(*unmapped_lien_types))

    mapped_lien_type_details = {}
    for mapped_lien_type_data in mapped_lien_types:
        master_lien_type = mapped_lien_type_data[2]
        mapped_lien_type = mapped_lien_type_data[3]

        if master_lien_type not in mapped_lien_type_details:
            mapped_lien_type_details[master_lien_type] = []

        mapped_lien_type_details[master_lien_type].append(mapped_lien_type)

    lien_types_data = {
        'unmapped_lien_type_data': unmapped_lien_types_list,
        'mapped_lien_type_data': mapped_lien_type_details,
        'mapped_lien_types' : list(mapped_lien_type_details.keys())
    }
        
    return ServiceResponse.success(data=lien_types_data, message="Unmapped Lien Types")

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