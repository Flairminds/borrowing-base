import { SettingOutlined, CloseOutlined, FilterOutlined, EditOutlined } from '@ant-design/icons';
import { Popover, Select } from 'antd';
import Input from 'antd/es/input/Input';
import dayjs from "dayjs";
import React, { useEffect, useState } from 'react';
import { TbReorder } from "react-icons/tb";
import CrossIcon from '../../../assets/CrossIcon.svg';
import RightIcon from '../../../assets/RightIcon.svg';
import upDownArrow from "../../../assets/sortArrows/up-and-down-arrow.svg";
import upArrowIcon from "../../../assets/sortArrows/up.svg";
import { CellDetailsModal } from '../../../modal/showCellDetailsModal/CellDetailsModal';
import { updateSeletedColumns } from '../../../services/dataIngestionApi';
import { fmtDisplayVal } from '../../../utils/helperFunctions/formatDisplayData';
import { filterData } from '../../../utils/helperFunctions/HeaderColumnFilter';
import { showToast } from '../../../utils/helperFunctions/toastUtils';
import { BaseFilePreviewReorder } from '../../columnReorderComponent/baseFilePreviewReorder.jsx/BaseFilePreviewReorder';
import { Icons } from '../../icons';
import { DynamicInputComponent } from '../dynamicInputsComponent/DynamicInputComponent';
import tableStyles from './DynamicTableComponents.module.css';

