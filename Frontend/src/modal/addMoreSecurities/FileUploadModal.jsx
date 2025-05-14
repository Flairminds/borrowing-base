import { Modal } from 'antd';
import React, { useEffect, useState } from 'react';
import * as XLSX from 'xlsx';
import PCOFAddSecSampleFile from '../../assets/template File/PCOF Add Base Data.xlsx';
import PFLTAddSecSampleFile from '../../assets/template File/PFLT Add Base Data.xlsx';
import { ColumnMappingModal } from '../../components/columnMappingModal/ColumnMappingModal';
import { ModalComponents } from '../../components/modalComponents';
import { DynamicFileUploadComponent } from '../../components/reusableComponents/dynamicFileUploadComponent/DynamicFileUploadComponent';
import { CustomButton } from '../../components/uiComponents/Button/CustomButton';
import { compareAddSecurities, uploadAddMoreSecFile, validateAddSecurities } from '../../services/dataIngestionApi';
import { fmtDateValue } from '../../utils/helperFunctions/formatDisplayData';
import { exportToExcel } from '../../utils/helperFunctions/jsonToExcel';
import { showToast } from '../../utils/helperFunctions/toastUtils';
import { SrcFileValidationErrorModal } from '../srcFIleValidationErrorModal/srcFileValidationErrorModal';
import styles from "./FileUploadModal.module.css";


