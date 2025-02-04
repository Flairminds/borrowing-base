INSERT INTO public.base_data_mapping
(bdm_id, fund_type, company_id, bd_sheet_name, bd_column_name, bd_column_lookup, bd_column_datatype, bd_column_is_required, bd_column_unit, sf_file_type, sf_sheet_name, sf_column_name, sf_column_lookup, sf_column_datatype, sf_column_categories, sd_ref_table_name, formula, description, "comments", created_by, created_at, modified_by, modified_at, is_editable)
VALUES(nextval('base_data_mapping_bdm_id_seq'::regclass), 'PCOF', 1, 'PL BB Build', 'Investment Name', 'investment_name', 'String', false, NULL, 'master_comp', 'PCOF IV', 'Asset', NULL, NULL, NULL, 'sf_sheet_pcof_iv', NULL, NULL, NULL, 1, now(), NULL, NULL, false);


INSERT INTO public.base_data_mapping
(bdm_id, fund_type, company_id, bd_sheet_name, bd_column_name, bd_column_lookup, bd_column_datatype, bd_column_is_required, bd_column_unit, sf_file_type, sf_sheet_name, sf_column_name, sf_column_lookup, sf_column_datatype, sf_column_categories, sd_ref_table_name, formula, description, "comments", created_by, created_at, modified_by, modified_at, is_editable)
VALUES(nextval('base_data_mapping_bdm_id_seq'::regclass), 'PCOF', 1, 'PL BB Build', 'Issuer', 'issuer', 'String', false, NULL, 'master_comp', 'PCOF IV', 'MC Name', NULL, NULL, NULL, 'sf_sheet_pcof_iv', NULL, NULL, NULL, 1, now(), NULL, NULL, false);

INSERT INTO public.base_data_mapping
(bdm_id, fund_type, company_id, bd_sheet_name, bd_column_name, bd_column_lookup, bd_column_datatype, bd_column_is_required, bd_column_unit, sf_file_type, sf_sheet_name, sf_column_name, sf_column_lookup, sf_column_datatype, sf_column_categories, sd_ref_table_name, formula, description, "comments", created_by, created_at, modified_by, modified_at, is_editable)
VALUES(nextval('base_data_mapping_bdm_id_seq'::regclass), 'PCOF', 1, 'PL BB Build', 'Leverage LTV Thru PCOF IV', 'leverage_ltv_thru_pcof_iv', 'String', false, NULL, 'master_comp', 'PCOF IV', 'LTV', NULL, NULL, NULL, 'sf_sheet_pcof_iv', NULL, NULL, NULL, 1, now(), NULL, NULL, false);

INSERT INTO public.base_data_mapping
(bdm_id, fund_type, company_id, bd_sheet_name, bd_column_name, bd_column_lookup, bd_column_datatype, bd_column_is_required, bd_column_unit, sf_file_type, sf_sheet_name, sf_column_name, sf_column_lookup, sf_column_datatype, sf_column_categories, sd_ref_table_name, formula, description, "comments", created_by, created_at, modified_by, modified_at, is_editable)
VALUES(nextval('base_data_mapping_bdm_id_seq'::regclass), 'PCOF', 1, 'PL BB Build', 'Classifications Quoted / Unquoted', 'classifications_quoted_unquoted', 'String', NULL, NULL, 'master_comp', 'PCOF III Borrrowing Base', 'Quoted / Unquoted', NULL, NULL, NULL, 'sf_sheet_pcof_iii_borrrowing_base', NULL, NULL, NULL, 1, now(), NULL, NULL, false);

INSERT INTO public.base_data_mapping
(bdm_id, fund_type, company_id, bd_sheet_name, bd_column_name, bd_column_lookup, bd_column_datatype, bd_column_is_required, bd_column_unit, sf_file_type, sf_sheet_name, sf_column_name, sf_column_lookup, sf_column_datatype, sf_column_categories, sd_ref_table_name, formula, description, "comments", created_by, created_at, modified_by, modified_at, is_editable)
VALUES(nextval('base_data_mapping_bdm_id_seq'::regclass), 'PCOF', 1, 'PL BB Build', 'Classifications Warehouse Asset', 'classifications_warehouse_asset', 'String', NULL, NULL, 'master_comp', 'PCOF III Borrrowing Base', 'Warehouse Yes / No', NULL, NULL, NULL, 'sf_sheet_pcof_iii_borrrowing_base', NULL, NULL, NULL, 1, now(), NULL, NULL, false);

