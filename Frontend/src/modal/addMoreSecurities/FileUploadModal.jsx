import { Modal } from 'antd';
import React, { useEffect, useState } from 'react';
import * as XLSX from 'xlsx';
import PCOFAddSecSampleFile from '../../assets/template File/PCOF Add Base Data.xlsx';
import PFLTAddSecSampleFile from '../../assets/template File/PFLT Add Base Data.xlsx';
import { ModalComponents } from '../../components/modalComponents';
import { DynamicFileUploadComponent } from '../../components/reusableComponents/dynamicFileUploadComponent/DynamicFileUploadComponent';
import { CustomButton } from '../../components/uiComponents/Button/CustomButton';
import { uploadAddMoreSecFile, validateAddSecurities } from '../../services/dataIngestionApi';
import { showToast } from '../../utils/helperFunctions/toastUtils';
import { SrcFileValidationErrorModal } from '../srcFIleValidationErrorModal/srcFileValidationErrorModal';
import styles from "./FileUploadModal.module.css";


export const FileUploadModal = ({ isOpenFileUpload, handleCancel, addsecFiles, setAddsecFiles, previewFundType, dataId, reportId, handleBaseDataPreview, data }) => {
	const [validationInfo, setValidationInfo] = useState([]);
	const [validationModal, setValidationModal] = useState(false);

	useEffect(() => {
		if (!isOpenFileUpload) {
			setAddsecFiles([]);
		}
	}, [isOpenFileUpload]);

	const EXCEL_COLUMNS = {
		PFLT: ["obligor name", "security name", "loan type"],
		PCOF: ["investment name", "issuer"]
	};

	const DATA_COLUMNS = {
		PFLT: ["obligor_name", "security_name", "loan_type"],
		PCOF: ["investment_name", "issuer"]
	};

	const showDuplicateModal = (processedRows, previewFundType, onConfirm, onCancel) => {
		const isNewAdded = processedRows.some((d) => d.action === "add");

		Modal.confirm({
			title: <span style={{lineHeight: "2rem"}}>{"Records Found"}</span>,
			content: (
				<>
					<p><strong>Duplicate Records Found :</strong></p>
					<ul>
						{processedRows
							.filter((d) => d.action === "overwrite")
							.map((d, index) => (
								<li key={index}>
									{previewFundType === "PFLT" ? (
										<>
											<strong>Obligor:</strong> {d["Obligor Name"]},{" "}
											<strong>Security:</strong> {d["Security Name"]},{" "}
											<strong>Loan Type:</strong> {d["Loan Type (Term / Delayed Draw / Revolver)"]}
										</>
									) : (
										<>
											<strong>Investment Name:</strong> {d["Investment Name"]},{" "}
											<strong>Issuer:</strong> {d["Issuer"]}
										</>
									)}
								</li>
							))}
					</ul>
					{isNewAdded && <p><strong>New Records Found :</strong></p>}
					<ul>
						{processedRows
							.filter((d) => d.action === "add")
							.map((d, index) => (
								<li key={index}>
									{previewFundType === "PFLT" ? (
										<>
											<strong>Obligor:</strong> {d["Obligor Name"]},{" "}
											<strong>Security:</strong> {d["Security Name"]},{" "}
											<strong>Loan Type:</strong> {d["Loan Type (Term / Delayed Draw / Revolver)"]}
										</>
									) : (
										<>
											<strong>Investment Name:</strong> {d["Investment Name"]},{" "}
											<strong>Issuer:</strong> {d["Issuer"]}
										</>
									)}
								</li>
							))}
					</ul>
				</>
			),
			icon: <span style={{ color: "red", fontSize: "18px" }}>⚠️</span>,
			okText: "Confirm",
			cancelText: "Cancel",
			onOk: onConfirm,
			onCancel: onCancel,
			okButtonProps: {
				style: { backgroundColor: "#0EB198", borderColor: "#0EB198", color: "#fff" }
			},
			cancelButtonProps: {
				style: {
					borderColor: "#0EB198",
					color: "#000",
					backgroundColor: "#fff",
					':hover': { borderColor: "#0EB198", color: "#000" },
					':focus': { borderColor: "#0EB198", color: "#000" }
				}
			}
		});
	};

	const readExcelFile = (file) => {
		return new Promise((resolve, reject) => {
			const reader = new FileReader();
			reader.readAsBinaryString(file);
			reader.onload = (e) => {
				try {
					const binaryStr = e.target.result;
					const workbook = XLSX.read(binaryStr, { type: "binary", cellDates: true });
					const sheetName = workbook.SheetNames[0];
					const sheetData = XLSX.utils.sheet_to_json(workbook.Sheets[sheetName], { header: 1 });
					const formatDate = (date) => {
						if (Object.prototype.toString.call(date) === "[object Date]" && !isNaN(date)) {
							const month = (date.getMonth() + 1).toString().padStart(2, "0");
							const day = date.getDate().toString().padStart(2, "0");
							const year = date.getFullYear();
							return `${month}-${day}-${year}`;
						}
						return date;
					};

					const formattedData = sheetData.map((row) =>
						row.map((cell) => (typeof cell === "object" && cell instanceof Date ? formatDate(cell) : cell))
					);

					resolve(formattedData);
				} catch (error) {
					reject("Error reading Excel file");
				}
			};

			reader.onerror = () => reject("File reading failed");
		});
	};

	const processExcelData = (sheetData, previewFundType) => {
		const columnMap = DATA_COLUMNS[previewFundType];
		const headers = sheetData[0].map((h) => {
			const lower = h?.toString().trim();
			return columnMap.find((col, i) => lower.includes(EXCEL_COLUMNS[previewFundType][i])) || lower;
		});
		return sheetData.slice(1).map((row) => {
			const rowData = {};
			headers.forEach((header, index) => {
				rowData[header] = row[index]?.toString().trim() || "";
			});
			return rowData;
		}).filter((row) => Object.values(row).some((value) => value !== ""));
	};

	const checkForDuplicates = (processedRows, data, previewFundType) => {
		const normalize = (value) => value?.trim() || "";

		const existingRecords = new Map(
			data.map((d) => {
				const key = previewFundType === "PFLT"
					? `${normalize(d.obligor_name?.display_value)}-${normalize(d.security_name?.display_value)}-${normalize(d.loan_type?.display_value)}`
					: `${normalize(d.investment_name?.display_value)}-${normalize(d.issuer?.display_value)}`;
				return [key, d.id?.value];
			})
		);

		let hasDuplicates = false;
		const finalRows = processedRows.map((row) => {
			const recordKey = previewFundType === "PFLT"
				? `${normalize(row["Obligor Name"])}-${normalize(row["Security Name"])}-${normalize(row["Loan Type (Term / Delayed Draw / Revolver)"])}`
				: `${normalize(row["Investment Name"])}-${normalize(row["Issuer"])}`;

			if (existingRecords.has(recordKey)) {
				hasDuplicates = true;
				return { ...row, action: "overwrite", id: existingRecords.get(recordKey) };
			} else {
				return { ...row, action: "add" };
			}
		});

		return { finalRows, hasDuplicates };
	};

	const handleSave = async () => {
		if (addsecFiles.length === 0) {
			showToast("error", "Please upload a file before saving.");
			return;
		}

		try {
			const file = addsecFiles[0];
			const sheetData = await readExcelFile(file);

			if (!sheetData || sheetData.length < 2) {
				showToast("error", "Uploaded file is empty or has an incorrect format.");
				return;
			}

			const processedRows = processExcelData(sheetData, previewFundType);

			if (!processedRows.length) {
				showToast("error", "No valid records found.");
				return;
			}

			const { finalRows, hasDuplicates } = checkForDuplicates(processedRows, data, previewFundType);
			const finalData = {
				records: finalRows.map(row =>
					Object.fromEntries(
						Object.entries(row).map(([key, value]) => [key.replace(/_/g, " "), value])
					)
				)
			};

			const validationResponse = await validateAddSecurities(finalData, previewFundType);

			if (validationResponse?.data?.error_code === "ERR_400") {
				showToast("error", validationResponse?.data?.message);
				setValidationInfo(validationResponse?.data?.result);
				setValidationModal(true);
				return;
			}


			if (hasDuplicates) {
				showDuplicateModal(
					finalRows,
					previewFundType,
					async () => {
						await uploadFile(finalData);
					},
					() => showToast("error", "Upload canceled. Please remove duplicate records.")
				);
				return;
			}

			await uploadFile(finalData);
		} catch (error) {
			console.error("Error in handleSave:", error);
			showToast("error", "An error occurred while processing the file.");
		}
	};

	const uploadFile = async (finalData) => {
		try {
			const response = await uploadAddMoreSecFile(
				finalData,
				dataId,
				previewFundType,
				reportId
			);

			const message = response?.data?.message || "File uploaded successfully.";
			if (response?.data?.success) {
				showToast("success", message);
				setAddsecFiles([]);
				handleCancel();
				await handleBaseDataPreview();
			} else {
				showToast("error", message);
			}
		} catch (error) {
			console.error("Error in uploadFile:", error);
			showToast("error", "Failed to upload file.");
		}
	};

	const fileDownloadOptions = {
		PCOF: {
			href: PCOFAddSecSampleFile,
			name: 'PCOF Add Base Data.xlsx'
		},
		PFLT: {
			href: PFLTAddSecSampleFile,
			name: 'PFLT Add Base Data.xlsx'
		}
	};


	return (
		<>
			<Modal
				title={<ModalComponents.Title title='Add Securities Data' showDescription={true} description="Add more securities data which are not present in the extracted base data" />}
				open={isOpenFileUpload}
				onCancel={handleCancel}
				footer={null}
				width={700}
			>
				<DynamicFileUploadComponent
					uploadedFiles={addsecFiles}
					setUploadedFiles={setAddsecFiles}
					supportedFormats={['csv', 'xlsx']}
					fundType={previewFundType}
					fileDownloadOptions={fileDownloadOptions}
					showDownload={true}
				/>
				<div className={styles.buttonContainer}>
					<CustomButton isFilled={false} text="Cancel" onClick={handleCancel} />
					<CustomButton isFilled={true} text="Save" onClick={handleSave} />
				</div>
			</Modal>

			{validationModal &&
				<SrcFileValidationErrorModal isModalOpen = {validationModal} setIsModalOpen={setValidationModal} validationInfoData = {validationInfo} />
			}
		</>
	);
};
