import { Popover } from 'antd';
import React from 'react';
import { useDropzone } from 'react-dropzone';
import { showToast } from '../../../utils/helperFunctions/toastUtils';
import styles from './DynamicFileUploadComponent.module.css';

export const DynamicFileUploadComponent = ({
	uploadedFiles,
	setUploadedFiles,
	supportedFormats = ['xlsx', 'xlsm'], // supported extensions
	fundType,
	fileDownloadOptions = {},
	showDownload = true
}) => {
	// Setup Dropzone
	const { getRootProps, getInputProps } = useDropzone({
		accept: supportedFormats.reduce((acc, ext) => {
			acc[`.${ext}`] = [];
			return acc;
		}, {}),
		multiple: true,
		onDrop: (acceptedFiles) => {
			const validFiles = acceptedFiles.filter(file => {
				const fileExtension = file.name.split('.').pop()?.toLowerCase();
				return supportedFormats.includes(fileExtension);
			});

			if (validFiles.length > 0) {
				setUploadedFiles(prev => [...prev, ...validFiles]);
			} else {
				showToast('error', 'Invalid file format. Please upload a valid file.');
			}
		}
	});

	const downloadFile = fileDownloadOptions[fundType];

	return (
		<div>
			{showDownload && downloadFile && (
				<div className={styles.downloadContainer}>
					<Popover placement="bottomRight" content="Refer to sample template file">
						<a
							href={downloadFile.href}
							rel="noreferrer"
							download={downloadFile.name}
							className={styles.downloadLink}
						>
							Download sample file template
						</a>
					</Popover>
				</div>
			)}

			<div {...getRootProps({ className: styles.dropzone })}>
				<input {...getInputProps()} accept={supportedFormats.map(ext => `.${ext}`).join(',')} />
				<div>
					<b>
						{uploadedFiles?.length > 0
							? uploadedFiles.map((file) => file.name).join(', ')
							: 'Drag and drop files here, or'}
					</b>
					<span className={styles.browseText}>Browse</span>
				</div>
				<p className={styles.supportedFormats}>
					Supported file formats: {supportedFormats.map(ext => ext.toUpperCase()).join(', ')}
				</p>
			</div>
		</div>
	);
};
