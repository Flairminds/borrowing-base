import { MinusCircleOutlined, PlusOutlined } from "@ant-design/icons";
import { Form, Input, DatePicker, Button, Radio, Tabs, Col, Row } from "antd";
import Modal from "antd/es/modal/Modal";
import dayjs from "dayjs";
import React, { useEffect, useState } from "react";
import { useDropzone } from "react-dropzone";
import * as XLSX from "xlsx";
import PCOF_OTHER_INFO_SAMPLE from '../../assets/template File/PCOF - Other Info.xlsx';
import PFLT_OTHER_INFO_SAMPLE from '../../assets/template File/PFLT - Other Info.xlsx';
import { generateBaseDataFile, getDateReport } from "../../services/api";
import { submitOtherInfo } from "../../services/dataIngestionApi";
import { PFLTData, PCOFData, OTHER_INFO_OPTIONS, PFLT_COLUMNS_NAME, PCOF_COLUMNS_NAME } from "../../utils/constants/constants";
import { fmtDateValue, fmtDisplayVal, formatColumnName } from "../../utils/helperFunctions/formatDisplayData";
import { showToast } from "../../utils/helperFunctions/toastUtils";
import styles from "./AddAdditionalInformationModal.module.css";
import { useNavigate } from 'react-router';
import { UIComponents } from "../../components/uiComponents";
import { ModalComponents } from "../../components/modalComponents";
import { SrcFileValidationErrorModal } from "../srcFIleValidationErrorModal/srcFileValidationErrorModal";

const { TabPane } = Tabs;

