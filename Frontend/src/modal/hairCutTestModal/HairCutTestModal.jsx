import { Button, Modal, Switch } from 'antd';
import { useEffect, useRef, useState } from 'preact/hooks';
import React from 'react';
import CrossIcon from '../../assets/CrossIcon.svg';
import RightIcon from '../../assets/RightIcon.svg';
import ButtonStyles from '../../components/uiComponents/Button/ButtonStyle.module.css';
import { getConenctrationAnalysis } from '../../services/api';
import { getLatestEntryOfModification } from '../../utils/helperFunctions/hairCutModifications';
import Styles from './HairCutTestModal.module.css';
import { ModalComponents } from '../../components/modalComponents';

export const HairCutTestModal = (
	{ isHairCutTestModalOpen,
		setIsHairCutTestModalOpen,
		hairCutTestData,
		setHairCutTestData,
		baseFile,
		setConcentrationTestTableData,
		setConentrationTestModalOpen,
		setHairCutArray,
		concentrationTestTableData}) => {

	const [hairCutInputText, setHairCutInputText] = useState();
	const [editableRowIndex, setEditableRowIndex] = useState(-2);
	const [loading, setLoading] = useState(false);
	const [appliedChanges, setAppliedChanges] = useState([]);
	const [showModification, setShowModification] = useState();
	const [initialValues, setInitialValues] = useState({});

	const inputRef = useRef(null);
	const handleCancel = () => {

		setIsHairCutTestModalOpen(false);
	};
	const handleHairCutInputChange = (value, index) => {
		setHairCutInputText(value);
	};

	const handleHairCutBox = (index, colName, colValue) => {
		if (colName == 'Haircut_number') {
			setHairCutInputText('');
			setEditableRowIndex(index);
			setTimeout(() => {
				inputRef?.current?.focus();
			}, 100);
		}
	};

	// Updated percentage change calculation to handle 0 initial value correctly
	const handleChangeSubmit = (e, rowIndex, currValue) => {
		e.stopPropagation();

		const updatedNumber = parseInt(hairCutInputText); // New haircut value
		const prevNumber = parseInt(currValue);// Current haircut value

		// Initialize initial values if not present
		if (initialValues[rowIndex] === undefined) {
			initialValues[rowIndex] = prevNumber;
		}

		const initialValue = initialValues[rowIndex];// Fetch the initial value for the row

		// *** Updated the percentage change formula to avoid division by zero ***
		const percentageChange = ((updatedNumber - initialValue) / Math.abs(initialValue || 1)) * 1;

		// Track the changes being made
		const currentChanges = {
			rowIndex: rowIndex,
			prev_val: initialValue,
			updated_val: parseInt(hairCutInputText),
			percentageChange: percentageChange
		};

		// Update the applied changes with the current change
		setAppliedChanges([...appliedChanges, currentChanges]);

		// Update the table data with the new haircut number
		setHairCutTestData(hairCutDisplayData => {
			const newData = [...hairCutDisplayData.data];
			newData[rowIndex] = {
				...newData[rowIndex],
				Haircut_number: parseInt(hairCutInputText) // Update the specific row
			};
			return { ...hairCutDisplayData, data: newData };
		});

		setEditableRowIndex(-1); // Close the editable row after submission
		setHairCutInputText(''); // Clear the input field after submission
	};


	const handleReview = async() => {
		setLoading(true);
		const updatedColumnArray = hairCutTestData.data
			.map((item) => {
				if (item.hasOwnProperty("Updated_Haircut_number")) {
					return {[item.Investment_Name]: item.Updated_Haircut_number};
				} else {
					return {[item.Investment_Name]: item.Haircut_number};
				}
			});

		const hairCutpayloadArray = updatedColumnArray.map(el => Object.values(el)[0]);

		setHairCutArray(updatedColumnArray);
		try {
			const res = await getConenctrationAnalysis(baseFile.id, hairCutpayloadArray, concentrationTestTableData?.Actual, concentrationTestTableData?.Result);
			// var stringRes = JSON.parse(res.data.replace(/\bNaN\b/g, "null"));
			setConcentrationTestTableData(res.data);
			setConentrationTestModalOpen(true);
			setIsHairCutTestModalOpen(false);
			setHairCutTestData({
				data: [],
				columns: []
			});

		} catch (err) {
			console.error(err);
		}
		setLoading(false);
	};

	const handleShowModificationChange = (checked) => {
		setShowModification(checked);
	};

	return (
		<>
			<Modal
				title={<span style={{fontWeight: '500', fontSize: '16px', padding: '0 0 0 3%' }}>Concentration Test</span>}
				centered
				open={isHairCutTestModalOpen}
				// onOk={handleOk}
				onCancel={handleCancel}
				width={'80%'}
				footer={[<ModalComponents.Footer key='footer-buttons' onClickCancel={handleCancel} onClickSubmit={handleReview} loading={loading} submitText='Review' />]}
			>
				<>
					<div className={Styles.modificationSwitchContainer}>
						<Switch
							className={Styles.modificationSwitch}
							size="small"
							onChange={handleShowModificationChange}
							style={{backgroundColor: showModification ? "#1EBEA5" : null }}
						/>
						Show rows with modifications
					</div>
					<div className={Styles.tableContainer}>
						<table className={Styles.table}>
							<thead>
								<tr className={Styles.headRow}>
									{hairCutTestData && hairCutTestData?.columns?.map((col, index) => (
										<th key={index} className={Styles.th}>
											{col.title}
										</th>
									))}
								</tr>
							</thead>
							<tbody>
								{hairCutTestData && hairCutTestData?.data?.map((row, rowIndex) => (
									<tr key={rowIndex}>
										{hairCutTestData && hairCutTestData?.columns.map((col) => (
											<td key={col} className={col.key == 'Haircut_number' ? `${Styles.hairCutDiv} ${Styles.td}` : `${Styles.td }`} onClick={() => handleHairCutBox(rowIndex, col.key, row[col.key])}>
												{col.key == 'Haircut_number' && editableRowIndex == rowIndex ?
													<div style={{display: 'flex'}}>
														<input
															ref={inputRef}
															className={Styles.hairCutInput}
															// onBlur={() =>setEditableRowIndex(-1)}
															type="text"
															value={hairCutInputText}
															onChange={(e) => handleHairCutInputChange(e.target.value, rowIndex)}
														/>
														<img style={{zIndex: 200}} src={RightIcon} alt="Right Icon" onClick={(e) => handleChangeSubmit(e, rowIndex, row[col.key])} />
														<img src={CrossIcon} alt="Cross Icon" onClick={() => setEditableRowIndex(-1)} />
													</div>
													:
													col.key == 'Haircut_number' && getLatestEntryOfModification(appliedChanges, rowIndex) && showModification ?
														<>
															<div className={Styles.updatedValue}>
																{row[col.key]}
															</div>
															<div className={Styles.prevValue}>
																{getLatestEntryOfModification(appliedChanges, rowIndex)}
															</div>
														</>
														:
														<>
															{row[col.key]}
														</>
												}
											</td>
										))}
									</tr>
								))}
							</tbody>
						</table>
					</div>
				</>

			</Modal>
		</>
	);
};