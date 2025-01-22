import { Select } from 'antd';
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router';
import { CustomButton } from '../../components/custombutton/CustomButton';
import { DynamicTableComponents } from '../../components/reusableComponents/dynamicTableComponent/DynamicTableComponents';
import { SourceFileModal } from '../../modal/sourceFileModal/SourceFileModal';
import { getBaseDataFilesList, getBaseFilePreviewData } from '../../services/dataIngestionApi';
import { fundOptionsArray } from '../../utils/constants/constants';
import { showToast } from '../../utils/helperFunctions/toastUtils';
import styles from './BaseDataFileList.module.css';

export const BaseDataFileList = ({ setBaseFilePreviewData }) => {
    const [baseDataFilesList, setBaseDataFilesList] = useState({});
    const [extractionInProgress, setExtractionInProgress] = useState(false);
    const [isPopupOpen, setIsPopupOpen] = useState(false);
    const [popupContent, setPopupContent] = useState(null);
    const [selectedFundType, setSelectedFundType] = useState(0);

    const navigate = useNavigate();

    const handleExtractNew = () => {
        navigate('/ingestion-files-list');
    };

    const handleSecurityMapping = () => {
        navigate('/security-mapping');
    };

    const handleBaseDataPreview = async (infoId) => {
        localStorage.setItem("extraction_info_id", infoId);
        try {
            const previewDataResponse = await getBaseFilePreviewData(infoId);
            const result = previewDataResponse.data?.result;
            if (result)
                setBaseFilePreviewData({
                    baseData: result.base_data_table,
                    reportDate: result.report_date,
                    baseDataMapping: result.base_data_mapping,
                    infoId: infoId
                });
            navigate('/base-data-preview');
        } catch (err) {
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


    const injectRenderForSourceFiles = (columns) => {
        return columns?.map((col) => {
            if (col.key === 'source_files') {
                return {
                    ...col,
                    render: (value, row) => (
                        <div>
                            {row.source_file_details?.map((file) => (
                                <div
                                    key={file.file_id}
                                    onClick={() => handleSourceFileClick(file)}
                                    style={{
                                        color: '#007BFF',
                                        cursor: 'pointer',
                                        textDecoration: 'underline',
                                        marginBottom: '2px'
                                    }}
                                >
                                    {file.file_name + file.extension}
                                </div>
                            ))}
                        </div>
                    )
                };
            }
            return col;
        });
    };

    const handleSourceFileClick = (fileDetails) => {
        setPopupContent(fileDetails); // Pass only the clicked file's details
        setIsPopupOpen(true);
    };

    const getFilesList = async (fundType) => {
        const Fund = (fundType === 1) ? 'PCOF' : (fundType === 2) ? 'PFLT' : undefined;
        try {
            const data = {
                "company_id": 1,
                "fund_type": Fund
            };
            const filesRes = await getBaseDataFilesList(data);
            const updatedColumns = injectRenderForSourceFiles(filesRes.data.result.columns);
            setBaseDataFilesList({ ...filesRes.data.result, columns: updatedColumns });
        } catch (err) {
            showToast('error', err?.response?.data.message);
        }
    };

    useEffect(() => {
        getFilesList(selectedFundType);
    }, [extractionInProgress]);

    setInterval(() => {
        if (extractionInProgress) {
            setExtractionInProgress(false);
        }
    }, 15000);

    useEffect(() => {
        if (baseDataFilesList && baseDataFilesList.data) {
            for (let i = 0; i < baseDataFilesList.data.length; i++) {
                if (baseDataFilesList.data[i].extraction_status == 'in progress') {
                    setExtractionInProgress(true);
                    break;
                }
            }
        }
    }, [baseDataFilesList]);

    const handleDropdownChange = (value) => {
        setSelectedFundType(value);
            getFilesList(value);
        
    };

    return (
        <div className={styles.pageContainer}>
            <div className={styles.baseFileListPage}>
                <div className={styles.headerContainer}>
                    <div className={styles.tableHeading}>
                        Base Data
                    </div>
                    <div className={styles.buttonsContainer}>
                        <div style={{margin: 'auto'}}>
                            <Select
                                defaultValue="Select Fund"
                                style={{ width: 140, borderRadius: '8px'}}
                                options={fundOptionsArray}
                                onChange={handleDropdownChange}
                            />
                        </div>
                        <CustomButton isFilled={true} onClick={handleSecurityMapping} text="Security Mapping" />
                        <CustomButton isFilled={true} onClick={handleExtractNew} text="Extract New Base Data" />
                    </div>
                </div>
                <div className={styles.baseDataTableContainer}>
                    <DynamicTableComponents data={baseDataFilesList?.data} columns={baseDataFilesList?.columns} additionalColumns={columnsToAdd} />
                </div>
            </div>
            {/* File Details Modal */}
            <SourceFileModal
                isVisible={isPopupOpen}
                onClose={() => setIsPopupOpen(false)}
                fileDetails={popupContent}
            />
        </div>
    );
};
