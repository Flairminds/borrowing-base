import { Modal, Select, Popover } from 'antd';
import Radio from 'antd/es/radio/radio';
import { useEffect } from 'preact/hooks';
import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { useNavigate } from 'react-router';
import { toast } from 'react-toastify';
import search from "../../assets/NavbarIcons/SearchIcon.svg";
import cross from "../../assets/Portflio/cross.svg";
import fileImg from "../../assets/Portflio/file.svg";
import PCOFSampleFile from '../../assets/template File/10.31.2023_PCOF_IV_Borrowing_Base_Basedata 5.xlsx';
import PFLTSampleFile from '../../assets/template File/PFLT 09.30.24 Borrowing Base Data.xlsx';
import { ErrorMessage } from '../../modal/errorMessageModal/ErrorMessage';
import { OverWriteDataModal } from '../../modal/overWriteDataModal/OverWriteDataModal';
import { uploadedFileList, validateInitialFile, assetSelectionList } from '../../services/api';
import { fundOptionsArray } from '../../utils/constants/constants';
import { fundOptionValueToFundName } from '../../utils/helperFunctions/borrowing_base_functions';
import { showToast } from '../../utils/helperFunctions/toastUtils';
import { Calender } from '../calender/Calender';
import { ModalComponents } from '../modalComponents';
import { ProgressBar } from '../progressBar/ProgressBar';
import { DynamicTableComponents } from '../reusableComponents/dynamicTableComponent/DynamicTableComponents';
import { UIComponents } from '../uiComponents';
import stylesUload from './UploadFile.module.css';
import { fmtDateValue } from '../../utils/helperFunctions/formatDisplayData';


