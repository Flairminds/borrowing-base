import React, { useEffect } from 'react';
import { CustomButton } from '../../components/custombutton/CustomButton';
import { getBlobFilesList } from '../../services/dataIngestionApi';
import { ingestionTableCols, ingestionTableData } from '../../utils/frontendTestingData';
import { showToast } from '../../utils/helperFunctions/toastUtils';
import styles from './DataIngestionPage.module.css';

export const DataIngestionPage = ({dataIngestionFileList, setDataIngestionFileList}) => {

    useEffect(() => {
        BlobFilesList();
    }, []);

    const BlobFilesList = async() => {
        try {
            const fileresponse = await getBlobFilesList();
            setDataIngestionFileList(fileresponse.data.result);
        } catch (err) {
            console.error(err);
            showToast("error", err.response.data.message);
        }
    };

  return (
    <div>
        <div className={styles.uploadBtnContainer}>
            <CustomButton
                isFilled={true}
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
                            <td className={styles.td}>
                                <input type="checkbox" />
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



    </div>
  );
};
