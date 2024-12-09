import React, { useState } from 'react';
import { Button, Modal } from 'antd';
import { TableComponent } from '../../components/Tables/TableComponent';
import stylesModalTable from "./TableViewModal.module.css"

export const TableViewModal = ({setOpenModal, openModal, data, columns, heading}) => {
  return (
    <div>
        <Modal
            title={
                <div className={stylesModalTable.heading}>
                      <h5 >{heading != '' ? heading : null}</h5>
                </div>
            }
            centered
            open={openModal}
            onOk={() => setOpenModal(false)}
            onCancel={() => setOpenModal(false)}
            width={1000}
            footer={[
              ]}
            >
            <div className={stylesModalTable.main}>
                <div className={stylesModalTable.btnDiv}>
                    <button className={stylesModalTable.buttonsFilled}>Included</button>
                    {/* <button className={stylesModalTable.buttons}>Not included</button> */}
                </div>
                <div>
                    <TableComponent data={data} columns={columns} showviewMore={false} />
                </div>
                
            </div>
            

        </Modal>
  </div>
  )
}
