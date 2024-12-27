import { DatePicker } from 'antd';
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router';
import { CustomButton } from '../../components/custombutton/CustomButton';
import { UploadExtractionFiles } from '../../modal/dataIngestionModals/uploadFilesModal/UploadExtractionFiles';
import { exportBaseDataFile, getBaseDataFilesList, getBaseFilePreviewData, getBlobFilesList } from '../../services/dataIngestionApi';
import { showToast } from '../../utils/helperFunctions/toastUtils';
import styles from './DataIngestionPage.module.css';
import { DynamicTableComponents } from '../../components/reusableComponents/dynamicTableComponent/DynamicTableComponents';

export const DataIngestionPage = ({dataIngestionFileList, setDataIngestionFileList, setBaseFilePreviewData, selectedIds}) => {

    const [uploadFilesPopupOpen, setUploadFilesPopupOpen] = useState(false);
    const [previewBaseDataLoading, setPreviewBaseDataLoading] = useState(false);
    const [previewReportDate, setPreviewReportDate] = useState('');

    const navigate = useNavigate();
    let extractionInterval;

    const blobFilesList = async() => {
        try {
            const fileresponse = await getBlobFilesList();
            const responseData = fileresponse.data.result;

            const columnsToAdd = [{
                'key': 'file_select',
                'label': '',
                'render': (value, row) => <input onClick={() => handleCheckboxClick(row.file_id)} type="checkbox" />
            }];

            const updatedData = {
                ...responseData,
                columns: [...columnsToAdd, ...responseData.columns]
            };

            setDataIngestionFileList(updatedData);

            // Adding additional column for checkboxes

        } catch (err) {
            console.error(err);
            showToast("error", err.response.data.message);
        }
    };

    useEffect(() => {
        blobFilesList();
    }, []);

    const handleCheckboxClick = (fileId) => {
        if (selectedIds?.current.indexOf(fileId) === -1) {
            selectedIds.current = [...selectedIds.current, fileId];
            // setSelectedIds([...selectedIds, fileId]);
        } else {
            selectedIds.current = selectedIds?.current.filter(id => id !== fileId);
            // setSelectedIds(selectedIds.filter(id => id !== fileId));
        }
    };

    const handleFileExtraction = () => {
        // setFileExtractionLoading(true);
        try {
            // const extractionResponse = exportBaseDataFile(selectedIds.current);
            console.info(selectedIds, 'check');
            showToast("info", "Data extraction started, it might take 2-3 minutes.");
            // If needed to call immediately
            // getExtractionStatus(9);

            extractionInterval = setInterval(() => getExtractionStatus(9), 30000);
        } catch (err) {
            console.error(err);
            showToast("error", err.response.data.message);
        }

        // setFileExtractionLoading(false);
    };

    const getExtractionStatus = async (fileID) => {
        const fileDetails = {
            // "report_date": ,
            "companyId": 1,
            "baseFileId": fileID
        };

        try {
            const extractionStatusRes = await getBaseDataFilesList(fileDetails);
            const extractionStatus = extractionStatusRes.data.result.data[0].extraction_status;
            console.info(extractionStatus, 'status');
            if (extractionStatus !== "In Progress") {
                console.info(extractionStatus, 'conditionn entered');
                clearInterval(extractionInterval);
            }
            if (extractionStatus === "completed" ) {
                return true;
            }
        } catch (err) {
            showToast('failure', err?.response?.data.message);
        }

        return false;

    };

    const handleDateChange = (date, dateString) => {
        setPreviewReportDate(dateString);
      };

    const handleBaseDataPreview = async() => {
        if (!previewReportDate || previewReportDate == "") {
            showToast('warning', "Select report Date");
            return;
        }
        setPreviewBaseDataLoading(true);

        try {
            const previewDataResponse = await getBaseFilePreviewData(previewReportDate, 1);
            console.info(previewDataResponse, 'base preview ');
            setBaseFilePreviewData(previewDataResponse.data.result);
            navigate('/base-data-preview');
        } catch (err) {
            console.error(err);
            showToast("error", err.response.data.message);
        }
        setPreviewBaseDataLoading(false);
    };

  return (
    <>
        <div className={styles.ingestionPageContainer}>
            <div className={styles.ingestionPage}>
                    <div className={styles.buttonsContainer}>
                        <CustomButton
                            isFilled={true}
                            onClick={() => setUploadFilesPopupOpen(true)}
                            text='Upload a File'
                        />

                    </div>

                    <div className={styles.buttonsContainer}>
                        <DatePicker
                            placeholder='Report Date'
                            onChange={handleDateChange}
                            allowClear={true}
                        />
                        <CustomButton
                            isFilled={true}
                            onClick={handleBaseDataPreview}
                            text='Preview Base Data'
                            loading={previewBaseDataLoading}
                            loadingText="Fetching Data"
                        />
                    </div>

                    <div className={styles.tableContainer}>
                        {/* <table className={styles.table}>
                            <thead>
                                <tr className={styles.headRow}>
                                    <>
                                    <th className={styles.th}></th>
                                    {dataIngestionFileList?.columns.map((col, index) => (
                                    <th key={index} className={styles.th}>
                                        {col.label}
                                    </th>
                                    ))}
                                    </>
                                </tr>
                            </thead>
                            <tbody>
                            {dataIngestionFileList?.data?.map((row, rowIndex) => (
                                <tr key={rowIndex}>
                                <>
                                    <td className={styles.td} >
                                        <input onClick={() => handleCheckboxClick(row.file_id)} type="checkbox" />
                                    </td>
                                    {dataIngestionFileList?.columns.map((col) => (
                                        <td key={col.key} className={styles.td}>
                                        {row[col.key]}
                                        </td>
                                    ))}
                                </>
                                </tr>
                            ))}
                            </tbody>
                        </table> */}

                        <DynamicTableComponents data={dataIngestionFileList?.data} columns={dataIngestionFileList?.columns} />

                    </div>

                    <div className={styles.extractDataBtn}>
                        <CustomButton
                            isFilled={true}
                            onClick={handleFileExtraction}
                            text='Extract Base Data'
                            // loading={fileExtractionLoading}
                        />
                </div>
            </div>
        </div>


        <UploadExtractionFiles
            uploadFilesPopupOpen={uploadFilesPopupOpen}
            setUploadFilesPopupOpen={setUploadFilesPopupOpen}
            blobFilesList={blobFilesList}
        />
    </>
  );
};
