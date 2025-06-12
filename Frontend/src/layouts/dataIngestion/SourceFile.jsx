import { SearchOutlined, CloseOutlined } from '@ant-design/icons';
import { Input, Select } from "antd";
import { useEffect, useState, React } from "react";
import { Calender } from "../../components/calender/Calender";
import { DynamicTableComponents } from '../../components/reusableComponents/dynamicTableComponent/DynamicTableComponents';
import { UIComponents } from "../../components/uiComponents";
import { LoaderSmall } from "../../components/uiComponents/loader/loader";
import { getBlobFilesList } from "../../services/dataIngestionApi";
import { fundOptionsArray } from "../../utils/constants/constants";
import { showToast } from "../../utils/helperFunctions/toastUtils";
import { FUND_BG_COLOR, STATUS_BG_COLOR } from "../../utils/styles";

export const SourceFilesTab = () => {
	const [selectedIds, setSelectedIds] = useState([]);
	const [uploadedSourceFiles, setUploadedSourceFiles] = useState({ data: [], columns: [] });
	const [dataLoading, setDataLoading] = useState(false);

	useEffect(() => {
		blobFilesList();
	}, []);

	const blobFilesList = async () => {
		const fundType = null;
		setDataLoading(true);
		try {
			const blobResponse = await getBlobFilesList(fundType);
			setUploadedSourceFiles(blobResponse.data.result || { data: [], columns: [] });
		} catch (err) {
			console.error(err);
			showToast("error", err.response?.data?.message || "Error loading files");
		} finally {
			setDataLoading(false);
		}
	};

	const toggleSelection = (fileId) => {
		setSelectedIds(prev =>
			prev.includes(fileId)
				? prev.filter(id => id !== fileId)
				: [...prev, fileId]
		);
	};

	return (
		<div style={{ padding: '24px' }}>
			<div style={{ background: '#fff', borderRadius: 8}}>
				<div style={{ fontSize: 22, fontWeight: 600, marginBottom: 8 }}>Uploaded Source Files</div>
				{dataLoading ? <LoaderSmall /> : (
					<SourceFileTable
						uploadedFiles={uploadedSourceFiles}
						selectedIds={selectedIds}
						toggleSelection={toggleSelection}
					/>
				)}
			</div>
		</div>
	);
};

const SourceFileTable = ({ uploadedFiles, selectedIds, toggleSelection }) => {
	const [showErrorsModal, setShowErrorsModal] = useState(false);
	const [validationInfoData, setValidationInfoData] = useState([]);
	const [dataIngestionFileListColumns, setDataIngestionFileListColumns] = useState([]);

	const [fund, setFund] = useState(fundOptionsArray[0].label);
	const [filteredData, setFilteredData] = useState([]);
	const [searchText, setSearchText] = useState('');
	const [reportDates, setReportDates] = useState(null);

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

		const updatedColumns = injectRender([...columnsToAdd, ...uploadedFiles.columns]);
		setDataIngestionFileListColumns(updatedColumns);
	}, [uploadedFiles.columns, selectedIds, toggleSelection]);

	// Filter data based on search
	useEffect(() => {
		const filtered = uploadedFiles?.data?.filter(item =>
			item?.file_name?.toLowerCase().includes(searchText.toLowerCase())
		);
		setFilteredData(filtered);
	}, [searchText, uploadedFiles]);

	useEffect(() => {
		const reportDateList = uploadedFiles?.data?.map(item => {
			if (item?.report_date) {
				return item.report_date;
			}
		});
		setReportDates(reportDateList);
	}, [uploadedFiles]);

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
		if ( fundOptionsArray[fund].label !== "-- Select Fund --") {
			const choosedFund = fundOptionsArray[fund].label;
			const selectedReportDateFiles = uploadedFiles?.data.filter(item => item.fund.includes(choosedFund));
			setFilteredData(selectedReportDateFiles);
		} else {
			setFilteredData(uploadedFiles?.data);
		}
		setFund(fund);
	};

	const handleDateChange = (date, dateString) => {
		if (date) {
			const selectedReportDateFiles = uploadedFiles?.data.filter(item => {
				if (fund !== "-- Select Fund --") {
					return item.report_date === dateString;
				} else {
					return item.report_date === dateString;
				}
			});
			setFilteredData(selectedReportDateFiles);
		} else {
			setFilteredData(uploadedFiles?.data);
		}
		setFund(0);
	};

	const handleSearch = (value) => {
		setSearchText(value);
	};

	const handleClearSearch = () => {
		setSearchText('');
	};

	return (
		<>
			<div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 8 }}>
				<span style={{ fontWeight: 500 }}>Filter by:</span>
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
				<UIComponents.Button text="View Archived" customStyle={{ background: '#2966d8', color: '#fff' }} btnDisabled={true} />
				<UIComponents.Button
					text="Archive Selected"
					customStyle={{ background: '#ffe58f', color: '#ad6800' }}
					// disabled={selectedRows.length === 0}
					btnDisabled={true}
				/>
				<UIComponents.Button
					text="Delete Selected"
					customStyle={{ background: '#ff7875', color: '#fff' }}
					// disabled={selectedRows.length === 0}
					btnDisabled={true}
				/>
			</div>
			<DynamicTableComponents
				data={filteredData}
				columns={dataIngestionFileListColumns}
			/>
		</>
	);
};