INSERT INTO public.base_data_mapping
(bdm_id, fund_type, company_id, bd_sheet_name, bd_column_name, bd_column_lookup, bd_column_datatype, bd_column_is_required, bd_column_unit, sf_file_type, sf_sheet_name, sf_column_name, sf_column_lookup, sf_column_datatype, sf_column_categories, sd_ref_table_name, formula, description, "comments", created_by, created_at, modified_by, modified_at, is_editable)
VALUES(nextval('base_data_mapping_bdm_id_seq'::regclass), 'PCOF', 1, 'PL BB Build', 'Classifications Warehouse Asset Expected Rating', 'classifications_warehouse_asset_expected_rating', 'String', NULL, NULL, 'master_comp', 'PCOF III Borrrowing Base', 'Warehouse - Credit Rating', NULL, NULL, NULL, 'sf_sheet_pcof_iii_borrrowing_base', NULL, NULL, NULL, 1, now(), NULL, NULL, false);

INSERT INTO public.base_data_mapping
(bdm_id, fund_type, company_id, bd_sheet_name, bd_column_name, bd_column_lookup, bd_column_datatype, bd_column_is_required, bd_column_unit, sf_file_type, sf_sheet_name, sf_column_name, sf_column_lookup, sf_column_datatype, sf_column_categories, sd_ref_table_name, formula, description, "comments", created_by, created_at, modified_by, modified_at, is_editable)
VALUES(nextval('base_data_mapping_bdm_id_seq'::regclass), 'PCOF', 1, 'PL BB Build', 'Classifications Approved Foreign Jurisdiction', 'classifications_approved_foreign_jurisdiction', 'String', NULL, NULL, 'master_comp', 'PCOF III Borrrowing Base', 'Approved Foreign Jurisdiction', NULL, NULL, NULL, 'sf_sheet_pcof_iii_borrrowing_base', NULL, NULL, NULL, 1, now(), NULL, NULL, false);

INSERT INTO public.base_data_mapping
(bdm_id, fund_type, company_id, bd_sheet_name, bd_column_name, bd_column_lookup, bd_column_datatype, bd_column_is_required, bd_column_unit, sf_file_type, sf_sheet_name, sf_column_name, sf_column_lookup, sf_column_datatype, sf_column_categories, sd_ref_table_name, formula, description, "comments", created_by, created_at, modified_by, modified_at, is_editable)
VALUES(nextval('base_data_mapping_bdm_id_seq'::regclass), 'PCOF', 1, 'PL BB Build', 'Classifications LTV Transaction', 'classifications_ltv_transaction', 'String', NULL, NULL, 'master_comp', 'PCOF III Borrrowing Base', 'LTV Transaction', NULL, NULL, NULL, 'sf_sheet_pcof_iii_borrrowing_base', NULL, NULL, NULL, 1, now(), NULL, NULL, false);

INSERT INTO public.base_data_mapping
(bdm_id, fund_type, company_id, bd_sheet_name, bd_column_name, bd_column_lookup, bd_column_datatype, bd_column_is_required, bd_column_unit, sf_file_type, sf_sheet_name, sf_column_name, sf_column_lookup, sf_column_datatype, sf_column_categories, sd_ref_table_name, formula, description, "comments", created_by, created_at, modified_by, modified_at, is_editable)
VALUES(nextval('base_data_mapping_bdm_id_seq'::regclass), 'PCOF', 1, 'PL BB Build', 'Classifications Noteless Assigned Loan', 'Classifications_noteless_assigned_loan', 'String', NULL, NULL, 'master_comp', 'PCOF III Borrrowing Base', 'Noteless Assigned Loan', NULL, NULL, NULL, 'sf_sheet_pcof_iii_borrrowing_base', NULL, NULL, NULL, 1, now(), NULL, NULL, false);

INSERT INTO public.base_data_mapping
(bdm_id, fund_type, company_id, bd_sheet_name, bd_column_name, bd_column_lookup, bd_column_datatype, bd_column_is_required, bd_column_unit, sf_file_type, sf_sheet_name, sf_column_name, sf_column_lookup, sf_column_datatype, sf_column_categories, sd_ref_table_name, formula, description, "comments", created_by, created_at, modified_by, modified_at, is_editable)
VALUES(nextval('base_data_mapping_bdm_id_seq'::regclass), 'PCOF', 1, 'PL BB Build', 'Classifications Undelivered Note', 'classifications_undelivered_note', 'String', NULL, NULL, 'master_comp', 'PCOF III Borrrowing Base', 'Undelivered Note', NULL, NULL, NULL, 'sf_sheet_pcof_iii_borrrowing_base', NULL, NULL, NULL, 1, now(), NULL, NULL, false);

