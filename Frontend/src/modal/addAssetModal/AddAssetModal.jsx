import { Button, Modal } from 'antd';
import React from 'react';
import { useDropzone } from 'react-dropzone';
import ButtonStyles from '../../components/Buttons/ButtonStyle.module.css';
import { AddAssetSelectionTableModal } from '../addAssetSelectionTableModal/AddAssetSelectionTableModal';
import Styles from './AddAssetModal.module.css';

export const AddAssetModal = (
    {
        isModalVisible,
        handleOk,
        handleCancel,
        loading,
        selectedFiles,
        setSelectedFiles,
        setSelectedUploadedFiles,
        setLastUpdatedState,
        isPreviewModal,
        handleDownloadExcel,
        previewModal,
        previewData,
        setPreviewData,
        previewColumns,
        setAddAssetSelectedData
    }
    ) => {

    const { getRootProps, getInputProps } = useDropzone({
        accept: [
          'text/csv',
          'document/csv',
          'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        ],
        multiple: true,
        onDrop: (acceptedFiles) => {
          setSelectedFiles([...selectedFiles, ...acceptedFiles]);
          setSelectedUploadedFiles([]);
          setLastUpdatedState('selectedFiles');
        },
      });


  return (
    <>
        <Modal
            title={<span style={{ color: '#909090', fontWeight: '500', fontSize: '14px', padding: '0 0 0 3%' }}>Import</span>}
            centered
            open={isModalVisible}
            onOk={handleOk}
            onCancel={handleCancel}
            width={'50%'}
            footer={[
                <div key="footer-buttons" className="px-4">
                <button key="back" onClick={handleCancel} className={ButtonStyles.outlinedBtn}>
                    Cancel
                </button>
                <Button className={ButtonStyles.filledBtn} loading={loading} key="submit" type="primary" style={{ backgroundColor: '#0EB198' }} onClick={handleOk}>
                    Load
                </Button>
                </div>
                ]}
        >
          <div className={Styles.container}>
            <div>
              <div>
                <p style={{ fontWeight: '500', fontSize: '20px', marginBottom: '-5px' }}>Upload File</p>
              </div>
              <br />
              <div>
                <div className={Styles.visible}>
                  <div {...getRootProps({ className: 'dropzone' })}>
                    <input {...getInputProps()} />
                    <div>
                      <span>
                        <b>{selectedFiles.length ? selectedFiles.map((file) => file.name).join(', ') : 'Drag and drop files here, or'}</b>
                      </span>
                      <span
                        style={{
                          color: '#3B7DDD',
                          textDecoration: 'underline',
                          cursor: 'pointer',
                          marginLeft: '5px'
                        }}
                      >
                        Browse
                      </span>
                    </div>
                    <p style={{ fontWeight: '400', color: 'rgb(109, 110, 111)' }}>Supported file format: CSV, XLSX</p>
                  </div>
                </div>
                <br />
              </div>
            </div>

            <div style={{ display: "flex", justifyContent: "space-between", paddingRight: "1rem" }}>
                {selectedFiles.length > 0 ? (
                  <div style={{ display: "flex", justifyContent: "space-between", width: "100%" }}>
                    <a
                      style={{
                        color: '#3B7DDD',
                        textDecoration: 'underline',
                        cursor: 'pointer',
                        marginLeft: '5px'
                      }}
                      onClick={handleDownloadExcel}
                    >
                      Download Created Assets
                    </a>
                    <button className={ButtonStyles.filledBtn} onClick={() => isPreviewModal(true)}>Asset Selection</button>
                  </div>
                ) : null}
                <AddAssetSelectionTableModal previewModal={previewModal} isPreviewModal={isPreviewModal} previewData={previewData} setPreviewData={setPreviewData} previewColumns={previewColumns} setAddAssetSelectedData={setAddAssetSelectedData} />
              </div>


            <div>
            {/* <Popover   placement="bottomRight" open={guidePopupOpen} content={<>Refer to sample template file</>} >
                  <a href="">Download sample file template</a>
            </Popover> */}
            </div>
          </div>
        </Modal>
    </>
  );
};
