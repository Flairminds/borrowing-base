alter sequence base_data_mapping_column_info_id_seq restart with 1;
INSERT INTO base_data_mapping_column_info (bdm_id, fund_type, sequence, is_selected)
SELECT
	bdm_id,
	fund_type,    
    ROW_NUMBER() OVER (ORDER BY bdm_id) + COALESCE((SELECT MAX(sequence) FROM base_data_mapping_column_info where fund_type = 'PCOF'), 0),
    case
    	when (ROW_NUMBER() OVER (ORDER BY bdm_id) + COALESCE((SELECT MAX(sequence) FROM base_data_mapping_column_info where fund_type = 'PCOF'), 0)) < 5 then true
    	else false
    end
FROM base_data_mapping where fund_type = 'PCOF';
INSERT INTO base_data_mapping_column_info (bdm_id, fund_type, sequence, is_selected)
SELECT
	bdm_id,
	fund_type,    
    ROW_NUMBER() OVER (ORDER BY bdm_id) + COALESCE((SELECT MAX(sequence) FROM base_data_mapping_column_info where fund_type = 'PFLT'), 0),
    case
    	when (ROW_NUMBER() OVER (ORDER BY bdm_id) + COALESCE((SELECT MAX(sequence) FROM base_data_mapping_column_info where fund_type = 'PFLT'), 0)) < 5 then true
    	else false
    end
FROM base_data_mapping where fund_type = 'PFLT';

INSERT INTO base_data_mapping_column_info (bdm_id, fund_type, sequence, is_selected)
SELECT 
	bdm_id,
	fund_type,    
    ROW_NUMBER() OVER (ORDER BY bdm_id) + COALESCE((SELECT MAX(sequence) FROM base_data_mapping_column_info where fund_type = 'PSSL'), 0),
    case
    	when (ROW_NUMBER() OVER (ORDER BY bdm_id) + COALESCE((SELECT MAX(sequence) FROM base_data_mapping_column_info where fund_type = 'PSSL'), 0)) < 5 then true
    	else false
    end
FROM base_data_mapping where fund_type = 'PSSL';