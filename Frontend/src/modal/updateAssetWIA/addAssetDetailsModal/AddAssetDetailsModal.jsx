import { Modal } from 'antd';
import { useState } from 'preact/hooks';
import React from 'react';
import { ModalComponents } from '../../../components/modalComponents';
import { updateAssetDefaultColumnsData } from '../../../utils/constants/constants';
import styles from './AddAssetDetailsModal.module.css';

export const AddAssetDetailsModal = (
	{
		addAssetDetailsModalOpen,
		setAddAssetDetailsModalOpen,
		addDeleteAssetData,
		selectedSheetNumber,
		handleAddDeleteAssets,
		enteredInputData,
		setEnteredInputData
	}) => {

	const [error, setError] = useState(false);
	const label = ((updateAssetDefaultColumnsData[selectedSheetNumber])?.split('_'))?.join(' ');

	const handleSubmit = () => {
		if (addDeleteAssetData.type !== 'delete' && enteredInputData.trim() === '') {
			setError(true);
		} else {
			setError(false);
			handleAddDeleteAssets();
			setEnteredInputData('');
			setAddAssetDetailsModalOpen(false);
		}
	};

	const handleCancel = () => {
		setAddAssetDetailsModalOpen(false);
		setEnteredInputData('');
		setError(false);
	};


	return (
		<Modal
			title={<span style={{ color: '#909090', fontWeight: '500', fontSize: '14px', padding: '0 0 0 3%' }}>
				{
					addDeleteAssetData.type == 'duplicate' ? <>Duplicate {label}</>
						:
						addDeleteAssetData.type != 'delete' ? <>Add {label}</>

							: <>Delete {label}</>
				}
			</span>}
			centered
			open={addAssetDetailsModalOpen}
			style={{ zIndex: 100 }}
			onCancel={handleCancel}
			width={'75%'}
			footer={<ModalComponents.Footer key='footer-buttons' onClickCancel={handleCancel} onClickSubmit={handleSubmit} submitText='Yes' />}
		>
			{addDeleteAssetData.type != 'delete' ?
				<div className={styles.formContainer}>
					<div className={styles.label}>{label}</div>
					<input
						type="text"
						value={enteredInputData}
						className={styles.input}
						placeholder={`Enter ${label}`}
						onChange={(e) => {
							setEnteredInputData(e.target.value);
							setError(false);
						}}
					/>
					{error && <div style={{ color: 'red', fontSize: '12px', marginTop: '5px' }}>{label} is required</div>}
				</div>
				:
				<>
					Are you sure you want to delete {label} ?
				</>
			}

		</Modal>
	);
};
