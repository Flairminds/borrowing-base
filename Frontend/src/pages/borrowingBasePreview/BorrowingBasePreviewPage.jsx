import React from 'react';
import styles from './BorrowingBasePreviewPage.module.css';

export const BorrowingBasePreviewPage = ({baseFilePreviewData}) => {

  console.info(baseFilePreviewData, 'data');

  return (
      <div className={styles.previewPage}>
          <div className={styles.tableContainer}>
              <table className={styles.table}>
                  <thead>
                      <tr className={styles.headRow}>
                          <>
                          {baseFilePreviewData?.columns.map((col, index) => (
                          <th key={index} className={styles.th}>
                              {col.label}
                          </th>
                          ))}
                          </>
                      </tr>
                  </thead>
                  <tbody>
                  {baseFilePreviewData?.data?.map((row, rowIndex) => (
                      <tr key={rowIndex}>
                      <>
                          {baseFilePreviewData?.columns.map((col) => (
                              <td key={col.key} className={styles.td}>
                              {row[col.key]}
                              </td>
                          ))}
                      </>
                      </tr>
                  ))}
                  </tbody>
              </table>
          </div>
      </div>
  );
};
