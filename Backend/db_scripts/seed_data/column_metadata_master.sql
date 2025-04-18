INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'borrower_stats') , 1, 'Closing Debt to Capitalization', 'initial_debt_to_capitalization_ratio', '{""}', 'Initial debt to capitalization ratio', NULL, 'float', 'percentage', 5, true, false, false, false, false, true, true, 1, NULL, NULL, '[ACM] [C-ACM(AC]', 'BT', NULL);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'borrower_stats'), 1, 'S&P Industry', 'sp_industry', '{""}', 'S&P Industry Data', NULL, 'string', NULL, 2, true, false, false, false, false, true, true, 1, NULL, NULL, '[ACM] [COI/LC]', 'BB', NULL);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'borrower_stats'), 1, 'PNNT Industry', 'pnnt_industry', '{}', 'PNNT Industry', NULL, 'string', NULL, 6, true, false, false, false, false, true, true, 1, NULL, NULL, '[ACM] [COI/LC]', 'BD', NULL);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'borrower_stats'), 1, 'Closing Date', 'closing_date', '{}', 'Closing Date', NULL, 'datetime', NULL, 7, true, false, false, false, false, true, true, 1, NULL, NULL, '[ACM] [COI/LC]', 'BA', NULL);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'borrower_stats'), 1, 'Closing Fixed Charge Coverage Ratio', 'closing_fixed_charge_coverage_ratio', '{""}', 'Closing Fixed Charge Coverage Ratio', NULL, 'float', NULL, 3, true, false, false, false, false, true, true, 1, NULL, NULL, '[ACM] [C-ACM(AC]', 'BS', NULL);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'borrower_stats'), 1, 'HoldCo Net Debt / EBITDA', 'initial_total_debt_ebitda', '{""}', 'Initial total debt to EBITDA', NULL, 'float', NULL, 1, true, false, false, false, false, true, true, 1, NULL, NULL, '[ACM] [C-ACM(AC]', 'BM', NULL);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'borrower_stats'), 1, '1st Lien Net Debt / EBITDA', 'current_interest_coverage_ratio', '{""}', '1st Lien Net Debt / EBITDA', NULL, 'float', NULL, 4, true, false, false, false, false, true, true, 1, NULL, NULL, '[ACM] [C-ACM(AC]', 'BK', NULL);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'borrower_stats'), 1, 'Company', 'company', '{""}', 'Company', NULL, 'string', NULL, 4, true, false, false, false, false, true, true, 1, NULL, NULL, NULL, 'A', NULL);

INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'securities_stats'), 1, 'Currency', 'currency', '{}', 'Currency', NULL, 'string', NULL, 14, true, false, false, false, false, true, true, 1, NULL, NULL, '[SI]', 'AA', NULL);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'securities_stats'), 1, 'Credit Facility Lien Type', 'credit_facility_lien_type', '{}', 'Credit Facility Lien Type', NULL, 'string', NULL, 9, true, false, false, false, false, true, true, 1, NULL, NULL, '[SI]', 'M', NULL);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'securities_stats'), 1, 'Type of Rate', 'type_of_rate', '{}', 'Type of Rate', NULL, 'string', NULL, 10, true, false, false, false, false, true, true, 1, NULL, NULL, '[SI]', 'R', NULL);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'securities_stats'), 1, 'LIBOR Floor', 'libor_loor', '{}', 'LIBOR Floor', NULL, 'float', 'percentage', 11, true, false, false, false, false, true, true, 1, NULL, NULL, '[SI]', 'T', '["NM"]'::json);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'securities_stats'), 1, 'PIK Coupon', 'pik_coupon', '{}', 'PIK Coupon', NULL, 'float', 'percentage', 13, true, false, false, false, false, true, true, 1, NULL, NULL, '[SI]', 'Y', '["NM"]'::json);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'securities_stats'), 1, 'Total Gross Leverage', 'total_gross_leverage', '{}', 'Total Gross Leverage', NULL, 'float', NULL, NULL, true, false, false, false, false, true, true, 1, NULL, NULL, NULL, 'AX', '["NM"]'::json);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'securities_stats'), 1, 'Pennant Gross Leverage', 'pennant_gross_leverage', '{}', 'Pennant Gross Leverage', NULL, 'float', NULL, NULL, true, false, false, false, false, true, true, 1, NULL, NULL, NULL, 'AY', '["NM"]'::json);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'securities_stats'), 1, 'LTV', 'ltv', '{}', 'LTV', NULL, 'float', 'percentage', NULL, true, false, false, false, false, true, true, 1, NULL, NULL, NULL, 'BU', '["NM"]'::json);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'securities_stats'), 1, 'Security', 'security', '{}', 'Security', NULL, 'string', NULL, 8, true, false, false, false, false, true, true, 1, NULL, NULL, NULL, 'A', NULL);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'securities_stats'), 1, 'EBITDA', 'ebitda', '{}', 'EBITDA', NULL, 'float', NULL, NULL, true, false, false, false, false, true, true, 1, NULL, NULL, NULL, 'AS', NULL);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'securities_stats'), 1, 'TEV', 'tev', '{}', 'TEV', NULL, 'float', NULL, NULL, true, false, false, false, false, true, true, 1, NULL, NULL, '[PSM]', 'AI', NULL);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'securities_stats'), 1, 'Maturity', 'maturity', '{}', 'Maturity', NULL, 'datetime', NULL, 16, true, false, false, false, false, true, true, 1, NULL, NULL, '[SI]', 'S', '["NM"]'::json);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'securities_stats'), 1, 'LTM Rev', 'ltm_rev', '{}', 'LTM Rev', NULL, 'float', 'currency', NULL, true, false, false, false, false, true, true, 1, NULL, NULL, '[C]', 'BX', NULL);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'securities_stats'), 1, 'Cash Spread to LIBOR', 'cash_spread_to_libor', '{}', 'Cash Spread to LIBOR', NULL, 'float', 'percentage', 12, true, false, false, false, false, true, true, 1, NULL, NULL, '[SI]', 'U', '["NM"]'::json);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'securities_stats'), 1, 'Obligor Country', 'obligor_country', '{}', 'Obligor Country', NULL, 'string', NULL, 15, true, false, false, false, false, true, true, 1, NULL, NULL, '[SI]', 'AB', NULL);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'securities_stats'), 1, 'Family Name', 'family_name1', '{}', 'Family Name', NULL, 'string', NULL, 16, true, false, false, false, false, true, true, 1, NULL, NULL, NULL, 'B', NULL);

INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'soi_mapping'), 1, 'SOI Name', 'soi_name', '{}', 'SOI Name', NULL, 'string', NULL, NULL, true, false, false, false, false, true, true, 1, NULL, NULL, NULL, 'B', NULL);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'soi_mapping'), 1, 'Security Name', 'security_name', '{}', 'Security Name', NULL, 'string', NULL, NULL, true, false, false, false, false, true, true, 1, NULL, NULL, NULL, 'C', NULL);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'soi_mapping'), 1, 'Security Type', 'security_type', '{}', 'Security Type', NULL, 'string', NULL, NULL, true, false, false, false, false, true, true, 1, NULL, NULL, NULL, 'E', NULL);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'soi_mapping'), 1, 'Family Name', 'family_name', '{}', 'Family Name', NULL, 'string', NULL, NULL, true, false, false, false, false, true, true, 1, NULL, NULL, NULL, 'D', NULL);


INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'pflt_borrowing_base'), 1, 'Participations', 'participations', '{}', 'Participations', NULL, 'integer', NULL, NULL, true, false, false, false, false, true, true, 1, NULL, NULL, NULL, 'AP', NULL);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'pflt_borrowing_base'), 1, 'Convertible into Equity', 'convertible_into_equity', '{}', 'Convertible into Equity', NULL, 'integer', NULL, NULL, true, false, false, false, false, true, true, 1, NULL, NULL, NULL, 'V', NULL);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'pflt_borrowing_base'), 1, 'DIP Loans', 'dip_loans', '{}', 'DIP Loans', NULL, 'integer', NULL, NULL, true, false, false, false, false, true, true, 1, NULL, NULL, NULL, 'AL', NULL);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'pflt_borrowing_base'), 1, 'Eligible Covie Lite (1L, Issue > $250mm, B3 / B-)', 'eligible_covie_lite_1l_issue_250mm_b3_b', '{}', 'Eligible Covie Lite (1L, Issue > $250mm, B3 / B-)', NULL, 'integer', NULL, NULL, true, false, false, false, false, true, true, 1, NULL, NULL, NULL, 'AE', NULL);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'pflt_borrowing_base'), 1, 'Stretch Senior (Y/N)', 'stretch_senior_y_n', '{}', 'Stretch Senior (Y/N)', NULL, 'string', NULL, NULL, true, false, false, false, false, true, true, 1, NULL, NULL, NULL, 'F', '[0, 1]'::json);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'pflt_borrowing_base'), 1, 'LTM EBITDA', 'ltm_ebitda', '{}', 'LTM EBITDA', NULL, 'float', NULL, NULL, true, false, false, false, false, true, true, 1, NULL, NULL, NULL, 'AZ', NULL);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'pflt_borrowing_base'), 1, 'Closing LTM EBITDA', 'closing_ltm_ebitda', '{}', 'Closing LTM EBITDA', NULL, 'float', 'currency', NULL, true, false, false, false, false, true, true, 1, NULL, NULL, NULL, 'O', NULL);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'pflt_borrowing_base'), 1, 'Obligations w/ Warrants attached', 'obligations_w_warrants_attached', '{}', 'Obligations w/ Warrants attached', NULL, 'integer', NULL, NULL, true, false, false, false, false, true, true, 1, NULL, NULL, NULL, 'AN', NULL);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'pflt_borrowing_base'), 1, 'Structured Finance Obligation / finance lease', 'structured_finance_obligation_finance_lease', '{}', 'Structured Finance Obligation / finance lease', NULL, 'integer', NULL, NULL, true, false, false, false, false, true, true, 1, NULL, NULL, NULL, 'AF', NULL);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'pflt_borrowing_base'), 1, 'Senior Debt', 'senior_debt', '{}', 'Senior Debt', NULL, 'float', NULL, NULL, true, false, false, false, false, true, true, 1, NULL, NULL, NULL, 'AV', NULL);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'pflt_borrowing_base'), 1, 'Total Debt', 'total_debt', '{}', 'Total Debt', NULL, 'float', NULL, NULL, true, false, false, false, false, true, true, 1, NULL, NULL, NULL, 'AX', NULL);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'pflt_borrowing_base'), 1, 'Equity Security', 'equity_security', '{}', 'Equity Security', NULL, 'integer', NULL, NULL, true, false, false, false, false, true, true, 1, NULL, NULL, NULL, 'W', NULL);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'pflt_borrowing_base'), 1, 'Subject of an Offer or Called for Redemption', 'subject_of_an_offer_or_called_for_redemption', '{}', 'Subject of an Offer or Called for Redemption', NULL, 'integer', NULL, NULL, true, false, false, false, false, true, true, 1, NULL, NULL, NULL, 'X', NULL);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'pflt_borrowing_base'), 1, 'Margin Stock', 'margin_stock', '{}', 'Margin Stock', NULL, 'integer', NULL, NULL, true, false, false, false, false, true, true, 1, NULL, NULL, NULL, 'Y', NULL);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'pflt_borrowing_base'), 1, 'Subject to Withholding Tax', 'subject_to_withholding_tax', '{}', 'Subject to Withholding Tax', NULL, 'integer', NULL, NULL, true, false, false, false, false, true, true, 1, NULL, NULL, NULL, 'Z', NULL);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'pflt_borrowing_base'), 1, 'Defaulted Collateral Loan at Acquisition', 'defaulted_collateral_loan_at_acquisition', '{}', 'Defaulted Collateral Loan at Acquisition', NULL, 'integer', NULL, NULL, true, false, false, false, false, true, true, 1, NULL, NULL, NULL, 'AA', NULL);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'pflt_borrowing_base'), 1, 'Credit Improved Loan', 'credit_improved_loan', '{}', 'Credit Improved Loan', NULL, 'integer', NULL, NULL, true, false, false, false, false, true, true, 1, NULL, NULL, NULL, 'AS', NULL);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'pflt_borrowing_base'), 1, 'Zero Coupon Obligation', 'zero_coupon_obligation', '{}', 'Zero Coupon Obligation', NULL, 'integer', NULL, NULL, true, false, false, false, false, true, true, 1, NULL, NULL, NULL, 'AC', NULL);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'pflt_borrowing_base'), 1, 'Covenant Lite', 'covenant_lite', '{}', 'Covenant Lite', NULL, 'integer', NULL, NULL, true, false, false, false, false, true, true, 1, NULL, NULL, NULL, 'AD', NULL);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'pflt_borrowing_base'), 1, 'Material Non-Credit Related Risk', 'material_non-credit_related_risk', '{}', 'Material Non-Credit Related Risk', NULL, 'integer', NULL, NULL, true, false, false, false, false, true, true, 1, NULL, NULL, NULL, 'AG', NULL);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'pflt_borrowing_base'), 1, 'Satisfies Other Criteria(1)', 'satisfies_other_criteria(1)', '{}', 'Satisfies Other Criteria(1)', NULL, 'integer', NULL, NULL, true, false, false, false, false, true, true, 1, NULL, NULL, NULL, 'AJ', NULL);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'pflt_borrowing_base'), 1, 'Primarily Secured by Real Estate', 'primarily_secured_by_real_estate', '{}', 'Primarily Secured by Real Estate', NULL, 'integer', NULL, NULL, true, false, false, false, false, true, true, 1, NULL, NULL, NULL, 'AH', NULL);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'pflt_borrowing_base'), 1, 'Interest Only Security', 'interest_only_security', '{}', 'Interest Only Security', NULL, 'integer', NULL, NULL, true, false, false, false, false, true, true, 1, NULL, NULL, NULL, 'AI', NULL);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'pflt_borrowing_base'), 1, 'Current LTM EBITDA', 'current_ltm_ebitda', '{}', 'Current LTM EBITDA', NULL, 'float', 'currency', NULL, true, false, false, false, false, true, true, 1, NULL, NULL, NULL, 'P', NULL);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'pflt_borrowing_base'), 1, 'Security', 'Security2', '{}', 'Security', NULL, 'string', NULL, NULL, true, false, false, false, false, true, true, 1, NULL, NULL, NULL, 'B', NULL);


INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'pcof_iii_borrrowing_base'), 1, 'Warehouse Yes / No', 'warehouse_yes_no', '{}', 'Warehouse Yes / No', NULL, 'string', NULL, NULL, true, false, false, false, false, true, true, 1, NULL, NULL, NULL, 'Y', NULL);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'pcof_iii_borrrowing_base'), 1, 'Warehouse - Credit Rating', 'warehouse_-_credit_rating', '{}', 'Warehouse - Credit Rating', NULL, 'string', NULL, NULL, true, false, false, false, false, true, true, 1, NULL, NULL, NULL, 'Z', NULL);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'pcof_iii_borrrowing_base'), 1, 'Approved Foreign Jurisdiction', 'approved_foreign_jurisdiction', '{}', 'Approved Foreign Jurisdiction', NULL, 'string', NULL, NULL, true, false, false, false, false, true, true, 1, NULL, NULL, NULL, 'I', NULL);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'pcof_iii_borrrowing_base'), 1, 'Noteless Assigned Loan', 'noteless_assigned_loan', '{}', 'Noteless Assigned Loan', NULL, 'string', NULL, NULL, true, false, false, false, false, true, true, 1, NULL, NULL, NULL, 'K', NULL);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'pcof_iii_borrrowing_base'), 1, 'Undelivered Note', 'undelivered_note', '{}', 'Undelivered Note', NULL, 'string', NULL, NULL, true, false, false, false, false, true, true, 1, NULL, NULL, NULL, 'L', NULL);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'pcof_iii_borrrowing_base'), 1, 'Structured Finance Obligation', 'structured_finance_obligation', '{}', 'Structured Finance Obligation', NULL, 'string', NULL, NULL, true, false, false, false, false, true, true, 1, NULL, NULL, NULL, 'M', NULL);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'pcof_iii_borrrowing_base'), 1, 'Third Party Finance Company', 'third_party_finance_company', '{}', 'Third Party Finance Company', NULL, 'string', NULL, NULL, true, false, false, false, false, true, true, 1, NULL, NULL, NULL, 'N', NULL);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'pcof_iii_borrrowing_base'), 1, 'Affiliate Investment', 'affiliate_investment', '{}', 'Affiliate Investment', NULL, 'string', NULL, NULL, true, false, false, false, false, true, true, 1, NULL, NULL, NULL, 'O', NULL);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'pcof_iii_borrrowing_base'), 1, 'Quoted / Unquoted', 'quoted_unquoted', '{}', 'Quoted / Unquoted', NULL, 'integer', NULL, NULL, true, false, false, false, false, true, true, 1, NULL, NULL, NULL, 'H', '["Yes", "No"]'::json);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'pcof_iii_borrrowing_base'), 1, 'LTV Transaction', 'ltv_transaction', '{}', 'LTV Transaction', NULL, 'string', NULL, NULL, true, false, false, false, false, true, true, 1, NULL, NULL, NULL, 'J', '[0, 1]'::json);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'pcof_iii_borrrowing_base'), 1, 'Defaulted / Restructured', 'defaulted_restructured', '{}', 'Defaulted / Restructured', NULL, 'string', NULL, NULL, true, false, false, false, false, true, true, 1, NULL, NULL, NULL, 'P', '[0, 1]'::json);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'pcof_iii_borrrowing_base'), 1, 'Security Name', 'security_name1', '{}', 'Security Name', NULL, 'string', NULL, NULL, true, false, false, false, false, true, true, 1, NULL, NULL, NULL, 'B', NULL);
INSERT INTO public.column_metadata_master
(fund_id, sheet_id, company_id, column_name, column_lookup, column_aliases, description, calculation_formula, data_type, unit, "sequence", is_raw_data_input, is_base_data_input, is_output, is_intermediate, is_index_column, is_mandatory, is_required, created_by, modified_by, modified_at, column_categories, column_number, exceptions)
VALUES(1, (SELECT smm_id from sheet_metadata_master WHERE lookup = 'pcof_iii_borrrowing_base'), 1, 'Family Name', 'family_name2', '{}', 'Family Name', NULL, 'string', NULL, NULL, true, false, false, false, false, true, true, 1, NULL, NULL, NULL, 'B', NULL);


