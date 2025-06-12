import { Modal, Select } from "antd";
import { useEffect, useRef, useState, React } from "react";
import { useNavigate } from "react-router";
import { Calender } from "../../components/calender/Calender";
import { DataMapping } from "../../components/dataIngestionSteps/DataMapping";
import { ExtractBaseData } from "../../components/dataIngestionSteps/ExtractBaseData";
import FundReport from "../../components/dataIngestionSteps/FundReport";
import ProgressBar from "../../components/dataIngestionSteps/ProgressBar/ProgressBar";
import { SelectFiles } from "../../components/dataIngestionSteps/SelectFiles";
import SelectFundDate from "../../components/dataIngestionSteps/SelectFundDate/SelectFundDate";
import { UploadFiles } from "../../components/dataIngestionSteps/UploadFiles";
import { DynamicTableComponents } from "../../components/reusableComponents/dynamicTableComponent/DynamicTableComponents";
import { UIComponents } from "../../components/uiComponents";
import { LoaderSmall } from "../../components/uiComponents/loader/loader";
import { exportBaseDataFile, getBaseDataFilesList } from "../../services/dataIngestionApi";
import { fundMap, fundOptionsArray } from "../../utils/constants/constants";
import { showToast } from "../../utils/helperFunctions/toastUtils";
import { FUND_BG_COLOR, STATUS_BG_COLOR } from "../../utils/styles";


