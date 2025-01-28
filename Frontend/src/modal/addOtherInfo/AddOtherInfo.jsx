import { MinusCircleOutlined, PlusOutlined } from "@ant-design/icons";
import { Form, Input, DatePicker, Button } from "antd";
import Modal from "antd/es/modal/Modal";
import React, { useEffect } from "react";
import { CustomButton } from "../../components/custombutton/CustomButton";
import { submitOtherInfo } from "../../services/dataIngestionApi";
import { showToast } from "../../utils/helperFunctions/toastUtils";
import styles from "./AddOtherInfo.module.css";

export const AddOtherInfo = ({ isOpen, onClose, dataId, data = {} }) => {
	const [form] = Form.useForm();

	useEffect(() => {
		if (data.other_info_list) {
			const temp = data.other_info_list.map(o => {
				return {
					currency: o.currency,
					"exchangeRate": o.exchange_rates,
					"CashCurrentAndPreborrowing": o.cash_current_and_preborrowing,
					borrowing: o.borrowing,
					"additionalExpenses1": o.additional_expenses_1,
					"additionalExpenses2": o.additional_expenses_2,
					"additionalExpenses3": o.additional_expenses_3,
					"currentCreditFacilityBalance": o.current_credit_facility_balance
				};
			});
			// console.log(new Date(data.determination_date).toISOString().split('T')[0].replace(/-/g, '/'));
			form.setFieldsValue({
				// "determinationDate": new Date(data.determination_date).toISOString().split('T')[0].replace(/-/g, '/'),
				"minimumEquityAmountFloor": data.minimum_equity_amount_floor,
				"financialDetails": temp
			});
		}
	}, [data]);

	const handleCancel = () => {
		form.resetFields();
		onClose();
	};

	const handleSubmit = async (values) => {
		const extractionInfoId = dataId;

		try {
			let otherInfoData = [];
			if (values.financialDetails) {
				otherInfoData = values.financialDetails.map((item) => {
					return ({
						currency: item.currency,
						"exchange_rates": item.exchangeRate,
						"cash_current_and_preborrowing": item.CashCurrentAndPreborrowing,
						borrowing: item.borrowing,
						"additional_expenses_1": item.additionalExpenses1,
						"additional_expenses_2": item.additionalExpenses2,
						"additional_expenses_3": item.additionalExpenses3,
						"current_credit_facility_balance": item.currentCreditFacilityBalance
					});
				});
			}
			const transformedData = {
				"extraction_info_id": extractionInfoId,
				"determination_date": values.determinationDate.format("MM-DD-YY"),
				"minimum_equity_amount_floor": values.minimumEquityAmountFloor,
				"other_data": otherInfoData
			};

			const response = await submitOtherInfo(transformedData);
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
		<Modal open={isOpen} onCancel={handleCancel} footer={null} width={"90%"}>
			<Form form={form} layout="vertical" onFinish={handleSubmit} autoComplete="off">
				<Form.Item
					label="Determination Date"
					name="determinationDate"
					rules={[{ required: true, message: "Please select a date!" }]}
					style={{ display: "inline-block", width: "20%" }}
				>
					<DatePicker style={{ width: "100%" }}/>
				</Form.Item>

				<Form.Item
					label="Minimum Equity Amount Floor"
					name="minimumEquityAmountFloor"
					rules={[{ required: true, message: "Please enter the amount!" }]}
					style={{ display: "inline-block", width: "20%", marginLeft: "4%" }}
				>
					<Input placeholder="Enter amount" />
				</Form.Item>

				<Form.List name="financialDetails">
					{(fields, { add, remove }) => (
						<>
							<div className={styles.rowHeader}>
								<div className={styles.column}>Currency</div>
								<div className={styles.column}>Exchange Rate</div>
								<div className={styles.column}>Borrowing</div>
								<div className={styles.column}>Credit Facility Balance</div>
								<div className={styles.column}>Cash Current And Preborrowing</div>
								<div className={styles.column}>Additional Expenses 1</div>
								<div className={styles.column}>Additional Expenses 2</div>
								<div className={styles.column}>Additional Expenses 3</div>
								{/* <div className={styles.column}>Action</div> */}
							</div>

							{fields.map(({ key, name, ...restField }) => (
								<div key={key} className={styles.row}>
									<Form.Item
										{...restField}
										name={[name, "currency"]}
										className={styles.column}
										rules={[{ required: true, message: "Enter currency" }]}
									>
										<Input placeholder="Currency" />
									</Form.Item>

									<Form.Item
										{...restField}
										name={[name, "exchangeRate"]}
										className={styles.column}
										rules={[{ required: true, message: "Enter exchange rate" }]}
									>
										<Input placeholder="Exchange Rate" />
									</Form.Item>

									<Form.Item
										{...restField}
										name={[name, "borrowing"]}
										className={styles.column}
										rules={[{ required: true, message: "Enter borrowing" }]}
									>
										<Input placeholder="Borrowing" />
									</Form.Item>

									<Form.Item
										{...restField}
										name={[name, "currentCreditFacilityBalance"]}
										className={styles.column}
										rules={[{ required: true, message: "Enter credit facility balance" }]}
									>
										<Input placeholder="Credit Facility Balance" />
									</Form.Item>

									<Form.Item
										{...restField}
										name={[name, "CashCurrentAndPreborrowing"]}
										className={styles.column}
										rules={[{ required: true, message: "Enter CashCurrentAndPreborrowing" }]}
									>
										<Input placeholder="CashCurrentAndPreborrowing" />
									</Form.Item>

									<Form.Item
										{...restField}
										name={[name, "additionalExpenses1"]}
										className={styles.column}
										rules={[{ required: true, message: "Enter expenses" }]}
									>
										<Input placeholder="Additional Expenses 1" />
									</Form.Item>

									<Form.Item
										{...restField}
										name={[name, "additionalExpenses2"]}
										className={styles.column}
										rules={[{ required: true, message: "Enter additional expenses" }]}
									>
										<Input placeholder="Additional Expenses 2" />
									</Form.Item>

									<Form.Item
										{...restField}
										name={[name, "additionalExpenses3"]}
										className={styles.column}
										rules={[{ required: true, message: "Enter additional expenses" }]}
									>
										<Input placeholder="Additional Expenses 3" />
									</Form.Item>

									{/* <Form.Item style={{width: "1rem", margin: "0"}}>
										<MinusCircleOutlined
											style={{ color: "red", marginLeft: "auto" }}
											onClick={() => remove(name)}
										/>
									</Form.Item> */}
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

				<div className={styles.buttonContainer}>
					<CustomButton isFilled={true} text="Save" onClick={() => form.submit()} />
					<CustomButton isFilled={false} text="Cancel" onClick={handleCancel} />
				</div>
			</Form>
		</Modal>
	);
};
