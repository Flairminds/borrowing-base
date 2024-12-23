import React from 'react';
import tableStyles from './DynamicTableComponents.module.css';

export const DynamicTableComponents = ({data, columns}) => {
  return (
    <>
    <table className={tableStyles.table}>
        <thead>
        <tr className={tableStyles.headRow}>
            {columns?.map((col, index) => (
            <th key={index} className={tableStyles.th}>
                {col.label}
            </th>
            ))}
        </tr>
        </thead>
        <tbody>
        {data?.map((row, rowIndex) => (
            <tr key={rowIndex}>
            {columns?.map((col) => (
                <td
                key={col.key}
                className={tableStyles.td}
                onClick={() =>
                    col.clickHandler && col.clickHandler(row[col.key], row)
                }
                >
                {col.render ? col.render(row[col.key], row) : row[col.key]}
                </td>
            ))}
            </tr>
        ))}
        </tbody>
    </table>
    </>
  );
};
