import { Button, Modal } from 'antd';
import React from 'react';
import warningIcon from '../../assets/uploadFIle/warning.svg';
import ButtonStyles from '../../components/Buttons/ButtonStyle.module.css';
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
			footer={[
				<div key="footer-buttons" className="px-4">
					<button key="back" onClick={handleOverWriteModalClose} className={ButtonStyles.outlinedBtn}>
						No
					</button>
					<Button className={ButtonStyles.filledBtn}
						key="submit" type="primary" style={{ backgroundColor: '#0EB198' }}
						onClick={handleoverWriteFIle}
					>
						Yes
					</Button>
				</div>
			]}
			>
				<div>
				</div>
			</Modal>
		</>
	);
};
