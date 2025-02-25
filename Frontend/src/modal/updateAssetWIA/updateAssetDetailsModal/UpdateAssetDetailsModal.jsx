import { Button, Modal, Popover, Tooltip,Switch } from 'antd';
import { useEffect, useRef, useState } from 'preact/hooks';
import React from 'react'
import AddIcon from '../../../assets/AddIcon.svg';
import CrossIcon from '../../../assets/CrossIcon.svg';
import DeleteIcon from '../../../assets/DeleteIcon.svg';
import RightIcon from '../../../assets/RightIcon.svg';
import DuplicateAssetIcon from '../../../assets/updateAssetIcons/DuplicateAssetIcon.svg'
import MoreOptionsIcon from '../../../assets/updateAssetIcons/MoreOptionsIcon.svg'
import ButtonStyles from '../../../components/Buttons/ButtonStyle.module.css';
import { getUpdateAssetData, updateModifiedAssets, updateSheetValues } from '../../../services/api';
import { updateAssetDefaultColumnsData, updateAssetModalData } from '../../../utils/constants/constants';
import { addAssetAtIndex, deleteAssetAtIndex, duplicateAsset, getLatestPrevValue, updateDataAfterChange } from '../../../utils/helperFunctions/updateAssetDataChange';
import { AddAssetDetailsModal } from '../addAssetDetailsModal/AddAssetDetailsModal';
import Styles from './UpdateAssetDetailsModal.module.css';
import {MoreOutlined} from '@ant-design/icons';
import { CustomButton } from '../../../components/custombutton/CustomButton';
import { ImportAssetFIleModal } from '../importAssetFIleModal/ImportAssetFIleModal';

