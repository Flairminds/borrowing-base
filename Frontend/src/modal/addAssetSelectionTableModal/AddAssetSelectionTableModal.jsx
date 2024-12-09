import React from 'react'
import { AddAssetDynamicTable } from '../../components/addAssetDynamicTable/AddAssetDynamicTable'
// import ButtonStyles from "../../components/Buttons/ButtonStyle.module.css";
// import {Whatif_Columns,Whatif_data} from "../../utils/Whatif_Data"
import  buttonStyle from '../../components/Buttons/ButtonStyle.module.css'
import { Modal } from 'antd';
import { useEffect, useState } from 'preact/hooks';
import { CreateAssetModal } from '../createAssetModal/CreateAssetModal';
import { generateAssetFormData, generateEmptyAssetFormData } from '../../utils/helperFunctions/addAssetFormData'

export const AddAssetSelectionTableModal = ({previewModal,isPreviewModal,previewColumns,previewData,setPreviewData,setAddAssetSelectedData}) => {
    const handleCancel = () => {
        isPreviewModal(false)
      };

      const [createAssetModalOpen, setCreateAssetModalOpen]= useState(false);
      const [createAssetFormData, setCreateAssetFormData] = useState();
      const [modificationData, setModificationData] = useState({
        data : '',
        index:''
      });
      

      const [selectedAssets, setSelectedAssets] = useState([]);
      const [showModifyButton, setShowModifyButton] = useState(true);


      useEffect(() => {
        setSelectedAssets(Array(previewData?.length).fill(true))
      },[previewData])

      const modifyAssetsData = (index, data) =>
      {
        if(index != -1)
        {
          const previewDataArray  = previewData;
          previewDataArray[index] = data;
          setPreviewData(previewDataArray);
        }
        else
        {
          setPreviewData([data, ...previewData]);
        }
        
      }

      const handleCreateAsset = () => {
        const modifiedData = generateEmptyAssetFormData()
        setShowModifyButton(false);
        setCreateAssetFormData(modifiedData);
        setCreateAssetModalOpen(true);
      }

      const handleSubmit = () => {
        let selectedData = [];
        for(let i =0 ; i<previewData.length ; i++)
          {
            if(selectedAssets[i] == true)
              {
                selectedData.push(previewData[i]);
              }
    
          }
          setAddAssetSelectedData(selectedData);
          isPreviewModal(false)
        }


  return (

    <div>
        <Modal
                title={<span style={{ color: '#909090', fontWeight: '500', fontSize: '14px', padding: '0 0 0 3%' }}></span>}
                centered
                open={previewModal}
                onOk={handleCancel}
                onCancel={handleCancel}
                width={'70%'}
                footer={[
                  
                  ]}
            >
              <div style={{textAlign:'end', padding:'1rem'}} >
                  <button className={buttonStyle.filledBtn} onClick={handleCreateAsset} > Create Asset </button>
              </div>
                
                <div style={{height:"70vh"}}>
                  <AddAssetDynamicTable data={previewData} columns={previewColumns} selectedAssets={selectedAssets} setSelectedAssets={setSelectedAssets} setModificationData={setModificationData} setCreateAssetModalOpen={setCreateAssetModalOpen} setCreateAssetFormData={setCreateAssetFormData}/>
                </div>

                <div style={{margin:'1rem', textAlign:'end'}}>
                  <button className={buttonStyle.filledBtn} style={{padding:'0.3rem 0.7rem'}} onClick={handleSubmit}> Submit</button>
                </div>

                <CreateAssetModal 
                  createAssetModalOpen={createAssetModalOpen} 
                  setCreateAssetModalOpen={setCreateAssetModalOpen} 
                  createAssetFormData={createAssetFormData} 
                  setCreateAssetFormData={setCreateAssetFormData} 
                  modifyAssetsData={modifyAssetsData} 
                  modificationData={modificationData} 
                  setModificationData={setModificationData} 
                  showModifyButton={showModifyButton}
                  setShowModifyButton={setShowModifyButton}
                />

            </Modal>
            
    </div>
  )
}