INSERT INTO public.base_data_mapping
(bdm_id, fund_type, company_id, bd_sheet_name, bd_column_name, bd_column_lookup, bd_column_datatype, bd_column_is_required, bd_column_unit, sf_file_type, sf_sheet_name, sf_column_name, sf_column_lookup, sf_column_datatype, sf_column_categories, sd_ref_table_name, formula, description, "comments", created_by, created_at, modified_by, modified_at, is_editable)
VALUES(nextval('base_data_mapping_bdm_id_seq'::regclass), 'PCOF', 1, 'PL BB Build', 'Classifications Structured Finance Obligation', 'classifications_structured_finance_obligation', 'String', NULL, NULL, 'master_comp', 'PCOF III Borrrowing Base', 'Structured Finance Obligation', NULL, NULL, NULL, 'sf_sheet_pcof_iii_borrrowing_base', NULL, NULL, NULL, 1, now(), NULL, NULL, false);

INSERT INTO public.base_data_mapping
(bdm_id, fund_type, company_id, bd_sheet_name, bd_column_name, bd_column_lookup, bd_column_datatype, bd_column_is_required, bd_column_unit, sf_file_type, sf_sheet_name, sf_column_name, sf_column_lookup, sf_column_datatype, sf_column_categories, sd_ref_table_name, formula, description, "comments", created_by, created_at, modified_by, modified_at, is_editable)
VALUES(nextval('base_data_mapping_bdm_id_seq'::regclass), 'PCOF', 1, 'PL BB Build', 'Classifications Third Party Finance Company', 'classifications_third_party_finance_company', 'String', NULL, NULL, 'master_comp', 'PCOF III Borrrowing Base', 'Third Party Finance Company', NULL, NULL, NULL, 'sf_sheet_pcof_iii_borrrowing_base', NULL, NULL, NULL, 1, now(), NULL, NULL, false);

INSERT INTO public.base_data_mapping
(bdm_id, fund_type, company_id, bd_sheet_name, bd_column_name, bd_column_lookup, bd_column_datatype, bd_column_is_required, bd_column_unit, sf_file_type, sf_sheet_name, sf_column_name, sf_column_lookup, sf_column_datatype, sf_column_categories, sd_ref_table_name, formula, description, "comments", created_by, created_at, modified_by, modified_at, is_editable)
VALUES(nextval('base_data_mapping_bdm_id_seq'::regclass), 'PCOF', 1, 'PL BB Build', 'Classifications Affiliate Investment', 'classifications_affiliate_investment', 'String', NULL, NULL, 'master_comp', 'PCOF III Borrrowing Base', 'Affiliate Investment', NULL, NULL, NULL, 'sf_sheet_pcof_iii_borrrowing_base', NULL, NULL, NULL, 1, now(), NULL, NULL, false);

INSERT INTO public.base_data_mapping
(bdm_id, fund_type, company_id, bd_sheet_name, bd_column_name, bd_column_lookup, bd_column_datatype, bd_column_is_required, bd_column_unit, sf_file_type, sf_sheet_name, sf_column_name, sf_column_lookup, sf_column_datatype, sf_column_categories, sd_ref_table_name, formula, description, "comments", created_by, created_at, modified_by, modified_at, is_editable)
VALUES(nextval('base_data_mapping_bdm_id_seq'::regclass), 'PCOF', 1, 'PL BB Build', 'Classifications Defaulted / Restructured', 'classifications_defaulted_restructured', 'String', NULL, NULL, 'master_comp', 'PCOF III Borrrowing Base', 'Defaulted / Restructured', NULL, NULL, NULL, 'sf_sheet_pcof_iii_borrrowing_base', NULL, NULL, NULL, 1, now(), NULL, NULL, false);

INSERT INTO public.base_data_mapping
(bdm_id, fund_type, company_id, bd_sheet_name, bd_column_name, bd_column_lookup, bd_column_datatype, bd_column_is_required, bd_column_unit, sf_file_type, sf_sheet_name, sf_column_name, sf_column_lookup, sf_column_datatype, sf_column_categories, sd_ref_table_name, formula, description, "comments", created_by, created_at, modified_by, modified_at, is_editable)
VALUES(nextval('base_data_mapping_bdm_id_seq'::regclass), 'PCOF', 1, 'PL BB Build', 'Leverage Total Capitalization', 'leverage_total_capitalization', 'String', NULL, NULL, 'master_comp', 'PCOF III Borrrowing Base', 'TotalCapitalization', NULL, NULL, NULL, 'sf_sheet_pcof_iii_borrrowing_base', NULL, NULL, NULL, 1, now(), NULL, NULL, false);