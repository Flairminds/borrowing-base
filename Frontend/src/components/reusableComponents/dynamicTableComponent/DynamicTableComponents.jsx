import React, { useEffect, useState } from 'react';
import tableStyles from './DynamicTableComponents.module.css';

export const DynamicTableComponents = ({data, columns, additionalColumns = []}) => {

    const [updatedColumnsData, setUpdatedColumnsData] = useState(columns);
    const [showSettingsDiv, setShowSettingsDiv] = useState(false);
    const [breaks, setBreaks] = useState([])
    const [selectedColumns, setSelectedColumns] = useState([])
    const [activeRowIndex, setActiveRowIndex] = useState(-1)

    useEffect(() => {
        if (columns && columns?.length > 0) {
            let temp = [...columns, ...additionalColumns]
            setUpdatedColumnsData(temp);
            setSelectedColumns(temp.map((t) => t.label))
            setBreaks([0, parseInt(columns.length / 3) + 1, (2 * parseInt(columns.length / 3)) + 1, columns.length])
        }
    }, [columns]);

    const handleOpenSettings = (e) => {
        e.preventDefault();
        setShowSettingsDiv(!showSettingsDiv);
    };

    const handleCheckboxClick = (e, val) => {
        e.preventDefault();
        const temp = [...selectedColumns];
        const index = temp.indexOf(val);
        if (index > -1) {
            temp.splice(index, 1);
        } else {
            temp.push(val);
        }
        setSelectedColumns(temp);
    };

  return (
    <>
        <div style={{position: 'relative', textAlign: 'right'}}>
            <div style={{cursor: 'pointer'}} onClick={(e) => handleOpenSettings(e)}>Settings</div>
            {showSettingsDiv &&
                <div style={{position: 'absolute', display: 'flex', zIndex: '200', top: '50', right: '0', backgroundColor: 'white', textAlign: 'left', padding: '10px', border: '1px solid #DCDEDE', borderRadius: '6px'}}>
                    {breaks?.map((b, i) => {
                        if (i !== 0) {
                            return (
                                <div key={i}>
                                    {updatedColumnsData?.slice(breaks[i - 1], breaks[i]).map((col, index) => {
                                        return <>
                                            <div key={index} style={{fontSize: 'small'}}>
                                                <input type="checkbox" id={col.key} name={col.key} value={col.key} onClick={(e) => handleCheckboxClick(e, col.label)} checked={selectedColumns.includes(col.label)}/>
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
        <table className={tableStyles.table}>
            <thead>
            <tr className={tableStyles.headRow}>
                {updatedColumnsData?.map((col, index) => {
                    if (selectedColumns.includes(col.label)) {
                        return (
                            <th key={index} className={tableStyles.th}>
                                {col.label}
                            </th>
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
                                return (
                                    <td key={col.key} className={tableStyles.td}
                                        style={{backgroundColor: activeRowIndex == rowIndex ? '#f2f2f2' : 'white'}}
                                        onClick={() => col.clickHandler && col.clickHandler(row[col.key], row)}>
                                        {col.render ? col.render(row[col.key], row) : row[col.key]}
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
    </>
  );
};
