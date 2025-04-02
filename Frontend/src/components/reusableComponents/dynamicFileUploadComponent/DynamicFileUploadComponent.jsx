import { Popover } from 'antd';
import React from 'react';
import { useDropzone } from 'react-dropzone';
import styles from './DynamicFileUploadComponent.module.css';


const mimeTypeMap = {
	csv: 'text/csv',
	xlsx: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
	pdf: 'application/pdf'
};

export const DynamicFileUploadComponent = ({
	uploadedFiles,
	setUploadedFiles,
	supportedFormats = ['csv', 'xlsx'],
	fundType,
	fileDownloadOptions = {},
	showDownload = true
}) => {

	const acceptedMimeTypes = supportedFormats
		.map(ext => mimeTypeMap[ext])
		.filter(Boolean);

	const { getRootProps, getInputProps } = useDropzone({
		accept: acceptedMimeTypes.reduce((acc, format) => ({ ...acc, [format]: [] }), {}),
		multiple: false,
		onDrop: (acceptedFiles) => {
			const file = acceptedFiles[0];
			if (file && acceptedMimeTypes.includes(file.type)) {
				setUploadedFiles([file]);
			} else {
				alert("Invalid file format. Please upload a valid file.");
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
				<input {...getInputProps()} />
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
