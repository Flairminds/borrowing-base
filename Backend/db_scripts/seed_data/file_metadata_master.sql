INSERT INTO public.file_metadata_master
(id, company_id, created_at, created_by, modified_by, modified_at, fund_ids, "name", lookup, "type", description, is_input, is_output)
VALUES(1, 1, now(), 1, NULL, NULL, '{1,2}', 'MasterComp.xlsx', 'master_comp', 'master_comp', 'Master data for company', true, false);