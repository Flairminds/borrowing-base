import { DatePicker, Form, Input, Modal, Select } from 'antd';
import React, { useState } from 'react';
import { ModalComponents } from '../../components/modalComponents';
import { CustomButton } from '../../components/uiComponents/Button/CustomButton';
import styles from './VAEModal.module.css';
import { UIComponents } from '../../components/uiComponents';
import { Table } from 'antd';
import { DynamicTableComponents } from '../../components/reusableComponents/dynamicTableComponent/DynamicTableComponents';

export const VAEModal = ({ visible, data, columnNames, onConfirm, onCancel }) => {
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

    const columns = [{
            label: 'Obligor',
            key: 'obligor',
        }, {
            label: 'Event Type',
			key: 'eventType'
        }, {
			label: 'Material Modification',
			key: 'materialModification'
        }, {
            label: 'VAE Decision Date',
			key: 'vaeDecisionDate'
		}, {
			label: 'Financials Date',
			key: 'financialsDate'
        }, {
            label: 'TTM EBITDA',
			key: 'ttmEbitda'
		}, {
			label: 'Senior Debt',
			key: 'seniorDebt'
		}, {
			label: 'Total Debt',
			key: 'totalDebt'
        }, {
			label: 'Unrestricted Cash',
			key: 'unrestrictedCash'
        }, {
			label: 'Net Senior Leverage',
			key: 'netSeniorLeverage'
		}, {
			label: 'Net Total Leverage',
			key: 'netTotalLeverage'
		}, {
			label: 'Interest Coverage',
			key: 'interestCoverage'
        }, {
			label: 'Recurring Revenue',
			key: 'recurringRevenue'
		}, {
			label: 'Debt-to-Revenue Ratio',
			key: 'debtToRecurringRevenueRatio'
        }, {
			label: 'Liquidity',
			key: 'liquidity'
		}, {
			label: 'Assigned Value',
			key: 'assignedValue'
        }
    ];

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
        >
            <div className={styles.modalContainer}>
                {showAdd ? (
                    <Form layout="vertical" className={styles.formContainer}>
                        <div className={styles.flexDiv}>
                            <Form.Item
                                label="Obligor"
                                className={styles.formItem}
                            >
                                <Input
                                    placeholder="Enter Obligor"
                                    value={formData.obligor}
                                    onChange={(e) => handleInputChange('obligor', e.target.value)}
                                />
                            </Form.Item>
                            <Form.Item
                                label="Event Type"
                                className={styles.formItem}
                            >
                                <Select
                                    placeholder="Select Event Type"
                                    options={eventTypeOptions}
                                    value={formData.eventType}
                                    onChange={(value) => handleInputChange('eventType', value)}
                                />
                            </Form.Item>
                            <Form.Item
                                label="Material Modification"
                                className={styles.formItem}
                            >
                                <Input
                                    placeholder="Enter Material Modification"
                                    value={formData.materialModification}
                                    onChange={(e) => handleInputChange('materialModification', e.target.value)}
                                />
                            </Form.Item>
                        </div>
                        <div className={styles.flexDiv}>
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
                            <Form.Item
                                label="TTM EBITDA"
                                className={styles.formItem}
                            >
                                <Input
                                    type="number"
                                    placeholder="Enter TTM EBITDA"
                                    value={formData.ttmEbitda}
                                    onChange={(e) => handleInputChange('ttmEbitda', e.target.value)}
                                />
                            </Form.Item>
                        </div>
                        <div className={styles.flexDiv}>
                            <Form.Item
                                label="Senior Debt"
                                className={styles.formItem}
                            >
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
                            <Form.Item
                                label="Net Senior Leverage"
                                className={styles.formItem}
                            >
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
                        </div>
                        <div className={styles.flexDiv}>
                            <Form.Item
                                label="Assigned Value"
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
						<DynamicTableComponents data={[{
                                key: '1',
                                obligor: 'Schlesinger Global, Inc.',
                                eventType: 'Initial Assigned Value at Closing',
                                materialModification: '-',
                                vaeDecisionDate: '2023-01-01',
                                financialsDate: '2023-01-01',
                                ttmEbitda: '1,000,000',
                                seniorDebt: '500,000',
                                totalDebt: '750,000',
                                unrestrictedCash: '250,000',
                                netSeniorLeverage: '2.5x',
                                netTotalLeverage: '3.0x',
                                interestCoverage: '3.5x',
                                recurringRevenue: '2,000,000',
                                debtToRecurringRevenueRatio: '0.375x',
                                liquidity: '500,000',
                                assignedValue: '900,000'
                            }]}
							columns={columns}
							/>
                        <Table
                            columns={columns}
                            dataSource={[{
                                key: '1',
                                obligor: 'Schlesinger Global, Inc.',
                                eventType: 'Initial Assigned Value at Closing',
                                materialModification: '-',
                                vaeDecisionDate: '2023-01-01',
                                financialsDate: '2023-01-01',
                                ttmEbitda: '1,000,000',
                                seniorDebt: '500,000',
                                totalDebt: '750,000',
                                unrestrictedCash: '250,000',
                                netSeniorLeverage: '2.5x',
                                netTotalLeverage: '3.0x',
                                interestCoverage: '3.5x',
                                recurringRevenue: '2,000,000',
                                debtToRecurringRevenueRatio: '0.375x',
                                liquidity: '500,000',
                                assignedValue: '900,000'
                            }]}
                            bordered
                            size="small"
                            pagination={false}
                            className={styles.vaeTable}
                        />
                    </div>
                )}
            </div>

            <div className={styles.buttonContainer}>
                <CustomButton 
                    isFilled={true} 
                    text={showAdd ? "Save" : "+ Add"} 
                    onClick={() => {
                        if (showAdd) {
                            onConfirm?.(formData);
                        }
                        setShowAdd(!showAdd);
                    }} 
                />
            </div>
        </Modal>
    );
};
