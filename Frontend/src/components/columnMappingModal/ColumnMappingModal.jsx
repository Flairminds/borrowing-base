import { Modal, Select } from 'antd';
import React, { useState, useEffect } from 'react';
import {saveMappedColumns } from '../../services/dataIngestionApi';
import { ModalComponents } from '../modalComponents';
import { CustomButton } from '../uiComponents/Button/CustomButton';
import styles from "./ColumnMappingModal.module.css";

const { Option } = Select;

export const ColumnMappingModal = ({
	visible,
	onClose,
	excelUnmappedColumns = [],
	systemUnmappedColumns = [],
	handleSave

}) => {
	const [mappings, setMappings] = useState({});

	useEffect(() => {
		setMappings({});
	}, [excelUnmappedColumns, systemUnmappedColumns]);

	const handleMappingChange = (excelCol, selectedSystemCol) => {
		setMappings((prev) => ({ ...prev, [excelCol]: selectedSystemCol }));
	};

	const saveExcelColumns = async () => {
		const allMapped = excelUnmappedColumns.every((col) => mappings[col]);
		// if (!allMapped) {
		// 	message.warning('Please map all columns before submitting.');
		// 	return;
		// }

		const mapped_columns = Object.entries(mappings).map(([excelCol, systemColId]) => {
			const systemCol = systemUnmappedColumns.find((col) => col.id === systemColId);
			return {
				id: systemCol.id,
				column_name: excelCol,
			};
		});


		const payload = {
			mapped_columns
		};

		try {
			await saveMappedColumns(payload);
			onClose();
			handleSave();
		} catch (error) {
			console.error('Failed to save mappings:', error);
			// message.error('Submission failed.');
		}
	};


	return (
		<Modal
			title={
				<ModalComponents.Title
					title="Unmapped Excel Columns"
					showDescription={true}
					description="Some of the columns from the uploaded Excel file are not yet mapped. Please map them to the appropriate system columns before continuing."
				/>
			}
			open={visible}
			onCancel={onClose}
			footer={null}
			width={700}
		>
			<div className={styles.tableWrapper}>
				<table className={styles.mappingTable}>
					<thead>
						<tr>
							<th>Excel Column</th>
							<th>System Column</th>
						</tr>
					</thead>
					<tbody>
						{excelUnmappedColumns.map((excelCol, index) => (
							<tr key={index}>
								<td className={styles.excelColCell}>{excelCol}</td>
								<td>
									<Select
										style={{ minWidth: '100%' }}
										placeholder="Select system column"
										onChange={(val) => handleMappingChange(excelCol, val)}
										value={mappings[excelCol]}
									>
										{systemUnmappedColumns.map((sysCol) => (
											<Option
												key={sysCol.id}
												value={sysCol.id}
												disabled={Object.values(mappings).includes(sysCol.id)}
											>
												{sysCol.column_name}
											</Option>
										))}
									</Select>
								</td>
							</tr>
						))}
					</tbody>
				</table>
			</div>

			<div className={styles.buttonContainer}>
				<CustomButton isFilled={false} text="Cancel" onClick={onClose} />
				<CustomButton isFilled={true} text="Save" onClick={saveExcelColumns} />
			</div>
		</Modal>
	);
};
