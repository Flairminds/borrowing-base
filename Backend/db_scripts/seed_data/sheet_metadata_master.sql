INSERT INTO public.sheet_metadata_master
(file_id, fund_id, company_id, "name", lookup, aliases, data_format, description, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_mandatory, is_required, created_by, modified_by, modified_at)
VALUES(SELECT id FROM file_metadata_master WHERE lookup = 'master_comp', 2, 1, 'PFLT Borrowing Base', 'pflt_borrowing_base', '{}', 'tabular', 'Sheet for PFLT Borrowing Base', 3, true, false, false, false, true, true, 1, NULL, NULL);
INSERT INTO public.sheet_metadata_master
(file_id, fund_id, company_id, "name", lookup, aliases, data_format, description, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_mandatory, is_required, created_by, modified_by, modified_at)
VALUES(SELECT id FROM file_metadata_master WHERE lookup = 'master_comp', 1, 1, 'Securities Stats', 'securities_stats', '{}', 'tabular', 'Sheet for Security Stats', 2, true, false, false, false, true, true, 1, NULL, NULL);
INSERT INTO public.sheet_metadata_master
(file_id, fund_id, company_id, "name", lookup, aliases, data_format, description, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_mandatory, is_required, created_by, modified_by, modified_at)
VALUES(SELECT id FROM file_metadata_master WHERE lookup = 'master_comp', 1, 1, 'PCOF III Borrrowing Base', 'pcof_iii_borrrowing_base', '{}', 'tabular', 'Sheet for PCOF III Borrrowing Base', 5, true, false, false, false, true, true, 1, NULL, NULL);
INSERT INTO public.sheet_metadata_master
(file_id, fund_id, company_id, "name", lookup, aliases, data_format, description, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_mandatory, is_required, created_by, modified_by, modified_at)
VALUES(SELECT id FROM file_metadata_master WHERE lookup = 'master_comp', 2, 1, 'SOI Mapping', 'soi_mapping', '{}', 'tabular', 'Sheet for SOI Mapping', 4, true, false, false, false, true, true, 1, NULL, NULL);
INSERT INTO public.sheet_metadata_master
(file_id, fund_id, company_id, "name", lookup, aliases, data_format, description, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_mandatory, is_required, created_by, modified_by, modified_at)
VALUES(SELECT id FROM file_metadata_master WHERE lookup = 'master_comp'1, 1, 1, 'Borrower Stats', 'borrower_stats', '{borrower,stat}', 'tabular', 'Sheet for borrower statistics', 1, true, false, false, false, true, true, 1, NULL, NULL);
