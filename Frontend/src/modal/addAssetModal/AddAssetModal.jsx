import { Button, Modal } from 'antd';
import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { ModalComponents } from '../../components/modalComponents';
import { UIComponents } from '../../components/uiComponents';
import ButtonStyles from '../../components/uiComponents/Button/ButtonStyle.module.css';
import { CustomButton } from '../../components/uiComponents/Button/CustomButton';
import { PCOFAddAssetData } from '../../utils/constants/addAssetSampleData';
import { exportToExcel } from '../../utils/helperFunctions/jsonToExcel';
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
		setAddAssetSelectedData,
		isAddLoadBtnDisable,
		fundType
	}
) => {


	const { getRootProps, getInputProps } = useDropzone({
		accept: {
			'text/csv': [],
			'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': []
		},
		multiple: true,
		onDrop: (acceptedFiles) => {
			setSelectedFiles([...selectedFiles, ...acceptedFiles]);
			setSelectedUploadedFiles([]);
			setLastUpdatedState('selectedFiles');
		}
	});

	const handleSampleFileDownload = () => {
		if (fundType === 'PCOF') {
			exportToExcel(PCOFAddAssetData, "PCOFAddAssetSampleFile.xlsx");
		} else {
			exportToExcel(PCOFAddAssetData, "PCOFAddAssetSampleFile.xlsx");
		}
	};

	return (
		<>
			<Modal
				title={<ModalComponents.Title title='Import File' />}
				centered
				open={isModalVisible}
				onOk={handleOk}
				onCancel={handleCancel}
				width={'50%'}
				footer={[
					<ModalComponents.Footer key={'footer-buttons'} onClickCancel={handleCancel} onClickSubmit={handleOk} submitText={'Load'} loading={loading} submitBtnDisabled={isAddLoadBtnDisable}/>
				]}
			>
				<div className={Styles.container}>
					<div>
						{/* <div>
							<p style={{ fontWeight: '500', fontSize: '20px', marginBottom: '-5px' }}>Upload File</p>
						</div> */}
						{/* <br /> */}
						<div
							onClick={handleSampleFileDownload}
							style={{ color: "#3B7DDD", textDecoration: "underline", cursor: "pointer" }}
						>
							DownloadSimpleFile
						</div>
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
								<UIComponents.Button onClick={() => isPreviewModal(true)} isFilled={true} text={'Asset Selection'} />
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
