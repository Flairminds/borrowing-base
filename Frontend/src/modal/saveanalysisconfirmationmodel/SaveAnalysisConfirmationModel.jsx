import {Input, Modal } from 'antd';
import React from 'react';
import ButtonStyles from '../../components/uiComponents/Button/ButtonStyle.module.css';
import { CustomButton } from '../../components/uiComponents/Button/CustomButton';
import { ModalComponents } from '../../components/modalComponents';

export const SaveAnalysisConfirmationModel = ({
	descriptionModal,
	handleCancel,
	isSetDescriptionModal,
	setDescriptionInput,
	whatIfanalysisLoader,
	SaveWhatIfAnalysis,
	descriptionInput
}) => {
	return (
		<Modal
			title="Do you want to add note?"
			centered
			open={descriptionModal}
			// onOk={handleSaveEbita}
			onCancel={handleCancel}
			width={'50%'}
			footer={[<ModalComponents.Footer key='footer-buttons' onClickCancel={() => {
				isSetDescriptionModal(false);
				setDescriptionInput('');
			}} loading={whatIfanalysisLoader} submitText='Save' onClickSubmit={SaveWhatIfAnalysis} />]}
		>
			<>
				<Input
					type="text"
					placeholder='Notes'
					value={descriptionInput}
					style={{width: '80%', margin: '1rem'}}
					onChange={(e) => setDescriptionInput(e.target.value)}
				/>
			</>
		</Modal>
	);
};


