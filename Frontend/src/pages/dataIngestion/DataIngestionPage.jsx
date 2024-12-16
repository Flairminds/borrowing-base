import React from 'react';
import { CustomButton } from '../../components/custombutton/CustomButton';
import styles from './DataIngestionPage.module.css';
import { ingestionTableCols, ingestionTableData } from '../../utils/frontendTestingData';

export const DataIngestionPage = () => {
  return (
    <div>
        <div className={styles.uploadBtnContainer}>
            <CustomButton
                isFilled={true}
                text='Upload a File'
            />
        </div>

        <div className={styles.tableContainer}>
            <table className={styles.table}>
                <thead>
                    <tr className={styles.headRow}>
                        {ingestionTableCols.map((col, index) => (
                        <th key={index} className={styles.th}>
                            {col.label}
                        </th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                {ingestionTableData.map((row, rowIndex) => (
                    <tr key={rowIndex}>
                    {ingestionTableCols.map((col) => (
                        <td key={col.key} className={styles.td}>
                        {row[col.key]}
                        </td>
                    ))}
                    </tr>
                ))}
                </tbody>
            </table>

        </div>



    </div>
  );
};