export const UploadFile = ({
	setIsAnalysisModalOpen,
	isAnalysisModalOpen,
	setBaseFile,
	setAssetSelectionData,
	getTrendGraphData,
	setReportDate,
	setWhatifAnalysisPerformed,
	availableClosingDates,
	fundType,
	setFundType
}) => {
	const [isModalVisible, setIsModalVisible] = useState(false);
	const [isLoaderVisible, setIsLoaderVisible] = useState(false);
	const [selectedFiles, setSelectedFiles] = useState([]);
	const [selectedUploadedFiles, setSelectedUploadedFiles] = useState([]);
	const [lastUpdatedState, setLastUpdatedState] = useState('');
	const [loading, setLoading] = useState(false);
	const [errorMessageModal, setErrorMessageModal] = useState(false);
	const [errorMessageData, setErrorMessageData] = useState('');
	const [guidePopupOpen, setGuidePopupOpen] = useState(false);
	const [progressBarPercent, setProgressBarPercent] = useState(100);
	const [fetchFileList, setFetchFileList] = useState([]);
	const [duplicateFileModalOpen, setDuplicateFileModalOpen] = useState(false);
	const [date, setDate] = useState(null);
	const [selectedOption, setSelectedOption] = useState(0);
	const [displayFetchData, setDisplayFetchData] = useState([]);
	const [searchTerm, setSearchTerm] = useState('');
	const [selectedTab, setSelectedTab] = useState('existing');
	const [filterDate, setFilterDate] = useState(null);
	const navigate = useNavigate();

	const getFileListColumns = [{
		key: "file_name",
		label: "Base File Name"
	}, {
		key: "closing_date",
		label: "Report Date"
	}, {
		key: "fund_type",
		label: "Fund"
	}, {
		key: "created_at",
		label: "Created At"
	}];

	useEffect(() => {
		if (isModalVisible) {
			setTimeout(() => {
				setGuidePopupOpen(false);
			}, 1000);
			setGuidePopupOpen(true);
		}
	}, [isModalVisible]);

	const fetchFiles = async () => {
		try {
			const response = await uploadedFileList();
			setFetchFileList(response.data.files_list);
			setDisplayFetchData(response.data.files_list);
		} catch (error) {
			console.error('Error fetching file list:', error);
		}
	};

	useEffect(() => {
		if (isAnalysisModalOpen) {
			fetchFiles();
		}
	}, [isAnalysisModalOpen]);

	const handleoverWriteFIle = async () => {
		setDuplicateFileModalOpen(false);
		try {
			if (selectedFiles.length > 0) {
				const validateResponse = await validateInitialFile(selectedFiles, date, fundType, 1);

				if (validateResponse.status === 200) {
					try {
						const res = await assetSelectionList(validateResponse.data.result.id);
						setAssetSelectionData({
							'base_data_file': `${validateResponse.data.result.file_name}`,
							'base_data_file_id': validateResponse.data.result.id,
							'user_id': validateResponse.data.result.user_id,
							'assetSelectionList': res.data
						});
						getTrendGraphData(fundType);
						navigate('/asset-selection');
						showToast('success', "File Loaded");
					} catch (err) {
						console.error(err);
					}
					setBaseFile({ id: validateResponse.data.result.id, name: selectedFiles[0].name });
					setLoading(false);
				}
			}
		} catch (err) {
			console.error(err);
			setSelectedFiles([]);
			// setIsLoaderVisible(false)
			setErrorMessageData(err.response.data.error_message);
			setErrorMessageModal(true);
		}
		// setLoading(false);
		setIsAnalysisModalOpen(false);
		// setIsModalVisible(false);
	};

	const handleOverWriteModalClose = () => {
		setLoading(false);
		setIsAnalysisModalOpen(false);
		// setIsModalVisible(false);
		setIsLoaderVisible(false);
		setDuplicateFileModalOpen(false);
		setSelectedFiles([]);
	};

	// Function not currently in use
	//   const CalculateResultsPFLT = async (validateResponse) => {
	//     setLoading(true);
	//     setIsAnalysisModalOpen(false);
	//     let selectedAssetsList = [];
	//     // for (let i = 0; i < assetSelectionData.assetSelectionList?.data.length; i++) {
	//     //     if (selectedAssets[i]) {
	//     //         selectedAssetsList.push(assetSelectionData.assetSelectionList?.data[i].Investment_Name);
	//     //     }
	//     // }

	//     try {
	//         const file_data = {
	//             'base_data_file': validateResponse.file_name,
	//             'base_data_file_id': validateResponse.data.id,
	//             'user_id': 1,
	//             'selected_assets': [],
	//         };
	//         const table_data_response = await uploadInitialFile(file_data);
	//         if (table_data_response.status === 200) {
	//             setTablesData(table_data_response?.data);
	//             setConstDate(table_data_response.data.closing_date);
	//             toast.success("Results Generated");
	//         }
	//     } catch (err) {
	//         setLoading(false);
	//         console.error(err);
	//     }
	//     setLoading(false);
	// };


	const handleFileUpload = async () => {
		// setLoading(true);

		if (!date) {
			// toast.error('Select Report date');
			showToast('error', "Select Report date");
			return;
		}

		if (!selectedOption) {
			showToast('error', "Select Fund");
			return;
		}

		setLoading(true);
		// setProgressBarPercent(1)
		// setIsLoaderVisible(true)
		const fundType = fundOptionValueToFundName(selectedOption);
		try {
			if (selectedFiles.length > 0) {
				const validateResponse = await validateInitialFile(selectedFiles, date, fundType, 0);
				// if(validateResponse.status === 200 && fundType == "PFLT")
				// {
				//   CalculateResultsPFLT(validateResponse);
				//   return
				// }
				if (validateResponse.status === 200) {
					// setProgressBarPercent(50)

					try {
						const res = await assetSelectionList(validateResponse.data.result.id);
						// setAssetSelectionData(res.data.assets_list);
						setAssetSelectionData({
							'base_data_file': `${validateResponse.data.result.file_name}`,
							'base_data_file_id': validateResponse.data.result.id,
							'user_id': validateResponse.data.result.user_id,
							'assetSelectionList': res.data
						});

						setFundType(fundOptionValueToFundName(selectedOption));
						getTrendGraphData(fundType);
						navigate('asset-selection');
						toast.success("File Loaded");
						setDate(null);
					} catch (err) {
						console.error(err);
					}

					setBaseFile({ id: validateResponse.data.result.id, name: selectedFiles[0].name });

				}
				setIsLoaderVisible(false);
			}
		} catch (err) {
			console.error(err);

			if (err.response.status == 409) {
				if (err.response.data.message == "This file already exists in the system. Do you want to replace it? You might lose what if analysis data.") {
					// setIsLoaderVisible(false)
					setDuplicateFileModalOpen(true);
					return;
				}
			} else {
				setSelectedFiles([]);
				setErrorMessageData(err.response.data.error_message);
				setErrorMessageModal(true);
			}

		}
		setLoading(false);
		// setIsModalVisible(false);
		// setIsAnalysisModalOpen(false)
	};


	const handleCancel = () => {
		setDate(null);
		// setIsModalVisible(false);
		setIsAnalysisModalOpen(false);
		setSelectedFiles([]);
		setSelectedOption(0);
	};

	const { getRootProps, getInputProps } = useDropzone({
		accept: {
			'text/csv': [],
			'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': []
		},
		multiple: true,
		onDrop: (acceptedFiles) => {
			setSelectedFiles([...selectedFiles, ...acceptedFiles]);
			setSelectedUploadedFiles([]);
			setLastUpdatedState('selectedFiles');
		}
	});

	const handleFileClick = async (fileId, fileName, userId, reportDate, fund) => {
		// setLoading(true)
		try {
			// const response = await uploadInitialFile({base_data_file_id:file_id, user_id:user_id, });
			const res = await assetSelectionList(fileId);
			if (res.status === 200) {

				setAssetSelectionData({
					'base_data_file': fileName,
					'base_data_file_id': fileId,
					'user_id': userId,
					'assetSelectionList': res.data
				});
				setFundType(fund);
				// getTrendGraphData(fund);
				navigate('asset-selection');
				setBaseFile({ name: fileName, id: fileId });
				setReportDate(reportDate);
				toast.success("File Loaded");
			}
		} catch (err) {
			console.error(err);
		}
	};

	const handleDropdownChange = (value) => {
		setSelectedOption(value);
		const fundType = value === 1 ? "PCOF" : value === 2 ? "PFLT" : null;
		const filteredData = fetchFileList.filter(file => {
			const matchesFundType = !fundType || file.fund_type === fundType;
			const matchesDate = !filterDate || file.closing_date === filterDate;
			return matchesFundType && matchesDate;
		});

		setDisplayFetchData(filteredData);
	};

	const handleDateFilterChange = (date, dateString) => {
		setFilterDate(dateString);
		const fundType = selectedOption === 1 ? "PCOF" : selectedOption === 2 ? "PFLT" : selectedOption === 2 ? "PSSL" : null;
		const filteredData = fetchFileList.filter(file => {
			const matchesDate = !dateString || fmtDateValue(file.closing_date) === fmtDateValue(dateString);
			const matchesFundType = !fundType || file.fund_type === fundType;
			return matchesDate && matchesFundType;
		});

		setDisplayFetchData(filteredData);
	};

	useEffect(() => {
		setFilterDate(null);
		setSelectedOption(0);
		setDisplayFetchData(fetchFileList);
	}, [selectedTab]);

	const handleSearch = (e) => {
		setSearchTerm(e.target.value);
		if (e.target.value == '') {
			setDisplayFetchData(fetchFileList);
		} else {
			const filteredData = fetchFileList.filter(file =>
				file.file_name.toLowerCase().includes(e.target.value.toLowerCase())
			);
			setDisplayFetchData(filteredData);
		}
	};

	return (
		<div className={stylesUload.main}>
			{isLoaderVisible ?
				<ProgressBar progressBarPercent={progressBarPercent} setProgressBarPercent={setProgressBarPercent} />
				:
				<div className={stylesUload.modalDiv} >
					<Modal
						title={<ModalComponents.Title title='Import File' showDescription={true} description='Use an existing file or upload a new base data file for borrowing base calculation.' />}
						centered
						style={{
							top: 10
						}}
						open={isAnalysisModalOpen}
						onOk={handleFileUpload}
						onCancel={handleCancel}
						width={'60%'}
						footer={[
							<ModalComponents.Footer key={'footer-buttons'} onClickCancel={handleCancel} onClickSubmit={handleFileUpload} loading={loading} submitText={'Load'} />
						]}
					>
						<div>
							<Radio.Group value={selectedTab} onChange={(e) => setSelectedTab(e.target.value)}>
								<Radio value="existing">List of existing base data files</Radio>
								<Radio value="upload">Upload a new base data file</Radio>
							</Radio.Group>
						</div>
						<div style={{ display: 'flex', flexDirection: 'row', alignItems: 'baseline' }}>
							{selectedTab === "existing" && <div style={{ padding: '0 10px 0 0' }}>Filter by</div>}
							<div style={{ padding: '0 5px 0 0' }}>
								<Calender
									key={selectedTab}
									setReportDate={setReportDate}
									setDate={setDate}
									fileUpload={true}
									setWhatifAnalysisPerformed={setWhatifAnalysisPerformed}
									availableClosingDates={availableClosingDates}
									onDateChange={selectedTab === 'existing' ? handleDateFilterChange : null}
								/>
							</div>
							<div style={{ padding: '0 5px 0 0' }}>
								<Select
									defaultValue={fundOptionsArray[0].label}
									style={{ width: 150, borderRadius: '8px', margin: "0.5rem 0rem" }}
									onChange={handleDropdownChange}
									value={selectedOption}
									onSelect={(value) => {
										setFundType(fundOptionValueToFundName(value)),
										setSelectedOption(value);
									}
									}
									options={fundOptionsArray}
								/>
							</div>
						</div>
						{selectedTab === "upload" && (
							<div className={stylesUload.container}>
								<div>
									<div style={{ marginLeft: 'auto', order: '2' }}>
										{selectedOption != 0 && (
											<Popover placement="bottomRight" open={guidePopupOpen} content={<>Refer to sample template file</>}>
												<a
													href={fundType === "PCOF" ? PCOFSampleFile : PFLTSampleFile}
													rel="noreferrer"
													download={fundType === "PCOF" ? 'PCOFBaseFile_template.xlsx' : 'PFLTBaseFile_template.xlsx'}
												>
													Download sample file template
												</a>
											</Popover>
										)}
									</div>
									<div>
										<div className={stylesUload.visible}>
											<div {...getRootProps({ className: 'dropzone' })}>
												<input {...getInputProps()} />
												<div>
													<span>
														<b>{selectedFiles.length ? selectedFiles.map((file) => file.name).join(', ') : 'Drag and drop files here, or'}</b>
													</span>
													<span
														style={{
															color: '#3B7DDD',
															textDecoration: 'underline',
															cursor: 'pointer',
															marginLeft: '5px'
														}}
													>
														Browse
													</span>
												</div>
												<p className={stylesUload.supportHeading}>Supported file format: CSV, XLSX</p>
											</div>
										</div>
									</div>
								</div>
								<div className={stylesUload.uploadedFileDiv}>
									{lastUpdatedState === 'selectedFiles' &&
										selectedFiles.map((file, index) => (
											<div className={stylesUload.dataMapping} key={index}>
											</div>
										))}
									{lastUpdatedState === 'selectedUploadedFiles' &&
										selectedUploadedFiles.map((file, index) => (
											<div className={stylesUload.dataMapping} key={index}>
												<div className={stylesUload.hoverContainer}>
													<div className={stylesUload.crossButton} onClick={() => handleRemoveFile(file)}>
														<img src={cross} alt={`Remove ${file.file_name}`} />
													</div>
													<img className={stylesUload.imgStyle} src={fileImg} alt={`Workflow ${index + 1}`} />
													<a>{file.file_name}</a>
												</div>
											</div>
										))}
								</div>
							</div>
						)}

						{selectedTab === "existing" && (
							<div className={stylesUload.existingFileDiv}>
								<div className={stylesUload.inputSearch}>
									<img src={search} alt="search" />
									<input
										type="text"
										placeholder="Search by file name"
										value={searchTerm}
										onChange={handleSearch}
										className={stylesUload.searchinputTag}
									/>
								</div>
								{searchTerm === '' || displayFetchData.length > 0 ? (
									<DynamicTableComponents
										data={displayFetchData}
										columns={getFileListColumns}
										additionalColumns={[
											{
												label: "",
												render: (value, file) => (
													<UIComponents.Button
														onClick={() => handleFileClick(file.base_data_file_id, file.file_name, file.user_id, file.closing_date, file.fund_type)}
														isFilled={true}
														text={'Use'}
													/>
												)
											}
										]}
										visibleSortHeader={true}
									/>
								) : (
									<div>No file available. Please upload a new file.</div>
								)}
							</div>
						)}
					</Modal>
				</div>
			}
			<OverWriteDataModal
				duplicateFileModalOpen={duplicateFileModalOpen}
				handleoverWriteFIle={handleoverWriteFIle}
				handleOverWriteModalClose={handleOverWriteModalClose}
			/>
			<ErrorMessage errorMessageModal={errorMessageModal} setErrorMessageModal={setErrorMessageModal} errorMessageData={errorMessageData} />
		</div>
	);
};