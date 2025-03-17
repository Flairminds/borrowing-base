import { Modal, Button } from 'antd';
import React, { useState } from 'react';
import Styles from "./WiaSimulationInfo.module.css";

export const WiaSimulationInfo = ({ selectedWIA, wiaSimulationModal, isWiaSimulationModal, simulationType }) => {

	const [selectedSheetNumber, setSelectedSheetNumber] = useState(0);

	// const previewSheets = ["PL BB Build"]
	const previewSheets = Object.keys(selectedWIA);


	const handleOk = () => {
		isWiaSimulationModal(true);
	};

	const handleCancel = () => {
		isWiaSimulationModal(false);
	};

	return (
		<Modal
			title={<span style={{ color: '#909090', fontWeight: '500', fontSize: '14px', padding: '0 0 0 3%' }}>{simulationType}</span>}
			centered
			open={wiaSimulationModal}
			onOk={handleOk}
			onCancel={handleCancel}
			width={'80%'}
			footer={[]}
		>
			<div>
				<div className={Styles.tabsContainer}>
					{previewSheets.map((sheet, index) => (
						<div onClick={() => setSelectedSheetNumber(index)} className={selectedSheetNumber == index ? Styles.active : Styles.tabs}>
							{sheet}
						</div>
					))}
				</div>
			</div>
			<div className={Styles.tableContainer}>
				<div className={Styles.scrollWrapper}>
					<table className={Styles.table}>
						<thead>
							<tr className={Styles.headRow}>
								{selectedWIA[previewSheets[selectedSheetNumber]]?.columns?.map((col, index) => (
									<th key={index} className={`${Styles.th} ${index === 0 ? Styles.firstColumn : ''}`}>
										{col.title}
									</th>
								))}
							</tr>
						</thead>
						<tbody>
							{selectedWIA[previewSheets[selectedSheetNumber]]?.data
								?.sort((a, b) => {
									// Sort based on 'changed' property: true values at the top
									const aChanged = selectedWIA[previewSheets[selectedSheetNumber]]?.columns?.some(col => a[col.key]?.changed);
									const bChanged = selectedWIA[previewSheets[selectedSheetNumber]]?.columns?.some(col => b[col.key]?.changed);
									return bChanged - aChanged; // bChanged comes before aChanged if true
								})
								.map((row, rowIndex) => (
									<tr key={rowIndex}>
										{selectedWIA[previewSheets[selectedSheetNumber]]?.columns?.map((col, colIndex) => (
											<>
												{
													selectedWIA[previewSheets[selectedSheetNumber]]?.new_data.includes(row.Investment_Name?.current_value) ? (
														<td key={colIndex} className={Styles.addedRow}>
															{col.key == "Investment_Name" ?
																<>
																	{row[col.key]?.current_value}
																	<span className={Styles.newTag}>New</span>
																</>
																:
																row[col.key]?.current_value }
														</td>

													)
														: row[col.key]?.changed ? (
															<td key={colIndex} className={Styles.td}>
																<div className={Styles.currentValue}>
																	{row[col.key]?.current_value}
																</div>
																<div className={Styles.previousValue}>
																	{row[col.key]?.previous_value}
																</div>
															</td>
														) : (
															<td key={colIndex} className={Styles.td}>
																{row[col.key]?.current_value}
															</td>
														)}
											</>
										))}
									</tr>

								))}
						</tbody>
					</table>

				</div>
			</div>

		</Modal>
	);
};
