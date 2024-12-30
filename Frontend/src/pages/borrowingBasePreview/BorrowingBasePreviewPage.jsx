import React from 'react';
import { DynamicTableComponents } from '../../components/reusableComponents/dynamicTableComponent/DynamicTableComponents';
import styles from './BorrowingBasePreviewPage.module.css';

export const BorrowingBasePreviewPage = ({baseFilePreviewData}) => {

  return (
      <div className={styles.previewPage}>
          <div className={styles.tableContainer}>
              <DynamicTableComponents data={baseFilePreviewData?.data} columns={baseFilePreviewData?.columns} />
          </div>
      </div>
  );
};
