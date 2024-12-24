import React from 'react';
import { useNavigate } from 'react-router';
import { CustomButton } from '../../components/custombutton/CustomButton';
import { DynamicTableComponents } from '../../components/reusableComponents/dynamicTableComponent/DynamicTableComponents';
import { ingestionTableCols, ingestionTableData } from '../../utils/frontendTestingData';
import styles from './BaseDataFileList.module.css';

export const BaseDataFileList = () => {

    const navigate = useNavigate();

    const handleExtractNew = () => {
        navigate('/ingestion-files-list');
    };

  return (
    <div className={styles.pageContainer}>
        <div className={styles.baseFileListPage}>
            <div className={styles.buttonsContainer}>
                <CustomButton
                    isFilled={true}
                    onClick={handleExtractNew}
                    text='Extract New Base Data'
                />
            </div>

            <div className={styles.baseDataTableContainer}>
                <DynamicTableComponents data={ingestionTableData} columns={ingestionTableCols} />
            </div>

        </div>
    </div>
  );
};
