import React, { useEffect, useState } from 'react';
import { FaRegEdit } from "react-icons/fa";
import { DynamicTableComponents } from '../../components/reusableComponents/dynamicTableComponent/DynamicTableComponents';
import { HandleSecurityMappingModal } from '../../modal/securityMappingModals/handleSecurityMapping/HandleSecurityMappingModal';
import { getUnmappedSecurityData } from '../../services/dataIngestionApi';
import { showToast } from '../../utils/helperFunctions/toastUtils';
import styles from "./SecurityMappingPage.module.css";

export const SecurityMappingPage = () => {
	const [unmappedSecurities, setUnmappedSecurities] = useState([]);
	const [activeSecurity, setActiveSecurity] = useState("");
	const [isMappingPopupOpen, setIsMappingPopupOpen] = useState(false);
	const [securityViewType, setSecurityViewType] = useState("unmapped");
	const [searchText, setSearchText] = useState("");

	const handleSearch = (event) => {
		setSearchText(event.target.value);
	};

	const filteredData = unmappedSecurities?.data
		? unmappedSecurities.data.filter((item) =>
			item["cashfile_securities"] &&
			item["cashfile_securities"].toLowerCase().includes(searchText.toLowerCase())
		)
		: [];

	const dataToDisplay = searchText ? filteredData : unmappedSecurities?.data;

	const getMappingData = async (securityType) => {
		try {
			const mappingRes = await getUnmappedSecurityData(securityType);
			setUnmappedSecurities(mappingRes.data.result);
		} catch (err) {
			showToast("error", err?.response?.data?.message || "Failed to load data");
		}
	};

	useEffect(() => {
		if (securityViewType) {
			getMappingData(securityViewType);
		}
	}, []);

	const handleSecurityEdit = (security) => {
		setActiveSecurity(security);
		setIsMappingPopupOpen(true);
	};

	const changeSecurityView = (securityType) => {
		setSecurityViewType(securityType);
		getMappingData(securityType);
	};

	const additionalColumns = securityViewType == "unmapped" ? [{
		key: "",
		label: "",
		'render': (value, row) => <div style={{ textAlign: 'center', cursor: 'pointer' }}> <FaRegEdit onClick={() => handleSecurityEdit(row.cashfile_securities)} /> </div>
	}] : [];

	return (
		<div>
			<div className={styles.securityOverview}>
				<div onClick={() => changeSecurityView("all")} className={styles.securityOverviewCard}>All Securities</div>
				<div onClick={() => changeSecurityView("unmapped")} className={`${styles.securityOverviewCard} ${styles.background}`}>Unmapped Securities</div>
			</div>



			<div className={styles.tableContainer}>
				<div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
					<div className={styles.pageTitle}>
						{securityViewType === "all" ? <>All Securities</> : <>Unmapped Securities</>}
					</div>
					<input
						type="text"
						placeholder="Security/Facility Name"
						style={{ width: '200px', borderRadius: '5px' }}
						value={searchText}
						onChange={handleSearch}
					/>
				</div>
				<DynamicTableComponents data={dataToDisplay} columns={unmappedSecurities?.columns} additionalColumns={additionalColumns} />
			</div>
			<HandleSecurityMappingModal isOpen={isMappingPopupOpen} setIsOpen={setIsMappingPopupOpen} activeSecurity={activeSecurity} />

		</div>
	);
};
