import React from 'react';
import ButtonStyles from '../../components/Buttons/ButtonStyle.module.css';
import { Button, Input, Modal } from 'antd';
import { CustomButton } from '../../components/custombutton/CustomButton';

export const SaveAnalysisConfirmationModel = ({
    descriptionModal,
    handleCancel,
    isSetDescriptionModal,
    setDescriptionInput,
    whatIfanalysisLoader,
    save_what_if_analysis,
    descriptionInput
}) => {
    return (
        <Modal
                title="Do you want to add note?"
                centered
                open={descriptionModal}
                // onOk={handleSaveEbita}
                onCancel={handleCancel}
                width={'50%'}
                footer={[
                    <div key="footer-buttons" className="px-4">
                    <button key="back" onClick={()=>{isSetDescriptionModal(false); setDescriptionInput('') }} className={ButtonStyles.outlinedBtn}>
                        Cancel
                    </button>
                    <CustomButton
                    isFilled={true}
                    loading={whatIfanalysisLoader}
                    loadingText="Saving..."
                    text="Save"
                    onClick={save_what_if_analysis}
                    />
                    </div>
                ]}    
            >
                <>
                    <Input
                        type="text" 
                        placeholder='Notes'
                        value={descriptionInput}
                        style={{width:'80%' , margin:'1rem'}}
                        onChange={(e)=>setDescriptionInput(e.target.value)}
                    />
                </>
            </Modal>
    );
};


