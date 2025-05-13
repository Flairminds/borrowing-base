import { Modal } from 'antd';
import React, { useEffect, useState } from 'react';
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
	const [emptyColumnsList, setEmptyColumnsList] = useState([]);
	const getMissingData = () => {
		if (data && data.length > 0) {
			let emptyColumns = [];
			const cols = Object.keys(data[0]);
			const excludedFields = ['created_at', 'created_by', 'modified_at', 'modified_by', 'is_manually_added', 'base_data_info_id', 'company_id', 'id', 'loanx_id', 'report_date'];
			for (let j = 0; j < cols.length; j++) {
				let colValueEmpty = true;
				for (let i = 0; i < data.length; i++) {
					if (!(!excludedFields.includes(cols[j]) && (!data[i][cols[j]] || !data[i][cols[j]].cellActualValue))) {
						colValueEmpty = false;
						break;
					}
				}
				if (colValueEmpty) {
					emptyColumns.push(columnNames?.find(col => col.key === cols[j]));
				}
			}
			setEmptyColumnsList(emptyColumns);
		}
	};

	useEffect(() => {
		getMissingData();
	}, [data]);

	return (
		<Modal
			title={
				<ModalComponents.Title
					title="Empty Base Data Fields"
					showDescription={true}
					description="The following field values are not provided in the base data. Please review before proceeding."
				/>
			}
			open={visible}
			onCancel={onCancel}
			footer={null}
			width={800}
		>
			<div className={styles.scrollableContent}>
				{emptyColumnsList && emptyColumnsList.length > 0 ?
					<>
						{emptyColumnsList.map((e, i) => {
							return (
								<div key={i}>
									{i + 1}. {e.label} <span style={{color: '#0067e3'}}>{e.bd_column_is_required ? '[Required]' : ''} {e.is_one_time_input ? '[One-time input]' : ''} {e.is_on_going_input_rarely_updated ? '[On-going input]' : ''} {e.is_on_going_input ? '[On-going input]' : ''} {e.description ? `[${e.description}]` : ''}</span>
								</div>
							);
						})}
					</> : <></>}
				{/* {missingDataRows && missingDataRows.length === 0 ? (
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
				)} */}
			</div>

			<div className={styles.buttonContainer}>
				<CustomButton isFilled={false} text="Cancel" onClick={onCancel} />
				<CustomButton isFilled={true} text="Confirm & Proceed" onClick={onConfirm} />
			</div>
		</Modal>
	);
};
