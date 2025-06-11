import { UploadOutlined, SearchOutlined, CloseOutlined } from '@ant-design/icons';
import { Checkbox, Upload, Input } from 'antd';
import React, { useEffect, useState } from 'react';
import { DynamicTableComponents } from '../reusableComponents/dynamicTableComponent/DynamicTableComponents';
import { UIComponents } from '../uiComponents';
import { showToast } from '../../utils/helperFunctions/toastUtils';
import { getBlobFilesList } from '../../services/dataIngestionApi';
import { FUND_BG_COLOR, STATUS_BG_COLOR } from '../../utils/styles';
import { LoaderSmall } from '../uiComponents/loader/loader';
import FundReport from './FundReport';

export const UploadFiles = ({ uploadedFiles, setUploadedFiles, selectedFund, selectedDate }) => {
	const [showUploader, setShowUploader] = useState(false);
	const [dataLoading, setDataLoading] = useState(false);
	const [showErrorsModal, setShowErrorsModal] = useState(false);
	const [validationInfoData, setValidationInfoData] = useState([]);
	const [dataIngestionFileListColumns, setDataIngestionFileListColumns] = useState([]);
	const [searchText, setSearchText] = useState('');
	const [filteredData, setFilteredData] = useState([]);

	useEffect(() => {
		blobFilesList(selectedFund, selectedDate);
	}, [selectedFund]);

	useEffect(() => {
		const filtered = uploadedFiles?.data?.filter(item =>
			item?.file_name?.toLowerCase().includes(searchText.toLowerCase())
		);
		setFilteredData(filtered);
	}, [searchText, uploadedFiles]);

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
							{row.extraction_status === 'Failed' && row.validation_info &&
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
			const blobResponse = await getBlobFilesList(fundType, reportDate);
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

	const handleFiles = (fileList) => {
		if (fileList && fileList.length > 0) {
			setUploadedFiles(prev => [...prev, ...fileList]);
		}
	};

	const handleSearch = (value) => {
		setSearchText(value);
	};

	const handleClearSearch = () => {
		setSearchText('');
	};

	const UploaderSection = () => (
		<div
			style={{
				border: '1px dashed #d9d9d9',
				borderRadius: 8,
				padding: 12,
				textAlign: 'center',
			}}
		>
			<Upload.Dragger
				multiple
				showUploadList={false}
				beforeUpload={() => false}
				onChange={({ fileList }) => handleFiles(fileList)}
			>
				<p style={{ color: '#aaa', fontSize: 32, margin: 0 }}>
					<UploadOutlined />
				</p>
				<p>Drag and drop your files here, or</p>
				<UIComponents.Button text="Browse Files" />
			</Upload.Dragger>
		</div>
	);

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

			{showUploader && <UploaderSection />}

			{dataLoading ? <LoaderSmall /> :
				<div style={{padding: '25px', background: 'rgb(245, 245, 245)', borderRadius: '5px' }}>
					<div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '7px' }}>
						<h3 style={{fontWeight: 'bold', fontSize: 'large', margin: 0}}>Uploaded files</h3>
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
					<div style={{margin: '10px 0'}}>
						<DynamicTableComponents data={filteredData} columns={dataIngestionFileListColumns} />
					</div>
				</div>
			}
		</>
	);
};