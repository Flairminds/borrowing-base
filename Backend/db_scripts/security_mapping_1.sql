delete from pflt_security_mapping a using (
	select MAX(ctid) as ctid, soi_name, master_comp_security_name, security_type from pflt_security_mapping
	group by (soi_name, master_comp_security_name, security_type) having COUNT(*) > 1) b
where (a.soi_name = b.soi_name
		and a.master_comp_security_name = b.master_comp_security_name
		and a.security_type = b.security_type
		and a.ctid <> b.ctid)
	or a.master_comp_security_name is null;
	
ALTER TABLE pflt_security_mapping ADD CONSTRAINT unique_record UNIQUE (soi_name, master_comp_security_name, security_type);