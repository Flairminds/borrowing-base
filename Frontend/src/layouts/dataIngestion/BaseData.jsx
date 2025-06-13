import { Select } from "antd";
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router";
import { Calender } from "../../components/calender/Calender";
import { DynamicTableComponents } from "../../components/reusableComponents/dynamicTableComponent/DynamicTableComponents";
import { UIComponents } from "../../components/uiComponents";
import { LoaderSmall } from "../../components/uiComponents/loader/loader";
import { getBaseDataFilesList, getBaseFilePreviewData } from "../../services/dataIngestionApi";
import { fundMap, fundOptionsArray } from "../../utils/constants/constants";
import { showToast } from "../../utils/helperFunctions/toastUtils";
import { FUND_BG_COLOR, STATUS_BG_COLOR } from "../../utils/styles";


export const BaseDataTab = () => {
	const [reportDates, setReportDates] = useState(null);
	const [fund, setFund] = useState(fundOptionsArray[0].label);
	const [filteredData, setFilteredData] = useState([]);
	const [dataLoading, setDataLoading] = useState(false);
	const [baseDataFilesList, setBaseDataFilesList] = useState([]);

	const navigate = useNavigate();

	useEffect(() => {
		getFilesList();
	}, []);

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
									// onClick={() => handleSourceFileClick(file)}
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

	const handleBaseDataPreview = async (row) => {
		localStorage.setItem("extraction_info_id", row.id);
		if (row.extraction_status == 'failed') {
			alert(row.comments);
			return;
		}
		navigate(`/data-ingestion/base-data-preview/${row.id}`);
	};

	const columnsToAdd = [{
		'key': 'file_preview',
		'label': '',
		'render': (value, row) => <div onClick={() => handleBaseDataPreview(row)}
			style={{color: row.extraction_status.toLowerCase() === "completed" ? 'green' : 'red', cursor: 'pointer'}} title={row.extraction_status.toLowerCase() === "completed" ? 'Click to preview base data' : 'Click to view errors' } >
			{row.extraction_status.toLowerCase() === "completed" ? 'Preview Base Data' : (row.extraction_status.toLowerCase() === "failed" ? 'Errors' : '')}
		</div>
	}];

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
			setFilteredData(filesRes.data.result.data);
		} catch (err) {
			showToast('error', err?.response?.data.message);
			setDataLoading(false);
		}
	};

	const handleDateChange = (date, dateString) => {
		if (date) {
			const selectedReportDateFiles = baseDataFilesList?.data.filter(item => {
				if (fund !== "-- Select Fund --") {
					return item.report_date === dateString && item.fund === fundOptionsArray[fund].label;
				} else {
					return item.report_date === dateString;
				}
			});
			setFilteredData(selectedReportDateFiles);
		} else {
			setFilteredData(baseDataFilesList?.data);
			setFund(0);
		}
	};

	const handleDropdownChange = (fund) => {
		if ( fundOptionsArray[fund].label !== "-- Select Fund --") {
			const choosedFund = fundOptionsArray[fund].label;
			const selectedReportDateFiles = baseDataFilesList?.data.filter(item => item.fund === choosedFund);
			setFilteredData(selectedReportDateFiles);
		} else {
			setFilteredData(baseDataFilesList?.data);
		}
		setFund(fund);
	};

	const handleNewExtractBaseData = () => {
		navigate('/data-ingestion/extract-new-base-data');
	};

	return (
		<>
			<div style={{ background: '#fff', borderRadius: 8, padding: 24 }}>
				<div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 8 }}>
					<h1 style={{ fontSize: 24, fontWeight: 600 }}>Extracted Base Data</h1>
					<div style={{ display: 'flex', alignItems: "center", gap: 2 }}>
						<div style={{ padding: '0 5px 0 0' }}>
							<div style={{display: "flex", alignItems: "center", padding: "0 5px 0 7px"}}>
								<Calender
									fileUpload={true}
									availableClosingDates={reportDates}
									onDateChange={handleDateChange}
								/>
							</div>
						</div>
						<div style={{ padding: '0 5px 0 0' }}>
							<Select
								defaultValue={fundOptionsArray[0].label}
								style={{ width: 150, borderRadius: '8px', margin: "0.5rem 0rem" }}
								onChange={handleDropdownChange}
								value={fund}
								options={fundOptionsArray}
							/>
						</div>
						<UIComponents.Button
							text="+ Extract New Base Data"
							isFilled={true}
							onClick={handleNewExtractBaseData}
						/>
					</div>
				</div>
				{dataLoading ? <LoaderSmall /> :
					<div>
						<DynamicTableComponents data={filteredData} columns={baseDataFilesList?.columns} additionalColumns={columnsToAdd} />
					</div>
				}
			</div>
		</>
	);
};