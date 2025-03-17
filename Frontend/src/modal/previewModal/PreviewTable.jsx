import { Modal } from 'antd';
import React, { useState } from 'react';
import { UIComponents } from '../../components/uiComponents';
import { drillDownData } from '../../services/api';
import { DrillDownModal } from '../drillDownModal/DrillDownModal';
import Styles from './PreviewTable.module.css';

export const PreviewTable = ({whatIfAnalysisId, dataPreviewPopup, setDataPreviewPopup, baseFile, previewTableData, whatIfAnalysisType }) => {

	const [selectedSheetNumber, setSelectedSheetNumber] = useState(0);
	const [drillDownPopupOpen, setDrillDownPopupOpen] = useState(false);
	const [drillDownPopupData, setDrillDownPopupData] = useState({});
	const [drillDownString, setDrillDownString] = useState("");
	const previewSheets = ['Included'];

	const handleCancel = () => {
		setDataPreviewPopup(false);
	};

	const handleCellClick = async (rowName, colName) => {
		try {
			const res = await drillDownData(1, baseFile.id, colName, rowName, whatIfAnalysisId);
			setDrillDownPopupData(res.data.response_dict);
			setDrillDownString(colName);
		} catch (err) {
			console.error(err);
		}
		setDrillDownPopupOpen(true);
	};

	const currentSheetData = previewTableData?.[previewSheets[selectedSheetNumber]];

	return (
		<>
			<Modal
				title={<span style={{ color: '#909090', fontWeight: '500', fontSize: '14px', padding: '0 0 0 3%' }}>Data Preview</span>}
				centered
				open={dataPreviewPopup}
				onCancel={handleCancel}
				width={'70%'}
				footer={null}
			>
				<>
					<div className={Styles.messageContainer}>
						* Click on any cell to validate the intermediate calculation.
					</div>
					<div className={Styles.tabsContainer}>
						{previewSheets.map((sheet, index) => (
							<div
								key={index}
								onClick={() => setSelectedSheetNumber(index)}
								className={selectedSheetNumber === index ? Styles.active : Styles.tabs}
							>
								{sheet}
							</div>
						))}
					</div>

					{whatIfAnalysisType === "base_data_file" && (

						<div className={Styles.tableContainer}>
							<table className={Styles.table}>
								<thead>
									<tr className={Styles.headRow}>
										{previewTableData?.columns?.map((col, index) => (

											<th key={index} className={Styles.th}>
												{col.title}
											</th>
										))}
									</tr>
								</thead>
								<tbody>
									{previewTableData?.data?.map((row, rowIndex) => (
										<tr key={rowIndex}>
											{previewTableData?.columns?.map((col) => (
												<td
													key={col.key}
													onClick={() => handleCellClick(row.Company.current_value, col.title)}
													className={`${Styles.td} ${row[col.key]?.changed ? Styles.changedCell : ''}`}
												>
													{row[col.key]?.changed ? (
														<>
															<div className={Styles.currentValue} style={{ backgroundColor: '#CDFFF7' }}>
																{row[col.key]?.current_value}
															</div>
															<div className={Styles.previousValue} style={{ backgroundColor: '#FFE2E5' }}>
																{row[col.key]?.previous_value}
															</div>
														</>
													) : (
														row[col.key]?.current_value
													)}
												</td>
											))}
										</tr>
									))}
								</tbody>
							</table>
						</div>
					)}

					{whatIfAnalysisType === "change_Ebitda" && (
						<div className={Styles.tableContainer}>
							<table className={Styles.table}>
								<thead>
									<tr className={Styles.headRow}>
										{previewTableData?.columns?.map((col, index) => (
											<th key={index} className={Styles.th}>
												{col.title}
											</th>
										))}
									</tr>
								</thead>
								<tbody>
									{previewTableData?.data?.map((row, rowIndex) => (
										<tr key={rowIndex}>
											{previewTableData?.columns?.map((col) => (
												<td
													key={col.key}
													onClick={() => handleCellClick(row.Company.current_value, col.title)}
													className={`${Styles.td} ${row[col.key]?.changed ? Styles.changedCell : ''}`}
												>
													{row[col.key]?.changed ? (
														<>
															<div className={Styles.currentValue} style={{ backgroundColor: '#CDFFF7' }}>
																{row[col.key]?.current_value}
															</div>
															<div className={Styles.previousValue} style={{ backgroundColor: '#FFE2E5' }}>
																{row[col.key]?.previous_value}
															</div>
														</>
													) : (
														row[col.key]?.current_value
													)}
												</td>
											))}
										</tr>
									))}
									{/* {previewTableData?.new_data?.map((row, rowIndex) => (
                  <tr style={{backgroundColor:"red"}} key={rowIndex} className={Styles.newDataRow}>
                    {previewTableData?.columns?.map((col) => (
                      <td  style={{backgroundColor:"rgb(238, 246, 252)"}}
                        key={col.key}
                        className={Styles.td}
                      >
                        {row[col.key]?.current_value}
                      </td>
                    ))}
                  </tr>
                ))} */}
								</tbody>
							</table>
						</div>
					)}

					{whatIfAnalysisType === "add_asset" && (
						<div className={Styles.tableContainer}>
							<table className={Styles.table}>
								<thead>
									<tr className={Styles.headRow}>
										{previewTableData?.columns?.map((col, index) => (
											<th key={index} className={Styles.th}>
												{col.title}
											</th>
										))}
									</tr>
								</thead>
								<tbody>
									{previewTableData?.data?.map((row, rowIndex) => (
										<tr key={rowIndex}>
											{previewTableData?.columns?.map((col) => (
												<td
													key={col.key}
													onClick={() => handleCellClick(row.Company.current_value, col.title)}
													className={`${Styles.td} ${row[col.key]?.changed ? Styles.changedCell : ''}`}
												>
													{isChanged ? (
														<>
															{row[col.key]?.current_value}
															{row[col.key]?.previous_value}
															{colIndex === 0 && (
																<>
																	<UIComponents.Button size='small' text='New' />
																</>
															)}
														</>
													) : (
														row[col.key]?.current_value
													)}
												</td>
											))}
										</tr>
									))}
									{/* {previewTableData?.new_data?.map((row, rowIndex) => (
                  <tr style={{backgroundColor:"red"}} key={rowIndex} className={Styles.newDataRow}>
                    {previewTableData?.columns?.map((col) => (
                      <td  style={{backgroundColor:"rgb(238, 246, 252)"}}
                        key={col.key}
                        className={Styles.td}
                      >
                        {row[col.key]?.current_value}
                      </td>
                    ))}
                  </tr>
                ))} */}
								</tbody>
							</table>
						</div>
					)}


					<DrillDownModal
						baseFile={baseFile}
						drillDownPopupOpen={drillDownPopupOpen}
						setDrillDownPopupOpen={setDrillDownPopupOpen}
						drillDownPopupData={drillDownPopupData}
						setDrillDownPopupData={setDrillDownPopupData}
						drillDownString={drillDownString}
						setDrillDownString={setDrillDownString}
						whatIfAnalysisId={whatIfAnalysisId}
					/>
				</>
			</Modal>
		</>
	);
};