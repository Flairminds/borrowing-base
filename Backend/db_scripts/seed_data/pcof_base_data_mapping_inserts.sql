INSERT INTO public.base_data_mapping
(bdm_id, fund_type, company_id, bd_sheet_name, bd_column_name, bd_column_lookup, bd_column_datatype, bd_column_is_required, bd_column_unit, sf_file_type, sf_sheet_name, sf_column_name, sf_column_lookup, sf_column_datatype, sf_column_categories, sd_ref_table_name, formula, description, "comments", created_by, created_at, modified_by, modified_at, is_editable)
VALUES(nextval('base_data_mapping_bdm_id_seq'::regclass), 'PCOF', 1, 'PL BB Build', 'Investment Name', 'Investment Name', 'String', false, NULL, 'master_comp', 'PCOF IV', 'Asset', NULL, NULL, NULL, 'pcof_pcof_iv', NULL, NULL, NULL, 1, now(), NULL, NULL, false);


INSERT INTO public.base_data_mapping
(bdm_id, fund_type, company_id, bd_sheet_name, bd_column_name, bd_column_lookup, bd_column_datatype, bd_column_is_required, bd_column_unit, sf_file_type, sf_sheet_name, sf_column_name, sf_column_lookup, sf_column_datatype, sf_column_categories, sd_ref_table_name, formula, description, "comments", created_by, created_at, modified_by, modified_at, is_editable)
VALUES(nextval('base_data_mapping_bdm_id_seq'::regclass), 'PCOF', 1, 'PL BB Build', 'Issuer', 'Issuer', 'String', false, NULL, 'master_comp', 'PCOF IV', 'MC Name', NULL, NULL, NULL, 'pcof_pcof_iv', NULL, NULL, NULL, 1, now(), NULL, NULL, false);

INSERT INTO public.base_data_mapping
(bdm_id, fund_type, company_id, bd_sheet_name, bd_column_name, bd_column_lookup, bd_column_datatype, bd_column_is_required, bd_column_unit, sf_file_type, sf_sheet_name, sf_column_name, sf_column_lookup, sf_column_datatype, sf_column_categories, sd_ref_table_name, formula, description, "comments", created_by, created_at, modified_by, modified_at, is_editable)
VALUES(nextval('base_data_mapping_bdm_id_seq'::regclass), 'PCOF', 1, 'PL BB Build', 'Leverage LTV Thru PCOF IV', 'Leverage LTV Thru PCOF IV', 'String', false, NULL, 'master_comp', 'PCOF IV', 'LTV', NULL, NULL, NULL, 'pcof_pcof_iv', NULL, NULL, NULL, 1, now(), NULL, NULL, false);

INSERT INTO public.base_data_mapping
(bdm_id, fund_type, company_id, bd_sheet_name, bd_column_name, bd_column_lookup, bd_column_datatype, bd_column_is_required, bd_column_unit, sf_file_type, sf_sheet_name, sf_column_name, sf_column_lookup, sf_column_datatype, sf_column_categories, sd_ref_table_name, formula, description, "comments", created_by, created_at, modified_by, modified_at, is_editable)
VALUES(nextval('base_data_mapping_bdm_id_seq'::regclass), 'PCOF', 1, 'PL BB Build', 'Classifications Quoted / Unquoted', 'Classifications Quoted / Unquoted', 'String', NULL, NULL, 'master_comp', 'PCOF III Borrrowing Base', 'Quoted / Unquoted', NULL, NULL, NULL, 'pcof_pcof_iii_borrrowing_base', NULL, NULL, NULL, 1, now(), NULL, NULL, false);

INSERT INTO public.base_data_mapping
(bdm_id, fund_type, company_id, bd_sheet_name, bd_column_name, bd_column_lookup, bd_column_datatype, bd_column_is_required, bd_column_unit, sf_file_type, sf_sheet_name, sf_column_name, sf_column_lookup, sf_column_datatype, sf_column_categories, sd_ref_table_name, formula, description, "comments", created_by, created_at, modified_by, modified_at, is_editable)
VALUES(nextval('base_data_mapping_bdm_id_seq'::regclass), 'PCOF', 1, 'PL BB Build', 'Classifications Warehouse Asset', 'Classifications Warehouse Asset', 'String', NULL, NULL, 'master_comp', 'PCOF III Borrrowing Base', 'Warehouse Yes / No', NULL, NULL, NULL, 'pcof_pcof_iii_borrrowing_base', NULL, NULL, NULL, 1, now(), NULL, NULL, false);

