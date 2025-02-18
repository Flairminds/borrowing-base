import React, { useEffect, useState } from 'react';
import { FaRegEdit } from "react-icons/fa";
import { DynamicTableComponents } from '../../components/reusableComponents/dynamicTableComponent/DynamicTableComponents';
import { HandleSecurityMappingModal } from '../../modal/securityMappingModals/handleSecurityMapping/HandleSecurityMappingModal';
import { getUnmappedSecurityData } from '../../services/dataIngestionApi';
import { showToast } from '../../utils/helperFunctions/toastUtils';
import styles from "./SecurityMappingPage.module.css";

export const SecurityMappingPage = () => {
	const securityType = "unmapped";
	const [unmappedSecurities, setUnmappedSecurities] = useState([]);
	const [activeSecurity, setActiveSecurity] = useState("");
	const [isMappingPopupOpen, setIsMappingPopupOpen] = useState(false);

	const getMappingData = async () => {
		try {
			const mappingRes = await getUnmappedSecurityData(securityType);
			setUnmappedSecurities(mappingRes.data.result);
		} catch (err) {
			showToast("error", err?.response?.data?.message || "Failed to load data");
		}
	};

	useEffect(() => {
		getMappingData();
	}, []);

	const handleSecurityEdit = (security) => {
		setActiveSecurity(security);
		setIsMappingPopupOpen(true);

	};

	const additionalColumns = [{
		key: "",
		label: "",
		'render': (value, row) => <div style={{textAlign: 'center'}}> <FaRegEdit onClick={() => handleSecurityEdit(row.cashfile_securities)} /> </div>
	}];

	return (
		<div>
			<div className={styles.securityOverview}>
				<div className={styles.securityOverviewCard}>All Securities</div>
				<div className={styles.securityOverviewCard}>Unmapped Securities</div>
			</div>

			<div className={styles.pageTitle}>Unmapped Securites</div>
			<div className={styles.tableContainer}>
				<DynamicTableComponents data={unmappedSecurities?.data} columns={unmappedSecurities?.columns} additionalColumns={additionalColumns} />
			</div>
			<HandleSecurityMappingModal isOpen={isMappingPopupOpen} setIsOpen={setIsMappingPopupOpen} activeSecurity={activeSecurity} />

		</div>
	);
};
