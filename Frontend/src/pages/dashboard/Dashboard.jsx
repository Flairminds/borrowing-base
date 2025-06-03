import { useEffect } from 'preact/hooks';
import React, { useState } from 'react';
import { PortfollioDashboard } from '../../components/portfollioDashboard/PortfollioDashboard';
import { TableGraph } from '../../components/tableGraph/TableGraph';
import { ConcentrationTestTable } from '../../layouts/dashboardLayouts/concentrationTestTable/ConcentrationTestTable';
import { PrincipleObligationTable } from '../../layouts/dashboardLayouts/PrincipleObligationTable/PrincipleObligationTable';
import { WhatIfAnalysis } from '../../layouts/dashboardLayouts/whatIfAnalysis/WhatIfAnalysis';
import { lineChartData } from '../../services/api';
import styles from './dashboard.module.css';
import { Loader } from '../../components/uiComponents/loader/loader';
// import { AssetSelectionPage } from '../../pages/assetSelection/AssetSelectionPage';
// import { previousSelectedAssetsArray } from '../../utils/helperFunctions/getSelectedAssets';


export const Dashboard = ({
	constDate,
	setConstDate,
	tablesData,
	setTablesData,
	setReportDate,
	reportDate,
	baseFile,
	setBaseFile,
	isAnalysisModalOpen,
	setIsAnalysisModalOpen,
	availableClosingDates,
	fundType,
	setFundType,
	setAssetSelectionData,
	getLandingPageData,
	whatifAnalysisPerformed,
	setWhatifAnalysisPerformed,
	selectedFund,
	setSelectedFund,
	setAvailableClosingDates,
	gettingDashboardData,
	setGettingDashboardData,
	gettingDates,
	setGettingDates,
	currentFund,
	setCurrentFund
}) => {

	const [trendGraphData, setTrendGraphData] = useState([]);
	// const [assetSelectionData, setAssetSelectionData] = useState([]);
	// const [selectedAssets, setSelectedAssets] = useState(assetSelectionData?.assetSelectionList?.data ? previousSelectedAssetsArray(assetSelectionData?.assetSelectionList?.data) : []);
	const [whatIfAnalysisListData, setWhatIfAnalysisListData ] = useState([]);

	useEffect(() => {
		if(fundType){
			getTrendGraphData(fundType);
		}
		if (!tablesData) {
			getLandingPageData();
		}
	}, [fundType, tablesData]);

	const getTrendGraphData = async(fund) => {
		try {
			const response = await lineChartData(1, fund);
			if (response.status == 200) {
				setTrendGraphData(response.data);
			}
		} catch (err) {
			console.error(err);
		}
	};

	return (
		<div className={styles.rootContainer}>
			<WhatIfAnalysis
				constDate={constDate}
				reportDate={reportDate}
				setReportDate={setReportDate}
				baseFile={baseFile}
				setTablesData={setTablesData}
				setWhatifAnalysisPerformed={setWhatifAnalysisPerformed}
				getTrendGraphData={getTrendGraphData}
				setBaseFile={setBaseFile}
				setTrendGraphData={setTrendGraphData}
				setAssetSelectionData={setAssetSelectionData}
				isAnalysisModalOpen={isAnalysisModalOpen}
				setIsAnalysisModalOpen={setIsAnalysisModalOpen}
				availableClosingDates={availableClosingDates}
				whatIfAnalysisListData={whatIfAnalysisListData}
				setWhatIfAnalysisListData={setWhatIfAnalysisListData}
				fundType={fundType}
				setFundType={setFundType}
				selectedFund={selectedFund}
				setSelectedFund={setSelectedFund}
				setAvailableClosingDates={setAvailableClosingDates}
				setGettingDashboardData={setGettingDashboardData}
				gettingDates={gettingDates}
				setGettingDates={setGettingDates}
				currentFund={currentFund}
				setCurrentFund={setCurrentFund}
			/>
			{gettingDashboardData ? <Loader/> :
				<div style={{display: 'flex', flexDirection: 'column', gap: '20px'}}>
					<PortfollioDashboard
						reportDate={reportDate}
						setReportDate={setReportDate}
						tablesData={tablesData}
						setTablesData={setTablesData}
						trendGraphData={trendGraphData}
						baseFile={baseFile}
						getTrendGraphData={getTrendGraphData}
						setWhatifAnalysisPerformed={setWhatifAnalysisPerformed}
						whatifAnalysisPerformed={whatifAnalysisPerformed}
						setBaseFile={setBaseFile}
						availableClosingDates={availableClosingDates}
						fundType={fundType}
						selectedFund={selectedFund}
						gettingDashboardData={gettingDashboardData}
						currentFund={currentFund}
					/>
					<TableGraph title="Segmentation Overview" tableData={tablesData?.segmentation_overview_data} tableColumns={tablesData?.segmentation_overview_data?.columns[0]?.data} chartsData={tablesData?.segmentation_chart_data?.segmentation_chart_data} yAxis= {tablesData?.segmentation_chart_data?.x_axis} />
					<TableGraph title="Security" tableData={tablesData?.security_data} tableColumns={tablesData?.security_data?.columns[0]?.data} chartsData={tablesData?.security_chart_data?.security_chart_data} yAxis={tablesData?.security_chart_data?.x_axis} />
					<ConcentrationTestTable baseFile={baseFile} title="Concentration Test" tablesData={tablesData} setTablesData={setTablesData} setWhatIfAnalysisListData={setWhatIfAnalysisListData} />
					<PrincipleObligationTable title="Principal Obligations" tablesData={tablesData} />
				</div>
			}
		</div>
	);
};