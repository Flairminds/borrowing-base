CREATE OR REPLACE FUNCTION public.trg_fn_pssl_base_data_history()
RETURNS trigger
LANGUAGE plpgsql
AS $function$
DECLARE
    new_pssl_bdh_id INTEGER;
BEGIN
    IF (TG_OP = 'DELETE') then
        SELECT nextval('pssl_base_data_history_pssl_bdh_id_seq') INTO new_pssl_bdh_id;
        INSERT INTO pssl_base_data_history
        SELECT TG_OP, now(), new_pssl_bdh_id, old.*;
        RETURN old;
    ELSIF (TG_OP = 'INSERT' OR TG_OP = 'UPDATE') then
        SELECT nextval('pssl_base_data_history_pssl_bdh_id_seq') INTO new_pssl_bdh_id;    
        INSERT INTO pssl_base_data_history
        SELECT TG_OP, now(), new_pssl_bdh_id, new.*;
        RETURN new;
    END IF;
END;
$function$
;

create trigger pssl_base_data_tr after
insert or delete or update on
pssl_base_data for each row execute function public.trg_fn_pssl_base_data_history();