import { Modal, Popover } from 'antd';
import React from 'react';
import { useDropzone } from 'react-dropzone';
import PCOFAddSecSampleFile from '../../assets/template File/PCOF Add Base Data.xlsx';
import PFLTAddSecSampleFile from '../../assets/template File/PFLT Add Base Data.xlsx';
import { CustomButton } from '../../components/uiComponents/Button/CustomButton';
import { uploadAddMoreSecFile } from '../../services/dataIngestionApi';
import { showToast } from '../../utils/helperFunctions/toastUtils';
import styles from "./FileUploadModal.module.css";
import { ModalComponents } from '../../components/modalComponents';

export const FileUploadModal = ({ isOpenFileUpload, handleCancel, addsecFiles, setAddsecFiles, previewFundType, dataId, reportId, handleBaseDataPreview }) => {
	const { getRootProps, getInputProps } = useDropzone({
		accept: {
			'text/csv': [],
			'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': []
		},
		multiple: false,
		onDrop: (acceptedFiles) => {
			setAddsecFiles((prevFiles) => [...prevFiles, ...acceptedFiles]);
		}
	});

	const handleSave = async () => {
		if (addsecFiles.length === 0) {
			showToast('error', "Please upload a file before saving.");
			return;
		}

		try {
			const file = addsecFiles[0];
			const response = await uploadAddMoreSecFile(file, dataId, previewFundType, reportId);
			const message = response?.data?.message || "File uploaded successfully.";

			if (response?.data?.success) {
				showToast('success', message);
				setAddsecFiles([]);
				handleCancel();
				await handleBaseDataPreview();
			} else {
				showToast('error', message);
			}
		} catch (error) {
			showToast('error', "Failed to upload file.");
		}
	};



	return (
		<Modal
			title={<ModalComponents.Title title='Add Securities Data' showDescription={true} description="Add more securities data which are not present in the extracted base data" />}
			open={isOpenFileUpload}
			onCancel={handleCancel}
			footer={null}
			width={700}
		>
			<div className={styles.downloadContainer}>
				<Popover placement="bottomRight" content={<>Refer to sample template file</>}>
					<a
						href={previewFundType === "PCOF" ? PCOFAddSecSampleFile : PFLTAddSecSampleFile}
						rel="noreferrer"
						download={previewFundType === "PCOF" ? 'PCOF Add Base Data.xlsx' : 'PFLT Add Base Data.xlsx'}
						className={styles.downloadLink}
					>
						Download sample file template
					</a>
				</Popover>
			</div>
			<div {...getRootProps({ className: styles.dropzone })}>
				<input {...getInputProps()} />
				<div>
					<b>
						{addsecFiles?.length > 0
							? addsecFiles.map((file) => file.name).join(', ')
							: 'Drag and drop files here, or'}
					</b>
					<span className={styles.browseText}>Browse</span>
				</div>
				<p className={styles.supportedFormats}>
					Supported file formats: CSV, XLSX
				</p>
			</div>
			<div className={styles.buttonContainer}>
				<CustomButton isFilled={false} text="Cancel" onClick={handleCancel} />
				<CustomButton isFilled={true} text="Save" onClick={handleSave} />
			</div>
		</Modal>
	);
};
