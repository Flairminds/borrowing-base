import { Button, Modal, Popover, Tooltip,Switch } from 'antd'
import React from 'react'
import Styles from './UpdateAssetDetailsModal.module.css'
import { useEffect, useRef, useState } from 'preact/hooks';
import CrossIcon from '../../../assets/CrossIcon.svg'
import RightIcon from '../../../assets/RightIcon.svg'
import { getUpdateAssetData, updateModifiedAssets, updateSheetValues } from '../../../services/api';
import ButtonStyles from '../../../components/Buttons/ButtonStyle.module.css'
import { updateAssetDefaultColumnsData, updateAssetModalData } from '../../../utils/constants/constants';
import { addAssetAtIndex, deleteAssetAtIndex, duplicateAsset, getLatestPrevValue, updateDataAfterChange } from '../../../utils/helperFunctions/updateAssetDataChange';
import {MoreOutlined} from '@ant-design/icons';
import MoreOptionsIcon from '../../../assets/updateAssetIcons/MoreOptionsIcon.svg'
import DuplicateAssetIcon from '../../../assets/updateAssetIcons/DuplicateAssetIcon.svg'
import DeleteIcon from '../../../assets/DeleteIcon.svg'
import AddIcon from '../../../assets/AddIcon.svg'
import { AddAssetDetailsModal } from '../addAssetDetailsModal/AddAssetDetailsModal';

