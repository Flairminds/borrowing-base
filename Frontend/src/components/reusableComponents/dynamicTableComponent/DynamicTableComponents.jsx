import { SettingOutlined, DragOutlined, CloseOutlined } from '@ant-design/icons';
import { Popover, Switch } from 'antd';
import dayjs from "dayjs";
import React, { useEffect, useState } from 'react';
import { TbReorder } from "react-icons/tb";
import CrossIcon from '../../../assets/CrossIcon.svg';
import RightIcon from '../../../assets/RightIcon.svg';
import { CellDetailsModal } from '../../../modal/showCellDetailsModal/CellDetailsModal';
import { updateSeletedColumns } from '../../../services/dataIngestionApi';
import { showToast } from '../../../utils/helperFunctions/toastUtils';
import { BaseFilePreviewReorder } from '../../columnReorderComponent/baseFilePreviewReorder.jsx/BaseFilePreviewReorder';
import { DynamicInputComponent } from '../dynamicInputsComponent/DynamicInputComponent';
import tableStyles from './DynamicTableComponents.module.css';


export const DynamicTableComponents = (
	{
		data,
		columns,
		additionalColumns = [],
		showCellDetailsModal = false,
		showSettings = false,
		enableStickyColumns = false,
		enableColumnEditing = false,
		onChangeSave,
		getCellDetailFunc = () => {},
		cellDetail = null,
		refreshDataFunction,
		previewFundType
	}) => {

	const [updatedColumnsData, setUpdatedColumnsData] = useState(columns);
	const [showSettingsDiv, setShowSettingsDiv] = useState(false);
	const [breaks, setBreaks] = useState([]);
	const [selectedColumns, setSelectedColumns] = useState([]);
	const [activeRowIndex, setActiveRowIndex] = useState(-1);
	const [modalVisible, setModalVisible] = useState(false);
	// const [cellDetails, setCellDetails] = useState({ rowIndex: -1, column: '' });
	const [editingCell, setEditingCell] = useState(null);
	const [inputValue, setInputValue] = useState({
		value: "",
		displayValue: ""
	});
	const [isInUpdateMode, setIsInUpdateMode] = useState(false);


	useEffect(() => {
		if (columns && columns?.length > 0) {
			const temp = [...columns, ...additionalColumns];
			setUpdatedColumnsData(temp);
			let selectedColumntoDisplay = [];
			if (showSettings) {
				selectedColumntoDisplay = columns.filter((col) => col.is_selected);
			} else {
				selectedColumntoDisplay = columns;
			}
			const initalColumnsConsidered = [...selectedColumntoDisplay, ...additionalColumns];
			const intialColumns = initalColumnsConsidered.map((t) => t.label);
			console.info(intialColumns, 'test', initalColumnsConsidered);
			setSelectedColumns(intialColumns);
			setBreaks([0, parseInt(columns.length / 3) + 1, (2 * parseInt(columns.length / 3)) + 1, columns.length]);
		}
	}, [columns]);

	const updateVisibleColumns = async () => {
		const updatedSelectedColumnIds = selectedColumns?.map((col) => {
			const columnData = columns.find((c) => c.label == col);
			const columnId = columnData?.bdm_id;
			return columnId;
		});

		try {
			const res = await updateSeletedColumns(updatedSelectedColumnIds, previewFundType);
			showToast("success", res.data.message);
		} catch (err) {
			console.error(err);
			showToast('error', err.response?.data?.message || 'Failed to Update');
		}
	};

	const handleOpenSettings = (e) => {
		e.preventDefault();
		if (showSettingsDiv) {
			updateVisibleColumns();
		}
		setShowSettingsDiv(!showSettingsDiv);
	};

	const handleCheckboxClick = (e, val) => {
		const selectedColumnsArray = [...selectedColumns];
		const index = selectedColumnsArray.indexOf(val);
		if (index > -1) {
			setSelectedColumns(selectedColumns?.filter((col) => col != val));
		} else {
			setSelectedColumns([...selectedColumns, val]);
		}
	};

	const handleCellClick = (rowIndex, columnKey, columnName, cellValue) => {
		if (showCellDetailsModal) {
			getCellDetailFunc(rowIndex, columnKey, columnName, cellValue);
			setModalVisible(true);
		}
	};

	const handleCellEdit = (rowIndex, columnkey, cellValue, dataType) => {
		setEditingCell({ rowIndex, columnkey });
		if (dataType === "date" && cellValue) {
			setInputValue({
				value: dayjs(cellValue),
				displayValue: cellValue
			});
		} else {
			setInputValue({
				value: cellValue,
				displayValue: cellValue
			});
		}
	};

	const handleInputChange = (e) => {
		setInputValue({
			value: e.target.value,
			displayValue: e.target.value
		});
	};

	const handleDateChange = (date, dateString) => {
		setInputValue({
			value: date,
			displayValue: dateString
		});
	};

	const handleSaveEdit = async () => {

		const { rowIndex, columnkey } = editingCell;
		console.info(rowIndex, columnkey, '----', inputValue);
		const saveStatus = await onChangeSave(rowIndex, columnkey, inputValue.displayValue);

		if (saveStatus.success) {
			setEditingCell(null);
			setInputValue({
				value: null,
				displayValue: ""
			});
			showToast("success", "Data updated successfully");
		} else {
			showToast("error", saveStatus.msg);
		}
	};

	const handleCancelEdit = (e) => {
		e.stopPropagation();
		setEditingCell(null);
		setInputValue({
			value: null,
			displayValue: ""
		});
	};

	const handleToggleChange = (value) => {
		setIsInUpdateMode(value);
		if (!value) {
			setEditingCell(null);
			setInputValue({
				value: null,
				displayValue: ""
			});
		}
	};


	return (
		<>
			{showSettings &&
		<div style={{position: 'relative', textAlign: 'right'}}>
			<div style={{cursor: 'pointer'}}>
				{(showCellDetailsModal && enableColumnEditing) &&
				<>
					<div style={{display: 'inline-block', fontSize: 'small'}}>
						<span style={{margin: '7px'}}>View Only</span>
						<Switch size='small' style={{backgroundColor: '#0EB198' }} onChange={handleToggleChange} />
						<span style={{margin: '7px'}}>Edit Mode</span>
					</div>
					<div style={{display: 'inline-block', margin: '5px 15px'}}>
                        <SettingOutlined onClick={(e) => handleOpenSettings(e)} style={{display: 'inline-block', margin: '0px 8px'}} title='Select/Unselect columns'/>
                        <Popover trigger={'click'} placement="bottomRight" title={"Reorder Columns"} content={<BaseFilePreviewReorder selectedColumns={selectedColumns} totalColumnsData={columns} refreshDataFunction={refreshDataFunction} />}>
                        <TbReorder size={20} title='Reorder columns'/>
                            {/* <DragOutlined style={{fontSize: '20px', margin: '0px 3px'}} /> */}
                        </Popover>
                    </div>
				</>
				}
			</div>
			{showSettingsDiv &&
			<div style={{position: 'absolute', display: 'flex', zIndex: '500', top: '50', right: '0', backgroundColor: 'white', textAlign: 'left', padding: '5px', border: '1px solid #DCDEDE', borderRadius: '6px'}}>
				<div className={tableStyles.crossIcon}><CloseOutlined onClick={handleOpenSettings} /></div>
				{breaks?.map((b, i) => {
					if (i !== 0) {
						return (
							<div className={tableStyles.columnSelectionContainer} key={i}>
								{updatedColumnsData?.slice(breaks[i - 1], breaks[i]).map((col, index) => {
									return <>
										<div key={index} className={tableStyles.columnContainer} style={{fontSize: 'small'}}>
											<input className={tableStyles.checkbox} type="checkbox" id={col.key} name={col.key} value={col.key} onClick={(e) => handleCheckboxClick(e, col.label)} checked={selectedColumns.includes(col.label)}/>
											<label htmlFor={col.key}>{col.label}</label>
										</div>
									</>;
								}
								)}
							</div>);
					}
				})}
			</div>}
		</div>
			}
			<table className={tableStyles.table} style={{tableLayout: enableStickyColumns ? 'fixed' : 'auto'}}>
				<thead>
					<tr className={tableStyles.headRow}>
						{updatedColumnsData?.map((col, index) => {
							if (selectedColumns.includes(col.label)) {
								return (
									<>
										<th key={index} className={enableStickyColumns ? tableStyles.stickyColTh : tableStyles.th} title={col.label}>
											{col.label}
										</th>
									</>
								);
							}
						})}
					</tr>
				</thead>
				<tbody>
					{data?.length > 0 ?
						data?.map((row, rowIndex) => (
							<tr key={rowIndex} onClick={() => setActiveRowIndex(rowIndex)}>
								{updatedColumnsData?.map((col) => {
									if (selectedColumns.includes(col.label)) {
										const isEditable = enableColumnEditing && col.isEditable;
										let cellDisplayValue = row[col.key];
										let cellActualValue = row[col.key];
										let cellTitleValue = row[col.key];
										let cellOldValue = row[col.key];
										if (row[col.key] && row[col.key]['meta_info']) {
											cellDisplayValue = row[col.key]['display_value'];
											cellActualValue = row[col.key]['value'];
											cellTitleValue = row[col.key]['title'];
											cellOldValue = row[col.key]['old_value'];
										}
										const isValueEmpty = isEditable && !cellDisplayValue;
										const InputChnageFun = col.datatype == 'date' ? handleDateChange : handleInputChange;
										return (
											<td key={col.key} className={enableStickyColumns ? tableStyles.stickyColTd : isValueEmpty ? tableStyles.emptyValue : tableStyles.td}
												style={{backgroundColor: activeRowIndex == rowIndex ? '#f2f2f2' : 'white', color: cellActualValue != cellOldValue ? 'red' : 'auto'}}
												onClick={showCellDetailsModal && !isInUpdateMode ? () => handleCellClick(rowIndex, col.key, col.label, cellActualValue) : isEditable ? () => handleCellEdit(rowIndex, col.key, cellActualValue, col.datatype) : () => col.clickHandler && col.clickHandler(cellActualValue, row)} title={`${cellActualValue != cellOldValue ? 'Updated: ' + cellActualValue + '\nPrevious: ' + cellOldValue : cellTitleValue}`}>
												{enableColumnEditing && editingCell?.rowIndex === rowIndex && editingCell?.columnkey === col.key ?
													(
														<div className={tableStyles.editIconsContainer}>
															<DynamicInputComponent inputValue={inputValue?.value} inputType={col.datatype} onInputChange={InputChnageFun} autoFocusInput={true} />
															<img
																src={RightIcon}
																alt="Save"
																className={tableStyles.iconButton}
																onClick={handleSaveEdit}
															/>
															<img
																src={CrossIcon}
																alt="Cancel"
																className={tableStyles.iconButton}
																onClick={handleCancelEdit}
															/>
														</div>
													)
													:
													col.render ? col.render(cellDisplayValue, row) : (cellDisplayValue ? cellDisplayValue : '-')
												}
											</td>
										);
									}
								})}
							</tr>
						))
						: <tr>
							<td colSpan={updatedColumnsData?.length} className={tableStyles.td} style={{textAlign: 'center'}}>No Data</td>
						</tr>
					}
				</tbody>
			</table>
			<CellDetailsModal
				visible={modalVisible}
				onClose={() => setModalVisible(false)}
				cellDetails={cellDetail}
			/>
		</>
	);
};