import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router';
import { DynamicTableComponents } from '../../components/reusableComponents/dynamicTableComponent/DynamicTableComponents';
import { showToast } from '../../utils/helperFunctions/toastUtils';
import styles from './BorrowingBasePreviewPage.module.css';

export const BorrowingBasePreviewPage = ({baseFilePreviewData}) => {
    const navigate = useNavigate();
    const [mapping, setMapping] = useState({});
    useEffect(() => {
        let col = [];
        if (!baseFilePreviewData.reportDate) {
            showToast('info', 'No report date selected. Redirecting...');
            setTimeout(() => {
                navigate('/base-data-list');
            }, 1500);
        }
        baseFilePreviewData.baseData?.columns.forEach(c => {
            let a = baseFilePreviewData?.baseDataMapping?.find(bd => bd.bd_column_name == c.label);
            if (a) {
                col[a.bd_column_name] = `${a.rd_file_name} -> ${a.rd_sheet_name} -> ${a.rd_column_name}`;
            }
        });
        setMapping(col);
    }, [baseFilePreviewData]);

    return (
        <div className={styles.previewPage}>
            <div className={styles.tableContainer}>
                <div style={{position: 'fixed'}}>
                    Base Data for {baseFilePreviewData.reportDate}
                </div>
                <DynamicTableComponents data={baseFilePreviewData?.baseData?.data} columns={baseFilePreviewData?.baseData?.columns} enableStickyColumns={true} showSettings={true} ShowCellDetailsModal={true} />
            </div>
        </div>
        // <div>
        //     {Object.keys(mapping)?.map(m => {
        //         return (
        //             <div>{m}</div>
        //         )
        //     })}
        // </div>
    );
};
