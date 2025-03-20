from datetime import datetime, timezone
from sqlalchemy import text
import itertools

from models import db, LienTypeMaster, LienTypeMapping
from source.utility.ServiceResponse import ServiceResponse
from source.utility.Util import create_lookup

def get_unmapped_lien_types(fund_name):

    engine = db.get_engine()
    with engine.connect() as connection:
        unmapped_lien_types = connection.execute(text(f'''
            select ssss."[SI] Credit Facility Lien Type", MIN(ssss.source_file_id) AS source_file_id
            from sf_sheet_securities_stats ssss
            left join lien_type_mapping ltm ON ssss."[SI] Credit Facility Lien Type" = ltm.lien_type and is_deleted = false
            left join lien_type_master ltm2 on ltm2.id = ltm.master_lien_type_id and ltm2.fund_type = '{fund_name}'
            join source_files sf on sf.id = ssss.source_file_id and '{fund_name}' in (select unnest(fund_types) from source_files sf2 where sf.id = ssss.source_file_id)
            where (ltm2.fund_type is null or ltm.master_lien_type_id IS NULL OR ltm.is_deleted = TRUE) and ssss."[SI] Credit Facility Lien Type" is not NULL
            group by ssss."[SI] Credit Facility Lien Type"
            order by ssss."[SI] Credit Facility Lien Type"
        ''')).fetchall()
    unmapped_lien_type_data = [{'unmapped_lien_type': unmapped_lien_type[0], 'source_file_id': unmapped_lien_type[1]} for unmapped_lien_type in unmapped_lien_types]
    return ServiceResponse.success(data=unmapped_lien_type_data, message="Unmapped lien Types")

def get_mapped_lien_types(fund_name):
    engine = db.get_engine()
    with engine.connect() as connection:
        mapped_lien_types = connection.execute(text(f'''
            select 
	            ltmapping.master_lien_type_id,
	            ltmaster.lien_type as master_lien_type,
	            ltmapping.lien_type,
                ltmapping.id as mapping_id
            from lien_type_mapping ltmapping join lien_type_master ltmaster on ltmapping.master_lien_type_id = ltmaster.id
            where ltmaster.fund_type = '{fund_name}' and (ltmapping.is_deleted = false or ltmapping.is_deleted is null)
        ''')).fetchall()

    mapped_lien_type_data = [{
        'master_lien_type_id': mapped_lien_type[0],
        'master_lien_type': mapped_lien_type[1],
        'lien_type': mapped_lien_type[2],
        'mapping_id': mapped_lien_type[3]
    } for mapped_lien_type in mapped_lien_types]

    return ServiceResponse.success(data=mapped_lien_type_data, message="Mapped lien Types")

def get_master_lien_types(fund_name):
    engine = db.get_engine()
    with engine.connect() as connection:
        master_lien_types = connection.execute(text(f'''
            select ltmaster.id, ltmaster.lien_type from lien_type_master ltmaster where ltmaster.fund_type = '{fund_name}'
        ''')).fetchall()
    
    master_lien_type_data = [{'master_lien_type_id': master_lien_type[0], 'master_lien_type': master_lien_type[1]} for master_lien_type in master_lien_types]
    
    return ServiceResponse.success(data=master_lien_type_data, message="Master lien Types")

def add_mapping(lien_type_master_id, lien_type):
    try:
        lien_type_master = LienTypeMaster.query.filter_by(id = lien_type_master_id).first()
        company_id = 1 # hardcoded for now
        created_by = 1 # hardcoded for now

        lien_type_lookup = create_lookup(lien_type)

        lien_type_mapping = LienTypeMapping(company_id=company_id, created_by=created_by, master_lien_type_id=lien_type_master.id, lien_type=lien_type, lien_type_lookup=lien_type_lookup)
        return {'success': True, 'message': 'Lien Type mapped successfully', 'data': lien_type_mapping}
    except Exception as e:
        print(str(e))
        return {'success': False, 'message': 'Something went wrong while mapping Lien type', 'data': None}

def edit_mapping(mapping_id, master_lien_type_id):
    try:
        existing_mapping = LienTypeMapping.query.filter_by(id = mapping_id).first()
        existing_mapping.master_lien_type_id = master_lien_type_id
        existing_mapping.modified_by = 1 # for now
        existing_mapping.modified_at = datetime.now(timezone.utc).replace(tzinfo=None)
    
        db.session.commit()
        return {'success': True, 'message': 'Lien Type mapping edited successfully'}
    except Exception as e:
        print(str(e))
        return {'success': False, 'message': 'Something went wrong while editing Lien type mapping', 'data': None}    

def map_lien_type(mappings):
    lien_type_mappings = []
    for mapping in mappings:
        master_lien_type_id = mapping.get('master_lien_type_id')
        lien_type = mapping.get('lien_type')
        mapping_id = mapping.get("mapping_id")

        if mapping_id:
            edit_res = edit_mapping(mapping_id, master_lien_type_id)
            if edit_res['success'] is False:
                return ServiceResponse.error(message=add_res.get('message'))
        else:
            add_res = add_mapping(master_lien_type_id, lien_type)
            if add_res['success'] is False:
                return ServiceResponse.error(message=add_res.get('message'))
            lien_type_mapping = add_res['data']
            lien_type_mappings.append(lien_type_mapping)

    if lien_type_mappings:
        db.session.add_all(lien_type_mappings)
    db.session.commit()
    
    return ServiceResponse.success(message="Lien Type mapped successfully")

    #     lien_type_master = LienTypeMaster.query.filter_by(lien_type = master_lien_type).first()

    #     company_id = 1 # hardcoded for now
    #     created_by = 1 # hardcoded for now

    #     lien_type_lookup = create_lookup(lien_type)

    #     lien_type_mapping = LienTypeMapping(company_id=company_id, created_by=created_by, master_lien_type_id=lien_type_master.id, lien_type=lien_type, lien_type_lookup=lien_type_lookup)
    #     lien_type_mappings.append(lien_type_mapping)

    # db.session.add_all(lien_type_mappings)
    # db.session.commit()
    
    return ServiceResponse.success(message="Lien Type mapped successfully")

def add_lien_type_master(fund_type, master_lien_type, discription):
    company_id = 1
    created_by = 1

    lookup = create_lookup(master_lien_type)

    lien_type_master = LienTypeMaster(company_id=company_id, created_by=created_by, lien_type=master_lien_type, lien_type_lookup=lookup, description=discription, fund_type=fund_type)
    db.session.add(lien_type_master)
    db.session.commit()
 
    return ServiceResponse.success(message="Lien Type added successfully")

def delete_mapping(mapping_id):
    try:
        mapping = LienTypeMapping.query.filter_by(id=mapping_id).first()
        mapping.is_deleted = True
        mapping.deleted_by = 1 # for now
        mapping.deleted_at = datetime.now(timezone.utc).replace(tzinfo=None)
        # mapping.master_loan_type_id = None
        db.session.commit()
        return ServiceResponse.success(message="Lien Type deleted successfully")
    except Exception as e:
        print(str(e))
        return ServiceResponse.error(message="Something went wrong while deleting Lien Type mapping")