insert into column_metadata_master (
	fund_id , sheet_id , company_id , column_name , column_lookup , description , data_type , unit , "sequence" , is_raw_data_input , is_mandatory , is_required , created_by , 
	column_categories , column_number , exceptions 
) values 
	(1, (select smm_id from sheet_metadata_master where lookup = 'client_holdings'), 1, 'Issuer/Borrower Name', 'issuer_borrower_name', 'Issuer/Borrower Name', 'String', '', 
	1, true, true, true, 1, null, 'E', null),
	(1, (select smm_id from sheet_metadata_master where lookup = 'client_holdings'), 1, 'Current Par Amount (Issue Currency) - Settled', 'Current_Par_Amount_settled', 'Current Par Amount (Issue Currency) - Settled', 'float', 'currency', 
	2, true, true, true, 1, null, 'AG', null),
	(1, (select smm_id from sheet_metadata_master where lookup = 'client_holdings'), 1, 'Issue Name', 'issue_name', 'Issue Name', 'String', '', 
	3, true, true, true, 1, null, 'F', null),
	(1, (select smm_id from sheet_metadata_master where lookup = 'client_holdings'), 1, 'Deal Issue (Derived) Rating - Moody''s', 'deal_issue_rating_moodys', 'Deal Issue (Derived) Rating - Moody''s', 'String', '', 
	4, true, true, true, 1, null, 'AC', null),
	(1, (select smm_id from sheet_metadata_master where lookup = 'client_holdings'), 1, 'Deal Issue (Derived) Rating - S&P', 'deal_issue_rating_sp', 'Deal Issue (Derived) Rating - S&P', 'String', '', 
	5, true, true, true, 1, null, 'AD', null),
	(1, (select smm_id from sheet_metadata_master where lookup = 'client_holdings'), 1, 'Payment Period', 'payment_period', 'Payment Period', 'String', '', 
	6, true, true, true, 1, null, 'U', null),
	(1, (select smm_id from sheet_metadata_master where lookup = 'client_holdings'), 1, 'As Of Date', 'as_of_date', 'As Of Date', 'datetime', '', 
	7, true, true, true, 1, null, 'D', null),
	(1, (select smm_id from sheet_metadata_master where lookup = 'client_holdings'), 1, 'LoanX ID', 'loanx_id', 'LoanX ID', 'String', '', 
	8, true, true, true, 1, null, 'C', null),
	(1, (select smm_id from sheet_metadata_master where lookup = 'client_holdings'), 1, 'Par Amount (Deal Currency)', 'par_amount', 'Par Amount (Deal Currency)', 'float', 'currency', 
	9, true, true, true, 1, null, 'G', null),
	(1, (select smm_id from sheet_metadata_master where lookup = 'client_holdings'), 1, 'Principal Balance (Deal Currency)', 'principal_balance', 'Principal Balance (Deal Currency)', 'float', 'currency', 
	10, true, true, true, 1, null, 'H', null);


