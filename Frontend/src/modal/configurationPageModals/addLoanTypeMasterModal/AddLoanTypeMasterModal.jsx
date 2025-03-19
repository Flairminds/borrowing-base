import { Modal } from 'antd';
import React, { useState } from 'react';
import { ModalComponents } from '../../../components/modalComponents';
import { DynamicInputComponent } from '../../../components/reusableComponents/dynamicInputsComponent/DynamicInputComponent';
import { addLoanTypeMaster } from '../../../services/dataIngestionApi';
import { showToast } from '../../../utils/helperFunctions/toastUtils';
import styles from './AddLoanTypeMasterModal.module.css';

export const AddLoanTypeMasterModal = ({isOpen, setIsOpen, fundType, getEntryMappingInfo, selectedFundType, activeMappingType}) => {

	const [masterTypeInput, setMasterTypeInput] = useState("");

	const handleCancel = () => {
		setIsOpen(false);
		setMasterTypeInput("");
	};

	const handleAddMaster = async() => {
		try {
			const res = await addLoanTypeMaster(masterTypeInput, fundType, activeMappingType);
			console.info("res", res);
			showToast('success', res.data.message);
			getEntryMappingInfo(selectedFundType);
			handleCancel();
		} catch (err) {
			console.error(err);
			showToast('error', err.response.data.message);
		}
	};

	return (
		<Modal open={isOpen} onCancel={handleCancel} footer={null} width={"50%"}>
			<ModalComponents.Title title="Add Loan Type Master" />

			<div className={styles.inputContainer}>
				<DynamicInputComponent inputValue={masterTypeInput} onInputChange={(e) => setMasterTypeInput(e.target.value)} />
			</div>

			<div className={styles.modalFooterContainer}>
				<ModalComponents.Footer onClickCancel={handleCancel} submitText="Add master" onClickSubmit={handleAddMaster} />
			</div>

		</Modal>
	);
};
