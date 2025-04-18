INSERT INTO public.file_metadata_master
(id, company_id, created_at, created_by, modified_by, modified_at, fund_ids, "name", lookup, "type", description, is_input, is_output)
VALUES(1, 1, now(), 1, NULL, NULL, '{1,2}', 'MasterComp.xlsx', 'master_comp', 'master_comp', 'Master data for company', true, false);


insert into file_metadata_master (
	company_id , created_by, fund_ids , "name" , lookup , "type" , description, is_input 
) values 
	(1, 1, '{1,2}', 'CashFile.xlsx', 'cash_file', 'cashfile', 'cash_file_data', true)

INSERT INTO file_metadata_master (
	company_id , created_by, fund_ids , "name" , lookup , "type" , description, is_input 
) VALUES 
	(1, 1, '{1, 2}', 'OtherInfo.xlsx', 'other_info', 'otherinfo', 'add_other_info', true);