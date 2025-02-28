import React, { useEffect, useRef, useState } from 'react';
import { Route, Routes } from 'react-router';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import './app.css';
import { PageLayout } from './layouts/pageLayout/PageLayout';
import { AssetSelectionPage } from './pages/assetSelection/AssetSelectionPage';
import { BaseDataFileList } from './pages/baseDataFileList/BaseDataFileList';
import { BorrowingBasePreviewPage } from './pages/borrowingBasePreview/BorrowingBasePreviewPage';
import { Dashboard } from './pages/dashboard/Dashboard';
import { DataIngestionPage } from './pages/dataIngestion/DataIngestionPage';
import { SecurityMapping } from './pages/securityMapping/SecurityMapping';
import { ConcentrationTestMaster } from './pages/testMaster/ConcentrationTestMaster';
import { landingPageData } from './services/api';
import { previousSelectedAssetsArray } from './utils/helperFunctions/getSelectedAssets';
import { SecurityMappingPage } from './pages/securityMappingPage/SecurityMappingPage';



export function App() {

	const [tablesData, setTablesData] = useState(null);
	const [reportDate, setReportDate] = useState();
	const [constDate, setConstDate] = useState();
	const [availableClosingDates, setAvailableClosingDates] = useState();
	const [baseFile, setBaseFile] = useState({
		name: '',
		id: ''
	});
	const [isAnalysisModalOpen, setIsAnalysisModalOpen] = useState(false);
	const [fundType, setFundType] = useState("");
	const [assetSelectionData, setAssetSelectionData] = useState([]);
	const [selectedAssets, setSelectedAssets] = useState(assetSelectionData?.assetSelectionList?.data ? previousSelectedAssetsArray(assetSelectionData?.assetSelectionList?.data) : []);
	const [dataIngestionFileList, setDataIngestionFileList] = useState();
	const [baseFilePreviewData, setBaseFilePreviewData] = useState([]);
	const [previewPageId, setPreviewPageId] = useState(-1);
	const [previewFundType, setPreviewFundType] = useState("");

	// const [selectedIds, setSelectedIds] = useState([]);
	const selectedIds = useRef([]);

	const getLandingPageData = async() => {
		try {
			const res = await landingPageData(1);
			if (res.status == 200) {
				setConstDate(res.data.closing_date);
				setAvailableClosingDates(res.data.closing_dates);
				setTablesData(res.data);
				setReportDate(res.data.closing_date);
				setFundType(res.data.fund_name);
				setBaseFile({name: res.data.file_name, id: res.data.base_data_file_id});
			}
		} catch (err) {
			if (err.response.status == 404) {
				setIsAnalysisModalOpen(true);
			}
			console.error(err);
		}
	};

	useEffect(() => {
		setSelectedAssets(assetSelectionData?.assetSelectionList?.data ? previousSelectedAssetsArray(assetSelectionData?.assetSelectionList?.data) : []);
	}, [assetSelectionData]);


	return (
		<>
			<Routes>
				<Route path='/' element={<PageLayout />}>
					<Route path='/'
						element={
							<Dashboard
								constDate={constDate}
								setConstDate={setConstDate}
								tablesData={tablesData}
								setTablesData={setTablesData}
								reportDate={reportDate}
								setReportDate={setReportDate}
								baseFile={baseFile}
								setBaseFile={setBaseFile}
								isAnalysisModalOpen={isAnalysisModalOpen}
								setIsAnalysisModalOpen={setIsAnalysisModalOpen}
								availableClosingDates={availableClosingDates}
								fundType={fundType}
								setFundType={setFundType}
								setAssetSelectionData={setAssetSelectionData}
								getLandingPageData={getLandingPageData}
							/>
						}
					/>
					<Route path='/fund-setup' element={<ConcentrationTestMaster />} />
					<Route path='/asset-selection'
						element={
							<AssetSelectionPage
								baseFile={baseFile}
								setBaseFile={setBaseFile}
								setTablesData={setTablesData}
								setAssetSelectionData={setAssetSelectionData}
								assetSelectionData={assetSelectionData}
								selectedAssets={selectedAssets}
								setSelectedAssets={setSelectedAssets}
								setIsAnalysisModalOpen={setIsAnalysisModalOpen}
								setConstDate={setConstDate}
								fundType={fundType}
							/>
						}
					/>
					<Route path='/ingestion-files-list'
						element={
							<DataIngestionPage
								dataIngestionFileList={dataIngestionFileList}
								setDataIngestionFileList={setDataIngestionFileList}
								baseFilePreviewData={baseFilePreviewData}
								setBaseFilePreviewData= {setBaseFilePreviewData}
								selectedIds={selectedIds}
								// setSelectedIds={setSelectedIds}
							/>
						}
					/>
					<Route path='/base-data-list'
						element={
							<BaseDataFileList
								setBaseFilePreviewData={setBaseFilePreviewData}
								setPreviewPageId={setPreviewPageId}
								setPreviewFundType={setPreviewFundType}
							/>
						}
					/>
					<Route path='/base-data-preview/:infoId'
						element={
							<BorrowingBasePreviewPage
								baseFilePreviewData={baseFilePreviewData}
								setBaseFilePreviewData={setBaseFilePreviewData}
								previewPageId={previewPageId}
								previewFundType={previewFundType}
							/>
						}
					/>
					<Route path='/security-mapping' element={<SecurityMappingPage />} />
					<Route path='/securities-mapping' element={<SecurityMapping />} />
				</Route>
			</Routes>
			<ToastContainer />
		</>
	);
}