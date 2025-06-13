import { Modal } from 'antd';
import React, { useRef, useState } from 'react';
import { useNavigate } from 'react-router';
import { DataMapping } from '../../components/dataIngestionSteps/DataMapping';
import { ExtractBaseData } from '../../components/dataIngestionSteps/ExtractBaseData';
import FundReport from '../../components/dataIngestionSteps/FundReport';
import ProgressBar from '../../components/dataIngestionSteps/ProgressBar/ProgressBar';
import { SelectFiles } from '../../components/dataIngestionSteps/SelectFiles';
import SelectFundDate from '../../components/dataIngestionSteps/SelectFundDate/SelectFundDate';
import { UploadFiles } from '../../components/dataIngestionSteps/UploadFiles';
import { UIComponents } from '../../components/uiComponents';
import { exportBaseDataFile, getBaseDataFilesList } from '../../services/dataIngestionApi';
import { fundOptionsArray } from '../../utils/constants/constants';
import { showToast } from '../../utils/helperFunctions/toastUtils';
import { useSelector } from 'react-redux';

const ExtractNewBaseData = () => {
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
	const [extractionInProgressInModal, setExtractionInProgressInModal] = useState(false);
	const [unmappedSecurities, setUnmappedSecurities] = useState([]);
	const [showUnmappedSecuritiesModal, setShowUnmappedSecuritiesModal] = useState(false);

	const extractionStatus = useSelector((store) => store.diExtractionStatus?.inProgressStatus);

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

	const handleStartExtraction = async (e, ignoreUnmappedCheck = false) => {
		e.preventDefault();
		if (ignoreUnmappedCheck) {
			setExtractionInProgressInModal(true);
		} else {
			setExtractionInProgress(true);
		}
		try {
			const extractionResponse = await exportBaseDataFile(selectedIds.current, selectedFund, ignoreUnmappedCheck);
			console.info(extractionResponse, 'rex');
			const extractionData = extractionResponse?.data.result;
			showToast("info", extractionResponse.data.message);

			extractionInterval = setInterval(() => getExtractionStatus(extractionData), 3000);
		} catch (err) {
			console.error(err);
			showToast("error", err.response.data.message);
			if (err.response.data.result && err.response.data.result.data.length > 0) {
				setUnmappedSecurities(err.response.data.result.data);
				setShowUnmappedSecuritiesModal(true);
			}
		} finally {
			setExtractionInProgress(false);
			setExtractionInProgressInModal(false);
		}
	};
	// const handleStartExtraction = async (ignoreUnmappedCheck = false) => {
	// 	try {
	// 		setExtractionInProgress(true);
	// 		// setBaseFilePreviewData([]);
	// 		const extractionResponse = await exportBaseDataFile(selectedIds.current, selectedFund, ignoreUnmappedCheck);
	// 		console.info(extractionResponse, 'rex');
	// 		const extractionData = extractionResponse?.data.result;
	// 		showToast("info", extractionResponse.data.message);
	// 		// getExtractionStatus(9);

	// 		extractionInterval = setInterval(() => getExtractionStatus(extractionData), 3000);
	// 	} catch (err) {
	// 		console.error(err);
	// 		setExtractionInProgress(false);
	// 		showToast("error", err.response.data.message);
	// 		if (err.response.data.result && err.response.data.result.data.length > 0) {
	// 			setUnmappedSecurities(err.response.data.result.data);
	// 			setShowUnmappedSecuritiesModal(true);
	// 		}
	// 	}

	// 	// setFileExtractionLoading(false);
	// };

	return (
		<>
			<div style={{ background: '#fff', borderRadius: 8, padding: 24, margin: '12px' }}>
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
						onClick={(e) => {
							if (currentStep < stepContent.length - 1) {
								setCurrentStep(s => s + 1);
							} else {
								handleStartExtraction(e);
							}
						}}
						customStyle={{ minWidth: 100 }}
						btnDisabled={
							!(selectedDate && selectedFund !== "-- Select Fund --") ? true : extractionStatus ? true : false }
						loading={extractionInProgress}
						loadingText='Extraction started...'
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
					<div style={{display: 'flex', justifyContent: 'flex-end'}}>
						<UIComponents.Button
							onClick={() => setShowUnmappedSecuritiesModal(false)}
							text='Cancel'
						// loading={fileExtractionLoading}
						/>
						{/* <UIComponents.Button
							isFilled={true}
							btnDisabled={true}
							onClick={() => {}}
							text='Review Mapping'
						// loading={fileExtractionLoading}
						/> */}
						<UIComponents.Button
							loading={extractionInProgressInModal}
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
};

export default ExtractNewBaseData;