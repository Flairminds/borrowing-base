import React, { useEffect, useState } from 'react';
import { FaRegEdit } from "react-icons/fa";
import { Loader } from '../../components/loader/loader';
import { DynamicTableComponents } from '../../components/reusableComponents/dynamicTableComponent/DynamicTableComponents';
import { HandleSecurityMappingModal } from '../../modal/securityMappingModals/handleSecurityMapping/HandleSecurityMappingModal';
import { getUnmappedSecurityData } from '../../services/dataIngestionApi';
import { showToast } from '../../utils/helperFunctions/toastUtils';
import styles from "./SecurityMappingPage.module.css";
import { BackOption } from '../../components/BackOption/BackOption';
import { useNavigate } from 'react-router';
import { AllSecurityModal } from '../../modal/allSecurityModal/AllSecurityModal';
import { Select } from 'antd';

export const SecurityMappingPage = () => {
	const [unmappedSecurities, setUnmappedSecurities] = useState([]);
	const [activeSecurity, setActiveSecurity] = useState("");
	const [isMappingPopupOpen, setIsMappingPopupOpen] = useState(false);
	const [securityViewType, setSecurityViewType] = useState("unmapped");
	const [searchText, setSearchText] = useState("");
	const [dataLoading, setDataLoading] = useState(false);
	const [isModalVisible, setIsModalVisible] = useState(false);
	const [selectedSecurity, setSelectedSecurity] = useState(null);
	const navigate = useNavigate();

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
			setUnmappedSecurities({});
			setDataLoading(true);
			const mappingRes = await getUnmappedSecurityData(securityType);
			setUnmappedSecurities(mappingRes.data.result);
			setDataLoading(false);
		} catch (err) {
			showToast("error", err?.response?.data?.message || "Failed to load data");
			setDataLoading(false);
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

	const handleAllSecurities = (security) => {
		setSelectedSecurity(security);
		setIsModalVisible(true);
	};
	const changeSecurityView = (securityType) => {
		setSecurityViewType(securityType);
		getMappingData(securityType);
	};

	const additionalColumns = [{
		key: "",
		label: "",
		'render': (value, row) => (
			<div style={{ textAlign: 'center', cursor: 'pointer' }}>
				{securityViewType == "unmapped"
					? <FaRegEdit onClick={() => handleSecurityEdit(row.cashfile_securities)} />
					: <FaRegEdit onClick={() => handleAllSecurities(row)} />}
			</div>
		)
	}];


	return (
		<div>

			<div className={styles.backOptionContainer}>
				<BackOption onClick={() => navigate('/base-data-list')}
					text={`<- Base Data`} />
			</div>
			<div className={styles.securityOverview}>
				<div onClick={() => changeSecurityView("all")} className={securityViewType == "all" ? `${styles.securityOverviewCard} ${styles.background}` : `${styles.securityOverviewCard}`}>
					<div><b>All Securities</b></div>
					<div className={styles.cardTitle}>{unmappedSecurities?.all_securities_count}</div>
				</div>
				<div onClick={() => changeSecurityView("unmapped")} className={securityViewType == "unmapped" ? `${styles.securityOverviewCard} ${styles.background}` : `${styles.securityOverviewCard}`}>
					<div><b>Unmapped Securities</b></div>
					<div className={styles.cardTitle}>{unmappedSecurities?.unmapped_securities_count}</div>
				</div>
			</div>
			<div className={styles.tableContainer}>
				<div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
					<div className={styles.pageTitle}>
						{securityViewType === "all" ? <>All Securities</> : <>Unmapped Securities</>}
					</div>
					<input
						type="text"
						placeholder="Security/Facility Name"
						style={{ width: '350px', borderRadius: '5px', outline: "none", border: "1px solid #888D8D", padding: '7px' }}
						value={searchText}
						onChange={handleSearch}
					/>
				</div>
				{dataLoading ? <div style={{ textAlign: 'center' }}><Loader /></div> :
					<DynamicTableComponents data={dataToDisplay} columns={unmappedSecurities?.columns} additionalColumns={additionalColumns} />}
			</div>
			<HandleSecurityMappingModal isOpen={isMappingPopupOpen} setIsOpen={setIsMappingPopupOpen} activeSecurity={activeSecurity} getMappingData={getMappingData} />
			<AllSecurityModal isOpen={isModalVisible} setIsOpen={setIsModalVisible} security={selectedSecurity} getMappingData={getMappingData} />
		</div>
	);
};
