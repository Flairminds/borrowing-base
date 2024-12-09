import React from 'react';
import { PrincipleBB } from "../../../utils/BB_1Data";
import {columns_obligations} from "../../../utils/BB_1Data.jsx"
import styleCCTable from "../../../components/Tables/Concentration_testTable/Concentration_testTable.module.css";
import up from "../../../assets/Portflio/up.svg";
import { TableComponent } from '../TableComponent';

export const Principle_obligationTable = ({title, tablesData}) => {
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