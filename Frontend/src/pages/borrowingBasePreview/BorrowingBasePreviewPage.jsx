import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router';
import { CustomButton } from '../../components/custombutton/CustomButton';
import { DynamicTableComponents } from '../../components/reusableComponents/dynamicTableComponent/DynamicTableComponents';
import { getBaseDataCellDetail, generateBaseDataFile } from '../../services/api';
import { editBaseData, getBaseFilePreviewData } from '../../services/dataIngestionApi';
import { showToast } from '../../utils/helperFunctions/toastUtils';
import styles from './BorrowingBasePreviewPage.module.css';
import { AddOtherInfo } from '../../modal/addOtherInfo/AddOtherInfo';

export const BorrowingBasePreviewPage = ({baseFilePreviewData, setBaseFilePreviewData, previewPageId}) => {
    const navigate = useNavigate();
    const [mapping, setMapping] = useState({});
    const [cellDetail, setCellDetail] = useState({});
    const [isAddFieldModalOpen, setIsAddFieldModalOpen] = useState(false);

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

    const handleBaseDataPreview = async () => {
        try {
            const previewDataResponse = await getBaseFilePreviewData(previewPageId);
            const result = previewDataResponse.data?.result;
            if (result)
                setBaseFilePreviewData({
                    baseData: result.base_data_table,
                    reportDate: result.report_date,
                    baseDataMapping: result.base_data_mapping
                });
        } catch (err) {
            showToast("error", err.response.data.message);
        }
    };

    const handleSaveEdit = async (rowIndex, columnkey, inputValue) => {
            const updatedData = [...baseFilePreviewData?.baseData?.data];
            const changes = [{
                    id: updatedData[rowIndex].id['value'],
                    [columnkey]: inputValue
                }
            ];

            try {
                await editBaseData(changes);
                await handleBaseDataPreview();
                updatedData[rowIndex][columnkey] = inputValue;
                console.info(baseFilePreviewData, 'base preivew state');
                setBaseFilePreviewData({
                    ...baseFilePreviewData,
                    'baseData': {
                        ...baseFilePreviewData.baseData,
                        'data': updatedData
                    }
                });
                // setBaseFilePreviewData({...BorrowingBasePreviewPage.baseData, data: updatedData});
                return {success: "failure", msg: "Update success"};
            } catch (error) {
                // showToast("error", error?.response?.data?.message || "Failed to update data");
                return {success: "failure", msg: error?.response?.data?.message || "Failed to update data"};
            }
        };

    const generateBaseData = async(e) => {
        // e.preventDefault();
        try {
            const response = await generateBaseDataFile({ 'bdi_id': baseFilePreviewData.infoId});
            const detail = response?.data;
            showToast('success', detail?.message);
        } catch (error) {
            showToast('error', error.message);
        }
    };

    return (
        <div className={styles.previewPage}>
            <div className={styles.tableContainer}>
                <div style={{display: 'flex', justifyContent: 'space-between'}}>
                    <div>
                        Base Data for {baseFilePreviewData.reportDate} ({baseFilePreviewData?.baseData?.data ? baseFilePreviewData?.baseData?.data.length : ''})
                    </div>
                    <div>
                        <button onClick={(e) => generateBaseData(e)} style={{outline: 'none', backgroundColor: '#0EB198', color: 'white', padding: '5px 10px', borderRadius: '5px', border: '0px'}}>Trigger BB Calculation</button>
                        <button onClick={() => setIsAddFieldModalOpen(true)} style={{outline: 'none', backgroundColor: '#0EB198', color: 'white', padding: '5px 10px', borderRadius: '5px', border: '0px ', margin: '0 10px'}}>Add Other Info</button>
                    </div>
                </div>
                <div>
                    <DynamicTableComponents
                        data={baseFilePreviewData?.baseData?.data}
                        columns={baseFilePreviewData?.baseData?.columns}
                        enableStickyColumns={true}
                        showSettings={true}
                        showCellDetailsModal={true}
                        enableColumnEditing={true}
                        onChangeSave={handleSaveEdit}
                        getCellDetailFunc={getCellDetail}
                        cellDetail={cellDetail}
                        refreshDataFunction={handleBaseDataPreview}
                    />
                </div>
            </div>
            <AddOtherInfo isOpen={isAddFieldModalOpen} onClose={() => setIsAddFieldModalOpen(false)}/>
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
