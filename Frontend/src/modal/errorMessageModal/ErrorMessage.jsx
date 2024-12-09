import { Modal, Button } from 'antd';
import parse from 'html-react-parser';
import React from 'react';
import waring from "../../assets/uploadFIle/warning.svg";
import ButtonStyles from "../../components/Buttons/ButtonStyle.module.css";

export const ErrorMessage = ({errorMessageModal, setErrorMessageModal, errorMessageData}) => {

    // const ErrorKeys = Object.keys(errorMessageData)
    const ErrorKeys = ['Sheet Modifications', 'Column Modifications', 'Data Format Modifications', 'Row Modifications'];

  return (
    <>
      <Modal
            title={
            <div style={{display: "flex", flexDirection: "column"}}>
                    <div style={{display: "flex", marginBottom: '0.3rem 0rem' }}>
                        <img style={{height: "20px", width: "40px", marginTop: "5px"}} src={waring}/>
                        <span style={{ fontWeight: '600', fontSize: '20px', padding: '0' }}>
                            Unable to process your excel file</span>
                        </div>
                {/* <div style={{display:"flex",flexDirection:"column", paddingLeft:"9px"}}>
                    <span style={{fontWeight:"400", fontSize:"14px", paddingLeft:"32px", paddingTop:"10px"}}>Percent column of 'Pricing' sheet must be float64</span>
                </div> */}
                </div>}
            centered
            open={errorMessageModal}
            // onOk={handleEbitaAnalysis}
            onCancel={() => setErrorMessageModal(false)}
            width={'50%'}
            footer={[
                <div key="footer-buttons" >
                {/* <button key="back" onClick={()=>setEbitdaModalOpen(false)} className={ButtonStyles.outlinedBtn}>
                    Cancel
                </button> */}
                <Button className={ButtonStyles.filledBtn}
                        key="submit" type="primary" style={{ backgroundColor: '#0EB198' }} onClick={() => setErrorMessageModal(false)}
                >
                    Got it
                </Button>
                </div>
            ]}
            >
                <div style={{margin: '1rem 1rem'}}>
                    {/* <Input
                        type="text"
                        placeholder='EBITDA values supported values : -99 to 100'
                        style={{width:'80%' , margin:'1rem'}}
                        // onChange={(e)=>setEbitaChangeValue(e.target.value)}
                    /> */}

                    {ErrorKeys.map((el) => (
                        <>
                            {errorMessageData[el]?.length > 0 ?
                                <>
                                    <h6>{el}</h6>
                                    <ul>
                                        {errorMessageData[el].map((error) => (
                                        <li key={error}>{parse(error)}</li>
                                        ))}
                                    </ul>
                                </>
                                :
                                null
                            }
                        </>
                    )
                    ) }

                    {/* {parse('<h1>Hello, World!</h1>')} */}

                </div>
            </Modal>
    </>


  );
};