insert into column_metadata_master (
	fund_id , sheet_id , company_id , column_name , column_lookup , description , data_type , unit , "sequence" , is_raw_data_input , is_mandatory , is_required , created_by , 
	column_categories , column_number , exceptions 
) values 
	(1, (select smm_id from sheet_metadata_master where lookup = 'us_bank_holdings'), 1, 'Issuer/Borrower Name', 'issuer_borrower_name', 'Issuer/Borrower Name', 'String', '', 
	1, true, true, true, 1, null, 'F', null),
	(1, (select smm_id from sheet_metadata_master where lookup = 'us_bank_holdings'), 1, 'Current Par Amount (Issue Currency) - Settled', 'current_par_amount_settled', 'Current Par Amount (Issue Currency) - Settled', 'float', 'currency', 
	2, true, true, true, 1, null, 'M', null),
	(1, (select smm_id from sheet_metadata_master where lookup = 'us_bank_holdings'), 1, 'Security/Facility Name', 'security_facility_name', 'Security/Facility Name', 'String', '', 
	3, true, true, true, 1, null, 'D', null),
	(1, (select smm_id from sheet_metadata_master where lookup = 'us_bank_holdings'), 1, 'Maturity Date', 'maturity_date', 'Maturity Date', 'datetime', '', 
	4, true, true, true, 1, null, 'T', null),
	(1, (select smm_id from sheet_metadata_master where lookup = 'us_bank_holdings'), 1, 'Market Value Indenture', 'market_value_indenture', 'Market Value Indenture', 'float', '', 
	5, true, true, true, 1, null, 'Q', null),
	(1, (select smm_id from sheet_metadata_master where lookup = 'us_bank_holdings'), 1, 'Issue Name', 'issue_name_usbh', 'Issue Name', 'String', '', 
	6, true, true, true, 1, null, 'E', null);


-- Validation for Add Other Info
-- PFLT
INSERT INTO column_metadata_master (
	fund_id , sheet_id , company_id , column_name , column_lookup , description , data_type , unit , "sequence" , is_raw_data_input , is_mandatory , is_required , created_by , 
	column_categories , column_number , exceptions 
) VALUES 
	(2, (select smm_id from sheet_metadata_master where lookup = 'input'), 1, 'Determination Date', 'determination_date', 'Determination Date', 'datetime', '', 
	1, true, true, true, 1, null, 'A', null),
	(2, (select smm_id from sheet_metadata_master where lookup = 'input'), 1, 'Minimum Equity Amount Floor ($)', 'minimum_equity_amount_floor', 'Minimum Equity Amount Floor ($)', 'float', 'currency', 
	2, true, true, true, 1, null, 'A', null);

