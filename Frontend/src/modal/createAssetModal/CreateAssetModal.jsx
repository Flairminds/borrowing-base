import { Modal } from 'antd';
import { useEffect, useState } from 'preact/hooks';
import React from 'react';
import buttonStyle from '../../components/uiComponents/Button/ButtonStyle.module.css';
import { generateAssetData } from '../../utils/helperFunctions/addAssetFormData';
import styles from './CreateAssetModal.module.css';
import { UIComponents } from '../../components/uiComponents';

export const CreateAssetModal = ({createAssetModalOpen, setCreateAssetModalOpen, createAssetFormData, setCreateAssetFormData, modifyAssetsData, modificationData, showModifyButton, setShowModifyButton}) => {

	const handleCancel = () => {
		// setCreateAssetFormData([])
		const updatedData = createAssetFormData.map(item => ({
			...item,
			value: ' '
		}));
		setCreateAssetFormData([]);
		setCreateAssetModalOpen(false);
		setShowModifyButton(true);
	};

	const handleInputChange = (index, key, value) => {
		const columnData = [...createAssetFormData];
		const num = Number(value);

		// Check if the conversion results in a valid number
		if (!isNaN(num)) {
			value = num;
		}
		columnData[index] = {
			...columnData[index],
			value: value
		};
		setCreateAssetFormData(columnData);
	};

	const handleCreateButton = () => {
		const createAssetData = generateAssetData(createAssetFormData);
		modifyAssetsData(-1, createAssetData);
		const updatedData = createAssetFormData.map(item => ({
			...item,
			value: '' // Set value to an empty string (or space as per your example)
		}));
		// Step 3: Update the state
		// setData(updatedData);
		setCreateAssetFormData([]);
		setCreateAssetModalOpen(false);
	};

	const handleModifyButton = () => {
		const createAssetData = generateAssetData(createAssetFormData);
		modifyAssetsData(modificationData.index, createAssetData);
		// const updatedData = createAssetFormData.map(item => ({
		//   ...item,
		//   value: ' ' // Set value to an empty string (or space as per your example)
		// }));
		// const updatedData = [...createAssetFormData];
		// for(let i =0 ;i<updatedData.length; i++)
		// {
		//   let assetData= {...updatedData[i]};
		//   assetData.value = '';
		// }
		// // Step 3: Update the state
		// // setData(updatedData);
		setCreateAssetFormData([]);
		setCreateAssetModalOpen(false);

	};

	return (
		<div>

			<Modal
				title={<span style={{ color: '#909090', fontWeight: '500', fontSize: '14px', padding: '0 0 0 3%' }}>Create Asset</span>}
				centered
				open={createAssetModalOpen}
				// onOk={handleCancel}
				onCancel={handleCancel}
				width={'70%'}
				footer={[

				]}
			>
				<div className={styles.formContainer}>
					{createAssetFormData?.map((column, index) => (
						<div className={styles.formItem}>
							<div className={styles.formlabel}>
								{column.title}
							</div>
							<div>
								<input className={styles.forminput} type="text" value={createAssetFormData[index]?.value} onChange={(e) => handleInputChange(index, column.key, e.target.value)} />
							</div>
						</div>
					))
					}
				</div>

				<div className={styles.submitBtn}>
					<UIComponents.Button onClick={() => handleCreateButton()} text='Create Asset' isFilled={true} />
					{showModifyButton && <UIComponents.Button onClick={() => handleModifyButton()} text='Modify Asset' isFilled={true} />}
				</div>

				{/* <div className={styles.submitBtn}>
          </div> */}

			</Modal>
		</div>
	);
};
