-- update concentration test table values

update concentration_test set ct_code = 'MINELIS' where test_name = 'Min. Eligible Issuers (#)';
update concentration_test set ct_code = 'ISSUERS' where test_name = '8 or 9 Issuers?';
update concentration_test set ct_code = 'SECLSPL' where test_name = 'Second Lien and Split Lien';
update concentration_test set ct_code = 'DIPCOLL' where test_name = 'DIP Collateral Loans';
update concentration_test set ct_code = 'MAXLTVT' where test_name = 'Max. LTV Transactions';
update concentration_test set ct_code = 'MAXFEPI' where test_name = 'Max. Foreign Eligible Portfolio Investments';
update concentration_test set ct_code = 'MAXWARA' where test_name = 'Max. Warehouse Assets';
update concentration_test set ct_code = 'SECLIEN' where test_name = 'Second Lien';
update concentration_test set ct_code = 'MAXINCO' where test_name = 'Max. Industry Concentration (% BB)';
update concentration_test set ct_code = 'MAXCONT' where test_name = 'Max. Contribution to BB with Maturity > 8 years';
update concentration_test set ct_code = 'MAXICLA' where test_name = 'Max. Industry Concentration (Largest Industry, % BB)';
update concentration_test set ct_code = 'MAXICSL' where test_name = 'Max. Industry Concentration (2nd Largest Industry, % BB)';

update concentration_test set unit = 'issuer' where ct_code in ('MINELIS', 'ISSUERS');
update concentration_test set data_type = 'float' where ct_code not in ('MINELIS', 'ISSUERS');