INSERT INTO column_metadata_master (
	fund_id , sheet_id , company_id , column_name , column_lookup , description , data_type , unit , "sequence" , is_raw_data_input , is_mandatory , is_required , created_by , 
	column_categories , column_number , exceptions 
) VALUES 
	(2, (select smm_id from sheet_metadata_master where lookup = 'other_sheet'), 1, 'Currency', 'currency', 'Currency', 'string', '', 
	1, true, true, true, 1, null, 'A', null),
	(2, (select smm_id from sheet_metadata_master where lookup = 'other_sheet'), 1, 'Borrowing', 'borrowing', 'Borrowing', 'float', '', 
	2, true, true, true, 1, null, 'B', null),
	(2, (select smm_id from sheet_metadata_master where lookup = 'other_sheet'), 1, 'Exchange Rates', 'exchange_rates', 'Exchange Rates', 'float', '', 
	3, true, true, true, 1, null, 'C', null),
	(2, (select smm_id from sheet_metadata_master where lookup = 'other_sheet'), 1, 'Current Credit Facility Balance', 'current_credit_facility_balance', 'Current Credit Facility Balance', 'float', '', 
	4, true, true, true, 1, null, 'D', null),
	(2, (select smm_id from sheet_metadata_master where lookup = 'other_sheet'), 1, 'Cash Current And Preborrowing', 'cash_current_and_preborrowing', 'Cash Current And Preborrowing', 'float', '', 
	5, true, true, true, 1, null, 'E', null),
	(2, (select smm_id from sheet_metadata_master where lookup = 'other_sheet'), 1, 'Additional Expenses 1', 'additional_expenses_1', 'Additional Expenses 1', 'float', '', 
	6, true, true, true, 1, null, 'F', null),
	(2, (select smm_id from sheet_metadata_master where lookup = 'other_sheet'), 1, 'Additional Expenses 2', 'additional_expenses_2', 'Additional Expenses 2', 'float', '', 
	7, true, true, true, 1, null, 'G', null),
	(2, (select smm_id from sheet_metadata_master where lookup = 'other_sheet'), 1, 'Additional Expenses 3', 'additional_expenses_3', 'Additional Expenses 3', 'float', '', 
	8, true, true, true, 1, null, 'H', null);


-- PCOF
INSERT INTO column_metadata_master (
	fund_id , sheet_id , company_id , column_name , column_lookup , description , data_type , unit , "sequence" , is_raw_data_input , is_mandatory , is_required , created_by , 
	column_categories , column_number , exceptions 
) VALUES 
	(1, (select smm_id from sheet_metadata_master where lookup = 'availability_borrower'), 1, 'Borrower', 'borrower', 'Borrower', 'string', '', 
	1, true, true, true, 1, null, 'A', null),
	(1, (select smm_id from sheet_metadata_master where lookup = 'availability_borrower'), 1, 'Determination Date', 'determination_date', 'Determination Date', 'datetime', '', 
	2, true, true, true, 1, null, 'A', null),
	(1, (select smm_id from sheet_metadata_master where lookup = 'availability_borrower'), 1, 'Revolving Closing Date', 'revolving_closing_date', 'Revolving Closing Date', 'datetime', '', 
	3, true, true, true, 1, null, 'A', null),
	(1, (select smm_id from sheet_metadata_master where lookup = 'availability_borrower'), 1, 'Commitment Period', 'commitment_period_(3_years_from_final_closing_date,_as_defined_in_lpa)', 'Commitment Period', 'string', '', 
	4, true, true, true, 1, null, 'A', null),
	(1, (select smm_id from sheet_metadata_master where lookup = 'availability_borrower'), 1, 'Facility Size', '(b)_facility_size', 'Facility Size', 'float', '', 
	5, true, true, true, 1, null, 'A', null),
	(1, (select smm_id from sheet_metadata_master where lookup = 'availability_borrower'), 1, 'Loans (USD)', 'loans_(usd)', 'Loans (USD)', 'float', '', 
	6, true, true, true, 1, null, 'A', null),
	(1, (select smm_id from sheet_metadata_master where lookup = 'availability_borrower'), 1, 'Loans (CAD)', 'loans_(cad)', 'Loans (CAD)', 'float', '', 
	7, true, true, true, 1, null, 'A', null);