export const UpdateAssetDetailsModal = ({
    isupdateAssetModalOpen,
    setIsupdateAssetModalOpen,
    updateAssetTableData ,
    setUpdateAssetTableData,
    selectedCellData,
    setSelectedCellData,
    setSelectedOption,
    baseFile,
    whatIfAnalysisId,
    setWhatIfAnalysisId,
    setTablesData,
    setWhatifAnalysisPerformed,
    setSaveBtn
}) => {

    const [selectedSheetNumber, setSelectedSheetNumber] = useState(updateAssetModalData.defaultSelectedSheet);
    const [updateAssetInputText,setUpdateAssetInputText ] = useState('');
    const [appliedChanges, setAppliedChanges] = useState([]);
    const [enteredInputData,setEnteredInputData] = useState('')
    const [addedDeletedAssets, setAaddedDeletedAssets] = useState({
        addedAssets:[],
        deletedAssets:[]
    })
    const [addDeleteAssetData, setAddDeleteAssetData] = useState({
        index:-1,
        type:'',
    })
    const [loading, setLoading] = useState(false)
    const [addAssetDetailsModalOpen , setAddAssetDetailsModalOpen] = useState(false);
    const [showModification, setShowModification] = useState(false)
    
    const previewSheets = updateAssetTableData?.table_data?.sheets

    const handleCancel = () => {
        setIsupdateAssetModalOpen(false);
        setSelectedOption(0);
        setAppliedChanges([]);
        setLoading(false);
        setSelectedSheetNumber(updateAssetModalData.defaultSelectedSheet)
    }

    const handleInputFocus = (investment_name, colName) => {
        setSelectedCellData({investment_name : investment_name,colName:colName});
        setUpdateAssetInputText('');
    }

    const handleCellInputChange = (e) =>
    {
        setUpdateAssetInputText(e.target.value);
    }

    const handleCommitChange = (e, investment_name, colKey, colName, currValue) => {
        e.stopPropagation();
        updateDataAfterChange(updateAssetTableData, investment_name ,colKey,selectedSheetNumber, updateAssetInputText);
        const currentChanges = {
            row_name: investment_name,
            column_name: colName,
            updated_value: updateAssetInputText,
            prev_value:currValue
        }
        setAppliedChanges([...appliedChanges, currentChanges]);
        setSelectedCellData({
            investment_name : '',
            colName:''
        })
        setUpdateAssetInputText('')
    }

    const handleCancelChange = () => {
        setUpdateAssetInputText('');
        setSelectedCellData({
            investment_name : '',
            colName:''
        })
    }

    const handleSheetChange = async(sheetName) => {

        let totalChangesOnSheet ={
            updated_assets:[],
            rows_to_add:[],
            rows_to_delete:[]
        };
        if(updateAssetTableData?.changes)
        {
           totalChangesOnSheet.updated_assets = [...updateAssetTableData?.changes , ...appliedChanges]
        }
        else
        {
            totalChangesOnSheet.updated_assets = [...appliedChanges]
        }

        if(addedDeletedAssets.addedAssets.length > 0)
        {
            totalChangesOnSheet.rows_to_add = addedDeletedAssets.addedAssets;
        }

        if(addedDeletedAssets?.deletedAssets?.length > 0)
        {
            totalChangesOnSheet.rows_to_delete = addedDeletedAssets?.deletedAssets
        }

        try{
            if(appliedChanges.length> 0 || addedDeletedAssets?.addedAssets?.length > 0 || addedDeletedAssets?.deletedAssets?.length > 0 )
            {
                const res = await updateSheetValues(baseFile.id,selectedSheetNumber,totalChangesOnSheet,whatIfAnalysisId);
                setWhatIfAnalysisId(res.data.result.modified_base_data_file_id);
            }
        }
        catch(err)
        {
            console.error(err)

        }

        setAaddedDeletedAssets({
            addedAssets:[],
            deletedAssets:[]
        })
        totalChangesOnSheet ={
            updated_assets:[],
            rows_to_add:[]
        }

        try{
            const res = await getUpdateAssetData(baseFile.id, sheetName, whatIfAnalysisId)
            setUpdateAssetTableData(res.data.result);
            console.log(res.data.result , "Result");
            setAppliedChanges([]);
            setUpdateAssetInputText('')
            setSelectedSheetNumber(sheetName)
            console.log(sheetName , "Result");
        }
        catch(err)
        {
            console.error(err)
        }

    }

    const updateAssetApply = async() => {
        setLoading(true)
        let currentAnalysisId= undefined;
        let totalChangesOnSheet ={
            updated_assets:{}
        };
        if(updateAssetTableData?.changes)
        {
           totalChangesOnSheet.updated_assets = [...updateAssetTableData?.changes , ...appliedChanges]
        }
        else
        {
            totalChangesOnSheet.updated_assets = [...appliedChanges]
        }
        try{
            if(totalChangesOnSheet.updated_assets.length> 0)
            {
                const res = await updateSheetValues(baseFile.id,selectedSheetNumber,totalChangesOnSheet,whatIfAnalysisId);
                setWhatIfAnalysisId(res.data.result.modified_base_data_file_id);
                currentAnalysisId = res.data.result.modified_base_data_file_id;
            }
        }
        catch(err)
        {
            console.error(err)
        }
        if(!currentAnalysisId)
        {
            currentAnalysisId = whatIfAnalysisId
        }


        try{
            const res = await updateModifiedAssets(currentAnalysisId);
            setWhatifAnalysisPerformed(true)
            setSaveBtn(true)
            setTablesData(res.data.result);
            handleCancel()
        }
        catch(err)
        {
            console.error(err);
        }
        setLoading(false)

    }

    const updateAddDeleteData = (rowIndex,operationType) => {
        setAddDeleteAssetData({
            index: rowIndex,
            type:operationType
        })
        setAddAssetDetailsModalOpen(true)
    }

    const handleAddDeleteAssets = () => {
        let effectiveIndex;
        if(addDeleteAssetData.type == 'addAbove') effectiveIndex = addDeleteAssetData.index;
        else if(addDeleteAssetData.type == 'addBelow') effectiveIndex = addDeleteAssetData.index+1;
        else if(addDeleteAssetData.type == 'duplicate') effectiveIndex = addDeleteAssetData.index+1;
        else effectiveIndex = addDeleteAssetData.index;

        if(addDeleteAssetData.type == 'duplicate')
        {
            const resultData = duplicateAsset(updateAssetTableData, effectiveIndex, enteredInputData , updateAssetDefaultColumnsData[selectedSheetNumber], selectedSheetNumber)
            setAppliedChanges([...appliedChanges, ...resultData.duplicatechangesArray])
            setAaddedDeletedAssets({
                ...addedDeletedAssets,
                addedAssets :[...addedDeletedAssets.addedAssets, {row_identifier:enteredInputData, row_index:effectiveIndex}]
            })
            setUpdateAssetTableData(resultData.updatedTableData)
            setEnteredInputData('');
            setAddAssetDetailsModalOpen(false)
        }
        else if(addDeleteAssetData.type != 'delete'){
            const resultData = addAssetAtIndex(updateAssetTableData, effectiveIndex, enteredInputData , updateAssetDefaultColumnsData[selectedSheetNumber], selectedSheetNumber)
            setUpdateAssetTableData(resultData)
            setAaddedDeletedAssets({
                ...addedDeletedAssets,
                addedAssets :[...addedDeletedAssets.addedAssets, {row_identifier:enteredInputData, row_index:effectiveIndex}]
            })
            setEnteredInputData('');
            setAddAssetDetailsModalOpen(false)
        }
        else
        {
            const resultData = deleteAssetAtIndex(updateAssetTableData,effectiveIndex,updateAssetDefaultColumnsData[selectedSheetNumber],selectedSheetNumber)
            setUpdateAssetTableData(resultData.updatedData)
            setAaddedDeletedAssets({
                ...addedDeletedAssets,
                deletedAssets :[...addedDeletedAssets.deletedAssets, {row_identifier:resultData.rowName}]
            })
            setAddAssetDetailsModalOpen(false)
        }
    }

    const MoreOptionContent = ({rowIndex}) => (
        <div className={Styles.optionsContainer}>
            <div onClick={() => updateAddDeleteData(rowIndex, 'addAbove')} className={Styles.option}>
                <img className={Styles.optionIcon} src={AddIcon} alt="Add Icon" />
                Insert 1 row above
            </div>
            <div onClick={() => updateAddDeleteData(rowIndex, 'addBelow')} className={Styles.option}>
                <img className={Styles.optionIcon} src={AddIcon} alt="Add Icon" />
                Insert 1 row below
            </div>
            <div onClick={() => updateAddDeleteData(rowIndex, 'delete')} className={`${Styles.option} ${Styles.redText}`}>
                <img className={Styles.optionIcon} src={DeleteIcon} alt="Delete Icon" />
                Delete
            </div>
        </div>
    )

    const handleShowModificationChange = (checked) => {
        setShowModification(checked)
    }

  return (
    <>
    <Modal
        title={<span style={{ color: '#909090', fontWeight: '500', fontSize: '14px', padding: '0 0 0 3%' }}>Update Asset Details</span>}
        centered
        open={isupdateAssetModalOpen}
        onCancel={handleCancel}
        width={'98%'}
        footer={<>
            <div key="footer-buttons" className="px-4">
                <button key="back" onClick={handleCancel} className={ButtonStyles.outlinedBtn}>
                    Cancel
                </button>
                <Button className={ButtonStyles.filledBtn} loading={loading} key="submit" type="primary" style={{ backgroundColor: '#0EB198' }} onClick={updateAssetApply}>
                    Apply
                </Button>
                </div>
        </>}
      >
      <>
        <div>
            {/* <div className={Styles.WIAnameInput}>Borrowing base may 24th-Copy</div> */}
            <div className={Styles.WIAInformation}>
                Here, you have the ability to update the details of each and every asset with any value you choose and perform comprehensive 'what-if analysis' to evaluate various scenarios and potential outcomes based on those changes.
            </div>
            <div className={Styles.modificationSwitchContainer}>
                <Switch 
                    className={Styles.modificationSwitch} 
                    size="small" 
                    onChange={handleShowModificationChange} 
                    style={{backgroundColor:showModification ? "#1EBEA5":null }}
                    />
                Show rows with modifications
            </div>

        </div>

        <div className={Styles.tabsContainer}>
            {previewSheets?.map((sheet, index) => (
                <div onClick={() => handleSheetChange(sheet)} className={selectedSheetNumber == sheet ? Styles.active : Styles.tabs}>
                {sheet} 
                </div>
            ))}
        </div>
        <div className={Styles.tableContainer}>
            <table className={Styles.table}>
                <thead>
                <tr className={Styles.headRow}>
                    {updateAssetTableData && updateAssetTableData?.table_data[selectedSheetNumber]?.columns.map((col, index) => (
                    <th key={index} className={Styles.th}>
                        {col.label}
                    </th>
                    ))}
                    <th className={Styles.th}></th>
                </tr>
                </thead>
                <tbody>
                {updateAssetTableData && updateAssetTableData?.table_data[selectedSheetNumber]?.data.map((row, rowIndex) => (
                    <tr key={rowIndex}>
                    {updateAssetTableData && updateAssetTableData?.table_data[selectedSheetNumber]?.columns.map((col) => (
                        
                        <td 
                            key={col}
                            className={Styles.td}
                        >
                          
                                <div className={Styles.inputCellDiv}>
                                <input 
                                    className={showModification && getLatestPrevValue(updateAssetTableData?.changes ,appliedChanges, row[updateAssetDefaultColumnsData[selectedSheetNumber]], col.label) ? Styles.currValueInput : Styles.assetUpdateInput} 
                                    onFocus={() =>handleInputFocus(row[updateAssetDefaultColumnsData[selectedSheetNumber]],col.label)}
                                    type="text" 
                                    value={selectedCellData.investment_name == row[updateAssetDefaultColumnsData[selectedSheetNumber]] && selectedCellData.colName == col.label ? updateAssetInputText : row[col.key]  }  
                                    onChange={(e) => handleCellInputChange(e)} 
                                />
                                {selectedCellData.investment_name == row[updateAssetDefaultColumnsData[selectedSheetNumber]] && selectedCellData.colName == col.label  &&
                                <>
                                <img 
                                    style={{zIndex:200}} src={RightIcon} alt="Right Icon" 
                                    onClick={(e)=> handleCommitChange(e,row[updateAssetDefaultColumnsData[selectedSheetNumber]],col.key, col.label ,row[col.key])} 
                                />
                                <img 
                                    src={CrossIcon} alt="Cross Icon" 
                                    onClick={() => handleCancelChange()} 
                                />
                                </>
                                }
                                </div>
                            {showModification && getLatestPrevValue(updateAssetTableData?.changes ,appliedChanges, row[updateAssetDefaultColumnsData[selectedSheetNumber]], col.label) && 
                            <div className={`${Styles.inputCellDiv} ${Styles.prevValueText}`}>
                                {getLatestPrevValue(updateAssetTableData?.changes ,appliedChanges, row[updateAssetDefaultColumnsData[selectedSheetNumber]], col.label)}
                            </div>
                            }


                        </td>
                    ))}
                    <td className={Styles.td}>
                    <img onClick={() => updateAddDeleteData(rowIndex, 'duplicate')} src={DuplicateAssetIcon} alt="Duplicate Asset Icon" className={Styles.editAssetOptionImage} />

                    <Popover placement="bottomLeft" content={<MoreOptionContent rowIndex={rowIndex} />}>
                        <img src={MoreOptionsIcon} alt="More Options Icon" className={Styles.editAssetOptionImage} />
                    </Popover>
                    </td>
                    </tr>
                ))}
                </tbody>
            </table>
            </div>

      </>
        
      </Modal>

      <AddAssetDetailsModal
        addAssetDetailsModalOpen={addAssetDetailsModalOpen}
        setAddAssetDetailsModalOpen={setAddAssetDetailsModalOpen}
        addDeleteAssetData={addDeleteAssetData}
        selectedSheetNumber={selectedSheetNumber}
        handleAddDeleteAssets={handleAddDeleteAssets}
        enteredInputData={enteredInputData}
        setEnteredInputData={setEnteredInputData}

      />

    </>
  )
}
