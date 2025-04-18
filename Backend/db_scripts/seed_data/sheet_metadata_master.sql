INSERT INTO public.sheet_metadata_master
(file_id, fund_id, company_id, "name", lookup, aliases, data_format, description, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_mandatory, is_required, created_by, modified_by, modified_at)
VALUES((SELECT id FROM file_metadata_master WHERE lookup = 'master_comp'), 2, 1, 'PFLT Borrowing Base', 'pflt_borrowing_base', '{}', 'tabular', 'Sheet for PFLT Borrowing Base', 3, true, false, false, false, true, true, 1, NULL, NULL);
INSERT INTO public.sheet_metadata_master
(file_id, fund_id, company_id, "name", lookup, aliases, data_format, description, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_mandatory, is_required, created_by, modified_by, modified_at)
VALUES((SELECT id FROM file_metadata_master WHERE lookup = 'master_comp'), 1, 1, 'Securities Stats', 'securities_stats', '{}', 'tabular', 'Sheet for Security Stats', 2, true, false, false, false, true, true, 1, NULL, NULL);
INSERT INTO public.sheet_metadata_master
(file_id, fund_id, company_id, "name", lookup, aliases, data_format, description, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_mandatory, is_required, created_by, modified_by, modified_at)
VALUES((SELECT id FROM file_metadata_master WHERE lookup = 'master_comp'), 1, 1, 'PCOF III Borrrowing Base', 'pcof_iii_borrrowing_base', '{}', 'tabular', 'Sheet for PCOF III Borrrowing Base', 5, true, false, false, false, true, true, 1, NULL, NULL);
INSERT INTO public.sheet_metadata_master
(file_id, fund_id, company_id, "name", lookup, aliases, data_format, description, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_mandatory, is_required, created_by, modified_by, modified_at)
VALUES((SELECT id FROM file_metadata_master WHERE lookup = 'master_comp'), 2, 1, 'SOI Mapping', 'soi_mapping', '{}', 'tabular', 'Sheet for SOI Mapping', 4, true, false, false, false, true, true, 1, NULL, NULL);
INSERT INTO public.sheet_metadata_master
(file_id, fund_id, company_id, "name", lookup, aliases, data_format, description, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_mandatory, is_required, created_by, modified_by, modified_at)
VALUES((SELECT id FROM file_metadata_master WHERE lookup = 'master_comp'),1, 1, 'Borrower Stats', 'borrower_stats', '{borrower,stat}', 'tabular', 'Sheet for borrower statistics', 1, true, false, false, false, true, true, 1, NULL, NULL);


	
insert into sheet_metadata_master (
	fund_id, company_id, name, lookup, data_format , description ,"sequence" , is_raw_data_input , is_mandatory , is_required, created_by ,
	file_id 
) values 
	( 2, 1, 'US Bank Holdings', 'us_bank_holdings', 'tabular', 'Sheet for US Bank Holdings', 1, true, true, true, 1, (select id from file_metadata_master where lookup = 'cash_file') ),
	( 2, 1, 'Client Holdings', 'client_holdings', 'tabular', 'Sheet for Client Holdings', 2, true, true, true, 1, (select id from file_metadata_master where lookup = 'cash_file'));


-- Validation For Add Other Info
-- PFLT
INSERT INTO sheet_metadata_master (
	fund_id, company_id, name, lookup, data_format , description ,"sequence" , is_raw_data_input , is_mandatory , is_required, created_by ,
	file_id 
) VALUES 
	( 2, 1, 'Input', 'input', 'key_value', 'Sheet for Add Other Info - Input', 1, true, true, true, 1, (select id from file_metadata_master where lookup = 'other_info') ),
	( 2, 1, 'Other Sheet', 'other_sheet', 'tabular', 'Sheet for Add Other Info - Other Sheet', 2, true, true, true, 1, (select id from file_metadata_master where lookup = 'other_info'));

-- PCOF
INSERT INTO sheet_metadata_master (
	fund_id, company_id, name, lookup, data_format , description ,"sequence" , is_raw_data_input , is_mandatory , is_required, created_by ,
	file_id 
) VALUES 
	( 1, 1, 'Availability Borrower', 'availability_borrower', 'key_value', 'Sheet for Add Other Info - Availability Borrower', 1, true, true, true, 1, (select id from file_metadata_master where lookup = 'other_info') ),
	( 1, 1, 'Principle Obligations', 'principle_obligations', 'tabular', 'Sheet for Add Other Info - Principle Obligations', 2, true, true, true, 1, (select id from file_metadata_master where lookup = 'other_info')),
	( 1, 1, 'Subscription Bb', 'subscription_bb', 'tabular', 'Sheet for Add Other Info - Subscription Bb', 3, true, true, true, 1, (select id from file_metadata_master where lookup = 'other_info')),
	( 1, 1, 'Pricing', 'pricing', 'tabular', 'Sheet for Add Other Info - Pricing', 4, true, true, true, 1, (select id from file_metadata_master where lookup = 'other_info')),
	( 1, 1, 'Portfolio Leverageborrowingbase', 'portfolio_leverageborrowingbase', 'tabular', 'Sheet for Add Other Info - Portfolio Leverageborrowingbase', 5, true, true, true, 1, (select id from file_metadata_master where lookup = 'other_info')),
	( 1, 1, 'Advance Rates', 'advance_rates', 'tabular', 'Sheet for Add Other Info - Advance Rates', 6, true, true, true, 1, (select id from file_metadata_master where lookup = 'other_info')),
	( 1, 1, 'Concentration Limits', 'concentration_limits', 'tabular', 'Sheet for Add Other Info - Concentration Limits', 7, true, true, true, 1, (select id from file_metadata_master where lookup = 'other_info')),
	( 1, 1, 'Other Metrics', 'other_metrics', 'key_value', 'Sheet for Add Other Info - Other Metrics', 8, true, true, true, 1, (select id from file_metadata_master where lookup = 'other_info'));
	