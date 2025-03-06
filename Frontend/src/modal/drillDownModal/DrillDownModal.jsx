import { Modal } from 'antd';
import parse from 'html-react-parser';
import { useEffect, useState } from 'preact/hooks';
import React from 'react';
import { toast } from 'react-toastify';
import { drillDownData } from '../../services/api';
import style from './DrillDownModal.module.css';

export const DrillDownModal = (
    {
        drillDownPopupOpen,
        setDrillDownPopupOpen,
        drillDownPopupData,
        setDrillDownPopupData,
        baseFile,
        drillDownString,
        setDrillDownString,
        whatIfAnalysisId
    }) => {


    const [drillDownState, setDrillDownState] = useState(false);
    const [drillDownStateData, setDrillDownStateData] = useState();
    const [drillDownStateString, setDrillDownStateString] = useState(drillDownString);

    const handleValue = async(col_name) => {
        try {
            const res = await drillDownData(1,baseFile.id, col_name, drillDownPopupData.row_name, whatIfAnalysisId);
            setDrillDownStateString(drillDownString + " > " + col_name);
            setDrillDownStateData(res.data.response_dict);
            setDrillDownState(true);
        } catch (err) {
            toast.error('The value cannot be broken down further.');
            console.error(err);
        }
        setDrillDownPopupOpen(true);
    };

    const addEvents = () => {
        drillDownPopupData?.formula_variable_data?.forEach((id) => {
              const element = document.getElementById(id.key);
              if (element) {
                    element.style.color = id.color;
                    element.onclick = () => handleValue(id.value);
                }
            });
                        drillDownPopupData?.formula_values_data?.forEach((id) => {
              const spanelement = document.getElementById(id.key);
              if (spanelement) {
                    spanelement.style.color = id.color;
                }
            });
    };

    useEffect(() => {
        setTimeout(() => {
            addEvents();
        }, 1000);
    });


    return (
    <>
        <Modal
                title={<span style={{ color: '#909090', fontWeight: '500', fontSize: '14px', padding: '0 0 0 3%' }}>Formula</span>}
                centered
                open={drillDownPopupOpen}
                // onOk={handleOk}
                // onCancel={handleCancel}
                onCancel={() => setDrillDownPopupOpen(false)}
                width={'70%'}
                footer={[
                  <></>
                  ]}
        >
            <>
            <div className={style.drillDowmInfo}>{drillDownString}</div>
            <div className={style.popUpContainer}>
                <div className={style.infoDiv}>
                    <div className={style.titleDiv}>
                        <span className={style.titlelable}>
                           Parameter :
                        </span>
                        {drillDownPopupData?.col_name}
                    </div>
                </div>

                <div className={style.infoDiv}>
                    <div className={style.titleDiv}>
                        <span className={style.titlelable}>
                            Company :
                        </span>
                        {drillDownPopupData?.row_name}
                    </div>
                </div>
                <div className={`${style.infoDiv} ${style.formulaDiv}`}>
                    <div style={{overflowX: 'auto', whiteSpace: 'nowrap', padding: '0.5rem'}}>
                    {parse(drillDownPopupData?.formula_variable_string ? drillDownPopupData?.formula_variable_string : "<> </>" )}
                    </div>
                </div>
                <div className={style.infoDiv}>
                    {parse(drillDownPopupData?.formula_values_string ? drillDownPopupData?.formula_values_string : "<> </>" )}
                </div>

            </div>
            </>

            <DrillDownModal
                drillDownPopupOpen={drillDownState}
                setDrillDownPopupOpen={setDrillDownState}
                drillDownPopupData={drillDownStateData}
                setDrillDownPopupData={setDrillDownStateData}
                baseFile={baseFile}
                drillDownString={drillDownStateString}
                setDrillDownString={setDrillDownString}
            />
        </Modal>

    </>

  );
};