export const AddAdditionalInformationModal = (
	{
		isAddFieldModalOpen,
		setIsAddFieldModalOpen,
		onClose,
		dataId,
		data = {},
		setTriggerBBCalculation,
		previewFundType,
		selectedFiles,
		setSelectedFiles,
		baseFilePreviewData,
		previewPageId,
		getborrowingbasedata,
		setLoading
	}
) => {
	const [form] = Form.useForm();
	const [initialFormData, setInitialFormData] = useState(null);
	const [addType, setAddType] = useState("add");
	const [uploadedData, setUploadedData] = useState({});
	const [validationModalOpen, setValidationModalOpen] = useState(false);
	const [validationInfoList, setValidationInfoList] = useState([]);
	const navigate = useNavigate();

	const selectedData = previewFundType === "PCOF" ? PCOFData : PFLTData;

	useEffect(() => {
		const formData = {};
		if (previewFundType === "PCOF") {
			formData["borrower"] = uploadedData["borrower"] || data?.other_data?.["borrower"] || null;
			formData["determination_date"] = uploadedData.determination_date ? dayjs(uploadedData.determination_date) : dayjs(data?.other_data?.determination_date) || null;
			formData["revolving_closing_date"] = uploadedData.revolving_closing_date ? dayjs(uploadedData.revolving_closing_date) : dayjs(data?.other_data?.revolving_closing_date) || null;
			formData["commitment_period_(3_years_from_final_closing_date,_as_defined_in_lpa)"] = uploadedData["commitment_period_(3_years_from_final_closing_date,_as_defined_in_lpa)"] || data?.other_data?.["commitment_period_(3_years_from_final_closing_date,_as_defined_in_lpa)"] || null;
			formData["(b)_facility_size"] = uploadedData["(b)_facility_size"] || data?.other_data?.["(b)_facility_size"] || null;
			formData["loans_(cad)"] = uploadedData["loans_(cad)"] ? uploadedData["loans_(cad)"] : data?.other_data?.["loans_(cad)"] || null;
			formData["loans_(usd)"] = uploadedData["loans_(usd)"] || data?.other_data?.["loans_(usd)"] || null;

			formData["principle_obligations"] = uploadedData["principle_obligations"]?.length > 0 ? uploadedData["principle_obligations"]
				: data?.other_data?.["principle_obligations"]?.length > 0 ? data.other_data["principle_obligations"] : null;

			formData["advance_rates"] = uploadedData["advance_rates"]?.length > 0 ? uploadedData["advance_rates"]
				: data?.other_data?.["advance_rates"]?.length > 0 ? data.other_data["advance_rates"].map(item => ({
					...item,
					advance_rate: item.advance_rate ? `${(item.advance_rate * 100)}` : null
				})) : null;

			formData["subscription_bb"] = uploadedData["subscription_bb"]?.length > 0 ? uploadedData["subscription_bb"]
				: data?.other_data?.["subscription_bb"]?.length > 0 ? data.other_data["subscription_bb"] : null;

			formData["pricing"] = uploadedData["pricing"]?.length > 0 ? uploadedData["pricing"]
				: data?.other_data?.["pricing"]?.length > 0 ? data.other_data["pricing"].map(item => ({
					...item,
					percent: item.percent ? `${(item.percent * 100)}` : null
				})) : null;

			formData["portfolio_leverageborrowingbase"] = uploadedData["portfolio_leverageborrowingbase"]?.length > 0 ? uploadedData["portfolio_leverageborrowingbase"]
				: data?.other_data?.["portfolio_leverageborrowingbase"]?.length > 0 ? data.other_data["portfolio_leverageborrowingbase"].map(item => ({
					...item,
					unquoted: item.unquoted ? `${(item.unquoted * 100)}` : null,
					quoted: item.quoted ? `${(item.quoted * 100)}` : null
				})) : null;

			formData["concentration_limits"] = uploadedData["concentration_limits"]?.length > 0 ? uploadedData["concentration_limits"]
				: data?.other_data?.["concentration_limits"]?.length > 0 ? data.other_data["concentration_limits"].map(item => ({
					...item,
					concentration_limit: item.concentration_limit ? `${(item.concentration_limit * 100)}` : null
				})) : null;

			formData["first_lien_leverage_cut-off_point"] = uploadedData["first_lien_leverage_cut-off_point"] || data?.other_data?.["first_lien_leverage_cut-off_point"] || null;
			formData["warehouse_first_lien_leverage_cut-off"] = uploadedData["warehouse_first_lien_leverage_cut-off"] || data?.other_data?.["warehouse_first_lien_leverage_cut-off"] || null;
			formData["last_out_attachment_point"] = uploadedData["last_out_attachment_point"] || data?.other_data?.["last_out_attachment_point"] || null;
			formData["trailing_12-month_ebitda"] = uploadedData["trailing_12-month_ebitda"] || data?.other_data?.["trailing_12-month_ebitda"] || null;
			formData["trailing_24-month_ebitda"] = uploadedData["trailing_24-month_ebitda"] || data?.other_data?.["trailing_24-month_ebitda"] || null;
			formData["total_leverage"] = uploadedData["total_leverage"] || data?.other_data?.["total_leverage"] || null;
			formData["ltv"] = uploadedData["ltv"] || data?.other_data?.["ltv"] || null;
			formData["concentration_test_threshold_1"] = uploadedData["concentration_test_threshold_1"] || data?.other_data?.["concentration_test_threshold_1"] || null;
			formData["concentration_test_threshold_2"] = uploadedData["concentration_test_threshold_2"] || data?.other_data?.["concentration_test_threshold_2"] || null;
			formData["threshold_1_advance_rate"] = uploadedData["threshold_1_advance_rate"] || data?.other_data?.["threshold_1_advance_rate"] || null;
			formData["threshold_2_advance_rate"] = uploadedData["threshold_2_advance_rate"] || data?.other_data?.["threshold_2_advance_rate"] || null;

		} else if (previewFundType === "PFLT") {
			formData["minimum_equity_amount_floor"] = uploadedData?.minimum_equity_amount_floor ? uploadedData.minimum_equity_amount_floor : data?.other_data?.input?.minimum_equity_amount_floor ? data.other_data.input.minimum_equity_amount_floor : null;
			formData["determination_date"] = uploadedData?.determination_date ? dayjs(uploadedData.determination_date) : data?.determination_date ? dayjs(data.determination_date) : null;
			formData["other_sheet"] = uploadedData?.other_sheet?.length > 0 ? uploadedData.other_sheet : data?.other_data?.other_sheet?.length > 0 ? data.other_data.other_sheet : null;
		}
		setInitialFormData(formData);
	}, [data, uploadedData]);

	const handleCancel = () => {
		form.resetFields();
		setIsAddFieldModalOpen(false);
		setSelectedFiles([]);
		setAddType("add");
	};

	const generateBaseData = async () => {
		// e.preventDefault();
		setTriggerBBCalculation(true);
		try {
			let run = false;
			if (baseFilePreviewData?.cardData['Unmapped Securities'] > 0) {
				if (confirm('The calculation will be inaccurate due to some unmapped securities. Do you want to proceed?')) {
					run = true;
				}
			} else {
				run = true;
			}
			if (run) {
				const response = await generateBaseDataFile({ 'bdi_id': previewPageId });
				const detail = response?.data;
				if (response.status === 200) {
					setLoading(true);
					showToast('success', detail?.message);
					const baseFileId = response.data.result.base_data_file_id;
					await getborrowingbasedata(baseFileId);
					navigate('/');
				}
			}
			setTriggerBBCalculation(false);
			return;
		} catch (error) {
			setTriggerBBCalculation(false);
			showToast('error', error.message);
		}
	};

	const handleSubmit = async (isTriggerCalled) => {
		const extractionInfoId = dataId;
		let values = form.getFieldsValue();
		try {
			let otherData = {};
			if (previewFundType === "PCOF") {
				values = {
					...values,
					"availability_borrower": {
						"borrower": values.borrower,
						"commitment_period_(3_years_from_final_closing_date,_as_defined_in_lpa)": values["commitment_period_(3_years_from_final_closing_date,_as_defined_in_lpa)"],
						"(b)_facility_size": values["(b)_facility_size"],
						"revolving_closing_date": dayjs(values?.revolving_closing_date?.format("YYYY-MM-DD")),
						"determination_date": dayjs(values?.determination_date),
						"loans_(cad)": values?.["loans_(cad)"],
						"loans_(usd)": values?.["loans_(usd)"]
					},
					"other_metrics": {
						"first_lien_leverage_cut-off_point": values["first_lien_leverage_cut-off_point"],
						"last_out_attachment_point": values["last_out_attachment_point"],
						"ltv": parseFloat((parseFloat(values["ltv"].replace("%", "")) / 100)),
						"threshold_1_advance_rate": parseFloat((parseFloat(values["threshold_1_advance_rate"].replace("%", "")) / 100)),
						"threshold_2_advance_rate": parseFloat((parseFloat(values["threshold_2_advance_rate"].replace("%", "")) / 100)),
						"concentration_test_threshold_1": parseFloat((parseFloat(values["concentration_test_threshold_1"].replace("%", "")) / 100)),
						"concentration_test_threshold_2": parseFloat((parseFloat(values["concentration_test_threshold_2"].replace("%", "")) / 100)),
						"total_leverage": values["total_leverage"],
						"trailing_12-month_ebitda": values["trailing_12-month_ebitda"],
						"trailing_24-month_ebitda": values["trailing_24-month_ebitda"],
						"warehouse_first_lien_leverage_cut-off": values["warehouse_first_lien_leverage_cut-off"]
					}
				};
				Object.keys(values).forEach((key) => {
					if (PCOFData[key]) {
						(PCOFData[key].Column || PCOFData[key].Header)?.forEach((item) => {
							if (item?.unit === "percent") {
								if (Array.isArray(values[key])) {
									values[key].forEach((ele) => {
										Object.keys(ele).forEach((element) => {
											if (element === item.name) {
												if (ele[element] !== "n/a" && `${ele[element]}`.includes("%")) {
													ele[element] = parseFloat(
														(parseFloat(ele[element].replace("%", "")) / 100)
													);
												} else {
													ele[element] = parseFloat(
														(parseFloat(ele[element]) / 100)
													);
												}
											}
										});
									});
								}
							}
						});
					}
				});

				otherData = {
					...values,
					"column_info": PCOF_COLUMNS_NAME
				};
			} else if (previewFundType === "PFLT") {
				values = {
					...values,
					"other_sheet": values["other_sheet"],
					"input": {
						"minimum_equity_amount_floor": `${values["minimum_equity_amount_floor"]}`,
						"determination_date": values.determination_date
					}
				};
				Object.keys(values).forEach((key) => {
					if (PFLTData[key]) {
						(PFLTData[key].Column || PFLTData[key].Header)?.forEach((item) => {
							if (item?.unit === "percent") {
								if (Array.isArray(values[key])) {
									values[key].forEach((ele) => {
										Object.keys(ele).forEach((element) => {
											if (element === item.name) {
												if (ele[element] !== "n/a" && `${ele[element]}`.includes("%")) {
													ele[element] = parseFloat(
														(parseFloat(ele[element].replace("%", "")) / 100)
													);
												}
											}
										});
									});
								}
							}
						});
					}
				});
				otherData = {
					...values,
					"column_info": PFLT_COLUMNS_NAME
				};
			}
			const transformedData = {
				"extraction_info_id": extractionInfoId,
				"determination_date": values.determination_date || dayjs(values.determination_date.format("YYYY-MM-DD")),
				"other_data": otherData,
				"fund_type": previewFundType
			};
			const response = await submitOtherInfo(transformedData);
			if (response.error_code == "ERR_400") {
				showToast('error', response.message);
				setValidationInfoList(response?.result);
				setIsAddFieldModalOpen(false);
				setValidationModalOpen(true);
			} else if (response?.message) {
				showToast("success", response?.message);
				form.resetFields();
				onClose();
			}
			if (isTriggerCalled && response?.["success"]) {
				generateBaseData();
			}

		} catch (error) {
			const errorMessage = error.response?.message || "Error: Failed to submit form data";
			console.error(error);
			showToast("error", errorMessage);
		}
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

	const handleChange = (e) => {
		setAddType(e.target.value);
	};

	const mapDataToPrincipalObligations = (data) => {
		const header = data[0];
		const temp = [];
		data.slice(1)?.forEach((row) => {
			if (row.length > 0) {
				const record = {};
				row.forEach((value, index) => {
					record[header[index].toLowerCase().replace(/ /g, "_")] = value;
				});
				temp.push(record);
			}
		});
		return temp;
	};

	const handleExtract = () => {
		if (selectedData.length === 0) {
			showToast("error", "No data found to extract");
			return;
		}

		const file = selectedFiles[0];
		const reader = new FileReader();
		reader.onload = (e) => {
			const data = new Uint8Array(e.target.result);
			const workbook = XLSX.read(data, { type: "array", cellDates: true, cellText: true });
			const sheetsData = workbook.SheetNames.map((sheetName) => {
				const sheet = workbook.Sheets[sheetName];
				const rawData = XLSX.utils.sheet_to_json(sheet, { header: 1, raw: true });

				const isPercentageCell = (row, cell) => {
					const columnIndex = row.indexOf(cell);
					let isPercentageColumn = false;
					if (columnIndex === 2) {
						isPercentageColumn = true;
					} else {
						const header = rawData[0][columnIndex];
						if (header && (header.toLowerCase().includes("percentage") ||
							header.toLowerCase().includes("percent") ||
							header.toLowerCase().includes("unquoted") ||
							header.toLowerCase().includes("advance rate")
						)) {
							isPercentageColumn = true;
						}
					}

					if (isPercentageColumn) {
						if (typeof cell === 'number' && cell === 0) {
							return false;
						}
						return true;
					}

					return false;
				};

				const formattedData = rawData.map((row) =>
					row.map((cell, index) => {
						if (cell instanceof Date) {
							return dayjs(cell).format("YYYY-MM-DD");
						}
						if (typeof cell === "string" && cell.includes("%")) {
							return cell;
						}
						if (typeof cell === "number" && cell >= 0 && cell <= 1 && isPercentageCell(row, cell)) {
							return `${(cell * 100)}`;
						}
						if (index !== 0 &&
							typeof row[0] === 'string' &&
							(row[0].toLowerCase().includes('threshold') || row[0].toLowerCase().includes('ltv')) &&
							typeof row[1] === 'number'
						) {
							return `${(cell * 100)}`;
						}

						return cell;
					})
				);
				return { sheetName, data: formattedData };
			});

			let uploadedDataValues = {};
			sheetsData.forEach((sheet) => {
				if (
					sheet.sheetName.toLocaleLowerCase() === "availability borrower" ||
					sheet.sheetName.toLocaleLowerCase() === "other metrics" ||
					sheet.sheetName.toLocaleLowerCase() === "input"
				) {
					const data = Object.fromEntries(sheet?.data?.slice(1).filter(row => row.length === 2));
					const transformedData = Object.fromEntries(
						Object.entries(data).map(([key, value]) => {
							const transformedKey = key.toLowerCase().replace(/\s+/g, '_');
							return [transformedKey, value];
						})
					);
					uploadedDataValues = { ...uploadedDataValues, ...transformedData };
				} else {
					uploadedDataValues[sheet.sheetName.toLowerCase().replace(/\s+/g, '_')] = mapDataToPrincipalObligations(sheet.data);
				}
			});
			setUploadedData((prevState) => ({ ...prevState, ...uploadedDataValues }));
			setSelectedFiles([]);
			setAddType("add");
		};
		reader.readAsArrayBuffer(file);
	};

	const exportSample = () => {
		const wb = XLSX.utils.book_new();

		const processData = (obj, sheetName) => {
			const rows = [];
			const columnSequence = data?.other_data?.column_info[sheetName]?.columns_info;

			const columnDetails = previewFundType === "PCOF" ? PCOFData[sheetName]?.Column || PCOFData[sheetName]?.Header :
				previewFundType === "PFLT" ? PFLTData[sheetName]?.Column || PFLTData[sheetName]?.Header : null;

			if (columnSequence && columnDetails) {
				const headerRow = columnSequence.map((col) => {
					const columnDetail = columnDetails.find((detail) => detail.name === col.col_name);
					return columnDetail ? columnDetail.label : col.display_name;
				});
				rows.push(headerRow);
			}

			if (sheetName === "input" || sheetName === "availability_borrower" || sheetName === "other_metrics") {
				for (const key in obj) {
					let formattedValue = fmtDateValue(obj[key]);
					if ((key.includes("threshold") || key.includes("ltv")) && key !== "") {
						formattedValue = `${formattedValue * 100}%`;
					}
					rows.push([formatColumnName(key), formattedValue]);
				}
			} else {
				obj.forEach((item) => {
					const row = columnSequence.map((col) => {
						const columnDetail = columnDetails.find((detail) => detail.name === col.col_name);
						const value = item[col.col_name] || "";

						if (columnDetail?.unit === "percent" && value !== "") {
							return `${value * 100}%`;
						}

						return value;
					});
					rows.push(row);
				});
			}

			const sheet = XLSX.utils.aoa_to_sheet(rows);
			const sheetNameForObject = formatColumnName(sheetName);
			XLSX.utils.book_append_sheet(wb, sheet, sheetNameForObject);
		};
		Object.entries(data.other_data || {}).forEach(([key]) => {
			if (Array.isArray(data.other_data[key]) || (typeof data.other_data[key] === "object" && data.other_data[key] !== null)) {
				if (key !== "column_info") processData(data.other_data[key], key);
			}
		});

		const xlsxArray = XLSX.write(wb, { bookType: "xlsx", type: "array" });
		const xlsxBlob = new Blob([xlsxArray], { type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" });
		saveAs(xlsxBlob, `${previewFundType} - Other Info - ${fmtDisplayVal(baseFilePreviewData.reportDate)}.xlsx`);
	};

	return (
		<>
			<Modal
				title={<ModalComponents.Title title='Additional Information' showDescription={true} description="Add more informations about the base data for borrowing base calculation" />}
				open={isAddFieldModalOpen} onCancel={handleCancel} footer={null} width={"90%"} style={{ top: 10 }}>
				<div style={{ display: "flex", justifyContent: "space-between", margin: "1rem 0" }}>
					<Radio.Group options={OTHER_INFO_OPTIONS} value={addType} onChange={handleChange} />
					{addType === "upload" && (
						<>
							{(typeof data === 'object' && data !== null && Object.keys(data).length > 0)
								? <a onClick={exportSample} style={{ paddingRight: "1rem", color: "blue", textDecoration: "underline" }}>Download file template</a>
								: <a href={previewFundType === "PCOF" ? PCOF_OTHER_INFO_SAMPLE : PFLT_OTHER_INFO_SAMPLE} style={{ paddingRight: "1rem" }}>Export file template</a>
							}
						</>
					)}
				</div>
				<Form
					form={form}
					layout="vertical"
					onFinish={handleSubmit}
					autoComplete="off"
					initialValues={initialFormData}
				// initialValues={initalFormData || selectedData == "PCOF" ? pcofEmptyFormStructure : pfltEmptyFormStructure}
				>
					{useEffect(() => {
						form.setFieldsValue(initialFormData);
					}, [initialFormData, form, uploadedData])}

					{addType === "add" && (
						<Tabs defaultActiveKey="1">
							{Object.keys(selectedData)?.map((sheet, index) => {
								const formattedSheetName = sheet.replace(/_/g, ' ').replace(/\b\w/g, char => char.toUpperCase());

								return (
									<TabPane tab={formattedSheetName} key={index + 1} forceRender>
										<>
											{selectedData[sheet]?.Header?.map((header, ind) => (
												<Form.Item
													key={ind}
													label={header.label + (header.unit && header.unit == 'percent' ? ' (%)' : '')}
													name={header.name}
													rules={[{ required: true, message: `Please enter ${header.label.toLowerCase()}!` }]}
													style={{ display: "inline-block", width: "25%", margin: "0 1rem 1rem 1rem" }}
												>
													{header.type === "datePicker" ? (
														<DatePicker style={{ width: "100%" }} />
													) : (
														<Input placeholder={`Enter ${header.label}`} />
													)}
												</Form.Item>
											))}

											{selectedData[sheet]?.Column?.length > 0 && (
												<Form.List name={sheet}>
													{(fields, { add, remove }) => (
														<>
															<div className={styles.rowHeader}
																style={{
																	display: "grid",
																	gridTemplateColumns: `repeat(${selectedData[sheet]?.Column?.length}, 1fr)`, // Dynamic grid
																	gap: "10px",
																	padding: "10px"
																}}>
																{selectedData[sheet]?.Column?.map((inputField, index) => (
																	<div key={index} className={styles.column}>
																		{inputField.label}
																	</div>
																))}
															</div>

															<div className={styles.rowContainer}>
																{fields?.map((field, index) => (
																	<div key={index} className={styles.row}
																		style={{
																			display: "grid",
																			gridTemplateColumns: `repeat(${selectedData[sheet]?.Column.length}, 1fr)`, // Dynamic grid
																			gap: "10px",
																			padding: "10px"
																		}}
																	>
																		{selectedData[sheet]?.Column?.map((inputField, index) => (
																			<Form.Item
																				key={index}
																				name={[field.name, inputField.name]}
																				noStyle
																			>
																				{inputField.type === "datePicker" ? (
																					<DatePicker
																						placeholder={inputField.label}
																						style={{
																							width: "100%",
																							padding: "4px",
																							borderRadius: "8px",
																							border: "1px solid rgba(201, 196, 196, 0.6)"
																						}}
																					/>
																				) : (
																					<Input
																						placeholder={inputField.label}
																						style={{
																							width: "100%",
																							padding: "4px",
																							borderRadius: "8px",
																							border: "1px solid rgba(201, 196, 196, 0.6)"
																						}}
																					/>
																				)}
																			</Form.Item>
																		))}
																	</div>
																))}
															</div>

															<Form.Item>
																<Button style={{ marginBottom: "1rem" }} type="dashed" onClick={() => add()} block icon={<PlusOutlined />}>
																	Add Details
																</Button>
															</Form.Item>
														</>
													)}
												</Form.List>
											)}

											<div className={styles.buttonContainer}>
												<UIComponents.Button isFilled={true} text="Save" onClick={() => handleSubmit(false)} />
												<UIComponents.Button isFilled={true} onClick={() => handleSubmit(true)} text={'Save & Trigger'} />
												<UIComponents.Button isFilled={false} text="Cancel" onClick={handleCancel} />
											</div>
										</>
									</TabPane>
								);
							})}
						</Tabs>
					)}

					{addType === "upload" && (
						<>
							<Form.Item>
								<div className={styles.visible}>
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
							</Form.Item>

							<div className={styles.buttonContainer}>
								<UIComponents.Button isFilled={true} text="Extract" onClick={handleExtract} />
								<UIComponents.Button isFilled={false} text="Cancel" onClick={handleCancel} />
							</div>
						</>
					)}
				</Form>
			</Modal>
			{validationModalOpen &&
				<SrcFileValidationErrorModal isModalOpen = {validationModalOpen} setIsModalOpen={setValidationModalOpen} validationInfoData = {validationInfoList} />
			}
		</>
	);
};
