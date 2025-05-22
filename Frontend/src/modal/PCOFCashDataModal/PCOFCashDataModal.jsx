import { DatePicker, Form, Input, Modal, Select } from 'antd';
import React, { useEffect, useState } from 'react';
import { ModalComponents } from '../../components/modalComponents';
import { CustomButton } from '../../components/uiComponents/Button/CustomButton';
import styles from './PCOFCashDataModal.module.css';

export const PCOFCashDataModal = ({ visible, onCancel, onConfirm }) => {

	return (
		<Modal
			title={<ModalComponents.Title
				title="Cash related data"
				showDescription={true}
				description="The details of Cash asset is empty. Please review in the base data table and proceed."
			/>}
			open={visible}
			onCancel={onCancel}
			footer={null}
			width={1200}
			style={{marginTop: '-25px', minHeight: '300px'}}
		>
			<div className={styles.modalContainer}>
				Investment Cost, Investment Par, Investment External Valuation
			</div>

			<div className={styles.buttonContainer}>
				<CustomButton isFilled={false} text="Cancel" onClick={onCancel} />
				<CustomButton isFilled={true} text="Confirm & Proceed" onClick={onConfirm} />
			</div>
		</Modal>
	);
};