export const DynamicTableComponents = ({
	data,
	columns,
	initialAdditionalColumns = [],
	additionalColumns = [],
	showCellDetailsModal = false,
	showSettings = false,
	enableStickyColumns = false,
	enableColumnEditing = false,
	onChangeSave,
	getCellDetailFunc = () => { },
	cellDetail = null,
	refreshDataFunction,
	previewFundType,
	filterSelections,
	visibleSortHeader = false,
	showFilter = true
}) => {

	const [updatedColumnsData, setUpdatedColumnsData] = useState(columns);
	const [columnSelectionList, setColumnSelectionList] = useState(columns);
	const [showSettingsDiv, setShowSettingsDiv] = useState(false);
	const [showFilterDiv, setShowFilterDiv] = useState(false);
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
	const [selectedSort, setSelectedSort] = useState({ name: null, type: null });
	const [displayData, setDisplayData] = useState([]);
	const [columnSearch, setColumnSearch] = useState('');


	useEffect(() => {
		if (data) {
			let temp = data;
			temp = temp.map((row, i) => {
				const tempCols = updatedColumnsData.map((col, j) => {
					const cellAV = row[col.key] && row[col.key]['meta_info'] ? row[col.key]['value'] : row[col.key];
					let cellDV = row[col.key] && row[col.key]['meta_info'] ? row[col.key]['display_value'] : row[col.key];
					switch (col.unit) {
					case 'percent': cellDV = `${(cellAV * 100).toFixed(2)}%`; break;
					case 'date': cellDV = `${((new Date(cellAV)).toLocaleDateString("en-US"))}`; break;
					default:
						break;
					}
					row[col.key] = row[col.key] && row[col.key]['meta_info'] ? {
						...row[col.key],
						isEditable: enableColumnEditing && col.isEditable,
						cellDisplayValue: cellDV,
						cellActualValue: cellAV && !isNaN(cellAV) ? parseFloat(cellAV) : cellAV,
						cellTitleValue: row[col.key] && row[col.key]['meta_info'] ? row[col.key]['title'] : row[col.key],
						cellOldValue: row[col.key] && row[col.key]['meta_info'] ? (row[col.key]['old_value'] && !isNaN(row[col.key]['old_value']) ? parseFloat(row[col.key]['old_value']) : row[col.key]['old_value']) : (!isNaN(row[col.key]) ? parseFloat(row[col.key]) : row[col.key]),
						isManuallyAdded: row["is_manually_added"].value,
						isValueEmpty: enableColumnEditing && col.isEditable && !cellDV,
						InputChnageFun: col.datatype == 'date' ? handleDateChange : handleInputChange
					} : row[col.key];
				});
				return row;
			});
			setDisplayData(temp);
		}
	}, [data]);

	useEffect(() => {
		if (columns && columns?.length > 0) {
			const temp = [...initialAdditionalColumns, ...columns, ...additionalColumns];
			setUpdatedColumnsData(temp);
			const temp1 = [...temp];
			setColumnSelectionList(temp1.sort((a, b) => a.label < b.label ? -1 : 1));
			let selectedColumntoDisplay = [];
			if (showSettings) {
				selectedColumntoDisplay = columns.filter((col) => col.is_selected);
			} else {
				selectedColumntoDisplay = columns;
			}
			const initalColumnsConsidered = [...initialAdditionalColumns, ...selectedColumntoDisplay, ...additionalColumns];
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

	const handleOpenFilter = (e) => {
		e.preventDefault();
		if (showFilterDiv) {
			// updateVisibleColumns();
		}
		setShowFilterDiv(!showFilterDiv);
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

	const handleCellClick = (rowId, columnKey, columnName, cellValue) => {
		if (showCellDetailsModal) {
			getCellDetailFunc(rowId, columnKey, columnName, cellValue);
			setModalVisible(true);
		}
	};

	const handleCellEdit = (rowIndex, columnkey, cellValue, dataType, rowId, unit) => {
		setEditingCell({ rowIndex, columnkey, id: rowId.value, unit: unit });
		if (dataType === "date" && cellValue) {
			setInputValue({
				value: dayjs(cellValue),
				displayValue: cellValue
			});
		} else {
			if (unit == 'percent') {
				setInputValue({
					value: cellValue * 100,
					displayValue: cellValue * 100
				});
			} else {
				setInputValue({
					value: cellValue,
					displayValue: cellValue
				});
			}
		}
		// setInputValue(cellValue);
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

		const { rowIndex, columnkey, id, unit } = editingCell;
		let value = inputValue.displayValue;
		if (unit == 'percent') {
			value = value / 100;
		}
		const saveStatus = await onChangeSave(rowIndex, columnkey, value, id);

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

	const handleToggleChange = (e) => {
		e.preventDefault();
		const temp = !isInUpdateMode;
		setIsInUpdateMode(temp);
		if (!temp) {
			setEditingCell(null);
			setInputValue({
				value: null,
				displayValue: ""
			});
		}
	};

	const handleSortArrowClick = (columnName) => {
		if (selectedSort.name === columnName) {
			if (selectedSort.type === 'asc') {
				const newSortType = 'desc';
				setSelectedSort({ name: columnName, type: newSortType });
				setDisplayData(filterData([...data], columnName, newSortType));
			} else if (selectedSort.type === 'desc') {
				setSelectedSort({ name: columnName, type: 'nosort' });
				setDisplayData([...data]);
			} else {
				const newSortType = 'asc';
				setSelectedSort({ name: columnName, type: newSortType });
				setDisplayData(filterData([...data], columnName, newSortType));
			}
		} else {
			const newSortType = 'asc';
			setSelectedSort({ name: columnName, type: newSortType });
			setDisplayData(filterData([...data], columnName, newSortType));
		}
	};

	return (
		<div>
			<div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
				<div>
					{displayData?.length} record(s)
				</div>
				{showSettings &&
					<div>
						<div style={{ cursor: 'pointer', position: 'relative' }}>
							{(showCellDetailsModal && enableColumnEditing) &&
								<>
									<div style={{ display: 'inline-block', margin: '5px 15px' }}>
										{showFilter && <FilterOutlined size={30} onClick={(e) => handleOpenFilter(e)} className={`${tableStyles.tableIcons} ${showFilterDiv ? tableStyles.tableIconsActive : ''}`} title='Filter data' />}
										<SettingOutlined size={30} onClick={(e) => handleOpenSettings(e)} className={`${tableStyles.tableIcons} ${showSettingsDiv ? tableStyles.tableIconsActive : ''}`} title='Select/Unselect columns' />
										<Popover trigger={'click'} placement="bottomRight" className={`${tableStyles.tableIcons}`} title={"Reorder Columns"} content={<BaseFilePreviewReorder selectedColumns={selectedColumns} totalColumnsData={columns} refreshDataFunction={refreshDataFunction} />}>
											<TbReorder size={30} title='Reorder columns' />
											{/* <DragOutlined style={{fontSize: '20px', margin: '0px 3px'}} /> */}
										</Popover>
										<EditOutlined size={30} className={`${tableStyles.tableIcons} ${isInUpdateMode && tableStyles.isEdited}`} onClick={(e) => handleToggleChange(e)} title='Edit Mode' />
									</div>
									{/* <div style={{display: 'inline-block', fontSize: 'small'}}>
								<span style={{margin: '7px'}}>View Only</span>
								<Switch size='small' style={{backgroundColor: '#0EB198' }} onChange={handleToggleChange} />
								<span style={{margin: '7px'}}>Edit Mode</span>
							</div> */}
								</>
							}
						</div>
						{showSettingsDiv &&
							<div style={{ position: 'absolute', zIndex: '500', top: '50', right: '0', backgroundColor: '#F6F8FB', textAlign: 'left', padding: '5px', border: '1px solid #DCDEDE', borderRadius: '6px', minWidth: '1400px' }}>
								<div style={{ display: 'flex', margin: '5px 0', justifyContent: 'space-between', alignItems: 'center' }}>
									<div>
										<Icons.InfoIcon style={{ margin: '0 5px 0 0' }} />
										Select columns to view data in the table
									</div>
									<div className={tableStyles.crossIcon}>
										<CloseOutlined onClick={handleOpenSettings} />
									</div>
								</div>
								<Input
									placeholder="Search columns"
									allowClear
									onChange={(e) => setColumnSearch(e.target.value)}
									style={{ marginBottom: 8 }}
								/>
								<div style={{ display: 'flex', flexWrap: 'wrap' }}>
									{breaks?.map((b, i) => {
										if (i !== 0) {
											const filteredCols = columnSelectionList
												.slice(breaks[i - 1], breaks[i])
												.filter(col => col.label.toLowerCase().includes(columnSearch?.toLowerCase()));

											if (filteredCols.length === 0) return null;
											return (
												<div className={tableStyles.columnSelectionContainer} key={i}>
													{filteredCols.map((col, index) => (
														<div key={index} className={tableStyles.columnContainer} style={{ fontSize: 'small' }}>
															<input
																className={tableStyles.checkbox}
																type="checkbox"
																id={col.key}
																name={col.key}
																value={col.key}
																onClick={(e) => handleCheckboxClick(e, col.label)}
																checked={selectedColumns.includes(col.label)}
															/>
															<label htmlFor={col.key} className={isInUpdateMode && col.isEditable ? tableStyles.isEdited : ""}>
																{col.label}
															</label>
														</div>
													))}
												</div>
											);
										}
									})}
								</div>
							</div>
						}
						{showFilterDiv &&
							filterSelections && filterSelections.length > 0 &&
							<div style={{ position: 'absolute', display: 'flex', justifyContent: 'space-between', zIndex: '500', top: '50', right: '0', backgroundColor: 'white', textAlign: 'left', minWidth: '40%', padding: '10px', border: '1px solid #DCDEDE', borderRadius: '5px' }}>
								<div className={tableStyles.crossIcon}><CloseOutlined onClick={handleOpenFilter} /></div>
								<div style={{ width: '90%' }}>
									{filterSelections.map((f, i) => {
										return (
											<div key={i}>
												<Select
													mode="multiple"
													allowClear
													style={{ flex: 1, minWidth: '90%', margin: '5px 0' }}
													placeholder={f.placeholder}
													onChange={f.onChange}
													value={f.value}
													options={f.options}
												/>
											</div>
										);
									})}
								</div>
							</div>}
					</div>}
			</div>
			<div style={{ overflow: 'auto', maxHeight: '75vh' }}>
				<table className={tableStyles.table} style={{ tableLayout: enableStickyColumns ? 'fixed' : 'auto' }}>
					<thead className={tableStyles.headRowThead}>
						<tr className={tableStyles.headRow}>
							{updatedColumnsData?.map((col, index) => {
								if (selectedColumns.includes(col.label)) {
									return (
										<th key={index} className={enableStickyColumns && index < 3 ? tableStyles.stickyColTh : tableStyles.th} title={col.label}>
											{col.label}
											{visibleSortHeader && col.label !== '' && col.key !== '' && (
												selectedSort.name === col.key && selectedSort.type === 'asc' ? (
													<img onClick={() => handleSortArrowClick(col.key)} style={{ paddingLeft: '5px', paddingBottom: '2px', margin: '0px 5px' }} src={upArrowIcon} alt="up" />
												) : selectedSort.name === col.key && selectedSort.type === 'desc' ? (
													<img onClick={() => handleSortArrowClick(col.key)} style={{ paddingLeft: '5px', paddingBottom: '2px', transform: 'rotate(180deg)', margin: '0px 5px' }} src={upArrowIcon} alt="down" />
												) : (
													<img onClick={() => handleSortArrowClick(col.key)} style={{ paddingLeft: '5px', paddingBottom: '2px', height: '13px', width: '14px' }} src={upDownArrow} alt="sort" />
												)
											)}
										</th>
									);
								}
							})}
						</tr>
					</thead>
					<tbody>
						{displayData?.length > 0 ?
							displayData?.map((row, rowIndex) => (
								<tr key={rowIndex} className={tableStyles.tr} onClick={() => setActiveRowIndex(rowIndex)}>
									{updatedColumnsData?.map((col, colIndex) => {
										if (selectedColumns.includes(col.label)) {
											return (
												<td key={col.key} className={`${enableStickyColumns && colIndex < 3 ? tableStyles.stickyColTd : row[col.key]?.isValueEmpty ? tableStyles.emptyValue : tableStyles.td} ${activeRowIndex == rowIndex ? tableStyles.activeCell : ''}  ${row[col.key]?.cellActualValue != row[col.key]?.cellOldValue ? tableStyles.editedCell : ''} ${row[col.key]?.isManuallyAdded && tableStyles.isManuallyAdd} ${(isInUpdateMode && col.isEditable) && tableStyles.isEdited}`}
													onClick={showCellDetailsModal && !isInUpdateMode ? () => handleCellClick(row['id']['value'], col.key, col.label, row[col.key]?.cellActualValue) : row[col.key]?.isEditable ? () => handleCellEdit(rowIndex, col.key, row[col.key]?.cellActualValue, col.datatype, row.id, col.unit) : () => col.clickHandler && col.clickHandler(row[col.key]?.cellActualValue, row)} title={`${row[col.key]?.cellActualValue != row[col.key]?.cellOldValue ? 'Updated: ' + fmtDisplayVal(row[col.key]?.cellActualValue, 3) + '\nPrevious: ' + fmtDisplayVal(row[col.key]?.cellOldValue, 3) : fmtDisplayVal(row[col.key]?.cellTitleValue, 3)}`}>
													{enableColumnEditing && editingCell?.rowIndex === rowIndex && editingCell?.columnkey === col.key ?
														(
															<div className={tableStyles.editIconsContainer}>
																<DynamicInputComponent inputValue={inputValue?.value} inputType={col.datatype} onInputChange={row[col.key]?.InputChnageFun} autoFocusInput={true} />
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
														col.render ? col.render(row[col.key]?.cellDisplayValue, row) : (row[col.key]?.cellDisplayValue ? fmtDisplayVal(row[col.key]?.cellDisplayValue) : typeof row[col.key] !== 'object' ? row[col.key] : '-')
													}
												</td>
											);
										}
									})}
								</tr>
							))
							: <tr>
								<td colSpan={updatedColumnsData?.length} className={tableStyles.td} style={{ textAlign: 'center' }}>No Data</td>
							</tr>}
					</tbody>
				</table>
			</div>
			<CellDetailsModal
				visible={modalVisible}
				onClose={() => setModalVisible(false)}
				cellDetails={cellDetail}
			/>
		</div>
	);
};