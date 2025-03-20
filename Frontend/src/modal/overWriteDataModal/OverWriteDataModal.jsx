import { Button, Modal } from 'antd';
import React from 'react';
import warningIcon from '../../assets/uploadFIle/warning.svg';
import { ModalComponents } from '../../components/modalComponents';
import ButtonStyles from '../../components/uiComponents/Button/ButtonStyle.module.css';
import Styles from './OverWriteDataModal.module.css';

export const OverWriteDataModal = ({duplicateFileModalOpen, handleoverWriteFIle, handleOverWriteModalClose}) => {
	return (
		<>
			<Modal title={
				<div className={Styles.modalTitleDiv} >
					<div className={Styles.DataImageDiv} >
						<img className={Styles.imgWaringIcon} src={warningIcon}/>
						<div className={Styles.headingData} >
							Data for the selected date already exists in the system. Do you want to replace it ?
						</div>
					</div>
					<div className={Styles.overwrittingHeading} >
						*Overwriting it will result in the loss of corresponding &quot;what if&quot; simulations.
					</div>
				</div>}

			open={duplicateFileModalOpen}
			onOk={handleoverWriteFIle}
			onCancel={handleOverWriteModalClose}
			width={'50%'}
			footer={[<ModalComponents.Footer key='footer-buttons' onClickCancel={handleOverWriteModalClose} onClickSubmit={handleoverWriteFIle} submitText='Yes' />]}
			>
				<div>
				</div>
			</Modal>
		</>
	);
};
