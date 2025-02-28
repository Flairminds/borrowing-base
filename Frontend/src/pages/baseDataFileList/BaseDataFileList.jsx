import { Select } from 'antd';
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router';
import { CustomButton } from '../../components/custombutton/CustomButton';
import { DynamicTableComponents } from '../../components/reusableComponents/dynamicTableComponent/DynamicTableComponents';
import { SourceFileModal } from '../../modal/sourceFileModal/SourceFileModal';
import { getBaseDataFilesList, getBaseFilePreviewData } from '../../services/dataIngestionApi';
import { fundOptionsArray } from '../../utils/constants/constants';
import { showToast } from '../../utils/helperFunctions/toastUtils';
import styles from './BaseDataFileList.module.css';
import { filterPreviewData } from '../../utils/helperFunctions/filterPreviewData';
import { Loader, LoaderSmall } from '../../components/loader/loader';

export const BaseDataFileList = ({ setBaseFilePreviewData, setPreviewPageId, setPreviewFundType }) => {
	const [baseDataFilesList, setBaseDataFilesList] = useState({});
	const [extractionInProgress, setExtractionInProgress] = useState(false);
	const [isPopupOpen, setIsPopupOpen] = useState(false);
	const [popupContent, setPopupContent] = useState(null);
	const [selectedFundType, setSelectedFundType] = useState(0);
	const [dataLoading, setDataLoading] = useState(false);

	const navigate = useNavigate();

	const handleExtractNew = () => {
		navigate('/ingestion-files-list');
	};

	const handleSecurityMapping = () => {
		navigate('/security-mapping');
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
					otherInfo: result.other_info
				});
			setPreviewPageId(row.id);
			setPreviewFundType(row.fund);
			navigate(`/base-data-preview/${row.id}`);
		} catch (err) {
			showToast("error", err.response.data.message);
			setDataLoading(false);
		}
	};

	const columnsToAdd = [{
		'key': 'file_preview',
		'label': '',
		'render': (value, row) => <div onClick={() => handleBaseDataPreview(row)}
			style={{color: '#0EB198', cursor: 'pointer'}}>
			{row.extraction_status === "completed" ? 'Preview Base Data' : (row.extraction_status === "failed" ? 'Errors' : '')}
		</div>
	}];


	const injectRenderForSourceFiles = (columns) => {
		return columns?.map((col) => {
			if (col.key === 'source_files') {
				return {
					...col,
					render: (value, row) => (
						<div>
							{row.source_file_details?.map((file) => (
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
									{file.file_name + file.extension}
								</div>
							))}
						</div>
					)
				};
			}
			return col;
		});
	};

	const handleSourceFileClick = (fileDetails) => {
		setPopupContent(fileDetails); // Pass only the clicked file's details
		setIsPopupOpen(true);
	};

	const getFilesList = async (fundType) => {
		const Fund = (fundType === 1) ? 'PCOF' : (fundType === 2) ? 'PFLT' : undefined;
		try {
			setDataLoading(true);
			const data = {
				"company_id": 1,
				"fund_type": Fund
			};
			const filesRes = await getBaseDataFilesList(data);
			const updatedColumns = injectRenderForSourceFiles(filesRes.data.result.columns);
			setBaseDataFilesList({ ...filesRes.data.result, columns: updatedColumns });
			setDataLoading(false);
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

	return (
		<div className={styles.pageContainer}>
			<div className={styles.baseFileListPage}>
				<div className={styles.headerContainer}>
					<div className={styles.tableHeading}>
						Extracted Base Data
					</div>
					<div className={styles.buttonsContainer}>
						<div style={{margin: 'auto'}}>
							<Select
								defaultValue="Select Fund"
								style={{ width: 140, borderRadius: '8px'}}
								options={fundOptionsArray}
								onChange={handleDropdownChange}
							/>
						</div>
						<CustomButton isFilled={true} onClick={handleSecurityMapping} text="Security Mapping" />
						<CustomButton isFilled={true} onClick={handleExtractNew} text="Extract New Base Data" />
					</div>
				</div>
				{dataLoading ? <Loader /> :
					<div className={styles.baseDataTableContainer}>
						<DynamicTableComponents data={baseDataFilesList?.data} columns={baseDataFilesList?.columns} additionalColumns={columnsToAdd} />
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
