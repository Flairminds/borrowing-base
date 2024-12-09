import { Modal } from 'antd'
import React from 'react'
import Styles from './ColumnSelectionPopup.module.css'
import { parametersForSelection } from '../../utils/parameterSelectionData'
import ButtonStyles from '../../components/Buttons/ButtonStyle.module.css'
import { useEffect, useState } from 'preact/hooks'
import { assetSelectionList, setConfigurations } from '../../services/api'
import { toast } from 'react-toastify'

export const ColumnSelectionPopup = ({setAssetSelectionData,assetSelectionData,baseFile, columnSelectionPopupOpen, setColumnSelectionPopupOpen,fundType}) => {
    
    const [selectedColumns,  setSelectedColumns] = useState([])
    const [checkBoxesDisabled, setCheckBoxesDisabled] = useState(false)

    const handleCheckBoxClick = (key) => {
        setSelectedColumns((prevSelectedKeys) =>
            prevSelectedKeys.includes(key)
              ? prevSelectedKeys.filter((selectedKey) => selectedKey !== key)
              : [...prevSelectedKeys, key]
          )
    }
    useEffect(() => {
        if(selectedColumns.length < 4)
            {
                setCheckBoxesDisabled(false);
            }
            else
            {
                setCheckBoxesDisabled(true)
            }
    }, [selectedColumns])

    const setConfiguration = async() => {
       
        const payload = {
            user_id : 1,
            assets_selection_columns : selectedColumns,
        }
        try{
            const res = await setConfigurations(payload);
            assestSelection()
            toast.success('Configurations Set Successfully')
        }
        catch(err)
        {
            console.error(err);
        }
        setColumnSelectionPopupOpen(false);
    }

    const handleCancel = () => {
        setColumnSelectionPopupOpen(false)
    }
    const assestSelection =async() =>{
                try {
                  const res =  await assetSelectionList(baseFile.id);
                  setAssetSelectionData(res.data.assets_list);
                  setAssetSelectionData({...assetSelectionData,'assetSelectionList': res.data
                  });
                  getTrendGraphData(fundType);
                  setDate(null)
                }
                catch(err){
                  console.error(err);
                }
    }

  return (
    <>
        <Modal
                title={
                    <div style={{display:"flex", justifyContent:"space-between"}}>
                        <span style={{ color: '#909090', fontWeight: '600', fontSize: '18px', padding: '0 0 0 3%' }}>Select Parameters for Asset Selection</span>
                        <span style={{ color: '#909090', fontWeight: '500', fontSize: '14px', padding: '0rem 2rem' }}>*Select upto 4 Paramerts</span>
                    </div>
            }
                centered
                open={columnSelectionPopupOpen}
                onOk={setConfiguration}
                onCancel={handleCancel}
                width={'70%'}
                footer={[
                  <div key="footer-buttons" className="px-4">
                    <button key="back" onClick={setConfiguration} style={{padding:'5px 10px'}} className={ButtonStyles.filledBtn}>
                      Set
                    </button>
                  </div>
                  ]}
            >
            <>
                <div className={Styles.popUpContainer}>
                    <div className={Styles.errorMessage}>{checkBoxesDisabled == true ? <>*Only 4 columns allowded</> : null }</div>
                    <div className={Styles.listContainer}>
                        {parametersForSelection.map((parameter, index) => (
                            <>
                                <div key={index} className={Styles.listItem}>
                                    <input disabled={checkBoxesDisabled && !selectedColumns.includes(parameter.key)} type="checkbox" style={{margin: '0px 5px'}} onClick={() => handleCheckBoxClick(parameter.key)} />
                                    {parameter.label}
                                </div>
                            </>
                        ))
                        }
                    </div>

                </div>      
              
            </>
            </Modal>

    </>
  )
}