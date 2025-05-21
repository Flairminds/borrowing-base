import { DatePicker, Form, Input, Modal, Select } from 'antd';
import React, { useEffect, useState } from 'react';
import { ModalComponents } from '../../components/modalComponents';
import { CustomButton } from '../../components/uiComponents/Button/CustomButton';
import styles from './VAEModal.module.css';
import { UIComponents } from '../../components/uiComponents';
import { Table } from 'antd';
import { DynamicTableComponents } from '../../components/reusableComponents/dynamicTableComponent/DynamicTableComponents';
import { showToast } from '../../utils/helperFunctions/toastUtils';
import { saveVAEData, getVAEData } from '../../services/dataIngestionApi';
import { fmtDateValue, fmtDisplayVal } from '../../utils/helperFunctions/formatDisplayData';
import dayjs from "dayjs";

export const VAEModal = ({ visible, data, columnNames, onCancel }) => {
	const [vaeData, setVaeData] = useState([]);
	const [showAdd, setShowAdd] = useState(false);
	const [formData, setFormData] = useState({
		obligor: '',
		eventType: '',
		materialModification: '',
		vaeDecisionDate: null,
		financialsDate: null,
		ttmEbitda: '',
		seniorDebt: '',
		totalDebt: '',
		unrestrictedCash: '',
		netSeniorLeverage: '',
		netTotalLeverage: '',
		interestCoverage: '',
		recurringRevenue: '',
		debtToRecurringRevenueRatio: '',
		liquidity: '',
		assignedValue: ''
	});

	const eventTypeOptions = [
		{ value: 'credit_deterioration', label: '(a) Credit Quality Deterioration Event' },
		{ value: 'material_modification', label: '(b) Material Modification Event' },
		// Add other event types as needed
	];

	const handleInputChange = (field, value) => {
		setFormData(prev => ({
			...prev,
			[field]: value
		}));
	};

	useEffect(() => {
		fetchVAEData();
	}, []);

	useEffect(() => {
		if (formData.seniorDebt && formData.ttmEbitda) {
			let temp = (formData.seniorDebt - (formData.unrestrictedCash || 0)) / formData.ttmEbitda
			setFormData(prev => ({
				...prev,
				['netSeniorLeverage']: temp
			}));
		}
		if (formData.totalDebt && formData.ttmEbitda) {
			let temp = (formData.totalDebt - (formData.unrestrictedCash || 0)) / formData.ttmEbitda
			setFormData(prev => ({
				...prev,
				['netTotalLeverage']: temp
			}));
		}
		if (formData.recurringRevenue && formData.ttmEbitda) {
			let temp = (formData.ttmEbitda || 0) / formData.recurringRevenue
			setFormData(prev => ({
				...prev,
				['debtToRecurringRevenueRatio']: temp
			}));
		}
	}, [formData])

	const columns = [
		{
			title: 'Obligor',
			dataIndex: 'obligor',
			key: 'obligor',
			width: 150,
			fixed: 'left',
		},
		{
			title: 'Event Type',
			dataIndex: 'eventType',
			key: 'eventType',
			width: 180,
		},
		{
			title: 'Material Modification',
			dataIndex: 'materialModification',
			key: 'materialModification',
			width: 150,
		},
		{
			title: 'VAE Decision Date',
			dataIndex: 'vaeDecisionDate',
			key: 'vaeDecisionDate',
			width: 130,
		},
		{
			title: 'Financials Date',
			dataIndex: 'financialsDate',
			key: 'financialsDate',
			width: 130,
		},
		{
			title: 'TTM EBITDA',
			dataIndex: 'ttmEbitda',
			key: 'ttmEbitda',
			width: 120,
			align: 'right',
		},
		{
			title: 'Senior Debt',
			dataIndex: 'seniorDebt',
			key: 'seniorDebt',
			width: 120,
			align: 'right',
		},
		{
			title: 'Total Debt',
			dataIndex: 'totalDebt',
			key: 'totalDebt',
			width: 120,
			align: 'right',
		},
		{
			title: 'Unrestricted Cash',
			dataIndex: 'unrestrictedCash',
			key: 'unrestrictedCash',
			width: 130,
			align: 'right',
		},
		{
			title: 'Net Senior Leverage',
			dataIndex: 'netSeniorLeverage',
			key: 'netSeniorLeverage',
			width: 140,
			align: 'right',
		},
		{
			title: 'Net Total Leverage',
			dataIndex: 'netTotalLeverage',
			key: 'netTotalLeverage',
			width: 140,
			align: 'right',
		},
		{
			title: 'Interest Coverage',
			dataIndex: 'interestCoverage',
			key: 'interestCoverage',
			width: 130,
			align: 'right',
		},
		{
			title: 'Recurring Revenue',
			dataIndex: 'recurringRevenue',
			key: 'recurringRevenue',
			width: 140,
			align: 'right',
		},
		{
			title: 'Debt-to-Revenue Ratio',
			dataIndex: 'debtToRecurringRevenueRatio',
			key: 'debtToRecurringRevenueRatio',
			width: 160,
			align: 'right',
		},
		{
			title: 'Liquidity',
			dataIndex: 'liquidity',
			key: 'liquidity',
			width: 120,
			align: 'right',
		},
		{
			title: 'Assigned Value',
			dataIndex: 'assignedValue',
			key: 'assignedValue',
			width: 130,
			align: 'right',
		},
	];

	const fetchVAEData = async() => {
		try {
			const response = await getVAEData();
			if (response.data.success) {
				let temp = response.data.result.map((r) => {
					let keys = Object.keys(r);
					let t = {...r};
					for (let i = 0; i < keys.length; i++) {
						t[keys[i]] = fmtDisplayVal(t[keys[i]]);
					}
					return t;
				});
				setVaeData(temp);
			} else {
				showToast('error', response.message);
			}
		} catch (error) {
			console.error(error.message);
			showToast('error', 'Error in fetching VAE data');
		}
	};

	const handleSave = async() => {
		try {
			if (!formData.obligor) {
				showToast('error', 'Enter obligor name');
				return;
			}
			const payload = {
				obligor: formData.obligor,
				eventType: formData.eventType || null,
				materialModification: formData.materialModification || null,
				vaeDecisionDate: formData.vaeDecisionDate ? formData.vaeDecisionDate.format("YYYY-MM-DD") : null,
				financialsDate: formData.financialsDate || null,
				ttmEbitda: formData.ttmEbitda || null,
				seniorDebt: formData.seniorDebt || null,
				totalDebt: formData.totalDebt || null,
				unrestrictedCash: formData.unrestrictedCash || null,
				netSeniorLeverage: formData.netSeniorLeverage || null,
				netTotalLeverage: formData.netTotalLeverage || null,
				interestCoverage: formData.interestCoverage || null,
				recurringRevenue: formData.recurringRevenue || null,
				debtToRecurringRevenueRatio: formData.debtToRecurringRevenueRatio || null,
				liquidity: formData.liquidity || null,
				assignedValue: formData.liquidity ? (formData.liquidity / 100) : null
			};
			const response = await saveVAEData({vaeData: payload});
			if (response.data.success) {
				showToast('success', response.data.message);
				fetchVAEData();
				setShowAdd(false);
			} else {
				showToast('error', response.data.message);
			}
		} catch (error) {
			console.error(error.message);
			showToast('error', 'Request failed due to internal error');
		}
	}

	return (
		<Modal
			title={<ModalComponents.Title
				title="VAE Data"
				showDescription={true}
				description="The following field values are not provided in the base data. Please review before proceeding."
			/>}
			open={visible}
			onCancel={onCancel}
			footer={null}
			width={1200}
			style={{marginTop: '-75px'}}
		>
			<div className={styles.modalContainer}>
				{showAdd ? (
					<Form layout="vertical" className={styles.formContainer}>
						<div className={styles.flexDiv}>
							<Form.Item label="Obligor" className={styles.formItem} required={true}>
								<Input placeholder="Enter Obligor" value={formData.obligor}
									onChange={(e) => handleInputChange('obligor', e.target.value)}
								/>
							</Form.Item>
							<Form.Item label="Event Type" className={styles.formItem}>
								<Input
									placeholder="Event Type"
									value={formData.eventType}
									onChange={(e) => handleInputChange('eventType', e.target.value)}
								/>
							</Form.Item>
						</div>
						<div className={styles.flexDiv}>
							<Form.Item label="Material Modification" className={styles.formItem}>
								<Input
									placeholder="Enter Material Modification"
									value={formData.materialModification}
									onChange={(e) => handleInputChange('materialModification', e.target.value)}
								/>
							</Form.Item>
							<Form.Item
								label="Date of VAE Decision"
								className={styles.formItem}
							>
								<DatePicker
									className={styles.fullWidth}
									placeholder="Select VAE Decision Date"
									value={formData.vaeDecisionDate}
									onChange={(date) => handleInputChange('vaeDecisionDate', date)}
								/>
							</Form.Item>
							<Form.Item
								label="Date of Financials"
								className={styles.formItem}
							>
								<DatePicker
									className={styles.fullWidth}
									placeholder="Select Financials Date"
									value={formData.financialsDate}
									onChange={(date) => handleInputChange('financialsDate', date)}
								/>
							</Form.Item>
						</div>
						<div className={styles.flexDiv}>
							<Form.Item label="TTM EBITDA" className={styles.formItem}>
								<Input
									type="number"
									placeholder="Enter TTM EBITDA"
									value={formData.ttmEbitda}
									onChange={(e) => handleInputChange('ttmEbitda', e.target.value)}
								/>
							</Form.Item>
							<Form.Item label="Senior Debt" className={styles.formItem}>
								<Input
									type="number"
									placeholder="Enter Senior Debt"
									value={formData.seniorDebt}
									onChange={(e) => handleInputChange('seniorDebt', e.target.value)}
								/>
							</Form.Item>
							<Form.Item
								label="Total Debt"
								className={styles.formItem}
							>
								<Input
									type="number"
									placeholder="Enter Total Debt"
									value={formData.totalDebt}
									onChange={(e) => handleInputChange('totalDebt', e.target.value)}
								/>
							</Form.Item>
							<Form.Item
								label="Unrestricted Cash"
								className={styles.formItem}
							>
								<Input
									type="number"
									placeholder="Enter Unrestricted Cash"
									value={formData.unrestrictedCash}
									onChange={(e) => handleInputChange('unrestrictedCash', e.target.value)}
								/>
							</Form.Item>
						</div>
						<div className={styles.flexDiv}>
							<Form.Item label="Net Senior Leverage" className={styles.formItem}>
								<Input
									type="number"
									placeholder="Enter Net Senior Leverage"
									value={formData.netSeniorLeverage}
									onChange={(e) => handleInputChange('netSeniorLeverage', e.target.value)}
								/>
							</Form.Item>
							<Form.Item
								label="Net Total Leverage"
								className={styles.formItem}
							>
								<Input
									type="number"
									placeholder="Enter Net Total Leverage"
									value={formData.netTotalLeverage}
									onChange={(e) => handleInputChange('netTotalLeverage', e.target.value)}
								/>
							</Form.Item>
							<Form.Item
								label="Interest Coverage"
								className={styles.formItem}
							>
								<Input
									type="number"
									placeholder="Enter Interest Coverage"
									value={formData.interestCoverage}
									onChange={(e) => handleInputChange('interestCoverage', e.target.value)}
								/>
							</Form.Item>
						</div>
						<div className={styles.flexDiv}>
							<Form.Item
								label="Recurring Revenue"
								className={styles.formItem}
							>
								<Input
									type="number"
									placeholder="Enter Recurring Revenue"
									value={formData.recurringRevenue}
									onChange={(e) => handleInputChange('recurringRevenue', e.target.value)}
								/>
							</Form.Item>
							<Form.Item
								label="Debt-to-Recurring Revenue Ratio"
								className={styles.formItem}
							>
								<Input
									type="number"
									placeholder="Enter Debt-to-Recurring Revenue Ratio"
									value={formData.debtToRecurringRevenueRatio}
									onChange={(e) => handleInputChange('debtToRecurringRevenueRatio', e.target.value)}
								/>
							</Form.Item>
							<Form.Item
								label="Liquidity"
								className={styles.formItem}
							>
								<Input
									type="number"
									placeholder="Enter Liquidity"
									value={formData.liquidity}
									onChange={(e) => handleInputChange('liquidity', e.target.value)}
								/>
							</Form.Item>
							<Form.Item
								label="Assigned Value (%)"
								className={styles.formItem}
							>
								<Input
									type="number"
									placeholder="Enter Assigned Value"
									value={formData.assignedValue}
									onChange={(e) => handleInputChange('assignedValue', e.target.value)}
								/>
							</Form.Item>
						</div>
					</Form>
				) : (
					<div className={styles.viewContainer}>
						<Table
							columns={columns}
							dataSource={vaeData}
							scroll={{ x: 1500 }}
							pagination={false}
							bordered
							size="small"
							className={styles.vaeTable}
						/>
					</div>
				)}
			</div>

			<div className={styles.buttonContainer}>
				<CustomButton
					isFilled={true}
					text={showAdd ? "Save" : "+ Add"}
					onClick={() => showAdd ? handleSave(formData) : setShowAdd(!showAdd)}
				/>
			</div>
		</Modal>
	);
};
