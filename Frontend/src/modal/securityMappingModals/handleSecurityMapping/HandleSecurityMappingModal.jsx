import { Button, Modal } from 'antd';
import Form from 'antd/es/form/Form';
import Input from 'antd/es/input/Input';
import Radio from 'antd/es/radio/radio';
import React, { useEffect, useState } from 'react';
import { CustomButton } from '../../../components/custombutton/CustomButton';
import { DynamicTableComponents } from '../../../components/reusableComponents/dynamicTableComponent/DynamicTableComponents';
import { editPfltSecMapping, getProbableSecuritiesData, postAddSecurityMapping } from '../../../services/dataIngestionApi';
import { showToast } from '../../../utils/helperFunctions/toastUtils';
import styles from './HandleSecurityMappingModal.module.css';


export const HandleSecurityMappingModal = ({ isOpen, setIsOpen, activeSecurity, getMappingData }) => {

	const [probableEntriesData, setProbableEntriesData] = useState();
	const [selectedOption, setSelectedOption] = useState('mapToExisting');
	const [errors, setErrors] = useState({});
	const [formValues, setFormValues] = useState({});


	const handleOptionChange = e => {
		setSelectedOption(e.target.value);
	};

	const handleInputChange = (key, value) => {
		setFormValues((prev) => ({ ...prev, [key]: value }));
	};

	const handleSave = async () => {
		const newErrors = {};

		if (!formValues.soiName) {
			newErrors.soiName = 'SOI Name is required';
		}


		if (Object.keys(newErrors).length > 0) {
			setErrors(newErrors);
			return;
		}

		try {
			const payload = {
				soi_name: formValues.soiName || '',
				master_comp_security_name: formValues.masterCompSecurityName || '',
				family_name: formValues.familyName || '',
				security_type: formValues.securityType || '',
				cashfile_security_name: activeSecurity
			};

			const response = await postAddSecurityMapping(payload);

			if (response?.data?.success) {
				const successMessage = response.data.message || 'Security mapping added successfully';
				showToast('success', successMessage);
				setFormValues({});
				setErrors({});
			}
			await getMappingData("unmapped");
		} catch (error) {
			console.error("API Error:", error);
			showToast('error', error?.response?.data?.message || 'Error: Failed to add security mapping');
		}
	};
	// const handleFormCancel = () => {
	// 	setFormValues({});
	// 	setErrors({});
	// };

	const handleCancel = () => {
		setIsOpen(false);
		setFormValues({});
		setErrors({});
		// setProbableEntriesData(null);
	};

	const handleMapSecurity = async (secId, cashSecurity) => {
		const mappingData = {
			"id": secId,
			"cashfile_security_name": cashSecurity
		};
		try {
			const res = await editPfltSecMapping([mappingData]);
			showToast('success', res?.data?.message);
			await getMappingData("unmapped");
		} catch (error) {
			showToast("error", error?.response?.data?.message || "Failed to update data");
		}
		setProbableEntriesData(null);
		setIsOpen(false);
	};

	const additionalColumns = [{
		key: "",
		label: "",
		'render': (value, row) => <div onClick={() => handleMapSecurity(row.id, activeSecurity)} style={{ textAlign: 'center', cursor: 'pointer' }}> Use </div>
	}];

	const getProbableMappings = async () => {
		const res = await getProbableSecuritiesData(activeSecurity);
		setProbableEntriesData(res.data.result);
	};

	useEffect(() => {
		if (isOpen) {
			getProbableMappings();
		}
	}, [activeSecurity]);


	return (
		<Modal open={isOpen} onCancel={handleCancel} footer={null} width={"80%"}>
			<h5>{activeSecurity}</h5>
			<Radio.Group value={selectedOption} onChange={handleOptionChange} style={{ marginBottom: "16px" }}>
				<Radio value="mapToExisting">Map to Existing Record</Radio>
				<Radio value="addNewMapping">Add New Mapping</Radio>
			</Radio.Group>
			{selectedOption === 'mapToExisting' && (
				<DynamicTableComponents data={probableEntriesData?.data} columns={probableEntriesData?.columns} additionalColumns={additionalColumns}
				/>
			)}
			{selectedOption === 'addNewMapping' && (
				<div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
					<div style={{ padding: '16px', border: '1px solid #d9d9d9', borderRadius: '4px', width: '50%' }}>
						<Form layout="vertical">
							<Form.Item label="SOI Name" required>
								<Input
									style={{ width: '100%' }}
									value={formValues.soiName || ''}
									onChange={(e) => handleInputChange('soiName', e.target.value)}
								/>
								{errors.soiName && <span className={styles.errorText}>{errors.soiName}</span>}
							</Form.Item>

							<Form.Item label="Master Comp Security Name">
								<Input
									style={{ width: '100%' }}
									value={formValues.masterCompSecurityName || ''}
									onChange={(e) => handleInputChange('masterCompSecurityName', e.target.value)}
								/>
							</Form.Item>
							<Form.Item label="Family Name" >
								<Input
									style={{ width: '100%' }}
									value={formValues.familyName || ''}
									onChange={(e) => handleInputChange('familyName', e.target.value)}
								/>
							</Form.Item>
							<Form.Item label="Security Type" >
								<Input
									style={{ width: '100%' }}
									value={formValues.securityType || ''}
									onChange={(e) => handleInputChange('securityType', e.target.value)}
								/>
							</Form.Item>
							<Form.Item>
								<div style={{display: 'flex', justifyContent: "flex-end"}}>
									<CustomButton isFilled={false} text="Cancel" onClick={handleCancel} style={{ marginLeft: '8px' }} />
									<CustomButton isFilled={true} text="Save" onClick={handleSave} />
								</div>
							</Form.Item>
						</Form>
					</div>
				</div>
			)}
		</Modal>
	);
};