INSERT INTO public.base_data_mapping
(bdm_id, fund_type, company_id, bd_sheet_name, bd_column_name, bd_column_lookup, bd_column_datatype, bd_column_is_required, bd_column_unit, sf_file_type, sf_sheet_name, sf_column_name, sf_column_lookup, sf_column_datatype, sf_column_categories, sd_ref_table_name, formula, description, "comments", created_by, created_at, modified_by, modified_at, is_editable)
VALUES(nextval('base_data_mapping_bdm_id_seq'::regclass), 'PCOF', 1, 'PL BB Build', 'Classifications Warehouse Asset Expected Rating', 'Classifications Warehouse Asset Expected Rating', 'String', NULL, NULL, 'master_comp', 'PCOF III Borrrowing Base', 'Warehouse - Credit Rating', NULL, NULL, NULL, 'pcof_pcof_iii_borrrowing_base', NULL, NULL, NULL, 1, now(), NULL, NULL, false);

INSERT INTO public.base_data_mapping
(bdm_id, fund_type, company_id, bd_sheet_name, bd_column_name, bd_column_lookup, bd_column_datatype, bd_column_is_required, bd_column_unit, sf_file_type, sf_sheet_name, sf_column_name, sf_column_lookup, sf_column_datatype, sf_column_categories, sd_ref_table_name, formula, description, "comments", created_by, created_at, modified_by, modified_at, is_editable)
VALUES(nextval('base_data_mapping_bdm_id_seq'::regclass), 'PCOF', 1, 'PL BB Build', 'Classifications Approved Foreign Jurisdiction', 'Classifications Approved Foreign Jurisdiction', 'String', NULL, NULL, 'master_comp', 'PCOF III Borrrowing Base', 'Approved Foreign Jurisdiction', NULL, NULL, NULL, 'pcof_pcof_iii_borrrowing_base', NULL, NULL, NULL, 1, now(), NULL, NULL, false);

INSERT INTO public.base_data_mapping
(bdm_id, fund_type, company_id, bd_sheet_name, bd_column_name, bd_column_lookup, bd_column_datatype, bd_column_is_required, bd_column_unit, sf_file_type, sf_sheet_name, sf_column_name, sf_column_lookup, sf_column_datatype, sf_column_categories, sd_ref_table_name, formula, description, "comments", created_by, created_at, modified_by, modified_at, is_editable)
VALUES(nextval('base_data_mapping_bdm_id_seq'::regclass), 'PCOF', 1, 'PL BB Build', 'Classifications LTV Transaction', 'Classifications LTV Transaction', 'String', NULL, NULL, 'master_comp', 'PCOF III Borrrowing Base', 'LTV Transaction', NULL, NULL, NULL, 'pcof_pcof_iii_borrrowing_base', NULL, NULL, NULL, 1, now(), NULL, NULL, false);

INSERT INTO public.base_data_mapping
(bdm_id, fund_type, company_id, bd_sheet_name, bd_column_name, bd_column_lookup, bd_column_datatype, bd_column_is_required, bd_column_unit, sf_file_type, sf_sheet_name, sf_column_name, sf_column_lookup, sf_column_datatype, sf_column_categories, sd_ref_table_name, formula, description, "comments", created_by, created_at, modified_by, modified_at, is_editable)
VALUES(nextval('base_data_mapping_bdm_id_seq'::regclass), 'PCOF', 1, 'PL BB Build', 'Classifications Noteless Assigned Loan', 'Classifications Noteless Assigned Loan', 'String', NULL, NULL, 'master_comp', 'PCOF III Borrrowing Base', 'Noteless Assigned Loan', NULL, NULL, NULL, 'pcof_pcof_iii_borrrowing_base', NULL, NULL, NULL, 1, now(), NULL, NULL, false);

INSERT INTO public.base_data_mapping
(bdm_id, fund_type, company_id, bd_sheet_name, bd_column_name, bd_column_lookup, bd_column_datatype, bd_column_is_required, bd_column_unit, sf_file_type, sf_sheet_name, sf_column_name, sf_column_lookup, sf_column_datatype, sf_column_categories, sd_ref_table_name, formula, description, "comments", created_by, created_at, modified_by, modified_at, is_editable)
VALUES(nextval('base_data_mapping_bdm_id_seq'::regclass), 'PCOF', 1, 'PL BB Build', 'Classifications Undelivered Note', 'Classifications Undelivered Note', 'String', NULL, NULL, 'master_comp', 'PCOF III Borrrowing Base', 'Undelivered Note', NULL, NULL, NULL, 'pcof_pcof_iii_borrrowing_base', NULL, NULL, NULL, 1, now(), NULL, NULL, false);

