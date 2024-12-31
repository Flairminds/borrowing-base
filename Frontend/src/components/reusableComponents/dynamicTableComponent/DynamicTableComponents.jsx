import React, { useEffect, useState } from 'react';
import tableStyles from './DynamicTableComponents.module.css';

export const DynamicTableComponents = ({data, columns, additionalColumns = []}) => {

    const [updatedColumnsData, setUpdatedColumnsData] = useState(columns);
    useEffect(() => {
        if (columns && columns?.length > 0) {
            setUpdatedColumnsData([...columns, ...additionalColumns]);
        }
    }, [columns]);

  return (
    <>
    <table className={tableStyles.table}>
        <thead>
        <tr className={tableStyles.headRow}>
            {updatedColumnsData?.map((col, index) => (
            <th key={index} className={tableStyles.th}>
                {col.label}
            </th>
            ))}
        </tr>
        </thead>
        <tbody>
            {data?.length > 0 ?
                data?.map((row, rowIndex) => (
                    <tr key={rowIndex}>
                        {updatedColumnsData?.map((col) => (
                            <td key={col.key} className={tableStyles.td}
                                onClick={() => col.clickHandler && col.clickHandler(row[col.key], row)}>
                                {col.render ? col.render(row[col.key], row) : row[col.key]}
                            </td>
                        ))}
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
