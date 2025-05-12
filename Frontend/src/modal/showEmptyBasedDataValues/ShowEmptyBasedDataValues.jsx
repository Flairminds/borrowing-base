import { Modal } from 'antd';
import React from 'react';
import { ModalComponents } from '../../components/modalComponents';
import { CustomButton } from '../../components/uiComponents/Button/CustomButton';
import styles from './ShowEmptyBasedDataValues.module.css';

// export const ShowEmptyBasedDataValues = ({ visible, data, columnNames, onConfirm, onCancel, previewFundType }) => {
// 	const getMissingData = () => {
// 		const excludedFields = ['created_by', 'modified_at', 'modified_by', 'is_manually_added'];
// 		const rows = data || [];

// 		return rows
// 			.map((row) => {
// 				const nameKey = previewFundType === 'PFLT' ? 'obligor_name' : 'issuer';
// 				const obligorName = row[nameKey]?.display_value || "Unknown";
// 				const missingFields = [];

// 				Object.entries(row).forEach(([key, value]) => {
// 					if (
// 						value &&
// 						typeof value === "object" &&
// 						!excludedFields.includes(key)
// 					) {
// 						const isValueEmpty =
// 							value.value === null ||
// 							value.value === "" ||
// 							value.value === undefined;

// 						if (isValueEmpty && !excludedFields.includes(key)) {
// 							const labelObj = columnNames?.find(col => col.key === key);
// 							if (!labelObj) return;
// 							const label = labelObj.label;
// 							missingFields.push(label);
// 						}

// 					}
// 				});

// 				return {
// 					obligorName,
// 					missingFields
// 				};
// 			})
// 			.filter((entry) => entry.missingFields.length > 0);
// 	};

// 	const missingDataRows = getMissingData();

// 	return (
// 		<Modal
// 			title={
// 				<ModalComponents.Title
// 					title="Empty Base Data Fields"
// 					showDescription={true}
// 					description="The following fields are missing in the base data. Please review before proceeding."
// 				/>
// 			}
// 			open={visible}
// 			onCancel={onCancel}
// 			footer={null}
// 			width={800}
// 			bodyStyle={{ padding: 0 }}
// 		>
// 			<div className={styles.scrollableContent}>
// 				{missingDataRows.length === 0 ? (
// 					<p className={styles.noMissingDataText}>
// 						All fields are filled. No missing data.
// 					</p>
// 				) : (
// 					missingDataRows.map((row, index) => (
// 						<div key={index} className={styles.missingDataCard}>
// 							<p className={styles.obligorTitle}>{previewFundType === 'PFLT' ? 'Obligor Name' : 'Issuer'}: {row.obligorName}</p>
// 							<ul className={styles.missingFieldsList}>
// 								{row.missingFields.map((field, i) => (
// 									<li key={i} className={styles.missingFieldItem}>{field}</li>
// 								))}
// 							</ul>
// 						</div>
// 					))
// 				)}
// 			</div>

// 			<div className={styles.buttonContainer}>
// 				<CustomButton isFilled={false} text="Cancel" onClick={onCancel} />
// 				<CustomButton isFilled={true} text="Confirm & Proceed" onClick={onConfirm} />
// 			</div>
// 		</Modal>
// 	);
// };


export const ShowEmptyBasedDataValues = ({ visible, data, columnNames, onConfirm, onCancel, previewFundType }) => {
	const getMissingData = () => {
		if (data && data.length > 0) {
			let cols = Object.keys(data[0]);
			for (let i = 0; i < data.length; i++) {
				console.log(data[i]);
				const excludedFields = ['created_at', 'created_by', 'modified_at', 'modified_by', 'is_manually_added', 'base_data_info_id', 'company_id', 'id', 'loanx_id', 'report_date'];
				for (let j = 0; j < cols.length; j++) {
					if (!excludedFields.includes(cols[j]) && (!data[i][cols[j]] || !data[i][cols[j]].cellActualValue)) {
						console.log(data[i][cols[j]].cellActualValue, cols[j]);
					}
				}
			}
		}
	};

	const missingDataRows = getMissingData();

	return (
		<Modal
			title={
				<ModalComponents.Title
					title="Empty Base Data Fields"
					showDescription={true}
					description="The following fields are missing in the base data. Please review before proceeding."
				/>
			}
			open={visible}
			onCancel={onCancel}
			footer={null}
			width={800}
			bodyStyle={{ padding: 0 }}
		>
			<div className={styles.scrollableContent}>
				{missingDataRows && missingDataRows.length === 0 ? (
					<p className={styles.noMissingDataText}>
						All fields are filled. No missing data.
					</p>
				) : (
					missingDataRows && missingDataRows.map((row, index) => (
						<div key={index} className={styles.missingDataCard}>
							<p className={styles.obligorTitle}>{previewFundType === 'PFLT' ? 'Obligor Name' : 'Issuer'}: {row.obligorName}</p>
							<ul className={styles.missingFieldsList}>
								{row.missingFields.map((field, i) => (
									<li key={i} className={styles.missingFieldItem}>{field}</li>
								))}
							</ul>
						</div>
					))
				)}
			</div>

			<div className={styles.buttonContainer}>
				<CustomButton isFilled={false} text="Cancel" onClick={onCancel} />
				<CustomButton isFilled={true} text="Confirm & Proceed" onClick={onConfirm} />
			</div>
		</Modal>
	);
};
