import { Select } from 'antd'
import React from 'react'
// import { updateAssetData } from '../../utils/updateAssetData';
import { getUpdateAssetData } from '../../services/api';
import { toast } from 'react-toastify';
import { wiaOptions } from '../../utils/configurations/wiaOptions';

export const WhatIfAnalysisOptions = (
  { selectedOption,
    setSelectedOption,
    setIsModalVisible,
    setEbitdaModalOpen,
    setIsupdateAssetModalOpen,
    setUpdateAssetTableData,
    baseFile,
    whatIfAnalysisId,
    setWhatIfAnalysisId,
    setSaveBtn,
    fundType
  }) => {

  const handleDropdownChange = (value) => {
    setSaveBtn(false);
    setWhatIfAnalysisId(null);
    if(value == 1)
    {
        setIsModalVisible(true);
    }
    else if(value == 2)
    {
        setEbitdaModalOpen(true);
    }
    else if(value == 3)
    {
      getUpdateAssetSheetData();
      // setUpdateAssetTableData(updateAssetData)
    }
  }

  const getUpdateAssetSheetData = async() => {
    const defaultsheetName = fundType === 'PCOF' ? 'PL BB Build' : 'Loan List';
    const basefileid = baseFile.id;
    try{
      const res = await getUpdateAssetData(basefileid, defaultsheetName);
      setUpdateAssetTableData(res.data.result);
      setIsupdateAssetModalOpen(true);
    }
    catch(err)
    {
      toast.error("something went wrong");
      console.error(err);
    }

  }


  return (
    <>

  <div style={{ flex: "1" }}>
    <Select
      // className={ButtonStyles.filledBtn}
      defaultValue="-- What if Analysis --"
      style={{ width: 180, borderRadius: '8px', border: '1px solid #6D6E6F' }}
      onChange={handleDropdownChange}
      value={selectedOption}
      onSelect={(value) => setSelectedOption(value)}
      options={wiaOptions[fundType]}
    />
  </div>



        <div>

          {/* <AboutModal isAboutModalState={isAboutModalState} aboutModalState={aboutModalState}  /> */}
          {/* Preveiw */}
        </div>

    </>
  );
};
