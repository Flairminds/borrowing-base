import { DatePicker } from 'antd';
import React, { useState, useEffect } from 'react';
import LeverageBB from "../../assets/Portflio/Frame 761457 (1).svg";
import Subscription from "../../assets/Portflio/Frame 761457 (2).svg";
import Availability from "../../assets/Portflio/Frame 761457 (3).svg";
import Obligors from "../../assets/Portflio/Frame 761457 (4).svg";
import TotalBB from "../../assets/Portflio/Frame 761457.svg";
import { OverviewTableData } from '../../services/api';
import { filterDataByDateRange } from '../../utils/helperFunctions/filterDatabyDate';
import { CardTable } from '../cardTableComponent/CardTable';
import { Tabs } from '../tabs/Tabs';
import { TrendGraph } from '../trendGraph/TrendGraph';
import stylesOverView from "./PortfollioDashboard.module.css";

const { RangePicker } = DatePicker;

export const PortfollioDashboard = ({
	tablesData,
	trendGraphData,
	baseFile,
	getTrendGraphData,
	whatifAnalysisPerformed,
	fundType
}) => {
	const [activeComponent, setActiveComponent] = useState('');
	const [overviewTableData, setOverviewTableData] = useState();
	const [lineChartDisplaydata, setLineChartDisplaydata] = useState();

	const tabConfig = {
		"Total BB": { dashColor: '#00A473', imgSrc: TotalBB, title: 'Total Borrowing Base' },
		"Leverage BB": { dashColor: '#6554C0', imgSrc: LeverageBB, title: 'Leverage Borrowing Base' },
		"Subscription BB": { dashColor: '#1781CE', imgSrc: Subscription, title: 'Subscription Borrowing Base' },
		"Availability": { dashColor: '#1FBDD0', imgSrc: Availability, title: 'Availability' },
		"Obligors net capital": { dashColor: '#DA2853', imgSrc: Obligors, title: 'Obligors Net Capital' },
		"Advance Outstandings": { dashColor: '#1FBDD0', imgSrc: TotalBB, title: 'Advance Outstandings'},
		"Borrowing Base": { dashColor: '#6554C0', imgSrc: LeverageBB, title: 'Borrowing Base' },
		"Maximum Available Amount": {dashColor: '#6554C0', imgSrc: Subscription, title: 'Maximum Available Amount'},
		"Total Credit Facility Balance": { dashColor: '#1781CE', imgSrc: Subscription, title: 'Total Credit Facility Balance'},
		// duplicate img
		"Pro Forma Advances Outstanding": { dashColor: '#1781CE', imgSrc: Subscription, title: 'Pro Forma Advances Outstanding'}
	};
	const names = Object.keys(tabConfig);

	useEffect(() => {
		setLineChartDisplaydata(trendGraphData);
	}, [trendGraphData]);

	const tabClicked = async(tabNum, name) => {
		try {
			const response = await OverviewTableData(name, baseFile.id, 1);
			setOverviewTableData(response.data);
		} catch (err) {
			console.error(err);
		}
		setActiveComponent(name);
	};

	// const handleRangeChange = (value, dateStrings) => {
	//     setLineChartDisplaydata(filterDataByDateRange(trendGraphData, dateStrings[0], dateStrings[1]));
	// };

	return (
		<div>
			<div className={stylesOverView.main}>
				<div className={stylesOverView.titleDiv}>
					<div className={stylesOverView.overViewHeadingDiv}>
						<span className={stylesOverView.overViewHeading}>Overview</span>
						<span className={stylesOverView.fundTypeContainer}>{fundType}</span>

					</div>
					{/* <div className={stylesOverView.rangePickerDiv}>
                        <RangePicker format="YYYY-MM-DD" onChange={handleRangeChange} />
                    </div> */}
				</div>

				<div className={`${stylesOverView.tabGraphDiv} ${!whatifAnalysisPerformed ? stylesOverView.fixedHeight : null}`}>
					<div className={stylesOverView.tabsParent}>
						{tablesData?.card_data?.ordered_card_names.map((name, index) => (
							<div
								key={name}
								className={`${stylesOverView.tabsDiv} ${activeComponent === name ? stylesOverView.selectedTab : null}`}
								onClick={() => tabClicked(index + 1, name)}
							>
								<Tabs
									name={name}
									dashColor={tabConfig[name]?.dashColor || '#000'} // Default color if not found in config
									value={tablesData?.card_data[name][0]}
									imgsrc={tabConfig[name]?.imgSrc} // Default image if not found in config
									activeComponent={activeComponent}
									setActiveComponent={setActiveComponent}
									setOverviewTableData={setOverviewTableData}
								/>
							</div>
						))}
					</div>
					<div className={stylesOverView.graphDiv}>
						{activeComponent !== '' && tabConfig[activeComponent] ? (
							<CardTable
								setActiveComponent={setActiveComponent}
								title={tabConfig[activeComponent].title}
								overviewTableData={overviewTableData}
							/>
						) : (
							<TrendGraph lineChartDisplaydata={lineChartDisplaydata} />
						)}
					</div>
				</div>
			</div>
		</div>
	);
};

