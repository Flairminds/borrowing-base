import React from 'react';
import crossIcon from "../../assets/uploadFIle/cross.svg";
import { TableComponent } from '../Tables/TableComponent';
import Styles from './CardTable.module.css';

export const CardTable = ({title, overviewTableData, setActiveComponent}) => {
	return (
		<div className={Styles.cardContainer}>
			<div className={Styles.cardHeader}>
				<div className={Styles.heading} >{title}</div>
				<img style={{cursor: 'pointer'}} onClick={() => setActiveComponent("")} src={crossIcon} />
			</div>
			<div style={{padding: "1%"}}>
				<TableComponent
					showObligationTotal={title == 'Obligors Net Capital' ? false : true}  
					data={overviewTableData ? overviewTableData : null} 
					columns={overviewTableData ? overviewTableData.columns[0]?.data : null} 
				/>
			</div>
		</div>
	);
};