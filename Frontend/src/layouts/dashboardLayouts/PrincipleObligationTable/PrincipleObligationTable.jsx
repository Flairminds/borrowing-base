import React from 'react';
import styleCCTable from "../../../layouts/dashboardLayouts/concentrationTestTable/concentrationTestTable.module.css";
import { TableComponent } from '../../../components/Tables/TableComponent';

export const PrincipleObligationTable = ({title, tablesData}) => {
	return (
		<div className={styleCCTable.main}>
			{/* <h5 className='my-3'>{{title}}</h5> */}
			<TableComponent
				data={tablesData?.principal_obligation_data}
				columns={tablesData?.principal_obligation_data?.columns[0]?.data}
				heading={title}
			/>
		</div>
	);
};