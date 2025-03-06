import { Button, Modal } from 'antd';
import { useState } from 'preact/hooks';
import React from 'react';
import ButtonStyles from '../../../components/uiComponents/Button/ButtonStyle.module.css';
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


	const label = ((updateAssetDefaultColumnsData[selectedSheetNumber])?.split('_'))?.join(' ');

	const handleCancel = () => {
		setAddAssetDetailsModalOpen(false);
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
			style={{zIndex: 100}}
			onCancel={handleCancel}
			width={'75%'}
			footer={<>
				<div key="footer-buttons" className="px-4">
					<button key="back" onClick={handleCancel} className={ButtonStyles.outlinedBtn}>
						Cancel
					</button>
					<Button className={ButtonStyles.filledBtn} key="submit" type="primary" style={{ backgroundColor: '#0EB198' }} onClick={handleAddDeleteAssets}>
						Yes
					</Button>
				</div>
			</>}
		>
			{addDeleteAssetData.type != 'delete' ?
				<div className={styles.formContainer}>
					<div className={styles.label}>{label}</div>
					<input
						type="text"
						value={enteredInputData}
						className={styles.input}
						placeholder={`Enter ${label}`}
						onChange={(e) => setEnteredInputData(e.target.value)}
					/>
				</div>
				:
				<>
					Are you sure you want to delete {label} ?
				</>
			}

		</Modal>
	);
};
