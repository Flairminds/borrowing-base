import React from 'react'
import { UploadFile } from '../uploadFileComponent/UploadFile'
import Styles from './WhatIfAnalysis.module.css'
import { useEffect, useState } from 'preact/hooks';
import { useDropzone } from 'react-dropzone';
import { Modal, Button, Select ,Input } from 'antd';
import about from "../../assets/NavbarIcons/Default.svg"
import ButtonStyles from "../../components/Buttons/ButtonStyle.module.css";
import { EbitdaAnalysis, addNewAsset, changeParameter, downLoadReportSheet, downloadExcelAssest, getListOfWhatIfAnalysis, get_preview_table, intermediateMetricsTable, saveWhatIfAnalysis } from '../../services/api';
import {toast} from 'react-toastify'
import { Popover, Tooltip } from 'antd';
import {WhatifTable} from "../../modal/WhatifTable/WhatifTable"
import {Whatif_Columns,Whatif_data} from "../../utils/Whatif_Data"
import { Calender } from '../calender/Calender';
// import {Options} from "../../utils/Options"
import { PreviewTable } from '../../modal/previewModal/PreviewTable';
import { AddAssetSelectionTableModal } from '../../modal/addAssetSelectionTableModal/AddAssetSelectionTableModal';
import aboutIcon from "../../assets/NavbarIcons/aboutIcon.png"
import { AboutModal } from '../../modal/AboutModal/AboutModal';
import { ParameterChange } from '../../modal/ParameterChange/ParameterChange';
import { arrayOfObjects } from '../../utils/helperFunctions/ArrayToObject';
import { WIAInformation } from '../wiaInformation/WIAInformation';
import { WhatIfAnalysisOptions } from '../whatIfAnalysisOptions/WhatIfAnalysisOptions';
import { AddAssetModal } from '../../modal/addAssetModal/AddAssetModal';
import { UpdateParameterModal } from '../../modal/updateParameterModal/UpdateParameterModal';
import { assetInventory } from '../../utils/asset';
import { AssetInventory } from '../../modal/assetInventoryModal/AssetInventory';
import { UpdateAssetDetailsModal } from '../../modal/updateAssetWIA/updateAssetDetailsModal/UpdateAssetDetailsModal';
import { SaveAnalysisConfirmationModel } from '../../modal/saveanalysisconfirmationmodel/SaveAnalysisConfirmationModel';
import { WhatIfAnalysisLib } from '../../modal/whatIfAnalysisLibrary/WhatIfAnalysisLib';

