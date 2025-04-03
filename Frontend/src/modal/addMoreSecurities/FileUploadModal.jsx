import { Modal, Popover } from 'antd';
import React, { useEffect } from 'react';
import { useDropzone } from 'react-dropzone';
import * as XLSX from 'xlsx';
import PCOFAddSecSampleFile from '../../assets/template File/PCOF Add Base Data.xlsx';
import PFLTAddSecSampleFile from '../../assets/template File/PFLT Add Base Data.xlsx';
import { ModalComponents } from '../../components/modalComponents';
import { CustomButton } from '../../components/uiComponents/Button/CustomButton';
import { uploadAddMoreSecFile } from '../../services/dataIngestionApi';
import { showToast } from '../../utils/helperFunctions/toastUtils';
import styles from "./FileUploadModal.module.css";


export const FileUploadModal = ({ isOpenFileUpload, handleCancel, addsecFiles, setAddsecFiles, previewFundType, dataId, reportId, handleBaseDataPreview, data }) => {
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
		Modal.confirm({
			title: "Records Found",
			content: (
				<div>
					<p><strong>Duplicate Records Found :</strong></p>
					<ul>
						{processedRows
							.filter((d) => d.action === "overwrite")
							.map((d, index) => (
								<li key={index}>
									{previewFundType === "PFLT" ? (
										<>
											<strong>Obligor:</strong> {d["obligor_name"]},{" "}
											<strong>Security:</strong> {d["security_name"]},{" "}
											<strong>Loan Type:</strong> {d["loan_type"]}
										</>
									) : (
										<>
											<strong>Investment Name:</strong> {d["investment_name"]},{" "}
											<strong>Issuer:</strong> {d["issuer"]}
										</>
									)}
								</li>
							))}
					</ul>
					<p><strong>New Records Found :</strong></p>
					<ul>
						{processedRows
							.filter((d) => d.action === "add")
							.map((d, index) => (
								<li key={index}>
									{previewFundType === "PFLT" ? (
										<>
											<strong>Obligor:</strong> {d["obligor_name"]},{" "}
											<strong>Security:</strong> {d["security_name"]},{" "}
											<strong>Loan Type:</strong> {d["loan_type"]}
										</>
									) : (
										<>
											<strong>Investment Name:</strong> {d["investment_name"]},{" "}
											<strong>Issuer:</strong> {d["issuer"]}
										</>
									)}
								</li>
							))}
					</ul>
				</div>
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
					const workbook = XLSX.read(binaryStr, { type: "binary" });
					const sheetName = workbook.SheetNames[0];
					const sheetData = XLSX.utils.sheet_to_json(workbook.Sheets[sheetName], { header: 1 });
					resolve(sheetData);
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
			const lower = h?.toString().toLowerCase().trim();
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
		const normalize = (value) => value?.toLowerCase().trim() || "";
		const existingRecords = new Set(data.map((d) => {
			return previewFundType === "PFLT"
				? `${normalize(d.obligor_name?.display_value)}-${normalize(d.security_name?.display_value)}-${normalize(d.loan_type?.display_value)}`
				: `${normalize(d.investment_name?.display_value)}-${normalize(d.issuer?.display_value)}`;
		}));

		let hasDuplicates = false;
		const finalRows = processedRows.map((row) => {
			const recordKey = previewFundType === "PFLT"
				? `${normalize(row["obligor_name"])}-${normalize(row["security_name"])}-${normalize(row["loan_type"])}`
				: `${normalize(row["investment_name"])}-${normalize(row["issuer"])}`;

			if (existingRecords.has(recordKey)) {
				hasDuplicates = true;
				return { ...row, action: "overwrite" };
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
			const finalData = { records: finalRows };
			console.log("FinalData :- ", finalData);

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
			showToast("success", "File uploaded successfully!");
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
