import { SearchOutlined, CloseOutlined } from '@ant-design/icons';
import { Input } from 'antd';
import React, { useEffect, useState } from 'react';
import { DynamicTableComponents } from '../reusableComponents/dynamicTableComponent/DynamicTableComponents';
import { FUND_BG_COLOR, STATUS_BG_COLOR } from '../../utils/styles';

export const SelectFiles = ({ uploadedFiles, selectedFiles, setSelectedFiles, selectedIds }) => {

	const [searchText, setSearchText] = useState('');
	const [showErrorsModal, setShowErrorsModal] = useState(false);
	const [validationInfoData, setValidationInfoData] = useState([]);
	const [filteredData, setFilteredData] = useState([]);
	const [dataIngestionFileListColumns, setDataIngestionFileListColumns] = useState([]);
	const [filesSelected, setFilesSelected] = useState(0);

	useEffect(() => {
		const columnsToAdd = [{
			'key': 'file_select',
			'label': '',
			'render': (value, row) => {
				const isDisabled = row['extraction_status'] === 'In Progress' || row['extraction_status'] === 'Failed';
				return (
					<div style={{display: 'flex', alignItems: 'center'}}>
						<input
							checked={selectedIds.current.includes(row.file_id)}
							onClick={() => handleCheckboxClick(row.file_id)}
							type="checkbox"
							disabled={isDisabled}
							style={{transform: 'scale(1.2)'}}
						/>
					</div>
				);
			}
		}];
		let updatedColumns = [...columnsToAdd, ...uploadedFiles.columns];
		updatedColumns = injectRender(updatedColumns);
		setDataIngestionFileListColumns(updatedColumns);
	}, []);

	useEffect(() => {
		const filtered = uploadedFiles?.data?.filter(item =>
			item?.file_name?.toLowerCase().includes(searchText.toLowerCase())
		);
		setFilteredData(filtered);
	}, [searchText, uploadedFiles]);

	const handleCheckboxClick = (fileId) => {
		if (selectedIds?.current.indexOf(fileId) === -1) {
			// setSelectedIds([...selectedIds, fileId]);
			selectedIds.current = [...selectedIds.current, fileId];
			// setFilesSelected(selectedIds.current.length);
			// setSelectedIds([...selectedIds, fileId]);
		} else {
			selectedIds.current = selectedIds?.current.filter(id => id !== fileId);
			// setFilesSelected(selectedIds.current.length);
			// setSelectedIds(selectedIds.filter(id => id !== fileId));
		}
		console.info('sel ids', selectedIds);
	};

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

	return (
		<div>
			<div style={{ fontWeight: 600, fontSize: 18, marginBottom: 16 }}>Select files for extraction</div>
			<div style={{padding: '25px', background: 'rgb(245, 245, 245)', borderRadius: '5px' }}>
				<div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '7px' }}>
					<h3 style={{fontWeight: 'bold', fontSize: 'large', margin: 0}}>Available files</h3>
				</div>
				<div style={{margin: '10px 0'}}>
					<DynamicTableComponents data={filteredData} columns={dataIngestionFileListColumns} />
				</div>
			</div>
		</div>
	);
};