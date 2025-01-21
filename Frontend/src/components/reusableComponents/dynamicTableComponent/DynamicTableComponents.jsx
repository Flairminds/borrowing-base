import { SettingOutlined, DragOutlined, MenuOutlined } from '@ant-design/icons';
import { Popover, Switch } from 'antd';
import React, { useEffect, useState } from 'react';
import { useDrag, useDrop, DndProvider } from "react-dnd";
import { HTML5Backend } from "react-dnd-html5-backend";
import CrossIcon from '../../../assets/CrossIcon.svg';
import RightIcon from '../../../assets/RightIcon.svg';
import { CellDetailsModal } from '../../../modal/showCellDetailsModal/CellDetailsModal';
import { showToast } from '../../../utils/helperFunctions/toastUtils';
import tableStyles from './DynamicTableComponents.module.css';

const ItemType = "COLUMN";

const DraggableColumn = ({ column, index, moveColumn }) => {
    const [, ref, drag] = useDrag({
      type: ItemType,
      item: { index },
    });
  
    const [, drop] = useDrop({
      accept: ItemType,
      hover: (item) => {
        if (item.index !== index) {
          moveColumn(item.index, index);
          item.index = index;
        }
      },
    });
  
    return (
      <div
        ref={(node) => drop(ref(node))} // Attach both drop and drag refs
        className={tableStyles.columnItem}
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          padding: "8px",
          border: "1px solid #ddd",
          marginBottom: "4px",
          backgroundColor: "#f9f9f9",
          cursor: "pointer",
        }}
      >
        <span>{column}</span>
        <MenuOutlined
          style={{ margin: "5px 7px", cursor: "grab" }}
          ref={drag} // Attach the drag ref only to the icon
        />
      </div>
    );
  };

const ColumnReorder = ({selectedColumns}) => {

    const [columns, setColumns] = useState(selectedColumns);

    const moveColumn = (fromIndex, toIndex) => {
        const updatedColumns = [...columns];
        const [moved] = updatedColumns.splice(fromIndex, 1);
        updatedColumns.splice(toIndex, 0, moved);
        setColumns(updatedColumns);
    };

    return (
        <DndProvider backend={HTML5Backend}>
      <div className={tableStyles.orderColumnContainer}>
        {columns.map((column, index) => (
          <DraggableColumn
            key={column}
            column={column}
            index={index}
            moveColumn={moveColumn}
          />
        ))}
      </div>
      <button onClick={() => console.info("Updated Order:", columns)}>Log Order</button>
    </DndProvider>
    );
};

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
        cellDetail = null
    }) => {

    const [updatedColumnsData, setUpdatedColumnsData] = useState(columns);
    const [showSettingsDiv, setShowSettingsDiv] = useState(false);
    const [breaks, setBreaks] = useState([]);
    const [selectedColumns, setSelectedColumns] = useState([]);
    const [activeRowIndex, setActiveRowIndex] = useState(-1);
    const [modalVisible, setModalVisible] = useState(false);
    // const [cellDetails, setCellDetails] = useState({ rowIndex: -1, column: '' });
    const [editingCell, setEditingCell] = useState(null);
    const [inputValue, setInputValue] = useState("");
    const [isInUpdateMode, setIsInUpdateMode] = useState(false);


    useEffect(() => {
        if (columns && columns?.length > 0) {
            const temp = [...columns, ...additionalColumns];
            setUpdatedColumnsData(temp);
            const initalColumnsConsidered = [...columns.slice(0, 10), ...additionalColumns];
            const intialColumns = initalColumnsConsidered.map((t) => t.label);
            setSelectedColumns(intialColumns);
            setBreaks([0, parseInt(columns.length / 3) + 1, (2 * parseInt(columns.length / 3)) + 1, columns.length]);
        }
    }, [columns]);

    const handleOpenSettings = (e) => {
        e.preventDefault();
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

    const handleCellEdit = (rowIndex, columnkey, cellValue) => {
        setEditingCell({ rowIndex, columnkey });
        setInputValue(cellValue);
    };

    const handleInputChange = (e) => {
        setInputValue(e.target.value);
    };

    const handleSaveEdit = async () => {

        const { rowIndex, columnkey } = editingCell;
        const saveStatus = await onChangeSave(rowIndex, columnkey, inputValue);

        if (saveStatus.success) {
            setEditingCell(null);
            setInputValue("");
            showToast("success", "Data updated successfully");
        } else {
            showToast("error", saveStatus.msg);
        }
    };

    const handleCancelEdit = (e) => {
        e.stopPropagation();
        setEditingCell(null);
        setInputValue("");
    };

    const handleToggleChange = (value) => {
        setIsInUpdateMode(value);
        if (!value) {
            setEditingCell(null);
            setInputValue("");
        }
    };


  return (
    <>
        {showSettings &&
        <div style={{position: 'relative', textAlign: 'right'}}>
            <div style={{cursor: 'pointer'}}>
                {(showCellDetailsModal && enableColumnEditing) &&
                <>
                    <div style={{display: 'inline-block'}}>
                        <span style={{margin: '7px'}}>View Only</span>
                        <Switch size='small' style={{backgroundColor: '#0EB198' }} onChange={handleToggleChange} />
                        <span style={{margin: '7px'}}>Edit Mode</span>
                    </div>
                    <div style={{display: 'inline-block', margin: '7px 25px'}}>
                        <SettingOutlined onClick={(e) => handleOpenSettings(e)} style={{ fontSize: '20px', margin: '0px 3px'}} />
                        <Popover trigger={'click'} placement="bottomRight" title={"Reorder Columns"} content={<ColumnReorder selectedColumns={selectedColumns} />}>
                            <DragOutlined style={{fontSize: '20px', margin: '0px 3px'}} />
                        </Popover>
                    </div>
                </>
                }
            </div>
            {showSettingsDiv &&
                <div style={{position: 'absolute', display: 'flex', zIndex: '500', top: '50', right: '0', backgroundColor: 'white', textAlign: 'left', padding: '5px', border: '1px solid #DCDEDE', borderRadius: '6px'}}>
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
        </div>}
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
                                    if (row[col.key] && row[col.key]['meta_info']) {
                                        cellDisplayValue = row[col.key]['display_value'];
                                        cellActualValue = row[col.key]['value'];
                                        cellTitleValue = row[col.key]['title'];
                                    }
                                    const isValueEmpty = isEditable && !cellDisplayValue;
                                return (
                                    <td key={col.key} className={enableStickyColumns ? tableStyles.stickyColTd : isValueEmpty ? tableStyles.emptyValue : tableStyles.td}
                                        style={{backgroundColor: activeRowIndex == rowIndex ? '#f2f2f2' : 'white'}}
                                        onClick={showCellDetailsModal && !isInUpdateMode ? () => handleCellClick(rowIndex, col.key, col.label, cellActualValue) : isEditable ? () => handleCellEdit(rowIndex, col.key, cellActualValue) : () => col.clickHandler && col.clickHandler(cellActualValue, row)} title={cellTitleValue}>
                                        {enableColumnEditing && editingCell?.rowIndex === rowIndex && editingCell?.columnkey === col.key ?
                                            (
                                                <div className={tableStyles.editIconsContainer}>
                                                    <input
                                                        type="text"
                                                        value={inputValue}
                                                        onChange={handleInputChange}
                                                        className={tableStyles.updateInput}
                                                        autoFocus
                                                    />
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
                        <td colSpan={updatedColumnsData?.length} className={tableStyles.td} style={{textAlign: 'center'}}>No data</td>
                    </tr>}
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