INSERT INTO column_metadata_master (
	fund_id , sheet_id , company_id , column_name , column_lookup , description , data_type , unit , "sequence" , is_raw_data_input , is_mandatory , is_required , created_by , 
	column_categories , column_number , exceptions 
) VALUES 
	(1, (select smm_id from sheet_metadata_master where lookup = 'principle_obligations'), 1, 'Principal Obligations', 'principle_obligations', 'Principal Obligations', 'string', '', 
	1, true, true, true, 1, null, 'A', null),
	(1, (select smm_id from sheet_metadata_master where lookup = 'principle_obligations'), 1, 'Currency', 'currency', 'Currency', 'string', '', 
	2, true, true, true, 1, null, 'B', null),
	(1, (select smm_id from sheet_metadata_master where lookup = 'principle_obligations'), 1, 'Amount', 'amount', 'Amount', 'float', '', 
	3, true, false, false, 1, null, 'C', null),
	(1, (select smm_id from sheet_metadata_master where lookup = 'principle_obligations'), 1, 'Spot Rate', 'spot_rate', 'Spot Rate', 'float', '', 
	4, true, true, true, 1, null, 'D', null),
	(1, (select smm_id from sheet_metadata_master where lookup = 'principle_obligations'), 1, 'Dollar Equivalent', 'dollar_equivalent', 'Dollar Equivalent', 'float', '', 
	5, true, true, true, 1, null, 'E', null);


INSERT INTO column_metadata_master (
	fund_id , sheet_id , company_id , column_name , column_lookup , description , data_type , unit , "sequence" , is_raw_data_input , is_mandatory , is_required , created_by , 
	column_categories , column_number , exceptions 
) VALUES 
	(1, (select smm_id from sheet_metadata_master where lookup = 'subscription_bb'), 1, 'Investor', 'investor', 'Investor', 'string', '', 
	1, true, false, false, 1, null, 'A', null),
	(1, (select smm_id from sheet_metadata_master where lookup = 'subscription_bb'), 1, 'Master/Feeder', 'master_feeder', 'Master/Feeder', 'string', '', 
	2, true, false, false, 1, null, 'B', null),
	(1, (select smm_id from sheet_metadata_master where lookup = 'subscription_bb'), 1, 'Ultimate Investor Parent', 'ultimate_investor_parent', 'Ultimate Investor Parent', 'string', '', 
	3, true, false, false, 1, null, 'C', null),
	(1, (select smm_id from sheet_metadata_master where lookup = 'subscription_bb'), 1, 'Designation', 'designation', 'Designation', 'string', '', 
	4, true, true, true, 1, null, 'D', null),
	(1, (select smm_id from sheet_metadata_master where lookup = 'subscription_bb'), 1, 'Commitment', 'commitment', 'Commitment', 'float', '', 
	5, true, false, false, 1, null, 'E', null),
	(1, (select smm_id from sheet_metadata_master where lookup = 'subscription_bb'), 1, 'Capital Called', 'capital_called', 'Capital Called', 'float', '', 
	6, true, false, false, 1, null, 'F', null);


INSERT INTO column_metadata_master (
	fund_id , sheet_id , company_id , column_name , column_lookup , description , data_type , unit , "sequence" , is_raw_data_input , is_mandatory , is_required , created_by , 
	column_categories , column_number , exceptions 
) VALUES 
	(1, (select smm_id from sheet_metadata_master where lookup = 'pricing'), 1, 'Pricing', 'pricing', 'Pricing', 'string', '', 
	1, true, true, true, 1, null, 'A', null),	
	(1, (select smm_id from sheet_metadata_master where lookup = 'pricing'), 1, 'Percent', 'percent', 'Percent', 'float', 'percent', 
	2, true, true, true, 1, null, 'B', null);



INSERT INTO column_metadata_master (
	fund_id , sheet_id , company_id , column_name , column_lookup , description , data_type , unit , "sequence" , is_raw_data_input , is_mandatory , is_required , created_by , 
	column_categories , column_number , exceptions 
) VALUES 
	(1, (select smm_id from sheet_metadata_master where lookup = 'portfolio_leverageborrowingbase'), 1, 'Investment Type', 'investment_type', 'Investment Type', 'string', '', 
	1, true, true, true, 1, null, 'A', null),
	(1, (select smm_id from sheet_metadata_master where lookup = 'portfolio_leverageborrowingbase'), 1, 'Unquoted (%)', 'unquoted', 'Unquoted (%)', 'float', 'percent', 
	2, true, true, true, 1, null, 'B', null),
	(1, (select smm_id from sheet_metadata_master where lookup = 'portfolio_leverageborrowingbase'), 1, 'Quoted (%)', 'quoted', 'Qquoted (%)', 'float', 'percent', 
	3, true, true, true, 1, null, 'C', null);

