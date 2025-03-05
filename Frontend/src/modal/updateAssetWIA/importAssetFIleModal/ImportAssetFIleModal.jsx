import { Modal } from 'antd';
import React, { useEffect, useState } from 'react';
import { useDropzone } from "react-dropzone";
import * as XLSX from "xlsx";
import { CustomButton } from '../../../components/custombutton/CustomButton';
import { cloWhatIfData, updateAssetDefaultColumnsData } from '../../../utils/constants/constants';
import { showToast } from '../../../utils/helperFunctions/toastUtils';
import { getCurrencyNumber, updateDataAfterChange } from '../../../utils/helperFunctions/updateAssetDataChange';
import styles from './ImportAssetFIleModal.module.css';

export const ImportAssetFIleModal = (
	{
		isOpen,
		setIsopen,
		updateAssetTableData,
		selectedSheetNumber,
		appliedChanges,
		setAppliedChanges,
		setIsButtonDisabled,
		fundType
	}) => {

	const [selectedFiles, setSelectedFiles] = useState([]);

	const handleCancel = () => {
		setSelectedFiles([]);
		setIsopen(false);
	};

	const { getRootProps, getInputProps } = useDropzone({
		accept: {
			'text/csv': [],
			'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': []
		},
		multiple: false,
		onDrop: (acceptedFiles) => {
			setSelectedFiles(acceptedFiles);
		}
	});

	const updateWhatIfSheetData = (excelFileData) => {
		if (excelFileData.length > 0) {
			const changesArray = [];
			for (let i = 0; i < excelFileData.length; i++) {
				const currentEntry = excelFileData[i];
				if (!currentEntry["Obligor Name"]) continue;
				// let filteredData = updateAssetTableData.table_data[selectedSheetNumber].data?.filter(el => el.Security_Name.toLowerCase().replace(/-/g, " ").replace(/,/g, "").replace(/\./g, "") == currentEntry["Security Name"].toLowerCase().replace(/-/g, " ").replace(/,/g, "").replace(/\./g, "") && el.Obligor_Name.toLowerCase().replace(/-/g, " ").replace(/,/g, "").replace(/\./g, "") == currentEntry["Obligor Name"].toLowerCase().replace(/-/g, " ").replace(/,/g, "").replace(/\./g, ""));

				let filteredData = updateAssetTableData.table_data[selectedSheetNumber].data?.
					filter((el) => {
						let isMatch = true;
						cloWhatIfData[fundType].matchingColumns.forEach((col) => {
							if (el[col.key].toLowerCase().replace(/-/g, " ").replace(/,/g, "").replace(/\./g, "") != currentEntry[col.label].toLowerCase().replace(/-/g, " ").replace(/,/g, "").replace(/\./g, "")) {
								isMatch = false;
							}
						});
						return isMatch;
					});
				if (filteredData.length <= 0) continue;
				filteredData = filteredData[0];

				if (fundType === "PCOF") {
					const updatedPar = getCurrencyNumber(filteredData["Investment Par"]) - getCurrencyNumber(currentEntry["Investment Par CLO"]);
					const commitmentChanges = {
						"row_name": filteredData[updateAssetDefaultColumnsData[selectedSheetNumber]],
						"column_name": "Investment Par",
						"updated_value": `${updatedPar}`,
						"prev_value": filteredData['Investment_Par']
					};
					changesArray.push(commitmentChanges);
					updateDataAfterChange(
						updateAssetTableData,
						filteredData[updateAssetDefaultColumnsData[selectedSheetNumber]],
						'Investment_Par',
						selectedSheetNumber,
						updatedPar
					);
				} else {
					// Update total commitment
					let updatedCommitment = getCurrencyNumber(filteredData['Total_Commitment_(Issue_Currency)']) - getCurrencyNumber(currentEntry["Total Commitment (Issue Currency) CLO"]);

					if (updatedCommitment < 0) {
						updatedCommitment = 0;
					}

					const commitmentChanges = {
						"row_name": filteredData[updateAssetDefaultColumnsData[selectedSheetNumber]],
						"column_name": "Total Commitment (Issue Currency)",
						"updated_value": `${updatedCommitment}`,
						"prev_value": filteredData['Total_Commitment_(Issue_Currency)']
					};
					changesArray.push(commitmentChanges);
					updateDataAfterChange(
						updateAssetTableData,
						filteredData[updateAssetDefaultColumnsData[selectedSheetNumber]],
						'Total_Commitment_(Issue_Currency)',
						selectedSheetNumber,
						updatedCommitment
					);
					// Update Outstanding principal
					let updatedOutstanding = getCurrencyNumber(filteredData["Outstanding_Principal_Balance_(Issue_Currency)"]) - getCurrencyNumber(currentEntry["Outstanding Principal Balance (Issue Currency) CLO"]);

					if (updatedOutstanding < 0) {
						updatedOutstanding = 0;
					}
					const outstandingChanges = {
						"row_name": filteredData[updateAssetDefaultColumnsData[selectedSheetNumber]],
						"column_name": "Outstanding Principal Balance (Issue Currency)",
						"updated_value": `${updatedOutstanding}`,
						"prev_value": filteredData['Outstanding_Principal_Balance_(Issue_Currency)']
					};
					changesArray.push(outstandingChanges);
					updateDataAfterChange(
						updateAssetTableData,
						filteredData[updateAssetDefaultColumnsData[selectedSheetNumber]],
						'Outstanding_Principal_Balance_(Issue_Currency)',
						selectedSheetNumber,
						updatedOutstanding
					);

				}

			}

			setAppliedChanges([...appliedChanges, ...changesArray]);
			setIsButtonDisabled(false);
		}
	};

	const handleFileUpload = () => {
		if (selectedFiles.length <= 0) {
			showToast("error", "Please upload a file");
			return;
		}
		const file = selectedFiles[0];
		const reader = new FileReader();

		reader.onload = (event) => {
			const data = new Uint8Array(event.target.result);
			const workbook = XLSX.read(data, { type: "array" });

			// const sheetName = workbook.SheetNames[0];
			const sheetName = 'CLO Data';
			const sheet = workbook.Sheets[sheetName];
			if (!sheet) {
				alert("File should have a 'CLO Data' sheet with required data. Please export for template.");
			}
			const excelFileData = XLSX.utils.sheet_to_json(sheet);
			updateWhatIfSheetData(excelFileData);
		};

		reader.readAsArrayBuffer(file);

		setIsopen(false);
		setSelectedFiles([]);

	};


	return (
		<Modal open={isOpen} onCancel={handleCancel} footer={null} width={"50%"}>
			<div className={styles.popupTitle}>
				Upload File
			</div>

			<div className={styles.fileUploadContainer}>
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

			<div className={styles.popupFooter}>
				<CustomButton isFilled={true} text='Upload' onClick={handleFileUpload} />
				<CustomButton text='Cancel' onClick={handleCancel} />
			</div>

		</Modal>
	);
};
