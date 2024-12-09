import React, { useState } from 'react';
import { BBConcentration } from '../../../utils/BBData';
import {Concentration_Coloum} from '../../../utils/BBData';
import styleCCTable from './Concentration_testTable.module.css';
import { TableComponent } from '../TableComponent';

export const  Concentration_testTable = ({title,tablesData,baseFile,setTablesData,setWhatIfAnalysisListData}) => {
  const concentrationTest = "Concentration Test";
  return (
    <div className={styleCCTable.main}>
      {/* <h5 className='my-3'>{{title}}</h5> */}
      <TableComponent 
        baseFile={baseFile} 
        isConcentrationTest={true}  
        data={tablesData?.concentration_test_data} 
        columns={tablesData?.concentration_test_data?.columns[0]?.data}  
        heading={title} 
        setTablesData={setTablesData} 
        setWhatIfAnalysisListData={setWhatIfAnalysisListData}
      />
    </div>
  );
};