export const WhatIfAnalysis = (
  { 
    getTrendGraphData,
    setBaseFile,
    setTrendGraphData,
    setAssetSelectionData,
    constDate,
    baseFile,
    setTablesData,
    setWhatifAnalysisPerformed,
    reportDate,
    setReportDate,
    isAnalysisModalOpen,
    setIsAnalysisModalOpen,
    availableClosingDates,
    whatIfAnalysisListData,
    setWhatIfAnalysisListData,
    fundType,
    setFundType
  }) => {

  const [selectedRow, setSelectedRow] = useState(null);
    // const[isAnalysisModalOpen,setIsAnalysisModalOpen] =useState(false)
    const [isModalVisible, setIsModalVisible] = useState(false);
    const [selectedFiles, setSelectedFiles] = useState([]);
    const [selectedUploadedFiles, setSelectedUploadedFiles] = useState([]);
    const [lastUpdatedState, setLastUpdatedState] = useState('');
    const [selectedOption, setSelectedOption] = useState()
    const [ebitdaModalOpen, setEbitdaModalOpen] = useState(false);
    const [ebitaChangeValue, setEbitaChangeValue] = useState({
      ebitaValue:"",
      leverage:"",
    });
    const [loading, setLoading] = useState(false);
    const [guidePopupOpen, setGuidePopupOpen] = useState(false)
    const[tableModal,setTableModal] = useState(false);
    const [selectedFiledata, setSelectedFiledata] = useState('')
    const [dataPreviewPopup, setDataPreviewPopup] = useState(false)
    const[saveBtn, setSaveBtn]= useState(false)
    const[whaIfAnalsisData,setWhaIfAnalsisData] = useState({
      typeOfAnalysis :'',
      analysisValue:''
    })
    const [inputValueUntitled, setInputValueUntitled] = useState("");
    const [descriptionModal,isSetDescriptionModal]=useState(false)
    const [descriptionInput,setDescriptionInput]=useState("")
    const [previewModal,isPreviewModal] = useState(false)
    const [previewData,setPreviewData]= useState()
    const [previewColumns,setPreviewColumns] =useState()
    const [selectedOptionUpdateValue, setSelectedOptionUpdateValue] = useState("");
    const [selectedOptionLeverage, setSelectedOptionLeverage] = useState(false);
    const [previewTableData,setPreviewTableData]= useState()
    const [whatIfanalysisLoader,setWhatIfanalysisLoader] = useState(false);
    const [parameterList,setParameterList]=useState()
    const [addAssetSelectedData, setAddAssetSelectedData] = useState([])
    const [downloadExcel,setDownloadExcel]=useState()
    const [apiResponseStatusParameter, setApiResponseStatusParameter] = useState(false);
    const [changeParameterSubmitDisplay,setChangeParameterSubmitDisplay] = useState(false);
    const [isAssetInventoryModal,setIsAssetInventoryModal] =useState(false)
    const [isupdateAssetModalOpen,setIsupdateAssetModalOpen] = useState(false)
    const [updateAssetTableData,setUpdateAssetTableData] = useState();
    const [selectedCellData , setSelectedCellData] = useState({
      investment_name : '',
      colName:''
    });
    const[whatIfAnalysisId,setWhatIfAnalysisId] =useState(null);
    const[whatIfAnalysisType,setWhatIfAnalysisType] = useState()
    const[simulationType,setSimulationType]=useState()
    useEffect(() => {
      if(selectedFiles.length > 0){
        getPreviewTable();
      }
    },[selectedFiles])

    const getMediateMetrics = async () =>{
      try{
          const res = await intermediateMetricsTable(baseFile.id,whatIfAnalysisId)
          setPreviewTableData(res.data)
          console.log(res);
          setWhatIfAnalysisType(res.data.simulation_type)
      }
      catch{

      }
  } 
      const getPreviewTable = async () => {
        
        try{
          const response = await get_preview_table(selectedFiles)
          var stringRes = JSON.parse(response.data.replace(/\bNaN\b/g, "null"));
          if(response.status===200){
            // isPreviewModal(true)   
            setPreviewData(stringRes.sheet1.data)
            setPreviewColumns(stringRes.sheet1.columns)
            setAddAssetSelectedData(stringRes.sheet1.data);

          }
        }
        catch(err)
        {
          console.log(err)
        }
        
      }
    
  

    const getWhatifAnalysisList = async () => {
      try{
        const response = await getListOfWhatIfAnalysis(1)
        setWhatIfAnalysisListData(response.data.result.data)
      }
      catch(err)
      {
        console.log(err)
      }
      
    }
  
    useEffect(() => {
      if(tableModal)
      {
      getWhatifAnalysisList();
      }
    } , [tableModal]);

  useEffect(() => {
    if(isModalVisible){
      setTimeout(() => {
        setGuidePopupOpen(false)
      }, 2000);
      setGuidePopupOpen(true)
    }
  },[isModalVisible])


    const handleReportDownload = async() => {
      try
      {
        const response = await downLoadReportSheet(baseFile.id,1);
        const blob = new Blob([response.data])
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${fundType}-Borrowing_Base_Report.xlsx`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a); 
      }
      catch(err)
      {
        console.log(err);
      }
    }
    
    const handleDownloadExcel = async()=>{
      try{
        setIsModalVisible(false)
        const response = await downloadExcelAssest(previewData)
        const blob = new Blob([response.data])
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'Borrowing_Base_Report.xlsx';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      }
      catch(err){
        console.log(err);
      } 
    }

    const handleOk = async() => {
      setLoading(true); 
            try {
                if (selectedFiles.length > 0) {
                    const response = await addNewAsset(selectedFiles,baseFile.id,0,addAssetSelectedData);
                    if(response.status == 200)
                    {
                      setWhatIfAnalysisId(response.data.what_if_analysis_id)
                      setWhatIfAnalysisType(response.data.what_if_analysis_type)
                      setTablesData(response.data)
                      setReportDate(response.data.closing_date);
                      setSelectedFiledata(selectedFiles)
                      setSelectedFiles([])
                      setSaveBtn(true)
                      setIsModalVisible(false)
                      setWhaIfAnalsisData({
                        typeOfAnalysis :'File ',
                        analysisValue:selectedFiles[0]?.name
                    })
                    setWhatifAnalysisPerformed(true)
                    }
                }
            }
            catch(err)
            {
                console.log(err);
                setSelectedFiles([])
            }
            setIsModalVisible(false);
            setSelectedOption(0)
            setLoading(false)
        // setIsModalVisible(false);
      };
    
      const handleSaveEbita = async()  =>{
        setInputValueUntitled("")
        setWhatIfanalysisLoader(true);
        if(whaIfAnalsisData.typeOfAnalysis == 'Ebitda change value' || whaIfAnalsisData.typeOfAnalysis == 'Leverage change value')
        {
          try{
              const response = await EbitdaAnalysis(parameterList,selectedOptionUpdateValue == "ebitda" ? 'Ebitda' : "Leverage" ,baseFile.id,1,inputValueUntitled,descriptionInput);
              if(response.status===200){
                toast.success("Saved")
                getWhatifAnalysisList()
                setDescriptionInput('')
                setSaveBtn(false)
                setWhatIfanalysisLoader(false);
                isSetDescriptionModal(false)
              }
          }
          catch(err){
            console.log(err);
          }
          setDescriptionInput('')
          setWhatIfAnalysisListData({
            typeOfAnalysis :'',
            analysisValue:''
          })
        }
        else if(whaIfAnalsisData.typeOfAnalysis == 'File ')
          {
            try{
              const response = await addNewAsset(selectedFiledata,baseFile.id,1,addAssetSelectedData,inputValueUntitled,descriptionInput,whatIfAnalysisType,whatIfAnalysisId);
              if(response.status===200){
                toast.success("Saved")
                getWhatifAnalysisList()
                setSaveBtn(false)
                isSetDescriptionModal(false)
                setWhatIfanalysisLoader(false);
              }
            }
            catch(err){
              console.log(err);
            }
            setWhatIfanalysisLoader(false);
            setInputValueUntitled('')
            isSetDescriptionModal(false)
            setWhatIfAnalysisListData({
              typeOfAnalysis :'',
              analysisValue:''
            })
          }


      }
      const save_what_if_analysis = async() =>{
        try{
          const res = await saveWhatIfAnalysis(whatIfAnalysisType,whatIfAnalysisId,inputValueUntitled,descriptionInput)
          console.log(res);
          // if(response.status===200){
            toast.success("Saved")
            getWhatifAnalysisList()
            setDescriptionInput('')
            setSaveBtn(false)
            setWhatIfanalysisLoader(false);
            isSetDescriptionModal(false)
          // }
          
        }
        catch(err){
          console.log(err);
          
        }
      }
    
      const handleCancel = () => {
        setSelectedRow(null);
        // setSelectedOptionUpdateValue('')
        setWhatIfanalysisLoader(false)
        isSetDescriptionModal(false)
        setDescriptionInput('')
        setIsModalVisible(false);
        setEbitdaModalOpen(false);
        setEbitaChangeValue({
          ebitaValue:"",
          leverage:""
        })
        setSelectedFiles([])
        setSelectedOption(0)
        setTableModal(false)
        setChangeParameterSubmitDisplay(false)
        setParameterList(null)
        setSelectedOptionUpdateValue(null)
        // isDuplicateFileModal(false)
      };
    
      const showModal = () => {
        setIsModalVisible(true);
      };

      const tableModalfunc =()=>{
        setTableModal(true)
      }

      const handleInputChange = (event) => {
        setInputValueUntitled(event.target.value);
      };

      const handleAboutModal =() =>{
        getMediateMetrics()
        setDataPreviewPopup(true)
      }

      const handleParameterRadioBtn = async (parameterType) => {
        setSelectedOptionUpdateValue(parameterType);
        setApiResponseStatusParameter(false);
        try {
          setChangeParameterSubmitDisplay(false);
          const res = await changeParameter(baseFile.id, parameterType);
          if (res.status === 200) {
            setApiResponseStatusParameter(true);
            setParameterList(res.data.result);
            setChangeParameterSubmitDisplay(true);
          }
        } catch (err) {
          console.error(err);
        }

      };

     

      
      

      const hanleAssetInventory =()=>{
        setIsAssetInventoryModal(true)
      }

      useEffect(() => {
        console.log(selectedOptionUpdateValue, 'selected');
      }, [selectedOptionUpdateValue]);
    
    return (
        <>
              {saveBtn && (
                  <WIAInformation baseFile={baseFile} whaIfAnalsisData={whaIfAnalsisData} isSetDescriptionModal={isSetDescriptionModal} />
                )}
                <div style={{display:"flex", gap:"20px", padding:"0 0 0 3.5%", alignItems:"center", justifyContent:'space-between', margin :'1rem 0rem'}}>
                <div style={{ display: "flex", alignItems: "center" }}>
                    <h5 style={{ fontSize: "26px", fontWeight: "600" }}>Borrowing Base Dashboard</h5> 
                     <span style={{fontWeight:"400",fontSize:"17px",paddingLeft:"0.5rem",color:"#6D6E6F",paddingBottom:"0.1rem"}}>Last imported on - {constDate}</span>
                   
                    {saveBtn && (
                      <div style={{display:"flex"}}>
                        <h3 style={{marginLeft:"5px" }} >/</h3>
                          <input className={Styles.inputUntittled}  placeholder="Untitled" value={inputValueUntitled} onChange={handleInputChange}/>
                      </div>
                    )}
                  </div>
                    <div style={{ display:"flex", alignItems:"center"}}>
                      <div style={{display:"flex"}}>
                        <div  style={{display:"flex"}}>
                          
                          <Calender setReportDate={setReportDate} setTablesData={setTablesData} setWhatifAnalysisPerformed={setWhatifAnalysisPerformed} setBaseFile={setBaseFile} 
                          availableClosingDates={availableClosingDates} setFundType={setFundType} getTrendGraphData={getTrendGraphData}
                          />

                        </div>
                        <div style={{paddingRight:"1rem",paddingTop:"0.3rem"}}>
                        {reportDate && <span style={{paddingLeft:"0.5rem",fontWeight:"400",fontSize:"16px",color:"#2A2E34"}}> {reportDate}</span>}
                        </div>

                    
                        <Popover  content={
                          <div style={{display:"flex", flexDirection:"column",gap:"10px"}}>
                              <div style={{fontWeight:"400",fontSize:"14px",cursor:"pointer"}} onClick={() => setIsAnalysisModalOpen(true)} > Import File</div>
                              
                              {/* <div style={{fontWeight:"400",fontSize:"14px",cursor:"pointer"}} onClick={hanleAssetInventory}>Assets Inventory</div> */}
                              <div style={{fontWeight:"400",fontSize:"14px",cursor:"pointer"}} onClick={handleAboutModal}>Intermediate Metrics</div>
                              <div style={{fontWeight:"400",fontSize:"14px",cursor:"pointer"}} onClick={tableModalfunc}>What if analysis library</div>
                              <div  style={{fontWeight:"400",fontSize:"14px",cursor:"pointer"}}onClick={handleReportDownload}>Export</div> 
                          </div>
                        }>
                           <img src={about}></img>
                        </Popover>
                        <AssetInventory setIsAssetInventoryModal={setIsAssetInventoryModal} isAssetInventoryModal={isAssetInventoryModal}/>
                        <UploadFile 
                          setReportDate={setReportDate}  
                          getTrendGraphData={getTrendGraphData} 
                          setBaseFile={setBaseFile} 
                          baseFile={baseFile}
                          setTablesData={setTablesData} 
                          setTrendGraphData={setTrendGraphData}  
                          setAssetSelectionData={setAssetSelectionData}
                          setWhatifAnalysisPerformed={setWhatifAnalysisPerformed} 
                          setIsAnalysisModalOpen={setIsAnalysisModalOpen} 
                          isAnalysisModalOpen={isAnalysisModalOpen}
                          availableClosingDates={availableClosingDates}
                          fundType={fundType}
                          setFundType={setFundType}
                          /> 

                      </div>
                          <WhatIfAnalysisOptions 
                            selectedOption={selectedOption} 
                            setSelectedOption={setSelectedOption} 
                            setIsModalVisible={setIsModalVisible} 
                            setEbitdaModalOpen={setEbitdaModalOpen}
                            setIsupdateAssetModalOpen={setIsupdateAssetModalOpen}
                            setUpdateAssetTableData={setUpdateAssetTableData}
                            baseFile={baseFile}
                            setWhatIfAnalysisId={setWhatIfAnalysisId}
                            setSaveBtn={setSaveBtn}
                            fundType={fundType}
                          /> 
                      <div>
                        <PreviewTable whatIfAnalysisId={whatIfAnalysisId} dataPreviewPopup={dataPreviewPopup} setDataPreviewPopup={setDataPreviewPopup} baseFile={baseFile} previewTableData={previewTableData} whatIfAnalysisType={whatIfAnalysisType}/>
                      </div> 
                    </div>
            </div> 

            <AddAssetModal 
              isModalVisible={isModalVisible} 
              handleOk={handleOk} 
              handleCancel={handleCancel} 
              loading={loading} 
              selectedFiles={selectedFiles}
              setSelectedFiles={setSelectedFiles}
              setSelectedUploadedFiles={setSelectedUploadedFiles}
              setLastUpdatedState={setLastUpdatedState}
              handleDownloadExcel={handleDownloadExcel}
              isPreviewModal={isPreviewModal}
              previewModal={previewModal}
              previewData={previewData}
              setPreviewData={setPreviewData}
              previewColumns={previewColumns}
              setAddAssetSelectedData={setAddAssetSelectedData}
            />


          <UpdateParameterModal
            ebitdaModalOpen={ebitdaModalOpen}
            // handleEbitaAnalysis={handleEbitaAnalysis}
            handleCancel={handleCancel}
            changeParameterSubmitDisplay={changeParameterSubmitDisplay}
            handleParameterRadioBtn={handleParameterRadioBtn}
            apiResponseStatusParameter={apiResponseStatusParameter}
            selectedOptionUpdateValue={selectedOptionUpdateValue}
            parameterList={parameterList}
            setParameterList={setParameterList}
            loading={loading}
            setLoading={setLoading}
            baseFile={baseFile}
            inputValueUntitled={inputValueUntitled}
            setTablesData={setTablesData}
            setReportDate={setReportDate}
            setEbitdaModalOpen={setEbitdaModalOpen}
            setWhaIfAnalsisData={setWhaIfAnalsisData}
            ebitaChangeValue={ebitaChangeValue}
            setWhatifAnalysisPerformed={setWhatifAnalysisPerformed}
            setEbitaChangeValue={setEbitaChangeValue}
            setSaveBtn={setSaveBtn}
            setInputValueUntitled={setInputValueUntitled}
            setSelectedOption={setSelectedOption}
            setWhatIfAnalysisId={setWhatIfAnalysisId}
            setWhatIfAnalysisType={setWhatIfAnalysisType}
          />

          <UpdateAssetDetailsModal
            setSelectedOption={setSelectedOption}
            isupdateAssetModalOpen={isupdateAssetModalOpen}
            setIsupdateAssetModalOpen={setIsupdateAssetModalOpen}
            updateAssetTableData={updateAssetTableData}
            setUpdateAssetTableData={setUpdateAssetTableData}
            selectedCellData={selectedCellData}
            setSelectedCellData={setSelectedCellData}
            baseFile={baseFile}
            whatIfAnalysisId={whatIfAnalysisId}
            setWhatIfAnalysisId={setWhatIfAnalysisId}
            setTablesData={setTablesData}
            setWhatifAnalysisPerformed={setWhatifAnalysisPerformed}
            setSaveBtn={setSaveBtn}
            fundType={fundType}
          />

        <WhatIfAnalysisLib
        tableModal={tableModal}
        handleOk ={handleOk}
        handleCancel ={handleCancel}
        setTableModal ={setTableModal}
        whatIfAnalysisListData ={whatIfAnalysisListData}
        Whatif_Columns ={Whatif_Columns}
        setTablesData ={setTablesData}
        setWhatifAnalysisPerformed ={setWhatifAnalysisPerformed}
        selectedRow = {selectedRow}
        setSelectedRow = {setSelectedRow}
        simulationType = {simulationType}
        setSimulationType = {setSimulationType}
        whatIfAnalysisId = {whatIfAnalysisId}
        whatIfAnalysisType ={whatIfAnalysisType}
        />

        <SaveAnalysisConfirmationModel
        descriptionModal={descriptionModal}
        handleCancel={handleCancel}
        isSetDescriptionModal={isSetDescriptionModal}
        setDescriptionInput={setDescriptionInput}
        whatIfanalysisLoader={whatIfanalysisLoader}
        SaveWhatIfAnalysis={save_what_if_analysis}
        descriptionInput={descriptionInput}
      />
         </>
  );
};
