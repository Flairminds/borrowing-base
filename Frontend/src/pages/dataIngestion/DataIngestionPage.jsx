import React, { useEffect, useState } from 'react';
import { CustomButton } from '../../components/custombutton/CustomButton';
import { UploadExtractionFiles } from '../../modal/dataIngestionModals/uploadFilesModal/UploadExtractionFiles';
import { getBlobFilesList } from '../../services/dataIngestionApi';
import { showToast } from '../../utils/helperFunctions/toastUtils';
import styles from './DataIngestionPage.module.css';

export const DataIngestionPage = ({dataIngestionFileList, setDataIngestionFileList}) => {

    const [uploadFilesPopupOpen, setUploadFilesPopupOpen] = useState(false);
    const [selectedIds, setSelectedIds] = useState([]);
    const [fileExtractionLoading, setFileExtractionLoading] = useState(false)

    useEffect(() => {
        blobFilesList();
    }, []);

    const blobFilesList = async() => {
        try {
            const fileresponse = await getBlobFilesList();
            setDataIngestionFileList(fileresponse.data.result);
        } catch (err) {
            console.error(err);
            showToast("error", err.response.data.message);
        }
    };

    const handleCheckboxClick = (fileId) => {
        if (selectedIds.indexOf(fileId) === -1) {
            setSelectedIds([...selectedIds, fileId]);
        } else {
            setSelectedIds(selectedIds.filter(id => id !== fileId));
        }
    };

    const handleFileExtraction = () => {
        console.info(selectedIds, 'ids');
        setFileExtractionLoading(true);
        setTimeout(() => {
            setFileExtractionLoading(false);
        }, 2000);
    };

  return (
    <>
    <div className={styles.ingestionPageContainer}>
        <div className={styles.ingestionPage}>
                <div className={styles.uploadBtnContainer}>
                    <CustomButton
                        isFilled={true}
                        onClick={() => setUploadFilesPopupOpen(true)}
                        text='Upload a File'
                    />
                </div>

            <div className={styles.containerParent}>
                <div className={styles.tableContainer}>
                    <table className={styles.table}>
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
                    </table>

                </div>
            </div>

                <div className={styles.extractDataBtn}>
                    <CustomButton
                        isFilled={true}
                        onClick={handleFileExtraction}
                        text='Extract Base Data'
                        loading={fileExtractionLoading}
                        loadingText="Extracting Base Data File"
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
