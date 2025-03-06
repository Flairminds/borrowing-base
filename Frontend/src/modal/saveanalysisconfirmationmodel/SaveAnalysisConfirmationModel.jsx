import {Input, Modal } from 'antd';
import React from 'react';
import ButtonStyles from '../../components/uiComponents/Button/ButtonStyle.module.css';
import { CustomButton } from '../../components/uiComponents/Button/CustomButton';

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
			footer={[
				<div key="footer-buttons" className="px-4">
					<button key="back" onClick={() => {
						isSetDescriptionModal(false);
						setDescriptionInput('');
					}} className={ButtonStyles.outlinedBtn}>
						Cancel
					</button>
					<CustomButton
						isFilled={true}
						loading={whatIfanalysisLoader}
						loadingText="Saving..."
						text="Save"
						onClick={SaveWhatIfAnalysis}
					/>
				</div>
			]}
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


