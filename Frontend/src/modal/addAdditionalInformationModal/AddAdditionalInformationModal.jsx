import { MinusCircleOutlined, PlusOutlined } from "@ant-design/icons";
import { Form, Input, DatePicker, Button } from "antd";
import Modal from "antd/es/modal/Modal";
import React, { useEffect, useState } from "react";
import { CustomButton } from "../../components/custombutton/CustomButton";
import { submitOtherInfo } from "../../services/dataIngestionApi";
import { showToast } from "../../utils/helperFunctions/toastUtils";
import styles from "./AddAdditionalInformationModal.module.css";
import { additionalDetailsFormStructure } from "../../utils/constants/constants";
import dayjs from "dayjs";

export const AddAdditionalInformationModal = (
	{
		isAddFieldModalOpen,
		setIsAddFieldModalOpen,
		onClose,
		dataId,
		data = {},
		handleBaseDataPreview }
) => {
	const [form] = Form.useForm();
	const [initalFormData, setInitalFormData] = useState(null);

	const emptyFormStructure = {
		"determination_date": "",
		"minimum_equity_amount_floor": "",
		"other_data": [{}]
	};

	useEffect(() => {
		console.info(data, 'ddd');
		const formData = {
			...data,
			"determination_date": data.determination_date && dayjs(data.determination_date),
			"minimum_equity_amount_floor": data.minimum_equity_amount_floor && data.minimum_equity_amount_floor,
			"other_data": data.other_data ? data.other_data : [{}]
		};
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
				"other_data": values.other_data
			};

			console.info(transformedData, '-test 123', values, 'vals');

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

	return (
		<Modal open={isAddFieldModalOpen} onCancel={handleCancel} footer={null} width={"90%"}>
			<Form form={form} layout="vertical" onFinish={handleSubmit} autoComplete="off" initialValues={initalFormData ? initalFormData : emptyFormStructure}>
				<Form.Item
					label="Determination Date"
					name="determination_date"
					rules={[{ required: true, message: "Please select a date!" }]}
					style={{ display: "inline-block", width: "20%" }}
				>
					<DatePicker style={{ width: "100%" }}/>
				</Form.Item>

				<Form.Item
					label="Minimum Equity Amount Floor"
					name="minimum_equity_amount_floor"
					rules={[{ required: true, message: "Please enter the amount!" }]}
					style={{ display: "inline-block", width: "20%", marginLeft: "4%" }}
				>
					<Input placeholder="Enter amount" />
				</Form.Item>

				<Form.List name="other_data">
					{(fields, { add, remove }, index) => (
						<>
							<div className={styles.rowHeader}>
								{additionalDetailsFormStructure.map((inputfield) => (
									<div key={inputfield.label} className={styles.column}>{inputfield.label}</div>
								))}
							</div>

							{fields.map((field, {...resetField}, index) => (
								<div key={index} className={styles.row}>

									{additionalDetailsFormStructure.map((inputfield) => (
										<Form.Item
											key={inputfield.name}
											// rules={[{ required: true }]}
											name={[field.name, inputfield.name]}
											noStyle
										>
											<Input
												defaultValue={inputfield?.value}
												placeholder={inputfield.label}
												style={{
													width: "100%",
													padding: '4px',
													borderRadius: "8px",
													border: "1px solid rgba(201, 196, 196, 0.6)"
												}}
											/>
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
