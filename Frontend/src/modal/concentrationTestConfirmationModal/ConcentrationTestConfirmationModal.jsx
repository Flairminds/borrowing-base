import { Button, Modal } from 'antd';
import React from 'react';
import ButtonStyles from '../../components/uiComponents/Button/ButtonStyle.module.css';
import { getListOfWhatIfAnalysis, lockHairCutTestData } from '../../services/api';
import styles from './ConcentrationTestConfirmationModal.module.css';
import { ModalComponents } from '../../components/modalComponents';

export const ConcentrationTestConfirmationModal = ({
	confirmationModalOpen, setConfirmationModalOpen, baseFile, hairCutArray, setTablesData,
	setConentrationTestModalOpen, setWhatIfAnalysisListData }) => {

	const handleCancel = () => {
		setConfirmationModalOpen(false);
	};

	const handleLock = async() => {
		try {
			const res = await lockHairCutTestData(baseFile.id, hairCutArray);
			setTablesData(res.data);
			getWhatifAnalysisList();
			setConentrationTestModalOpen(false);
		} catch (err) {
			console.error(err);
		}

		setConfirmationModalOpen(false);
	};

	const getWhatifAnalysisList = async () => {
		try {
			const response = await getListOfWhatIfAnalysis(1);
			setWhatIfAnalysisListData(response.data.Whatif_data);
		} catch (err) {
			console.error(err);
		}
	};

	return (
		<>

			<Modal
				title={<ModalComponents.Title title={'Confirm'} />}
				centered
				open={confirmationModalOpen}
				// onOk={handleOk}
				onCancel={handleCancel}
				width={'70%'}
				footer={[<ModalComponents.Footer key='footer-buttons' onClickCancel={handleCancel} onClickSubmit={handleLock} submitText={'Yes'} />]}
			>
				<div className={styles.Popupcontainer}>

				</div>
				<div>
					Applying the new hair cut number will delete all what-if simulations related to the previous hair-cut numbers.
				</div>
				<b>
					Would you like to proceed?
				</b>
			</Modal>
		</>
	);
};
