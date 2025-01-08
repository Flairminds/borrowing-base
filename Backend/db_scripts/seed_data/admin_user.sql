INSERT INTO public.companies
(company_id, company_name, admin_id, created_by, created_at, modified_by, modified_at)
VALUES(1, 'Onpepper', 1, 1, now());

INSERT INTO public.users
(user_id, username, display_name, company_id, created_by, created_at)
VALUES(1, 'Superadmin', 'Superadmin', 1, 1, now());