import { SearchOutlined, CloseOutlined } from '@ant-design/icons';
import { Input, Select } from "antd";
import React, { useEffect, useState } from "react";
import { Calender } from "../../components/calender/Calender";
import { DynamicTableComponents } from '../../components/reusableComponents/dynamicTableComponent/DynamicTableComponents';
import { UIComponents } from "../../components/uiComponents";
import { LoaderSmall } from "../../components/uiComponents/loader/loader";
import { getArchive, getBlobFilesList, updateArchiveStatus } from "../../services/dataIngestionApi";
import { fundOptionsArray } from "../../utils/constants/constants";
import { showToast } from "../../utils/helperFunctions/toastUtils";
import { FUND_BG_COLOR, STATUS_BG_COLOR } from "../../utils/styles";

export const SourceFilesTab = () => {
	// State management
	const [selectedIds, setSelectedIds] = useState([]);
	const [uploadedSourceFiles, setUploadedSourceFiles] = useState({ data: [], columns: [] });
	const [dataLoading, setDataLoading] = useState(false);
	const [isViewActive, setIsViewActive] = useState(false);
	const [showErrorsModal, setShowErrorsModal] = useState(false);
	const [validationInfoData, setValidationInfoData] = useState([]);
	const [dataIngestionFileListColumns, setDataIngestionFileListColumns] = useState([]);
	const [fund, setFund] = useState(fundOptionsArray[0].label);
	const [filteredData, setFilteredData] = useState([]);
	const [searchText, setSearchText] = useState('');
	const [reportDates, setReportDates] = useState(null);

	// Fetch source files on mount
	useEffect(() => {
		blobFilesList();
	}, []);

	const blobFilesList = async () => {
		setDataLoading(true);
		const payload = {
			"fund_type": null
		};
		try {
			const blobResponse = await getBlobFilesList(payload);
			setUploadedSourceFiles(blobResponse.data.result || { data: [], columns: [] });
		} catch (err) {
			console.error(err);
			showToast("error", err.response?.data?.message || "Error loading files");
		} finally {
			setDataLoading(false);
			setIsViewActive(false);
		}
	};

	const toggleSelection = (fileId) => {
		setSelectedIds(prev =>
			prev.includes(fileId)
				? prev.filter(id => id !== fileId)
				: [...prev, fileId]
		);
	};

	const handleViewArchived = async () => {
		setDataLoading(true);
		try {
			const res = await getArchive();
			const archiveData = res.data.result.data;
			setUploadedSourceFiles(archiveData);
		} catch (err) {
			console.error(err);
			showToast("error", err.response.data.message);
		} finally {
			setDataLoading(false);
			setIsViewActive(true);
		}
	};

	console.info(selectedIds, 'ids');
	const updateFilesArchiveStatus = async() => {
		setDataLoading(true);
		try {
			await updateArchiveStatus(selectedIds, !isViewActive);
			await blobFilesList();
		} catch (err) {
			console.error(err);
			showToast("error", err.response.data.message);
		} finally {
			setSelectedIds([]);
			setDataLoading(false);
		}
	};

	// Initialize table columns
	useEffect(() => {
		const columnsToAdd = [{
			key: 'file_select',
			label: '',
			render: (value, row) => {
				const isDisabled = ['In Progress', 'Failed'].includes(row.extraction_status);
				return (
					<div style={{ display: 'flex', alignItems: 'center' }}>
						<input
							checked={selectedIds.includes(row.file_id)}
							onChange={() => toggleSelection(row.file_id)}
							type="checkbox"
							disabled={isDisabled}
							style={{ transform: 'scale(1.3)' }}
						/>
					</div>
				);
			}
		}];

		const updatedColumns = injectRender([...columnsToAdd, ...uploadedSourceFiles.columns]);
		setDataIngestionFileListColumns(updatedColumns);
	}, [uploadedSourceFiles.columns, selectedIds]);

	// Filter data based on search
	useEffect(() => {
		const filtered = uploadedSourceFiles?.data?.filter(item =>
			item?.file_name?.toLowerCase().includes(searchText.toLowerCase())
		);
		setFilteredData(filtered);
	}, [searchText, uploadedSourceFiles]);

	// Extract report dates
	useEffect(() => {
		const reportDateList = uploadedSourceFiles?.data?.map(item => {
			if (item?.report_date) {
				return item.report_date;
			}
			return null;
		}).filter(date => date !== null);
		setReportDates(reportDateList);
	}, [uploadedSourceFiles]);

	const injectRender = (columns) => {
		return columns?.map((col) => {
			if (col.key === 'extraction_status') {
				return {
					...col,
					render: (value, row) => (
						<div>
							<span style={{
								display: 'inline-block',
								padding: '3px 7px',
								borderRadius: '8px',
								...(STATUS_BG_COLOR[row.extraction_status?.toLowerCase()] || {})
							}}>
								{row.extraction_status}
							</span>
							{row.extraction_status === 'Failed' && row.validation_info && (
								<span
									style={{ cursor: "pointer", paddingLeft: "3px" }}
									onClick={() => {
										setShowErrorsModal(true);
										setValidationInfoData(row.validation_info);
									}}
								>
									Show more
								</span>
							)}
						</div>
					)
				};
			}
			if (col.key === 'fund') {
				return {
					...col,
					render: (value, row) => (
						<div>
							{row.fund?.map((f, i) => (
								<span
									key={i}
									style={{
										display: 'inline-block',
										...(FUND_BG_COLOR[f] || {}),
										padding: '3px 7px',
										margin: '0 2px',
										borderRadius: '8px'
									}}
								>
									{f}
								</span>
							))}
						</div>
					)
				};
			}
			return col;
		});
	};

	const handleDropdownChange = (fund) => {
		if (fundOptionsArray[fund].label !== "-- Select Fund --") {
			const choosedFund = fundOptionsArray[fund].label;
			const selectedReportDateFiles = uploadedSourceFiles?.data.filter(item =>
				item.fund?.includes(choosedFund)
			);
			setFilteredData(selectedReportDateFiles || []);
		} else {
			setFilteredData(uploadedSourceFiles?.data || []);
		}
		setFund(fund);
	};

	const handleDateChange = (date, dateString) => {
		if (date) {
			const selectedReportDateFiles = uploadedSourceFiles?.data.filter(item =>
				item.report_date === dateString
			);
			setFilteredData(selectedReportDateFiles || []);
		} else {
			setFilteredData(uploadedSourceFiles?.data || []);
		}
	};

	const handleSearch = (value) => {
		setSearchText(value);
	};

	const handleClearSearch = () => {
		setSearchText('');
	};

	return (
		<div style={{ padding: '24px' }}>
			<div style={{ background: '#fff', borderRadius: 8}}>
				<div style={{ fontSize: 22, fontWeight: 600, marginBottom: 8 }}>Uploaded Source Files</div>
				<div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 8 }}>
					{/* <span style={{ fontWeight: 500 }}>Filter by:</span> */}
					<Select
						defaultValue={fundOptionsArray[0].label}
						style={{ width: 150, borderRadius: '8px', margin: "0.5rem 0rem" }}
						onChange={handleDropdownChange}
						value={fund}
						options={fundOptionsArray}
					/>
					<Calender
						fileUpload={true}
						availableClosingDates={reportDates}
						onDateChange={handleDateChange}
					/>
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
					<div style={{ flex: 1 }} />
					<UIComponents.Button
						text={isViewActive ? "View Source Files" : "View Archived"}
						customStyle={{ background: '#2966d8', color: '#fff' }}
						onClick={isViewActive ? blobFilesList : handleViewArchived}
					/>
					<UIComponents.Button
						text={isViewActive ? "Unarchive Selected" : "Archive Selected"}
						customStyle={{ background: '#ffe58f', color: '#ad6800' }}
						onClick={updateFilesArchiveStatus}
						btnDisabled={isViewActive && selectedIds.length === 0 ? true : false}
					/>
					<UIComponents.Button
						text="Delete Selected"
						customStyle={{ background: '#ff7875', color: '#fff' }}
						btnDisabled={true}
					/>
				</div>
				{dataLoading ? <LoaderSmall /> : (
					<DynamicTableComponents
						data={filteredData}
						columns={dataIngestionFileListColumns}
					/>
				)}
			</div>
		</div>
	);
};