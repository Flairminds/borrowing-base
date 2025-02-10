import { MinusCircleOutlined, PlusOutlined } from "@ant-design/icons";
import { Form, Input, DatePicker, Button } from "antd";
import Modal from "antd/es/modal/Modal";
import dayjs from "dayjs";
import React, { useEffect, useState } from "react";
import { CustomButton } from "../../components/custombutton/CustomButton";
import { submitOtherInfo } from "../../services/dataIngestionApi";
import { PFLTData, PCOFData } from "../../utils/constants/constants";
import { showToast } from "../../utils/helperFunctions/toastUtils";
import styles from "./AddAdditionalInformationModal.module.css";

export const AddAdditionalInformationModal = (
	{
		isAddFieldModalOpen,
		setIsAddFieldModalOpen,
		onClose,
		dataId,
		data = {},
		handleBaseDataPreview,
		previewFundType
	}
) => {
	const [form] = Form.useForm();
	const [initalFormData, setInitalFormData] = useState(null);

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
		const formData = {
			...data,
			"determination_date": data.determination_date && dayjs(data.determination_date),
			"other_data": data.other_data ? data.other_data : [{}]
		};

		if (previewFundType == "PCOF") {
			formData["revolving_closing_date"] = data.revolving_closing_date && dayjs(data.revolving_closing_date);
		} else {
			formData["minimum_equity_amount_floor"] = data.minimum_equity_amount_floor && data.minimum_equity_amount_floor;
		}
		console.info(formData, 'form');
		setInitalFormData(formData);
	}, [data]);

	const handleCancel = () => {
		form.resetFields();
		setIsAddFieldModalOpen(false);
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
						...el,
						"dollar_equivalent": el.amount * el.spot_rate
					};
				}));

				transformedData["other_data"] = updatedlist;
				transformedData["revolving_closing_date"] = values.revolving_closing_date.format("YYYY-MM-DD");
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
	console.info(selectedData, 'sel');
	console.info(initalFormData, 'initalFormData');

	const intialFormData = selectedData == "PCOF" ? pcofEmptyFormStructure : pfltEmptyFormStructure;

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
				{selectedData.Header.map((header) => (
					<Form.Item
						key={header.name}
						label={header.label}
						name={header.name}
						rules={[{ required: true, message: `Please enter ${header.label.toLowerCase()}!` }]}
						style={{ display: "inline-block", width: "20%", marginRight: "4%" }}
					>
						{header.type === "datePicker" ? (
							<DatePicker style={{ width: "100%" }} />
						) : (
							<Input placeholder={`Enter ${header.label}`} />
						)}
					</Form.Item>
				))}

				<Form.List name="other_data">
					{(fields, { add, remove }) => (
						<>
							<div className={styles.rowHeader}>
								{selectedData.Column.map((inputField) => (
									<div key={inputField.label} className={styles.column}>
										{inputField.label}
									</div>
								))}
							</div>

							{fields.map((field, index) => (
								<div key={field.key} className={styles.row}>
									{selectedData.Column.map((inputField) => (
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

							<Form.Item>
								<Button type="dashed" onClick={() => add()} block icon={<PlusOutlined />}>
									Add Details
								</Button>
							</Form.Item>
						</>
					)}
				</Form.List>
			</Form>
			<div className={styles.buttonContainer}>
				<CustomButton isFilled={true} text="Save" onClick={() => form.submit()} />
				<CustomButton isFilled={false} text="Cancel" onClick={handleCancel} />
			</div>
		</Modal>
	);
};
