import React, { useEffect, useState } from 'react';
import { FaRegEdit } from "react-icons/fa";
import { useNavigate } from 'react-router';
import { BackOption } from '../../../components/BackOption/BackOption';
import { DynamicTableComponents } from '../../../components/reusableComponents/dynamicTableComponent/DynamicTableComponents';
import { UIComponents } from '../../../components/uiComponents';
import { CustomButton } from '../../../components/uiComponents/Button/CustomButton';
import { AllSecurityModal } from '../../../modal/allSecurityModal/AllSecurityModal';
import { HandleSecurityMappingModal } from '../../../modal/securityMappingModals/handleSecurityMapping/HandleSecurityMappingModal';
import { getUnmappedSecurityData } from '../../../services/dataIngestionApi';
import { COLUMN_GROUPS, PAGE_ROUTES } from '../../../utils/constants/constants';
import { FilterMultiSelect } from '../../../utils/helperFunctions/FilterMultiSelect';
import { showToast } from '../../../utils/helperFunctions/toastUtils';
import styles from "./SecurityMappingPage.module.css";

export const SecurityMappingPage = ({selectedSecurities}) => {
	const [unmappedSecurities, setUnmappedSecurities] = useState([]);
	const [isMappingPopupOpen, setIsMappingPopupOpen] = useState(false);
	const [securityViewType, setSecurityViewType] = useState("unmapped");
	// const [searchText, setSearchText] = useState("");
	// const [searchText, setSearchText] = useState("");
	const [dataLoading, setDataLoading] = useState(false);
	const [isModalVisible, setIsModalVisible] = useState(false);
	const [selectedSecurity, setSelectedSecurity] = useState(null);
	const [filteredData, setFilteredData] = useState([]);
	const [isAnyCheckboxChecked, setIsAnyCheckboxChecked] = useState(false);
	// const [selectedSecurities, setSelectedSecurities] = useState([]);
	const navigate = useNavigate();

	// const handleSearch = (event) => {
	// 	setSearchText(event.target.value);
	// };

	// const filteredData = unmappedSecurities?.data
	// 	? unmappedSecurities.data.filter((item) =>
	// 		item["cashfile_securities"] &&
	// 		item["cashfile_securities"].toLowerCase().includes(searchText.toLowerCase())
	// 	)
	// 	: [];

	// const dataToDisplay = searchText ? filteredData : unmappedSecurities?.data;

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

	useEffect(() => {
		if (unmappedSecurities?.data) {
			setFilteredData(unmappedSecurities.data);
		}
	}, [unmappedSecurities]);

	useEffect(() => {
		if (!isMappingPopupOpen) {
			setIsAnyCheckboxChecked(securityViewType === "unmapped" && selectedSecurities.current.length > 0);
		}
	}, [isMappingPopupOpen, securityViewType]);


	const handleMappingPopup = () => {
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

	const hanldeCheckBoxClick = (security) => {
		if (selectedSecurities.current.includes(security)) {
			selectedSecurities.current = selectedSecurities.current.filter(sec => sec != security);
		} else {
			selectedSecurities.current = [...selectedSecurities.current, security];
		}
		setIsAnyCheckboxChecked(securityViewType == "unmapped" && selectedSecurities.current.length > 0 );
	};

	const additionalColumns = securityViewType == "all" ? [{
		key: "",
		label: "",
		'render': (value, row) => (
			<div style={{ textAlign: 'center', cursor: 'pointer' }}>
				<FaRegEdit onClick={() => handleAllSecurities(row)} />
			</div>
		)
	}] : [];

	const initialAdditionalColumns = [{
		key: "",
		label: "",
		'render': (value, row) => (
			<div style={{ textAlign: 'center', cursor: 'pointer' }}>
				<input type="checkbox" checked={selectedSecurities.current?.includes(row.cashfile_securities)} onClick={() => hanldeCheckBoxClick(row.cashfile_securities)} />
			</div>
		)
	}];


	return (
		<div>

			<div className={styles.backOptionContainer}>
				<BackOption onClick={() => navigate(PAGE_ROUTES.BASE_DATA_LIST.url)}
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
					<div style={{ display: "flex"}}>
						<FilterMultiSelect data={unmappedSecurities?.data} columns={COLUMN_GROUPS[securityViewType]}
							onFilterChange={(filtered) => setFilteredData(filtered)}
						/>
						{/* <input
							type="text"
							placeholder="Security/Facility Name"
							style={{ width: '350px', borderRadius: '5px', outline: "none", border: "1px solid #888D8D", padding: '7px' }}
							value={searchText}
							onChange={handleSearch}
						/> */}
						{securityViewType == "unmapped" && <CustomButton text='Edit Mapping' isFilled={true} onClick={handleMappingPopup} btnDisabled={!isAnyCheckboxChecked} /> }
					</div>

				</div>
				{dataLoading ? <div style={{textAlign: 'center'}}><UIComponents.Loader /></div> :
					<DynamicTableComponents data={filteredData} columns={unmappedSecurities?.columns} initialAdditionalColumns={initialAdditionalColumns} additionalColumns={additionalColumns} />}
			</div>
			<HandleSecurityMappingModal isOpen={isMappingPopupOpen} setIsOpen={setIsMappingPopupOpen} selectedSecurities={selectedSecurities} getMappingData={getMappingData} />
			<AllSecurityModal isOpen={isModalVisible} setIsOpen={setIsModalVisible} security={selectedSecurity} getMappingData={getMappingData} />
		</div>
	);
};