INSERT INTO column_metadata_master (
	fund_id , sheet_id , company_id , column_name , column_lookup , description , data_type , unit , "sequence" , is_raw_data_input , is_mandatory , is_required , created_by , 
	column_categories , column_number , exceptions 
) VALUES 
	(1, (select smm_id from sheet_metadata_master where lookup = 'advance_rates'), 1, 'Investor Type', 'investor_type', 'Investor Type', 'string', '', 
	1, true, true, true, 1, null, 'A', null),	
	(1, (select smm_id from sheet_metadata_master where lookup = 'advance_rates'), 1, 'Advance Rate (%)', 'advance_rate', 'Advance Rate (%)', 'float', 'percent', 
	2, true, true, true, 1, null, 'B', null);


INSERT INTO column_metadata_master (
	fund_id , sheet_id , company_id , column_name , column_lookup , description , data_type , unit , "sequence" , is_raw_data_input , is_mandatory , is_required , created_by , 
	column_categories , column_number , exceptions 
) VALUES 
	(1, (select smm_id from sheet_metadata_master where lookup = 'concentration_limits'), 1, 'Investors', 'investors', 'Investors', 'string', '', 
	1, true, true, true, 1, null, 'A', null),
	(1, (select smm_id from sheet_metadata_master where lookup = 'concentration_limits'), 1, 'Rank', 'rank', 'Ranks', 'string', '', 
	2, true, false, false, 1, null, 'B', null),
	(1, (select smm_id from sheet_metadata_master where lookup = 'concentration_limits'), 1, 'Concentration Limit (%)', 'concentration_limit', 'Concentration Limit (%)', 'float', 'percent', 
	3, true, true, true, 1, null, 'C', null);


INSERT INTO column_metadata_master (
	fund_id , sheet_id , company_id , column_name , column_lookup , description , data_type , unit , "sequence" , is_raw_data_input , is_mandatory , is_required , created_by , 
	column_categories , column_number , exceptions 
) VALUES 
	(1, (select smm_id from sheet_metadata_master where lookup = 'other_metrics'), 1, 'First Lien Leverage Cut-Off Point', 'first_lien_leverage_cut_off_point', 'First Lien Leverage Cut-Off Point', 'float', '', 
	1, true, true, true, 1, null, 'A', null),
	(1, (select smm_id from sheet_metadata_master where lookup = 'other_metrics'), 1, 'Warehouse First Lien Leverage Cut-Off', 'warehouse_first_lien_leverage_cut_off', 'Warehouse First Lien Leverage Cut-Off', 'float', '', 
	2, true, true, true, 1, null, 'A', null),
	(1, (select smm_id from sheet_metadata_master where lookup = 'other_metrics'), 1, 'Last Out Attachment Point', 'last_out_attachment_point', 'Last Out Attachment Point', 'float', '', 
	3, true, true, true, 1, null, 'A', null),
	(1, (select smm_id from sheet_metadata_master where lookup = 'other_metrics'), 1, 'Trailing 12-Month EBITDA', 'trailing_12_month_ebitda', 'Trailing 12-Month EBITDA', 'float', '', 
	4, true, true, true, 1, null, 'A', null),
	(1, (select smm_id from sheet_metadata_master where lookup = 'other_metrics'), 1, 'Trailing 24-Month EBITDA', 'trailing_24_month_ebitda', 'Trailing 24-Month EBITDA', 'float', '', 
	5, true, true, true, 1, null, 'A', null),
	(1, (select smm_id from sheet_metadata_master where lookup = 'other_metrics'), 1, 'Total Leverage', 'total_leverage', 'Total Leverage', 'float', '', 
	6, true, true, true, 1, null, 'A', null),
	(1, (select smm_id from sheet_metadata_master where lookup = 'other_metrics'), 1, 'LTV (%)', 'ltv', 'LTV (%)', 'float', 'percent', 
	7, true, true, true, 1, null, 'A', null),
	(1, (select smm_id from sheet_metadata_master where lookup = 'other_metrics'), 1, 'Concentration Test Threshold 1 (%)', 'concentration_test_threshold_1', 'Concentration Test Threshold 1 (%)', 'float', 'percent', 
	8, true, true, true, 1, null, 'A', null),
	(1, (select smm_id from sheet_metadata_master where lookup = 'other_metrics'), 1, 'Concentration Test Threshold 2 (%)', 'concentration_test_threshold_2', 'Concentration Test Threshold 2 (%)', 'float', 'percent', 
	9, true, true, true, 1, null, 'A', null),
	(1, (select smm_id from sheet_metadata_master where lookup = 'other_metrics'), 1, 'Threshold 1 Advance Rate (%)', 'threshold_1_advance_rate', 'Threshold 1 Advance Rate (%)', 'float', 'percent', 
	10, true, true, true, 1, null, 'A', null),
	(1, (select smm_id from sheet_metadata_master where lookup = 'other_metrics'), 1, 'Threshold 2 Advance Rate (%)', 'threshold_2_advance_rate', 'Threshold 2 Advance Rate (%)', 'float', 'percent', 
	11, true, true, true, 1, null, 'A', null);