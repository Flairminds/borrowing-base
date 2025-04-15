import { Select } from 'antd';
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router';
import { CustomButton } from '../../components/uiComponents/Button/CustomButton';
import { DynamicTableComponents } from '../../components/reusableComponents/dynamicTableComponent/DynamicTableComponents';
import { SourceFileModal } from '../../modal/sourceFileModal/SourceFileModal';
import { getBaseDataFilesList, getBaseFilePreviewData } from '../../services/dataIngestionApi';
import { fundMap, fundOptionsArray, PAGE_ROUTES } from '../../utils/constants/constants';
import { showToast } from '../../utils/helperFunctions/toastUtils';
import styles from './BaseDataFileList.module.css';
import { filterPreviewData } from '../../utils/helperFunctions/filterPreviewData';
import { UIComponents } from '../../components/uiComponents';
import { STATUS_BG_COLOR, FUND_BG_COLOR } from '../../utils/styles';
import { Calender } from '../../components/calender/Calender';
import { Icons } from '../../components/icons';

export const BaseDataFileList = ({ setBaseFilePreviewData, setPreviewPageId, setPreviewFundType }) => {
	const [baseDataFilesList, setBaseDataFilesList] = useState({});
	const [extractionInProgress, setExtractionInProgress] = useState(false);
	const [isPopupOpen, setIsPopupOpen] = useState(false);
	const [popupContent, setPopupContent] = useState(null);
	const [selectedFundType, setSelectedFundType] = useState(0);
	const [dataLoading, setDataLoading] = useState(false);
	const [reportDates, setReportDates] = useState([]);
	const [filteredData, setFilteredData] = useState([]);
	const [filterDate, setFilterDate] = useState(null);

	const navigate = useNavigate();

	const handleExtractNew = () => {
		navigate(PAGE_ROUTES.SOURCE_FILES.url);
	};

	const handleSecurityMapping = () => {
		navigate('/configuration?tab=security_mapping');
	};

	const handleBaseDataPreview = async (row) => {
		localStorage.setItem("extraction_info_id", row.id);
		if (row.extraction_status == 'failed') {
			alert(row.comments);
			return;
		}
		try {
			setDataLoading(true);
			const previewDataResponse = await getBaseFilePreviewData(row.id);
			const result = previewDataResponse.data?.result;
			if (result)
				setBaseFilePreviewData({
					baseData: result.base_data_table,
					reportDate: result.report_date,
					baseDataMapping: result?.base_data_mapping && result.base_data_mapping,
					cardData: result?.card_data && result.card_data[0],
					infoId: row.id,
					otherInfo: result.other_info,
					fundType: result?.fund_type
				});
			setPreviewPageId(row.id);
			setPreviewFundType(row.fund);
			navigate(`/data-ingestion/base-data-preview/${row.id}`);
		} catch (err) {
			showToast("error", err.response.data.message);
			setDataLoading(false);
		}
	};

	const columnsToAdd = [{
		'key': 'file_preview',
		'label': '',
		'render': (value, row) => <div onClick={() => handleBaseDataPreview(row)}
			style={{color: row.extraction_status.toLowerCase() === "completed" ? 'green' : 'red', cursor: 'pointer'}} title={row.extraction_status.toLowerCase() === "completed" ? 'Click to preview base data' : 'Click to view errors' } >
			{row.extraction_status.toLowerCase() === "completed" ? 'Preview Base Data' : (row.extraction_status.toLowerCase() === "failed" ? 'Errors' : '')}
		</div>
	}];


	const injectRenderForSourceFiles = (columns) => {
		return columns?.map((col) => {
			if (col.key === 'source_files') {
				return {
					...col,
					render: (value, row) => (
						<div>
							{row.source_file_details?.map((file, index) => (
								<div
									key={file.file_id}
									onClick={() => handleSourceFileClick(file)}
									style={{
										color: '#007BFF',
										cursor: 'pointer',
										textDecoration: 'underline',
										marginBottom: '2px'
									}}
								>
									{index + 1}. {file.file_name + file.extension}
								</div>
							))}
						</div>
					)
				};
			}
			if (col.key === 'extraction_status') {
				return {
					...col,
					render: (value, row) => (
						<div>
							<span style={{display: 'inline-block', padding: '3px 7px', borderRadius: '8px', ...(STATUS_BG_COLOR[row.extraction_status.toLowerCase()] || { backgroundColor: 'gray', color: 'white'})}}>
								{row.extraction_status.split(" ")
									.map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
									.join(" ")}
							</span>
						</div>
					)
				};
			}
			if (col.key === 'fund') {
				return {
					...col,
					render: (value, row) => (
						<div>
							<span style={{display: 'inline-block', padding: '3px 7px', borderRadius: '8px', ...(FUND_BG_COLOR[row.fund] || { backgroundColor: 'gray', color: 'white'})}}>
								{row.fund}
							</span>
						</div>
					)
				};
			}
			return col;
		});
	};

	const handleSourceFileClick = (fileDetails) => {
		setPopupContent(fileDetails);
		setIsPopupOpen(true);
	};

	const getFilesList = async (fundType) => {
		const Fund = fundMap[fundType];
		try {
			setDataLoading(true);
			const data = {
				"company_id": 1,
				"fund_type": Fund
			};
			const filesRes = await getBaseDataFilesList(data);
			const updatedColumns = injectRenderForSourceFiles(filesRes.data.result.columns);
			setBaseDataFilesList({ ...filesRes.data.result, columns: updatedColumns });
			const reportDatesArr = [];
			filesRes.data.result?.data?.forEach(d => reportDatesArr.push(d.report_date));
			setReportDates(reportDatesArr);
			setDataLoading(false);
			if (filterDate) {
				const temp = filesRes.data.result.data.filter(t => t.report_date == filterDate);
				setFilteredData(temp);
			} else {
				setFilteredData(filesRes.data.result.data);
			}
		} catch (err) {
			showToast('error', err?.response?.data.message);
			setDataLoading(false);
		}
	};

	useEffect(() => {
		getFilesList(selectedFundType);
	}, [extractionInProgress]);

	setInterval(() => {
		if (extractionInProgress) {
			setExtractionInProgress(false);
		}
	}, 15000);

	useEffect(() => {
		if (baseDataFilesList && baseDataFilesList.data) {
			for (let i = 0; i < baseDataFilesList.data.length; i++) {
				if (baseDataFilesList.data[i].extraction_status == 'in progress') {
					setExtractionInProgress(true);
					break;
				}
			}
		}
	}, [baseDataFilesList]);

	const handleDropdownChange = (value) => {
		setSelectedFundType(value);
		getFilesList(value);
	};

	const filterByDate = (value, dateString) => {
		try {
			if (dateString) {
				setFilterDate(dateString);
				let temp = [...baseDataFilesList.data];
				temp = temp.filter(t => t.report_date == dateString);
				setFilteredData(temp);
			} else {
				setFilterDate(null);
				setFilteredData(baseDataFilesList.data);
			}
		} catch (error) {
			console.error(error);
		}
	};

	return (
		<div className={styles.pageContainer}>
			<div className={styles.baseFileListPage}>
				<div className={styles.headerContainer}>
					<div className={styles.tableHeading}>
						Extracted Base Data
						<Icons.InfoIcon title={'Viewing list of extracted base data. You can preview the base data from here.'} />
					</div>
					<div className={styles.buttonsContainer}>
						<div style={{margin: 'auto'}}>
							<Select
								defaultValue="-- Select Fund --"
								style={{ width: 150, borderRadius: '8px'}}
								options={fundOptionsArray}
								onChange={handleDropdownChange}
							/>
						</div>
						<div>
							<Calender availableClosingDates={reportDates} onDateChange={filterByDate} fileUpload={true} />
						</div>
						{/* <CustomButton isFilled={true} onClick={handleSecurityMapping} text="Security Mapping" /> */}
						<CustomButton isFilled={true} onClick={handleExtractNew} text="+ Extract New Base Data" title='Upload new files or select existing files to extract new base data' />
					</div>
				</div>
				{dataLoading ? <UIComponents.Loader /> :
					<div className={styles.baseDataTableContainer}>
						<DynamicTableComponents data={filteredData} columns={baseDataFilesList?.columns} additionalColumns={columnsToAdd} />
					</div>}
			</div>
			{/* File Details Modal */}
			<SourceFileModal
				isVisible={isPopupOpen}
				onClose={() => setIsPopupOpen(false)}
				fileDetails={popupContent}
			/>
		</div>
	);
};