export const BaseDataTab = () => {
	// Extract New Base Data
	const [isExtractionMode, setIsExtractionMode] = useState(false);
	const [currentStep, setCurrentStep] = useState(0);
	const [selectedFund, setSelectedFund] = useState(fundOptionsArray[0].label);
	const [selectedDate, setSelectedDate] = useState(null);

	const [selectedFiles, setSelectedFiles] = useState([]);
	const [uploadedFiles, setUploadedFiles] = useState([]);
	const selectedIds = useRef([]);

	const stepContent = [
		<SelectFundDate
			key="step1"
			selectedFund={selectedFund}
			setSelectedFund={setSelectedFund}
			selectedDate={selectedDate}
			setSelectedDate={setSelectedDate}
		/>,
		<UploadFiles
			key="step2"
			selectedFund={selectedFund}
			selectedDate={selectedDate}
			uploadedFiles={uploadedFiles}
			setUploadedFiles={setUploadedFiles}
		/>,
		<SelectFiles
			key="step3"
			uploadedFiles={uploadedFiles}
			selectedFiles={selectedFiles}
			setSelectedFiles={setSelectedFiles}
			selectedIds={selectedIds}
		/>,
		<DataMapping
			key="step4"
			selectedFund={selectedFund}
			selectedDate={selectedDate}
			selectedFiles={selectedFiles}
		/>,
		<ExtractBaseData
			key="step5"
			selectedIds={selectedIds}
			uploadedFiles={uploadedFiles}
		/>
	];

	const [extractionInProgress, setExtractionInProgress] = useState(false);
	const [unmappedSecurities, setUnmappedSecurities] = useState([]);
	const [showUnmappedSecuritiesModal, setShowUnmappedSecuritiesModal] = useState(false);

	const navigate = useNavigate();
	let extractionInterval;

	const getExtractionStatus = async (extractData) => {
		try {
			const extractionStatusRes = await getBaseDataFilesList(extractData);
			const extractionStatus = extractionStatusRes.data.result.data[0].extraction_status;
			console.info(extractionStatus, 'status');
			if (extractionStatus !== "In progress") {
				console.info(extractionStatus, 'conditionn entered');
				clearInterval(extractionInterval);
			}
			if (extractionStatus === "Completed" ) {
				setExtractionInProgress(false);
				navigate(`/data-ingestion/base-data-preview/${extractData.id}`);
				return true;
			}
			setExtractionInProgress(false);
		} catch (err) {
			setExtractionInProgress(false);
			showToast('failure', err?.response?.data.message);
		}

		return false;

	};

	const handleStartExtraction = async (ignoreUnmappedCheck = false) => {
		try {
			setExtractionInProgress(true);
			// setBaseFilePreviewData([]);
			const extractionResponse = await exportBaseDataFile(selectedIds.current, selectedFund, ignoreUnmappedCheck);
			console.info(extractionResponse, 'rex');
			const extractionData = extractionResponse?.data.result;
			showToast("info", extractionResponse.data.message);
			// getExtractionStatus(9);

			extractionInterval = setInterval(() => getExtractionStatus(extractionData), 3000);
		} catch (err) {
			console.error(err);
			setExtractionInProgress(false);
			showToast("error", err.response.data.message);
			if (err.response.data.result && err.response.data.result.data.length > 0) {
				setUnmappedSecurities(err.response.data.result.data);
				setShowUnmappedSecuritiesModal(true);
			}
		}

		// setFileExtractionLoading(false);
	};

	if (isExtractionMode) {
		return (
			<>
				<div style={{ background: '#fff', borderRadius: 8, padding: 24 }}>
					<div style={{ marginBottom: 24 }}>
						<div style={{ fontSize: 24, fontWeight: 600 }}>Extract new Base Data</div>
					</div>
					<ProgressBar currentStep={currentStep} />
					{currentStep !== 0 &&
						<FundReport selectedDate={selectedDate} selectedFund={selectedFund} />
					}
					<div style={{ minHeight: 240 }}>{stepContent[currentStep]}</div>
					<div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 32 }}>
						<UIComponents.Button
							text="Back"
							disabled={currentStep === 0}
							btnDisabled={currentStep === 0 ? true : false}
							onClick={() => setCurrentStep(s => s - 1)}
							customStyle={{ minWidth: 100 }}
						/>
						<UIComponents.Button
							text={currentStep === stepContent.length - 1 ? 'Start Extraction' : 'Next'}
							isFilled={true}
							onClick={() => {
								if (currentStep < stepContent.length - 1) {
									setCurrentStep(s => s + 1);
								} else {
									handleStartExtraction();
								}
							}}
							customStyle={{ minWidth: 100 }}
							btnDisabled={(selectedDate && selectedFund !== "-- Select Fund --") ? false : true }
							loading={extractionInProgress}
						/>
					</div>
				</div>
				<Modal title={""} open={showUnmappedSecuritiesModal} footer={null} onCancel={() => setShowUnmappedSecuritiesModal(false)} style={{marginTop: '-50px'}}>
					{unmappedSecurities.length > 0 &&
					<div>
						<p>{unmappedSecurities.length} unmapped securities</p>
						<ol>
							{unmappedSecurities.map((item, index) => {
								if (item) {
									return <li key={index}>{item.asset} [{item.type}]</li>;
								}
							})}
						</ol>
						<div>
							<UIComponents.Button
								onClick={() => setExtractionInProgress(false)}
								text='Cancel'
							// loading={fileExtractionLoading}
							/>
							<UIComponents.Button
								isFilled={true}
								btnDisabled={true}
								onClick={() => {}}
								text='Review Mapping'
							// loading={fileExtractionLoading}
							/>
							<UIComponents.Button
								loading={extractionInProgress}
								loadingText='Extracting...'
								isFilled={true}
								onClick={(e) => handleStartExtraction(e, true)}
								text='Extract Base Data'
							// loading={fileExtractionLoading}
							/>
						</div>
					</div>}
				</Modal>
			</>
		);
	}

	const [reportDates, setReportDates] = useState(null);
	const [fund, setFund] = useState(fundOptionsArray[0].label);
	const [filteredData, setFilteredData] = useState([]);
	const [dataLoading, setDataLoading] = useState(false);
	const [baseDataFilesList, setBaseDataFilesList] = useState([]);

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
							onClick={() => setIsExtractionMode(true)}
						/>
					</div>
				</div>
				{dataLoading ? <LoaderSmall /> :
					<div>
						<DynamicTableComponents data={filteredData} columns={baseDataFilesList?.columns} />
					</div>
				}
			</div>
		</>
	);
};