from azure.core.exceptions import ResourceExistsError
import os
import mmap
from io import BytesIO

from source.app_configs import azureConfig
from source.utility.ServiceResponse import ServiceResponse
from source.utility.Log import Log
from models import SourceFiles, db

def upload_src_file_to_az_storage(files):
    blob_service_client, blob_client = azureConfig.get_az_service_blob_client()
    company_name = "Penennt"
    fund_name = "PFLT"

    source_files = []
    try:
        for file in files:
            print(file.filename)
            blob_name = f"{company_name}/{fund_name}/{file.filename}"
            
            # setting SourceFiles object
            file_name = os.path.splitext(file.filename)[0]
            extension = os.path.splitext(file.filename)[1]
            file_url = "file_url"
            file.seek(0, 2)  # Move to the end of the file
            file_size = file.tell()  # Get the size in bytes
            file.seek(0)
            print(file_size)
            company_id = 1
            is_validated = False
            is_extracted = False
            uploaded_by = 1

            blob_client.upload_blob(name=blob_name, data=file)
            source_file = SourceFiles(file_name=file_name, extension=extension, file_url=file_url, file_size=file_size, company_id=company_id, fund_type=fund_name, is_validated=is_validated, is_extracted=is_extracted, uploaded_by=uploaded_by)

            db.session.add(source_file)
            db.session.commit()
                # source_files.append(source_file)
            # try:
            #     db.session.add_all(source_files)
            #     db.session.commit()
            # except Exception as e:
            #     Log.func_error(e=e)
            #     return ServiceResponse.error(message="Could not save files to database.", status_code = 500)
            
        return ServiceResponse.success(message = "Files uploaded successfully")

    except ResourceExistsError as ree:
        Log.func_error(e=ree)
        return ServiceResponse.error(message="Files with same name already exist.", status_code=409)
    except Exception as e:
        Log.func_error(e=e)
        return ServiceResponse.error(message="Could not upload files.", status_code = 500)
    
def get_files_list():
    company_id = 1 # for Penennt
    fund_type = "PFLT"
    source_files = SourceFiles.query.filter_by(is_deleted=False, company_id=company_id, fund_type=fund_type).order_by(SourceFiles.uploaded_at.desc()).all()
    list_table = {
        "columns": [{
            "key": "file_name", 
            "label": "File Name",
        }, {
            "key": "uploaded_at", 
            "label": "Uploaded at",
        }, {
            "key": "fund", 
            "label": "Fund",
        }], 
        "data": []
    }

    for source_file in source_files:
        list_table["data"].append({
            "file_id": source_file.id,
            "file_name": source_file.file_name + source_file.extension, 
            "uploaded_at": source_file.uploaded_at.strftime("%Y-%m-%d"), 
            "fund": source_file.fund_type
        })
    
    return ServiceResponse.success(data=list_table)
        