INSERT INTO public.base_data_mapping
(bdm_id, fund_type, company_id, bd_sheet_name, bd_column_name, bd_column_lookup, bd_column_datatype, bd_column_is_required, bd_column_unit, sf_file_type, sf_sheet_name, sf_column_name, sf_column_lookup, sf_column_datatype, sf_column_categories, sd_ref_table_name, formula, description, "comments", created_by, created_at, modified_by, modified_at, is_editable)
VALUES(nextval('base_data_mapping_bdm_id_seq'::regclass), 'PCOF', 1, 'PL BB Build', 'Classifications Structured Finance Obligation', 'Classifications Structured Finance Obligation', 'String', NULL, NULL, 'master_comp', 'PCOF III Borrrowing Base', 'Structured Finance Obligation', NULL, NULL, NULL, 'pcof_pcof_iii_borrrowing_base', NULL, NULL, NULL, 1, now(), NULL, NULL, false);

INSERT INTO public.base_data_mapping
(bdm_id, fund_type, company_id, bd_sheet_name, bd_column_name, bd_column_lookup, bd_column_datatype, bd_column_is_required, bd_column_unit, sf_file_type, sf_sheet_name, sf_column_name, sf_column_lookup, sf_column_datatype, sf_column_categories, sd_ref_table_name, formula, description, "comments", created_by, created_at, modified_by, modified_at, is_editable)
VALUES(nextval('base_data_mapping_bdm_id_seq'::regclass), 'PCOF', 1, 'PL BB Build', 'Classifications Third Party Finance Company', 'Classifications Third Party Finance Company', 'String', NULL, NULL, 'master_comp', 'PCOF III Borrrowing Base', 'Third Party Finance Company', NULL, NULL, NULL, 'pcof_pcof_iii_borrrowing_base', NULL, NULL, NULL, 1, now(), NULL, NULL, false);

INSERT INTO public.base_data_mapping
(bdm_id, fund_type, company_id, bd_sheet_name, bd_column_name, bd_column_lookup, bd_column_datatype, bd_column_is_required, bd_column_unit, sf_file_type, sf_sheet_name, sf_column_name, sf_column_lookup, sf_column_datatype, sf_column_categories, sd_ref_table_name, formula, description, "comments", created_by, created_at, modified_by, modified_at, is_editable)
VALUES(nextval('base_data_mapping_bdm_id_seq'::regclass), 'PCOF', 1, 'PL BB Build', 'Classifications Affiliate Investment', 'Classifications Affiliate Investment', 'String', NULL, NULL, 'master_comp', 'PCOF III Borrrowing Base', 'Affiliate Investment', NULL, NULL, NULL, 'pcof_pcof_iii_borrrowing_base', NULL, NULL, NULL, 1, now(), NULL, NULL, false);

INSERT INTO public.base_data_mapping
(bdm_id, fund_type, company_id, bd_sheet_name, bd_column_name, bd_column_lookup, bd_column_datatype, bd_column_is_required, bd_column_unit, sf_file_type, sf_sheet_name, sf_column_name, sf_column_lookup, sf_column_datatype, sf_column_categories, sd_ref_table_name, formula, description, "comments", created_by, created_at, modified_by, modified_at, is_editable)
VALUES(nextval('base_data_mapping_bdm_id_seq'::regclass), 'PCOF', 1, 'PL BB Build', 'Classifications Defaulted / Restructured', 'Classifications Defaulted / Restructured', 'String', NULL, NULL, 'master_comp', 'PCOF III Borrrowing Base', 'Defaulted / Restructured', NULL, NULL, NULL, 'pcof_pcof_iii_borrrowing_base', NULL, NULL, NULL, 1, now(), NULL, NULL, false);

INSERT INTO public.base_data_mapping
(bdm_id, fund_type, company_id, bd_sheet_name, bd_column_name, bd_column_lookup, bd_column_datatype, bd_column_is_required, bd_column_unit, sf_file_type, sf_sheet_name, sf_column_name, sf_column_lookup, sf_column_datatype, sf_column_categories, sd_ref_table_name, formula, description, "comments", created_by, created_at, modified_by, modified_at, is_editable)
VALUES(nextval('base_data_mapping_bdm_id_seq'::regclass), 'PCOF', 1, 'PL BB Build', 'Leverage Total Capitalization', 'Leverage Total Capitalization', 'String', NULL, NULL, 'master_comp', 'PCOF III Borrrowing Base', 'TotalCapitalization', NULL, NULL, NULL, 'pcof_pcof_iii_borrrowing_base', NULL, NULL, NULL, 1, now(), NULL, NULL, false);