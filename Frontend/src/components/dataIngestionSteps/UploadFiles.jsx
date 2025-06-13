import { SearchOutlined, CloseOutlined } from '@ant-design/icons';
import { Checkbox, Input } from 'antd';
import React, { useEffect, useState } from 'react';
import { useDispatch } from 'react-redux'
import { setExtractionStatus } from '../../redux/slices/uploadFileStatus';
import { getBlobFilesList, uploadNewFile } from '../../services/dataIngestionApi';
import { showToast } from '../../utils/helperFunctions/toastUtils';
import { FUND_BG_COLOR, STATUS_BG_COLOR } from '../../utils/styles';
import { DynamicFileUploadComponent } from '../reusableComponents/dynamicFileUploadComponent/DynamicFileUploadComponent';
import { DynamicTableComponents } from '../reusableComponents/dynamicTableComponent/DynamicTableComponents';
import { UIComponents } from '../uiComponents';
import { LoaderSmall } from '../uiComponents/loader/loader';

export const UploadFiles = ({ uploadedFiles, setUploadedFiles, selectedFund, selectedDate }) => {
	const [showUploader, setShowUploader] = useState(false);
	const [dataLoading, setDataLoading] = useState(false);
	const [showErrorsModal, setShowErrorsModal] = useState(false);
	const [validationInfoData, setValidationInfoData] = useState([]);
	const [dataIngestionFileListColumns, setDataIngestionFileListColumns] = useState([]);
	const [searchText, setSearchText] = useState('');
	const [filteredData, setFilteredData] = useState([]);
	const [fileUploaded, setFileUploaded] = useState([]);
	const [fileUploading, setFileUploading] = useState(false);
	const [errorMessage, setErrorMessage] = useState(null);
	const [extractionInProgress, setExtractionInProgress] = useState(false);

	const dispatch = useDispatch();

	useEffect(() => {
		blobFilesList(selectedFund, selectedDate);
	}, [selectedFund]);

	useEffect(() => {
		const filtered = uploadedFiles?.data?.filter(item =>
			item?.file_name?.toLowerCase().includes(searchText.toLowerCase())
		);
		setFilteredData(filtered);
	}, [searchText, uploadedFiles]);

	useEffect(() => {
		if (extractionInProgress) {
			showToast('info', 'Please wait while extraction is in progress.');
			dispatch(setExtractionStatus(true));
			const intervalRef = { current: null };
			intervalRef.current = setInterval(async() => {
				const payload = {
					"fund_type": selectedFund,
					"report_date": selectedDate?.format('MM-DD-YYYY')
				};
				const fileresponse = await getBlobFilesList(payload);
				const responseData = fileresponse.data.result;
				const inProgressCount = responseData.data.slice(0, fileUploaded.length).filter(r => !['completed', 'failed'].includes(r.extraction_status.toLowerCase())).length;
				console.log('File check interval running');
				if (inProgressCount == 0) {
					clearInterval(intervalRef.current);
					setDataLoading(true);
					setUploadedFiles(responseData);
					let updatedColumns = [...responseData.columns];
					updatedColumns = injectRender(updatedColumns);
					setDataIngestionFileListColumns(updatedColumns);
					dispatch(setExtractionStatus(false));
					console.log('File check interval completed but running');
					showToast('success', 'All files extraction completed. Please refresh page.');
					setExtractionInProgress(false);
					setDataLoading(false);
					setFileUploaded([]);
				}
			}, 5000);
			return () => {
				// Cleanup the interval on component unmount
				if (intervalRef.current) {
					clearInterval(intervalRef.current);
				}
			};
		}
	}, [extractionInProgress]);

	const injectRender = (columns) => {
		return columns?.map((col) => {
			if (col.key === 'extraction_status') {
				return {
					...col,
					render: (value, row) => (
						<div>
							<span style={{display: 'inline-block', padding: '3px 7px', borderRadius: '8px', ...(STATUS_BG_COLOR[row.extraction_status.toLowerCase()] || {backgroundColor: 'gray', color: 'white'})}}>
								{row.extraction_status}
							</span>
							{row.extraction_status === 'Failed' && row.validation_info.length > 0 &&
								<span
									style={{cursor: "pointer", paddingLeft: "3px"}}
									onClick={() => {
										const recordData = Object.entries(row);
										recordData.forEach((data) => {
											if (data[0] === "validation_info") {
												setShowErrorsModal(true);
												setValidationInfoData(data[1]);
											}
										});
									}}
								>
									Show more
								</span>
							}
						</div>
					)
				};
			}
			if (col.key === 'fund') {
				return {
					...col,
					render: (value, row) => (
						<div>
							{row.fund.map((f, i) => {
								return (
									<span key={i} style={{display: 'inline-block', ...(FUND_BG_COLOR[f] || { backgroundColor: 'gray', color: 'white'}), padding: '3px 7px', margin: '0 2px', borderRadius: '8px'}}>
										{f}
									</span>
								);
							})}
						</div>
					)
				};
			}
			return col;
		});
	};

	const blobFilesList = async(fundType, reportDate) => {
		try {
			setDataLoading(true);
			const payload = {
				"fund_type": fundType,
				"report_date": reportDate?.format('MM-DD-YYYY')
			};
			const blobResponse = await getBlobFilesList(payload);
			const responseData = blobResponse.data.result;
			setUploadedFiles(responseData);

			let updatedColumns = [...responseData.columns];
			updatedColumns = injectRender(updatedColumns);
			setDataIngestionFileListColumns(updatedColumns);
			setDataLoading(false);
		} catch (err) {
			console.error(err);
			showToast("error", err.response.data.message);
			setDataLoading(false);
		}
	};

	const handleSearch = (value) => {
		setSearchText(value);
	};

	const handleClearSearch = () => {
		setSearchText('');
	};

	const handleUploadFile = async () => {
		setFileUploading(true);
		setErrorMessage(null);
		try {
			await uploadNewFile(fileUploaded, selectedDate, selectedFund);
			showToast('success', "File upload and extraction is in progress, it may take few minutes");
			await blobFilesList(selectedFund, selectedDate);
			setExtractionInProgress(true);
			setShowUploader(false);
		} catch (error) {
			showToast('error', error?.response?.data.message);
			setErrorMessage(error?.response?.data.message);
		} finally {
			setFileUploading(false);
		}
	};

	return (
		<>
			<div style={{ display: 'flex', alignItems: 'center', marginBottom: 8, padding: '0 7px' }}>
				<Checkbox
					style={{ transform: 'scale(1.3)', marginRight: "1rem"}}
					checked={showUploader}
					onChange={() => setShowUploader(!showUploader)}
				/>
				<span style={{ fontWeight: 600, fontSize: 18 }}>
					Upload source files
				</span>
			</div>

			{showUploader &&
				<div style={{margin: '12px 0 20px'}}>
					<div>
						<DynamicFileUploadComponent
							uploadedFiles={fileUploaded}
							setUploadedFiles={setFileUploaded}
							supportedFormats={['csv', 'xlsx', 'xlsm']}
							showDownload={false}
							fundType={selectedFund}
						/>
					</div>
					<div style={{display: 'flex', justifyContent: 'space-between', margin: '3px 0'}}>
						{errorMessage ? <p style={{color: 'red', fontSize: 'small'}}>*{errorMessage}</p> : <div></div>}
						<UIComponents.Button
							onClick = {handleUploadFile}
							text = 'Upload'
							loading = {fileUploading}
							loadingText = 'Uploading...'
							btnDisabled = {fileUploaded.length > 0 ? false : true}
						/>
					</div>
				</div>
			}

			{dataLoading ? <LoaderSmall /> :
				<div style={{padding: '25px', background: 'rgb(245, 245, 245)', borderRadius: '5px' }}>
					<div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '7px' }}>
						<h3 style={{fontWeight: 'bold', fontSize: 'large', margin: 0}}>Uploaded Source Files</h3>
						<div style={{display: 'flex', gap: 12}}>
							{extractionInProgress && <LoaderSmall />}
							<Input
								placeholder="Search by file name"
								value={searchText}
								onChange={(e) => handleSearch(e.target.value)}
								style={{ width: 200 }}
								suffix={
									searchText ?
										<CloseOutlined style={{ cursor: 'pointer' }} onClick={handleClearSearch} /> :
										<SearchOutlined />
								}
							/>
						</div>
					</div>
					<div style={{margin: '10px 0'}}>
						<DynamicTableComponents data={filteredData} columns={dataIngestionFileListColumns} />
					</div>
				</div>
			}
		</>
	);
};