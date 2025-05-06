import React from 'react';
import arrow from "../../assets/Portflio/Vector.svg";
import stylesTabs from "./TabsStyles.module.css";
// import { OverviewTableData } from '../../services/api';

export const Tabs = ({name, value, imgsrc, dashColor, comp, activeComponent, setActiveComponent, setOverviewTableData}) => {
	return (
		<>
			<img src={imgsrc} className={stylesTabs.tabImage} />
			<div className={stylesTabs.tabDataContainer}>
				<div className={stylesTabs.tabName} >{name}</div>
				<div className={stylesTabs.tabData}>{value?.data}</div>
				{value?.changeInValue ?
					<div className={stylesTabs.changeDiv}>
						<span style={{color: dashColor}}> -- </span>
						<span style={{color: '#0D6683'}}>change in value</span>
					</div>
					: null
				}
				<div>
					<span className={stylesTabs.prevValue}>{value?.prevValue}</span>
					{value?.prevValue && value?.percentageChange ? <>|</> : null }
					<span className={stylesTabs.percentageChangeDiv}>{value?.percentageChange}</span>
				</div>

			</div>
			<div className={stylesTabs.moreIcon}>
				<img src={arrow} alt="arrow" />
			</div>
		</>
	);
};
