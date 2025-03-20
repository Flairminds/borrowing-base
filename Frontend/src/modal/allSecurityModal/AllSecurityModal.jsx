import { Modal, Input } from "antd";
import React, { useState, useEffect } from "react";
import { CustomButton } from "../../components/uiComponents/Button/CustomButton";
import { editPfltSecMapping, postAddSecurityMapping } from "../../services/dataIngestionApi";
import { showToast } from "../../utils/helperFunctions/toastUtils";
import styles from './AllSecurityModal.module.css';

export const AllSecurityModal = ({ isOpen, setIsOpen, security, getMappingData }) => {
	const [formData, setFormData] = useState({
		cashfile_security_name: "",
		family_name: "",
		master_comp_security_name: "",
		security_type: "",
		soi_name: ""
	});
	const [errors, setErrors] = useState({});

	useEffect(() => {
		if (security) {
			setFormData(security);
		}
	}, [security]);

	const handleChange = (e) => {
		const { name, value } = e.target;
		setFormData((prev) => ({
			...prev,
			[name]: value
		}));
	};

	const handleCancel = () => {
		setIsOpen(false);
	};

	const handleSave = async () => {
		const newErrors = {};

		if (!formData.soi_name) {
			newErrors.soi_name = 'SOI Name is required';
		}

		if (Object.keys(newErrors).length > 0) {
			setErrors(newErrors);
			return;
		}

		try {
			const payload = {

				id: security.id,
				family_name: formData.family_name || '',
				cashfile_security_name: formData.cashfile_security_name,
				soi_name: formData.soi_name || '',
				master_comp_security_name: formData.master_comp_security_name || '',
				security_type: formData.security_type || ''
			};

			const response = await editPfltSecMapping([payload]);

			if (response?.data?.success) {
				const successMessage = 'Security mapping Edited successfully';
				showToast('success', successMessage);
				setFormData({
					cashfile_security_name: "",
					family_name: "",
					master_comp_security_name: "",
					security_type: "",
					soi_name: ""
				});
				setErrors({});
				handleCancel();
			}
			await getMappingData("all");
		} catch (error) {
			console.error("API Error:", error);
			showToast('error', error?.response?.data?.message || 'Error: Failed to add security mapping');
		}
	};

	return (
		<Modal open={isOpen} onCancel={handleCancel} footer={null} width={"40%"}>
			<h6>Edit Security Mapping</h6>
			<div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
				<div style={{ padding: '20px', border: '1px solid #d9d9d9', borderRadius: '4px', width: '90%' }}>
					<div style={{ marginBottom: 20 }}>
						<label htmlFor="soi_name" style={{ marginBottom: 7 }}> <span style={{ color: 'red' }}>*</span>SOI Name</label>
						<Input
							id="soi_name"
							name="soi_name"
							value={formData.soi_name}
							onChange={handleChange}
						/>
						{errors?.soi_name && <span className={styles.errorText}>{errors?.soi_name}</span>}
					</div>
					<div style={{ marginBottom: 20 }}>
						<label htmlFor="master_comp_security_name" style={{ marginBottom: 7 }}>Security Name</label>
						<Input
							id="master_comp_security_name"
							name="master_comp_security_name"
							value={formData.master_comp_security_name}
							onChange={handleChange}
						/>
					</div>
					<div style={{ marginBottom: 20 }}>
						<label htmlFor="family_name" style={{ marginBottom: 7 }}>Family Name</label>
						<Input
							id="family_name"
							name="family_name"
							value={formData.family_name}
							onChange={handleChange}
						/>
					</div>
					<div style={{ marginBottom: 20 }}>
						<label htmlFor="security_type" style={{ marginBottom: 7 }}>Security Type</label>
						<Input
							id="security_type"
							name="security_type"
							value={formData.security_type}
							onChange={handleChange}
						/>
					</div>
					<div style={{ marginBottom: 14 }}>
						<label htmlFor="cashfile_security_name" style={{ marginBottom: 7 }}>Security/Facility Name</label>
						<Input
							id="cashfile_security_name"
							name="cashfile_security_name"
							value={formData.cashfile_security_name}
							onChange={handleChange}
						/>
					</div>
					<div style={{ display: 'flex', justifyContent: "flex-end" }}>
						<CustomButton isFilled={false} text="Cancel" onClick={handleCancel} style={{ marginLeft: '8px' }} />
						<CustomButton isFilled={true} text="Save" onClick={handleSave} />
					</div>
				</div>
			</div>
		</Modal>
	);
};