export const FileUploadModal = ({ isOpenFileUpload, handleCancel, addsecFiles, setAddsecFiles, previewFundType, dataId, reportId, handleBaseDataPreview, data, columns }) => {
	const [validationInfo, setValidationInfo] = useState([]);
	const [showMappingModal, setShowMappingModal] = useState(false);
	const [validationModal, setValidationModal] = useState(false);
	const [isSaving, setIsSaving] = useState(false);
	const [excelColumns, setExcelColumns] = useState([]);
	const [systemColumns, setSystemColumns] = useState([]);
	const [showColumnsToExport, setShowColumnsToExport] = useState(false);
	const [selectedColumns, setSelectedColumns] = useState([]);
	const [updatedColumnsData, setUpdatedColumnsData] = useState(columns);

	useEffect(() => {
		if (!isOpenFileUpload) {
			setAddsecFiles([]);
		}
	}, [isOpenFileUpload]);

	const DEFAULT_EXPORT_COLUMNS = {
		PFLT: ["Obligor Name", "Security Name", "Loan Type"],
		PCOF: ["Investment Name", "Issuer"],
		PSSL: ["Borrower", "Loan Type"]
	};

	useEffect(() => {
		resetColumnSelection();
	}, [columns]);

	const resetColumnSelection = () => {
		if (columns && columns?.length > 0) {
			const temp = [...columns];
			setUpdatedColumnsData(temp.sort((a, b) => a.label < b.label ? -1 : 1));
			setSelectedColumns([...selectedColumns, ...DEFAULT_EXPORT_COLUMNS[previewFundType]]);
		}
	};

	const EXCEL_COLUMNS = {
		PFLT: ["obligor name", "security name", "loan type"],
		PCOF: ["investment name", "issuer"],
		PSSL: ["borrower", "loan type"]
	};

	const DATA_COLUMNS = {
		PFLT: ["obligor_name", "security_name", "loan_type"],
		PCOF: ["investment_name", "issuer"],
		PSSL: ["borrower", "loan_type"]
	};

	const PFLTItem = ({ data }) => (
		<li>
			<strong>Obligor:</strong> {data["Obligor Name"]},{" "}
			<strong>Security:</strong> {data["Security Name"]},{" "}
			<strong>Loan Type:</strong> {data["Loan Type (Term / Delayed Draw / Revolver)"]}
		</li>
	);

	const PCOFItem = ({ data }) => (
		<li>
			<strong>Investment Name:</strong> {data["Investment Name"]},{" "}
			<strong>Issuer:</strong> {data["Issuer"]}
		</li>
	);

	const PSSLItem = ({ data }) => (
		<li>
			<strong>Borrower:</strong> {data["Borrower"]},{" "}
			<strong>Loan Type:</strong> {data["Loan Type"]}
		</li>
	);




	const showDuplicateModal = (processedRows, previewFundType, onConfirm, onCancel) => {
		const isNewAdded = processedRows.some((d) => d.action === "add");

		Modal.confirm({
			title: <span style={{ lineHeight: "2rem" }}>{`${processedRows.length} records found in the sheet`}</span>,
			content: (
				<>
					<p><strong>{processedRows.filter((d) => d.action === "overwrite").length} existing records</strong></p>
					{/* <ul>
						{processedRows
							.filter((d) => d.action === "overwrite")
							.map((data, index) => {
								switch (previewFundType) {
								case "PFLT":
									return <PFLTItem key={index} data={data} />;
								case "PCOF":
									return <PCOFItem key={index} data={data} />;
								case "PSSL":
									return <PSSLItem key={index} data={data} />;
								default:
									return null;
								}
							})}
					</ul> */}
					{isNewAdded && <p><strong>{processedRows.filter((d) => d.action === "add").length} new records:</strong></p>}
					<ul>
						{processedRows
							.filter((d) => d.action === "add")
							.map((data, index) => {
								switch (previewFundType) {
								case "PFLT":
									return <PFLTItem key={index} data={data} />;
								case "PCOF":
									return <PCOFItem key={index} data={data} />;
								case "PSSL":
									return <PSSLItem key={index} data={data} />;
								default:
									return null;
								}
							})}
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
						row.map((cell) => (typeof cell === "object" && cell instanceof Date ? formatDate(cell) : (cell == '' ? null : cell)))
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
		const headers = sheetData?.[0]?.map((h) => {
			const lower = h?.toString()?.trim();
			return columnMap.find((col, i) => lower.includes(EXCEL_COLUMNS[previewFundType][i])) || lower;
		});
		let temp = sheetData?.slice(1)?.map((row) => {
			const rowData = {};
			headers.forEach((header, index) => {
				rowData[header] = row[index] != 0 ? (!row[index] ? null : isNaN(row[index]) ? row[index]?.toString().trim() || null : parseFloat(row[index])) : 0;
			});
			return rowData;
		}).filter((row) => Object.values(row).some((value) => value !== ""));
		temp = temp.filter(t => {
			for (const c of DEFAULT_EXPORT_COLUMNS[previewFundType]) {
				if (t[c]) return t;
			}
		});
		return temp;
	};

	const checkForDuplicates = (processedRows, data, previewFundType) => {
		const normalize = (value) => {
			if (value) {
				if (isNaN(value)) {
					return value?.trim();
				} else {
					return parseFloat(value);
				}
			} else {
				return null;
			}
		};

		const existingRecords = new Map(
			data.map((d) => {
				let key;
				switch (previewFundType) {
				case "PFLT":
					key = `${normalize(d.obligor_name?.display_value)}-${normalize(d.security_name?.display_value)}-${normalize(d.loan_type?.display_value)}`;
					break;
				case "PCOF":
					key = `${normalize(d.investment_name?.display_value)}-${normalize(d.issuer?.display_value)}`;
					break;
				case "PSSL":
					key = `${normalize(d.borrower?.display_value)}-${normalize(d.loan_type?.display_value)}`;
					break;
				}
				return [key, d.id?.value];
			})
		);

		let hasDuplicates = false;
		const finalRows = processedRows.map((row) => {
			let recordKey;
			switch (previewFundType) {
			case "PFLT":
				recordKey = `${normalize(row["Obligor Name"])}-${normalize(row["Security Name"])}-${normalize(row["Loan Type (Term / Delayed Draw / Revolver)"])}`;
				break;
			case "PCOF":
				recordKey = `${normalize(row["Investment Name"])}-${normalize(row["Issuer"])}`;
				break;
			case "PSSL":
				recordKey = `${normalize(row["Borrower"])}-${normalize(row["Loan Type"])}`;
				break;
			}

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
			setIsSaving(true);
			const file = addsecFiles[0];
			// const proceed = await fetchColumnComparisonAndSetState(file, previewFundType);
			// if (!proceed) return;
			const sheetData = await readExcelFile(file);

			if (!sheetData || sheetData.length < 2) {
				showToast("error", "Uploaded file is empty or has an incorrect format.");
				setIsSaving(false);
				return;
			}

			const processedRows = processExcelData(sheetData, previewFundType);
			if (!processedRows.length) {
				showToast("error", "No valid records found.");
				setIsSaving(false);
				return;
			}

			const { finalRows } = checkForDuplicates(processedRows, data, previewFundType);
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
				setIsSaving(false);
				return;
			}
			const hasNewAdditions = finalRows.some((d) => d.action === "add");
			const hasOverwrites = finalRows.some((d) => d.action === "overwrite");

			if (hasNewAdditions || hasOverwrites) {
				showDuplicateModal(
					finalRows,
					previewFundType,
					async () => {
						await uploadFile(finalData);
					},
					() => showToast("error", "Upload canceled. Please remove duplicate records.")
				);
				setIsSaving(false);
				return;
			}

			await uploadFile(finalData);
			setIsSaving(false);
		} catch (error) {
			console.error("Error in handleSave:", error);
			showToast("error", "An error occurred while processing the file.");
			setIsSaving(false);
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

	const getMappedExportData = (columns, rawData) => {
		return rawData.map(row => {
			const formattedRow = {};
			columns.forEach(col => {
				const rawValue = row[col.key];
				let value = "";
				// Prefer .value if present
				if (rawValue && typeof rawValue === "object" && "value" in rawValue) {
					value = rawValue.value;
				} else if (rawValue != null) {
					value = rawValue;
				}

				if (!isNaN(value)) {
					value = parseFloat(value);
				}
				formattedRow[col.label] = value;
			});
			return formattedRow;
		});
	};


	const handleExport = () => {
		const columnsToExport = columns.filter(c => selectedColumns.includes(c.label));
		const mappedData = getMappedExportData(columnsToExport, data);
		const percentColumns = [];
		columnsToExport.map(c => {
			if (c.unit == 'percent') {
				percentColumns.push(c.label);
			}
		});
		const dateColumns = [];
		columnsToExport.map(c => {
			if (c.unit == 'date') {
				dateColumns.push(c.label);
			}
		});
		exportToExcel(mappedData, columnsToExport, percentColumns, `${previewFundType} base data ${fmtDateValue(reportId)}.xlsx`);
		setShowColumnsToExport(false);
	};

	const fetchColumnComparisonAndSetState = async (file, fund_type) => {
		try {
			const response = await compareAddSecurities(file, fund_type);

			const { extra_columns_in_file, missing_columns_in_file } = response?.data?.result;

			setExcelColumns(extra_columns_in_file || []);
			setSystemColumns(missing_columns_in_file || []);

			if (missing_columns_in_file && missing_columns_in_file?.length > 0) {
				setShowMappingModal(true);
				return false;
			}

			return true;
		} catch (error) {
			console.error("Error in column comparison:", error);
			showToast("error", "An error occurred while comparing columns.");
			return false;
		}
	};

	const handleCheckboxClick = (e, val) => {
		if (val == 'Select All') {
			if (selectedColumns.length == updatedColumnsData.length) {
				setSelectedColumns([]);
			} else {
				setSelectedColumns(updatedColumnsData.map(item => item.label));
			}
			return;
		}
		const selectedColumnsArray = [...selectedColumns];
		const index = selectedColumnsArray.indexOf(val);
		if (index > -1) {
			setSelectedColumns(selectedColumns?.filter((col) => col != val));
		} else {
			setSelectedColumns([...selectedColumns, val]);
		}
	};

	const handleBackOfExport = () => {
		setShowColumnsToExport(false);
	};

	return (
		<>
			<Modal
				title={<ModalComponents.Title title='Bulk Update Securities Data' showDescription={true} description="Edit existing securities data or add more securities data which are not present in the extracted base data" />}
				open={isOpenFileUpload}
				onCancel={handleCancel}
				footer={null}
				width={700}
			>
				{!showColumnsToExport ?
					<div>
						<div style={{ display: "flex", justifyContent: "flex-end", marginBottom: "8px" }}>
							<a className="downloadLink" onClick={() => setShowColumnsToExport(true)}>
								Export extracted base data
							</a>
						</div>
						<DynamicFileUploadComponent
							uploadedFiles={addsecFiles}
							setUploadedFiles={setAddsecFiles}
							supportedFormats={['csv', 'xlsx']}
							fundType={previewFundType}
							showDownload={false}
						/>
						<div className={styles.buttonContainer}>
							<CustomButton isFilled={false} text="Cancel" onClick={handleCancel} />
							<CustomButton isFilled={true} loading={isSaving} btnDisabled={isSaving} loadingText='Saving...' text="Save" onClick={handleSave} />
						</div>
					</div>
					:
					<div>
						Select columns to export
						<div>
							<input className={styles.checkbox} type="checkbox" id={'Select All'} name={'Select All'} value={'Select All'} onClick={(e) => handleCheckboxClick(e, 'Select All')} checked={selectedColumns.length == updatedColumnsData.length} />
							<label htmlFor={'Select All'}>{'Select All'}</label>
						</div>
						<div style={{display: ' flex'}}>
							<div>
								{updatedColumnsData.slice(0, (updatedColumnsData.length / 2) + 1).map((col, i) => {
									return (
										<div key={i}>
											<input className={styles.checkbox} type="checkbox" id={col.key} name={col.key} value={col.key} onClick={(e) => handleCheckboxClick(e, col.label)} checked={selectedColumns.includes(col.label)} />
											<label htmlFor={col.key}>{col.label}</label>
										</div>
									);
								})}
							</div>
							<div>
								{updatedColumnsData.slice((updatedColumnsData.length / 2) + 1).map((col, i) => {
									return (
										<div key={i}>
											<input className={styles.checkbox} type="checkbox" id={col.key} name={col.key} value={col.key} onClick={(e) => handleCheckboxClick(e, col.label)} checked={selectedColumns.includes(col.label)} />
											<label htmlFor={col.key}>{col.label}</label>
										</div>
									);
								})}
							</div>
						</div>
						<div className={styles.buttonContainer}>
							<CustomButton isFilled={false} text="Back" onClick={handleBackOfExport} />
							<CustomButton isFilled={true} text="Export" onClick={handleExport} />
						</div>
					</div>}
			</Modal>

			<ColumnMappingModal
				visible={showMappingModal}
				onClose={() => setShowMappingModal(false)}
				excelUnmappedColumns={excelColumns}
				systemUnmappedColumns={systemColumns}
				handleSave ={handleSave}
				onSubmit={() => {
					setShowMappingModal(false);
				}}
			/>


			{validationModal &&
				<SrcFileValidationErrorModal isModalOpen={validationModal} setIsModalOpen={setValidationModal} validationInfoData={validationInfo} />
			}
		</>
	);
};