export const UpdateAssetDetailsModal = ({
	isupdateAssetModalOpen,
	setIsupdateAssetModalOpen,
	updateAssetTableData,
	setUpdateAssetTableData,
	selectedCellData,
	setSelectedCellData,
	setSelectedOption,
	baseFile,
	whatIfAnalysisId,
	setWhatIfAnalysisId,
	setTablesData,
	setWhatifAnalysisPerformed,
	setSaveBtn,
	fundType,
	setWhatIfAnalysisType
}) => {


	const [selectedSheetNumber, setSelectedSheetNumber] = useState();
	const [updateAssetInputText, setUpdateAssetInputText ] = useState('');
	const [appliedChanges, setAppliedChanges] = useState([]);
	const [enteredInputData, setEnteredInputData] = useState('');
	const [addedDeletedAssets, setAaddedDeletedAssets] = useState({
		addedAssets: [],
		deletedAssets: []
	});
	const [addDeleteAssetData, setAddDeleteAssetData] = useState({
		index: -1,
		type: ''
	});
	const [loading, setLoading] = useState(false);
	const [addAssetDetailsModalOpen, setAddAssetDetailsModalOpen] = useState(false);
	const [showModification, setShowModification] = useState(false);
	const [isButtonDisabled, setIsButtonDisabled] = useState(true);
	const [importFilePopup, setImportFilePopup ] = useState(false);

	useEffect(() => {
		if (fundType) {
			setSelectedSheetNumber(updateAssetModalData(fundType));
		}
	}, [fundType]);

	useEffect(() => {
	}, [updateAssetTableData]);

	const previewSheets = updateAssetTableData?.table_data?.sheets;

	const handleCancel = () => {
		setIsupdateAssetModalOpen(false);
		setIsButtonDisabled(true);
		setSelectedOption(0);
		setAppliedChanges([]);
		setLoading(false);
		setSelectedSheetNumber(updateAssetModalData(fundType))
	};

	const handleInputFocus = (investment_name, colName) => {
		setSelectedCellData({investment_name : investment_name,colName:colName});
		setUpdateAssetInputText('');
	};

	const handleCellInputChange = (e) => {
		setUpdateAssetInputText(e.target.value);
	};

	const handleCommitChange = (e, investment_name, colKey, colName, currValue) => {
		setIsButtonDisabled(false);
		e.stopPropagation();
		updateDataAfterChange(updateAssetTableData, investment_name, colKey, selectedSheetNumber, updateAssetInputText);
		const currentChanges = {
			row_name: investment_name,
			column_name: colName,
			updated_value: updateAssetInputText,
			prev_value:currValue
		};
		setAppliedChanges([...appliedChanges, currentChanges]);
		setSelectedCellData({
			investment_name : '',
			colName: ''
		});
		setUpdateAssetInputText('');
	};

	const handleCancelChange = () => {
		setUpdateAssetInputText('');
		setSelectedCellData({
			investment_name : '',
			colName: ''
		});
	};

	const handleSheetChange = async(sheetName) => {

		let totalChangesOnSheet = {
			updated_assets:[],
			rows_to_add:[],
			rows_to_delete:[]
		};
		if (updateAssetTableData?.changes) {
			totalChangesOnSheet.updated_assets = [...updateAssetTableData?.changes, ...appliedChanges];
		} else {
			totalChangesOnSheet.updated_assets = [...appliedChanges];
		}

		if (addedDeletedAssets.addedAssets.length > 0) {
			totalChangesOnSheet.rows_to_add = addedDeletedAssets.addedAssets;
		}

		if (addedDeletedAssets?.deletedAssets?.length > 0) {
			totalChangesOnSheet.rows_to_delete = addedDeletedAssets?.deletedAssets;
		}

		try {
			if (appliedChanges.length > 0 || addedDeletedAssets?.addedAssets?.length > 0 || addedDeletedAssets?.deletedAssets?.length > 0 ) {
				const res = await updateSheetValues(baseFile.id, selectedSheetNumber, totalChangesOnSheet, whatIfAnalysisId);
				setWhatIfAnalysisId(res.data.result.modified_base_data_file_id);
			}
		} catch (err) {
			console.error(err);

		}

		setAaddedDeletedAssets({
			addedAssets: [],
			deletedAssets: []
		});
		totalChangesOnSheet = {
			updated_assets:[],
			rows_to_add:[]
		};

		try {
			const res = await getUpdateAssetData(baseFile.id, sheetName, whatIfAnalysisId);
			setUpdateAssetTableData(res.data.result);
			setAppliedChanges([]);
			setUpdateAssetInputText('');
			setSelectedSheetNumber(sheetName);
		} catch (err) {
			console.error(err);
		}

	};

	const updateAssetApply = async() => {

		console.log(updateAssetTableData);
		setLoading(true);
		let currentAnalysisId = undefined;
		let totalChangesOnSheet = {
			updated_assets:{}
		};

		if (updateAssetTableData?.changes) {
			totalChangesOnSheet.updated_assets = [...updateAssetTableData?.changes , ...appliedChanges];
		} else {
			totalChangesOnSheet.updated_assets = [...appliedChanges];
		}

		if (addedDeletedAssets.addedAssets.length > 0) {
			totalChangesOnSheet.rows_to_add = addedDeletedAssets.addedAssets;
		}

		if (addedDeletedAssets?.deletedAssets?.length > 0) {
			totalChangesOnSheet.rows_to_delete = addedDeletedAssets?.deletedAssets;
		}

		console.info(totalChangesOnSheet, 'test-81--');
		try {
			if (appliedChanges.length > 0 || addedDeletedAssets?.addedAssets?.length > 0 || addedDeletedAssets?.deletedAssets?.length > 0) {
				const res = await updateSheetValues(baseFile.id, selectedSheetNumber, totalChangesOnSheet, whatIfAnalysisId);
				setWhatIfAnalysisId(res.data.result.modified_base_data_file_id);
				currentAnalysisId = res.data.result.modified_base_data_file_id;
			}
		} catch (err) {
			console.error(err);
		}
		if (!currentAnalysisId) {
			currentAnalysisId = whatIfAnalysisId;
		}


		try {
			const res = await updateModifiedAssets(currentAnalysisId);
			setWhatifAnalysisPerformed(true);
			setSaveBtn(true);
			setTablesData(res.data.result);
			handleCancel();
			setWhatIfAnalysisType(res.data.result.what_if_analysis_type);
		} catch (err) {
			console.error(err);
		}
		setLoading(false);

	};

	const updateAddDeleteData = (rowIndex, operationType) => {
		setAddDeleteAssetData({
			index: rowIndex,
			type: operationType
		});
		setAddAssetDetailsModalOpen(true);
	};

	const handleAddDeleteAssets = () => {
		let effectiveIndex;
		if (addDeleteAssetData.type == 'addAbove') effectiveIndex = addDeleteAssetData.index;
		else if (addDeleteAssetData.type == 'addBelow') effectiveIndex = addDeleteAssetData.index + 1;
		else if (addDeleteAssetData.type == 'duplicate') effectiveIndex = addDeleteAssetData.index + 1;
		else effectiveIndex = addDeleteAssetData.index;

		if (addDeleteAssetData.type == 'duplicate') {
			const resultData = duplicateAsset(updateAssetTableData, effectiveIndex, enteredInputData, updateAssetDefaultColumnsData[selectedSheetNumber], selectedSheetNumber);
			setAppliedChanges([...appliedChanges, ...resultData.duplicatechangesArray]);
			setAaddedDeletedAssets({
				...addedDeletedAssets,
				addedAssets: [...addedDeletedAssets.addedAssets, {row_identifier:enteredInputData, row_index:effectiveIndex}]
			});
			setUpdateAssetTableData(resultData.updatedTableData);
			setEnteredInputData('');
			setAddAssetDetailsModalOpen(false);
		} else if (addDeleteAssetData.type != 'delete') {
			const resultData = addAssetAtIndex(updateAssetTableData, effectiveIndex, enteredInputData, updateAssetDefaultColumnsData[selectedSheetNumber], selectedSheetNumber);
			setUpdateAssetTableData(resultData);
			setAaddedDeletedAssets({
				...addedDeletedAssets,
				addedAssets: [...addedDeletedAssets.addedAssets, {row_identifier:enteredInputData, row_index:effectiveIndex}]
			});
			setEnteredInputData('');
			setAddAssetDetailsModalOpen(false);
		} else {
			const resultData = deleteAssetAtIndex(updateAssetTableData, effectiveIndex, updateAssetDefaultColumnsData[selectedSheetNumber], selectedSheetNumber);
			setUpdateAssetTableData(resultData.updatedData);
			setAaddedDeletedAssets({
				...addedDeletedAssets,
				deletedAssets: [...addedDeletedAssets.deletedAssets, {row_identifier:resultData.rowName}]
			});
			setAddAssetDetailsModalOpen(false);
		}
		setIsButtonDisabled(false);
	};

	const MoreOptionContent = ({rowIndex}) => (
		<div className={Styles.optionsContainer}>
			<div onClick={() => updateAddDeleteData(rowIndex, 'addAbove') } className={Styles.option}>
				<img className={Styles.optionIcon} src={AddIcon} alt="Add Icon" />
				Insert 1 row above
			</div>
			<div onClick={() => updateAddDeleteData(rowIndex, 'addBelow')} className={Styles.option}>
				<img className={Styles.optionIcon} src={AddIcon} alt="Add Icon" />
				Insert 1 row below
			</div>
			<div onClick={() => updateAddDeleteData(rowIndex, 'delete')} className={`${Styles.option} ${Styles.redText}`}>
				<img className={Styles.optionIcon} src={DeleteIcon} alt="Delete Icon" />
				Delete
			</div>
		</div>
	);

	const handleShowModificationChange = (checked) => {
		setShowModification(checked);
	};

	return (
		<>
			<Modal
				title={<span style={{ color: '#909090', fontWeight: '500', fontSize: '14px', padding: '0 0 0 3%' }}>Update Asset Details</span>}
				centered
				open={isupdateAssetModalOpen}
				onCancel={handleCancel}
				width={'98%'}
				footer={<>
					<div key="footer-buttons" className="px-4">
						<button key="back" onClick={handleCancel} className={ButtonStyles.outlinedBtn}>
							Cancel
						</button>
						<Button className={isButtonDisabled ? ButtonStyles.DisbaledBtn : ButtonStyles.filledBtn} loading={loading} key="submit" type="primary" style={{ backgroundColor: '#0EB198' }} onClick={updateAssetApply} disabled={isButtonDisabled} >
							Apply
						</Button>
					</div>
				</>}
			>
				<>
					<div>
						{/* <div className={Styles.WIAnameInput}>Borrowing base may 24th-Copy</div> */}
						<div className={Styles.WIAInformation}>
							Here, you have the ability to update the details of each and every asset with any value you choose and perform comprehensive 'what-if analysis' to evaluate various scenarios and potential outcomes based on those changes.
						</div>
						<div className={Styles.modificationSwitchContainer}>
							<Switch
								className={Styles.modificationSwitch}
								size="small"
								onChange={handleShowModificationChange}
								style={{backgroundColor: showModification ? "#1EBEA5" : null }}
							/>
							Show rows with modifications
						</div>

					</div>

					<div className={Styles.wiaoptionsContainer}>
						<div className={Styles.tabsContainer}>
							{previewSheets?.map((sheet, index) => (
								<div key={index} onClick={() => handleSheetChange(sheet)} className={selectedSheetNumber == sheet ? Styles.active : Styles.tabs}>
									{sheet}
								</div>
							))}
						</div>
						<div className={Styles.fileOptionButtons}>
							<CustomButton text="Import" isFilled={true} onClick={() => setImportFilePopup(true)} />
							<CustomButton text="Export" isFilled={true} />
						</div>
					</div>
					<div className={Styles.tableContainer}>
						<table className={Styles.table}>
							<thead>
								<tr className={Styles.headRow}>
									{updateAssetTableData && updateAssetTableData?.table_data[selectedSheetNumber]?.columns.map((col, index) => (
										<th key={index} className={Styles.th}>
											{col.label}
										</th>
									))}
									<th className={Styles.th}></th>
								</tr>
							</thead>
							<tbody>
								{updateAssetTableData && updateAssetTableData?.table_data[selectedSheetNumber]?.data.map((row, rowIndex) => (
									<tr key={rowIndex}>
										{updateAssetTableData && updateAssetTableData?.table_data[selectedSheetNumber]?.columns.map((col) => (

											<td
												key={col}
												className={Styles.td}
											>

												<div className={Styles.inputCellDiv}>
													<input
														className={showModification && getLatestPrevValue(updateAssetTableData?.changes, appliedChanges, row[updateAssetDefaultColumnsData[selectedSheetNumber]], col.label) ? Styles.currValueInput : Styles.assetUpdateInput}
														onFocus={() => handleInputFocus(row[updateAssetDefaultColumnsData[selectedSheetNumber]], col.label)}
														type="text"
														value={selectedCellData.investment_name == row[updateAssetDefaultColumnsData[selectedSheetNumber]] && selectedCellData.colName == col.label ? updateAssetInputText : row[col.key]}
														onChange={(e) => handleCellInputChange(e)}
													/>
													{selectedCellData.investment_name == row[updateAssetDefaultColumnsData[selectedSheetNumber]] && selectedCellData.colName == col.label &&
													<>
														<img
															style={{zIndex: 200}} src={RightIcon} alt="Right Icon"
															onClick={(e) => handleCommitChange(e,row[updateAssetDefaultColumnsData[selectedSheetNumber]], col.key, col.label, row[col.key])}
														/>
														<img
															src={CrossIcon} alt="Cross Icon" 
															onClick={() => handleCancelChange()}
														/>
													</>
													}
												</div>
												{showModification && getLatestPrevValue(updateAssetTableData?.changes, appliedChanges, row[updateAssetDefaultColumnsData[selectedSheetNumber]], col.label) &&
												<div className={`${Styles.inputCellDiv} ${Styles.prevValueText}`}>
													{getLatestPrevValue(updateAssetTableData?.changes, appliedChanges, row[updateAssetDefaultColumnsData[selectedSheetNumber]], col.label)}
												</div>
												}


											</td>
										))}
										<td className={Styles.td}>
											<img onClick={() => updateAddDeleteData(rowIndex, 'duplicate')} src={DuplicateAssetIcon} alt="Duplicate Asset Icon" className={Styles.editAssetOptionImage} />

											<Popover placement="bottomLeft" content={<MoreOptionContent rowIndex={rowIndex} />}>
												<img src={MoreOptionsIcon} alt="More Options Icon" className={Styles.editAssetOptionImage} />
											</Popover>
										</td>
									</tr>
								))}
							</tbody>
						</table>
					</div>

				</>

			</Modal>

			<AddAssetDetailsModal
				addAssetDetailsModalOpen={addAssetDetailsModalOpen}
				setAddAssetDetailsModalOpen={setAddAssetDetailsModalOpen}
				addDeleteAssetData={addDeleteAssetData}
				selectedSheetNumber={selectedSheetNumber}
				handleAddDeleteAssets={handleAddDeleteAssets}
				enteredInputData={enteredInputData}
				setEnteredInputData={setEnteredInputData}
			/>

			<ImportAssetFIleModal
				isOpen={importFilePopup}
				setIsopen={setImportFilePopup}
				updateAssetTableData={updateAssetTableData}
				selectedSheetNumber={selectedSheetNumber}
				appliedChanges={appliedChanges}
				setAppliedChanges={setAppliedChanges}
				setIsButtonDisabled={setIsButtonDisabled}
			/>

		</>
	);
};
