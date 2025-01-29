import { useEffect } from 'preact/hooks';
import React, { useState } from 'react';
import { PortfollioDashboard } from '../../components/portfollioDashboard/PortfollioDashboard';
import { Concentration_testTable } from '../../components/Tables/Concentration_testTable/Concentration_testTable';
import { Principle_obligationTable } from '../../components/Tables/Principle_obligationTable/Principle_obligationTable';
// import { AssetSelectionPage } from '../../pages/assetSelection/AssetSelectionPage';
import { lineChartData } from '../../services/api';
// import { previousSelectedAssetsArray } from '../../utils/helperFunctions/getSelectedAssets';
import { TableGraph } from '../tableGraph/TableGraph';
import { WhatIfAnalysis } from '../whatIfAnalysis/WhatIfAnalysis';


export const PageLayout = ({
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
	getLandingPageData
}) => {

	const [trendGraphData, setTrendGraphData] = useState([]);
	// const [assetSelectionData, setAssetSelectionData] = useState([]);
	const [whatifAnalysisPerformed, setWhatifAnalysisPerformed] = useState(false);
	// const [selectedAssets, setSelectedAssets] = useState(assetSelectionData?.assetSelectionList?.data ? previousSelectedAssetsArray(assetSelectionData?.assetSelectionList?.data) : []);
	const [whatIfAnalysisListData, setWhatIfAnalysisListData ] = useState([]);

	useEffect(() => {
		if (!tablesData) {
			getTrendGraphData(fundType);
			getLandingPageData();
		}
	}, []);


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
		<>
			{/* <Sidebar  />
			<div className='w-100'
			> */}
			{/* <Navbar /> */}

			<>
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
				/>

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
				/>

				{fundType == "PCOF" ?
					<>
						<TableGraph
							title="Segmentation Overview"
							tableData={tablesData?.segmentation_overview_data}
							tableColumns={tablesData?.segmentation_overview_data?.columns[0]?.data}
							chartsData={tablesData?.segmentation_chart_data?.segmentation_chart_data}
							yAxis= {tablesData?.segmentation_chart_data?.x_axis}
						/>
						<TableGraph
							title="Security"
							tableData={tablesData?.security_data}
							tableColumns={tablesData?.security_data?.columns[0]?.data}
							chartsData={tablesData?.security_chart_data?.security_chart_data}
							yAxis={tablesData?.security_chart_data?.x_axis}
						/>

						<Concentration_testTable
							baseFile={baseFile}
							title="Concentration Test"
							tablesData={tablesData}
							setTablesData={setTablesData}
							setWhatIfAnalysisListData={setWhatIfAnalysisListData}
						/>
						<Principle_obligationTable
							title="Principal Obligations"
							tablesData={tablesData}
						/>
					</>
					:
					<>
						<TableGraph
							title="Segmentation Overview"
							tableData={tablesData?.segmentation_overview_data}
							tableColumns={tablesData?.segmentation_overview_data?.columns[0]?.data}
							chartsData={tablesData?.segmentation_chart_data?.segmentation_chart_data}
							yAxis= {tablesData?.segmentation_chart_data?.x_axis}
						/>
						<TableGraph
							title="Security"
							tableData={tablesData?.security_data}
							tableColumns={tablesData?.security_data?.columns[0]?.data}
							chartsData={tablesData?.security_chart_data?.security_chart_data}
							yAxis={tablesData?.security_chart_data?.x_axis}
						/>

						<Concentration_testTable
							baseFile={baseFile}
							title="Concentration Test"
							tablesData={tablesData}
							setTablesData={setTablesData}
							setWhatIfAnalysisListData={setWhatIfAnalysisListData}
						/>
						<Principle_obligationTable title="Principal Obligations" tablesData={tablesData}/>
					</>
				}
			</>
		</>
		// </div>
	);
};