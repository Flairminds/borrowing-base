import React, { useEffect, useState } from 'react';
import { DynamicTableComponents } from '../../components/reusableComponents/dynamicTableComponent/DynamicTableComponents';
import styles from './BorrowingBasePreviewPage.module.css';

export const BorrowingBasePreviewPage = ({baseFilePreviewData}) => {
    const [mapping, setMapping] = useState({})
    useEffect(() => {
        let col = []
        baseFilePreviewData.baseData.columns.forEach(c => {
            let a = baseFilePreviewData.baseDataMapping.find(bd => bd.bd_column_name == c.label)
            if (a) {
                col[a.bd_column_name] = `${a.rd_file_name} -> ${a.rd_sheet_name} -> ${a.rd_column_name}`
            }
        })
        setMapping(col)
    }, [baseFilePreviewData])

    return (
        <div className={styles.previewPage}>
            <div className={styles.tableContainer}>
                Base Data for {baseFilePreviewData.reportDate}
                <DynamicTableComponents data={baseFilePreviewData?.baseData?.data} columns={baseFilePreviewData?.baseData?.columns} />
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
