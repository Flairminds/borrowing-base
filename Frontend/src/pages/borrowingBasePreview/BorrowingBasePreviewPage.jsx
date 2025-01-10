import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router';
import { DynamicTableComponents } from '../../components/reusableComponents/dynamicTableComponent/DynamicTableComponents';
import { getBaseDataCellDetail } from '../../services/api';
import { showToast } from '../../utils/helperFunctions/toastUtils';
import styles from './BorrowingBasePreviewPage.module.css';

export const BorrowingBasePreviewPage = ({baseFilePreviewData}) => {
    const navigate = useNavigate();
    const [mapping, setMapping] = useState({});
    const [cellDetail, setCellDetail] = useState({});

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

    const getCellDetail = async(rowIndex, columnKey, columnName, cellValue) => {
        let temp = {
            "title": columnName,
            "data": {
                // 'Base data column name': columnName,
                'Value': cellValue,
                'Source file name': 'Not mapped',
                'Sheet name': 'Not mapped',
                'Column name': 'Not mapped',
                'Formula': 'Not mapped'
            }
        };
        try {
            console.log(rowIndex, columnKey, columnName, cellValue);
            const response = await getBaseDataCellDetail({ 'ebd_id': baseFilePreviewData.infoId, 'column_key': columnKey });
            const detail = response?.data?.result;
            const t = {
                ...temp.data,
                'Source file name': detail.file_name + detail.extension,
                'Sheet name': detail.sf_sheet_name,
                'Column name': detail.sf_column_name,
                'Formula': detail.formula ? detail.formula : 'Value same as source column value'
            };
            temp['data'] = t;
            setCellDetail(temp);
        } catch (error) {
            console.error(error.message);
            setCellDetail(temp);
        }
    };

    return (
        <div className={styles.previewPage}>
            <div className={styles.tableContainer}>
                <div style={{position: 'fixed'}}>
                    Base Data for {baseFilePreviewData.reportDate}
                </div>
                <DynamicTableComponents data={baseFilePreviewData?.baseData?.data} columns={baseFilePreviewData?.baseData?.columns} enableStickyColumns={true} showSettings={true} showCellDetailsModal={true} getCellDetailFunc={getCellDetail} cellDetail={cellDetail} />
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
