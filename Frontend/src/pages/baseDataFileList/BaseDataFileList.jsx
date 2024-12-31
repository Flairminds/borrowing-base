import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router';
import { CustomButton } from '../../components/custombutton/CustomButton';
import { DynamicTableComponents } from '../../components/reusableComponents/dynamicTableComponent/DynamicTableComponents';
import { ingestionTableCols, ingestionTableData } from '../../utils/frontendTestingData';
import styles from './BaseDataFileList.module.css';
import { getBaseDataFilesList, getBaseFilePreviewData } from '../../services/dataIngestionApi';
import { showToast } from '../../utils/helperFunctions/toastUtils';

export const BaseDataFileList = ({setBaseFilePreviewData}) => {

    const [baseDataFilesList, setaseDataFilesList] = useState({});

    const navigate = useNavigate();

    const handleExtractNew = () => {
        navigate('/ingestion-files-list');
    };

    const handleSecurityMapping = () => {
        navigate('/security-mapping');
    };

    const handleBaseDataPreview = async(info_id) => {
        try {
            const previewDataResponse = await getBaseFilePreviewData(info_id);
            console.info(previewDataResponse, 'base preview ');
            setBaseFilePreviewData(previewDataResponse.data.result);
            navigate('/base-data-preview');
        } catch (err) {
            console.error(err);
            showToast("error", err.response.data.message);
        }
    };

    const columnsToAdd = [{
        'key': 'file_preview',
        'label': '',
        'render': (value, row) => <div onClick={() => handleBaseDataPreview(row.id)}
                                    style={{display: row.extraction_status === "completed" ? 'block' : 'none', color: '#0EB198', cursor: 'pointer'}}>
                                    Preview Base Data
                                </div>
    }];

    const getFilesList = async () => {
        try {
            const data = {
                "company_id": 1
            };
            const filesRes = await getBaseDataFilesList(data);
            setaseDataFilesList(filesRes.data.result);
        } catch (err) {
            showToast('error', err?.response?.data.message);
            console.error(err);
        }
    };

    useEffect(() => {
        getFilesList();
    }, []);

  return (
    <div className={styles.pageContainer}>
        <div className={styles.baseFileListPage}>
        <div className={styles.buttonsContainer}>
                <CustomButton
                    isFilled={true}
                    onClick={handleSecurityMapping}
                    text='Security Mapping'
                />
                <CustomButton
                    isFilled={true}
                    onClick={handleExtractNew}
                    text='Extract New Base Data'
                />
            </div>

            <div className={styles.tableHeading}>
                Base Data
            </div>

            <div className={styles.baseDataTableContainer}>
                <DynamicTableComponents data={baseDataFilesList?.data} columns={baseDataFilesList?.columns} additionalColumns={columnsToAdd} />
            </div>

        </div>
    </div>
  );
};
