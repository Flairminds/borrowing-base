import { Input, Modal } from 'antd';
import React, { useEffect, useState } from 'react';
import { ModalComponents } from '../../components/modalComponents';
import { CustomButton } from '../../components/uiComponents/Button/CustomButton';
import styles from './VAEModal.module.css';
import { UIComponents } from '../../components/uiComponents';

export const VAEModal = ({ visible, data, columnNames, onConfirm, onCancel }) => {
	const [showAdd, setShowAdd] = useState(false);
	return (
		<Modal
			title={
				<ModalComponents.Title
					title="VAE Data"
					showDescription={true}
					description="The following field values are not provided in the base data. Please review before proceeding."
				/>
			}
			open={visible}
			onCancel={onCancel}
			footer={null}
			width={1200}
		>
			<div className={styles.modalContainer}>
				{showAdd ?
					<>
						<div className={styles.formContainer}>
							<div className={styles.flexDiv}>
								<Input className={styles.formItem} placeholder="Borrower" />
								<Input className={styles.formItem} placeholder="Event Type" />
								<Input className={styles.formItem} placeholder="Material Modification" />
							</div>
							<div className={styles.flexDiv}>
								<Input className={styles.formItem} placeholder="Date of VAE Decision" />
								<Input className={styles.formItem} placeholder="Date of Financials" />
								<Input className={styles.formItem} placeholder="TTM EBITDA" />
							</div>
							<div className={styles.flexDiv}>
								<Input className={styles.formItem} placeholder="Senior Debt" />
								<Input className={styles.formItem} placeholder="Total Debt" />
								<Input className={styles.formItem} placeholder="Unrestricted Cash" />
							</div>
						</div>
					</>
				: <div>
					<div className={styles.flexDiv}>
						<div className={styles.labelDiv} style={{width: '150px'}}>Obligor</div>
						<div>
							<div className={styles.labelDiv}>Event Type</div>
							<div className={styles.labelDiv}>Material Modification</div>
						</div>
						<div>
							<div className={styles.labelDiv}>Date of VAE Decision</div>
							<div className={styles.labelDiv}>Date of Financials</div>
						</div>
						<div>
							<div className={styles.flexDiv}>
								<div className={styles.labelDiv}>TTM EBITDA</div>
								<div className={styles.labelDiv}>Senior Debt</div>
								<div className={styles.labelDiv}>Total Debt</div>
								<div className={styles.labelDiv}>Unrestricted Cash</div>
								<div className={styles.labelDiv}>Net Senior Leverage</div>
								<div className={styles.labelDiv}>Net Total Leverage</div>
							</div>
							<div className={styles.flexDiv}>
								<div className={styles.labelDiv}>Interest Coverage</div>
								<div className={styles.labelDiv}>Recurring Revenue</div>
								<div className={styles.labelDiv}>Debt-to-Recurring Revenue Ratio</div>
								<div className={styles.labelDiv}>Liquidity</div>
								<div className={styles.labelDiv}>Assigned Value</div>
							</div>
						</div>
					</div>
					<div className={styles.flexDiv} style={{backgroundColor: '#ffc193', borderRadius: '3px'}}>
						<div className={styles.labelDiv} style={{width: '150px'}}>Schlesinger Global, Inc.</div>
						<div style={{width: '150px'}}>
							<div className={styles.labelDiv}>Initial Assigned Value at Closing</div>
							<div className={styles.labelDiv}>-</div>
						</div>
						<div>
							<div className={styles.labelDiv}>Date of VAE Decision</div>
							<div className={styles.labelDiv}>Date of Financials</div>
						</div>
						<div>
							<div className={styles.flexDiv}>
								<div className={styles.labelDiv}>TTM EBITDA</div>
								<div className={styles.labelDiv}>Senior Debt</div>
								<div className={styles.labelDiv}>Total Debt</div>
								<div className={styles.labelDiv}>Unrestricted Cash</div>
								<div className={styles.labelDiv}>Net Senior Leverage</div>
								<div className={styles.labelDiv}>Net Total Leverage</div>
							</div>
							<div className={styles.flexDiv}>
								<div className={styles.labelDiv}>Interest Coverage</div>
								<div className={styles.labelDiv}>Recurring Revenue</div>
								<div className={styles.labelDiv}>Debt-to-Recurring Revenue Ratio</div>
								<div className={styles.labelDiv}>Liquidity</div>
								<div className={styles.labelDiv}>Assigned Value</div>
							</div>
						</div>
					</div>
				</div>}
			</div>

			<div className={styles.buttonContainer}>
				<CustomButton isFilled={true} text={showAdd ? "Save" : "+ Add"} onClick={() => showAdd ? setShowAdd(false) : setShowAdd(true)} />
			</div>
		</Modal>
	);
};
