import { MinusCircleOutlined, PlusOutlined } from "@ant-design/icons";
import { Form, Input, DatePicker, Button, Radio, Tabs, Col, Row } from "antd";
import Modal from "antd/es/modal/Modal";
import dayjs from "dayjs";
import React, { useEffect, useState } from "react";
import { useDropzone } from "react-dropzone";
import * as XLSX from "xlsx";
import { CustomButton } from "../../components/custombutton/CustomButton";
import { submitOtherInfo } from "../../services/dataIngestionApi";
import { PFLTData, PCOFData, OTHER_INFO_OPTIONS } from "../../utils/constants/constants";
import { showToast } from "../../utils/helperFunctions/toastUtils";
import styles from "./AddAdditionalInformationModal.module.css";

const { TabPane } = Tabs;

export const AddAdditionalInformationModal = (
	{
		isAddFieldModalOpen,
		setIsAddFieldModalOpen,
		onClose,
		dataId,
		data = {},
		handleBaseDataPreview,
		previewFundType,
		selectedFiles,
		setSelectedFiles
	}
) => {
	const [form] = Form.useForm();
	const [initalFormData, setInitalFormData] = useState(null);
	const [addType, setAddType] = useState("add");
	const [uploadedData, setUploadedData] = useState({
		"inputData": {},
		"otherInfoData": []
	});

	const pfltEmptyFormStructure = {
		"determination_date": "",
		"minimum_equity_amount_floor": "",
		"other_data": [{}]
	};

	const pcofEmptyFormStructure = {
		"determination_date": "",
		"revolving_closing_date": "",
		"other_data": [{}]
	};

	useEffect(() => {
		const otherDataArray = Array.isArray(data.other_data) ? data.other_data : [];
		const uploadedOtherDataArray = Array.isArray(uploadedData?.otherInfoData) ? uploadedData.otherInfoData : [];

		const formData = {
			...data,
			"determination_date": uploadedData?.inputData?.determination_date ? dayjs(uploadedData.inputData.determination_date) : (data.determination_date ? dayjs(data.determination_date) : null),
			"other_data": [...otherDataArray, ...uploadedOtherDataArray]
		};
		
		if (previewFundType === "PCOF") {
			formData["revolving_closing_date"] = dayjs(uploadedData.inputData.revolving_closing_date) || dayjs(data.revolving_closing_date) || null;
			formData["commitment_period"] = uploadedData.inputData.commitment_period || data.commitment_period || null;
			formData["facility_size"] = uploadedData.inputData.facility_size || data.facility_size || null;
			formData["loans_cad"] = uploadedData.inputData["loans(cad)"] || data["loans_cad"] || null;
			formData["loans_usd"] = uploadedData.inputData["loans(usd)"] || data["loans_usd"] || null;
		} else {
			formData["minimum_equity_amount_floor"] = uploadedData?.inputData?.minimum_equity_amount_floor || data.minimum_equity_amount_floor;
		}
		setInitalFormData(formData);
	}, [data, uploadedData?.otherInfoData.length]);


	const handleCancel = () => {
		form.resetFields();
		setIsAddFieldModalOpen(false);
		setSelectedFiles([]);
		setAddType("add");
	};

	const handleSubmit = async (values) => {
		const extractionInfoId = dataId;

		try {
			// let otherInfoData = [];
			// if (values.financialDetails) {
			// 	otherInfoData = values.financialDetails.map((item) => {
			// 		return ({
			// 			currency: item.currency,
			// 			"exchange_rates": item.exchangeRate,
			// 			"cash_current_and_preborrowing": item.CashCurrentAndPreborrowing,
			// 			borrowing: item.borrowing,
			// 			"additional_expenses_1": item.additionalExpenses1,
			// 			"additional_expenses_2": item.additionalExpenses2,
			// 			"additional_expenses_3": item.additionalExpenses3,
			// 			"current_credit_facility_balance": item.currentCreditFacilityBalance
			// 		});
			// 	});
			// }
			const transformedData = {
				"extraction_info_id": extractionInfoId,
				"determination_date": values.determination_date.format("YYYY-MM-DD"),
				"minimum_equity_amount_floor": values.minimum_equity_amount_floor,
				"other_data": values.other_data,
				"fund_type": previewFundType
			};

			if (previewFundType == "PCOF") {
				const updatedlist = values.other_data.map((el => {
					return {
						...el
						// "dollar_equivalent": el.amount * el.spot_rate,
					};
				}));
 
				transformedData["other_data"] = updatedlist;
				transformedData["revolving_closing_date"] = values.revolving_closing_date.format("YYYY-MM-DD");
				transformedData["commitment_period"] = values.commitment_period;
				transformedData["facility_size"] = values.facility_size;
				transformedData["loans_usd"] = values.loans_usd;
				transformedData["loans_cad"] = values.loans_cad;
			}

			const response = await submitOtherInfo(transformedData);
			await handleBaseDataPreview();
			if (response.message) {
				showToast("success", response.message);
				form.resetFields();
				onClose();
			}
		} catch (error) {
			const errorMessage = error.response?.message || "Error: Failed to submit form data";
			console.error(error);
			showToast("error", errorMessage);
		}
	};

	const selectedData = previewFundType === "PCOF" ? PCOFData : PFLTData;

	const intialFormData = selectedData == "PCOF" ? pcofEmptyFormStructure : pfltEmptyFormStructure;

	const { getRootProps, getInputProps } = useDropzone({
		accept: {
			'text/csv': [],
			'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': [],
		},
		multiple: false,
		onDrop: (acceptedFiles) => {
			setSelectedFiles(acceptedFiles);
		}
	});

	const handleChange = (e) => {
		setAddType(e.target.value);
	};

	const handleExtract = () => {
		if (selectedData.length < 0) {
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

				const formattedData = rawData.map(row =>
					row.map(cell =>
						cell instanceof Date ? dayjs(cell).format("YYYY-MM-DD") : cell // Format dates, keep other values
					)
				);

				return { sheetName, data: formattedData };
			});

			let inputSheetData;
			let otherSheetData;
			sheetsData.map((sheet) => {
				if (sheet.sheetName.toLocaleLowerCase() === "input") {
					const data = Object.fromEntries(sheet?.data?.slice(1).filter(row => row.length === 2));
					inputSheetData = Object.fromEntries(
						Object.entries(data).map(([key, value]) => [key.toLowerCase().replace(/\s+/g, '_'), value])
					);
				}
				if (sheet.sheetName.toLocaleLowerCase().replace(" ", "_") === "other_sheet") {
					otherSheetData = sheet.data;
				}
			});

			const headers = otherSheetData[0];
			const uploadedOtherInfo = otherSheetData.slice(1)
				.filter(row => row.some(cell => cell != null && cell !== ""))
				.map(row => Object.fromEntries(headers.map((key, index) => [key.toLowerCase().replace(/\s+/g, "_"), row[index] ?? null])));

			setUploadedData({
				"inputData": inputSheetData,
				"otherInfoData": uploadedOtherInfo
			});
			setSelectedFiles([]);
			setAddType("add");
		};
		reader.readAsArrayBuffer(file);
	};

	return (
		<Modal open={isAddFieldModalOpen} onCancel={handleCancel} footer={null} width={"90%"}>
			<Form
				form={form}
				layout="vertical"
				onFinish={handleSubmit}
				autoComplete="off"
				initialValues={initalFormData || intialFormData}
				// initialValues={initalFormData || selectedData == "PCOF" ? pcofEmptyFormStructure : pfltEmptyFormStructure}
			>
				{useEffect(() => {
					form.setFieldsValue(initalFormData);
				}, [initalFormData])}
				<div style={{margin: "1rem 0"}}>
					<Radio.Group options={OTHER_INFO_OPTIONS} value={addType} onChange={handleChange} />
				</div>

				{addType === "add" &&
					<Form>
						<Tabs defaultActiveKey="1">
							{Object.keys(selectedData).map((sheet, index) => {
								const formattedSheetName = sheet.replace(/_/g, ' ').replace(/\b\w/g, char => char.toUpperCase());

								return (
									<TabPane tab={formattedSheetName} key={index + 1}>
										<>
											{selectedData[sheet]?.Header?.map((header) => (
												<Form.Item
													key={index}
													label={header.label}
													name={header.name}
													rules={[{ required: true, message: `Please enter ${header.label.toLowerCase()}!` }]}
													style={{ display: "inline-block", width: "20%", marginRight: "4%", marginBottom: "2.5rem" }}
												>
													{header.type === "datePicker" ? (
														<DatePicker style={{ width: "100%" }} />
													) : (
														<Input placeholder={`Enter ${header.label}`} />
													)}
												</Form.Item>
											))}

											{selectedData[sheet]?.Column?.length > 0 &&
												<Form.List name={selectedData[sheet]}>
													{(fields, { add, remove }) => (
														<>
															<div className={styles.rowHeader}
																style={{
																	display: "grid",
																	gridTemplateColumns: `repeat(${selectedData[sheet]?.Column?.length}, 1fr)`, // Dynamic grid
																	gap: "10px",
																	padding: "10px"
																}}>
																{selectedData[sheet]?.Column?.map((inputField) => (
																	<div key={inputField.label} className={styles.column}>
																		{inputField.label}
																	</div>
																))}
															</div>

															<div className={styles.rowContainer}>
																{fields.map((field, index) => (
																	<div key={index} className={styles.row}
																		style={{
																			display: "grid",
																			gridTemplateColumns: `repeat(${selectedData[sheet]?.Column.length}, 1fr)`, // Dynamic grid
																			gap: "10px",
																			padding: "10px"
																		}}
																	>
																		{selectedData[sheet]?.Column.map((inputField) => (
																			<Form.Item
																				key={inputField.name}
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
																							border: "1px solid rgba(201, 196, 196, 0.6)",
																						}}
																					/>
																				) : (
																					<Input
																						placeholder={inputField.label}
																						style={{
																							width: "100%",
																							padding: "4px",
																							borderRadius: "8px",
																							border: "1px solid rgba(201, 196, 196, 0.6)",
																						}}
																					/>
																				)}
																			</Form.Item>
																		))}
																	</div>
																))}
															</div>

															<Form.Item>
																<Button type="dashed" onClick={() => add()} block icon={<PlusOutlined />}>
																	Add Details
																</Button>
															</Form.Item>
														</>
													)}
												</Form.List>
											}

											<div className={styles.buttonContainer}>
												<CustomButton isFilled={true} text="Save" onClick={() => form.submit()} />
												<CustomButton isFilled={false} text="Cancel" onClick={handleCancel} />
											</div>
										</>
									</TabPane>
								);
							})}
						</Tabs>
					</Form>
				}

				{addType === "upload" &&
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
							<CustomButton isFilled={true} text="Extract" onClick={handleExtract} />
							<CustomButton isFilled={false} text="Cancel" onClick={handleCancel} />
						</div>
					</>
				}
			</Form>
		</Modal>
	);
};
