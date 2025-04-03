import React, { useState } from 'react';
import { Button, Modal } from 'antd';
export const SrcFileValidationErrorModal = ({
    isModalOpen=false,
    setIsModalOpen,
    validationInfoData=[]
}) => {
  
  const handleOk = () => {
    setIsModalOpen(false);
  };
  const handleCancel = () => {
    setIsModalOpen(false);
  };
  
  return (
    <>
      <Modal title={"List of Errors"} open={isModalOpen} footer={null} onCancel={handleCancel}>
             {
                validationInfoData.length > 0 &&
                <>
                    {validationInfoData.map((item, index) => {
                        return (
                            <ul key={index}>
                                {item && (
                                    <li>
                                        Column <b>{item?.column_name}</b> of sheet <b>{item?.sheet_name}</b>{" "}
                                        {item?.is_column_available
                                        ? `required ${item?.expected_type} but is in ${item?.actual_type} data type.`
                                        : `is not available.`}
                                    </li>
                                )}
                            </ul>
                        )
                    })}
                </>
             }
             
      </Modal>
    </>
  );
};
