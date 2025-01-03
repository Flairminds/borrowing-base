import { Modal, Select, Button } from 'antd';
import React, { useEffect, useState } from 'react';
import { DynamicTableComponents } from '../../components/reusableComponents/dynamicTableComponent/DynamicTableComponents';
import { postSourceFileData } from '../../services/dataIngestionApi';
import { showToast } from '../../utils/helperFunctions/toastUtils';
import styles from './SourceFileModal.module.css';

const { Option } = Select;

export const SourceFileModal = ({ isVisible, onClose, fileDetails }) => {
    const [sourceFileData, setsourceFileData] = useState({});
    const [selectedSheet, setSelectedSheet] = useState('');
    const [sheetOptions, setSheetOptions] = useState([]);

    // Static mapping for sheets by file type
    const staticSheetMapping = {
        Cash: ["US Bank Holdings", "Client Holdings"],
        'Master Comp': ["Borrower Stats", "Securities Stats", "PFLT Borrowing Base"]
    };

    const fetchSourceFileData = async (sheetName) => {
        try {
            const payload = {
                source_file_id: fileDetails?.file_id,
                source_file_type: fileDetails?.file_type,
                sheet_name: sheetName,
            };

            const response = await postSourceFileData(payload);
            setsourceFileData({ ...response.data.result });
            showToast('success', 'Source file data fetched successfully');
        } catch (error) {
            showToast('error', error.response?.data?.message || 'Failed to fetch source file data');
        }
    };

    useEffect(() => {
        if (fileDetails?.file_type) {
            const sheets = staticSheetMapping[fileDetails.file_type] || [];
            setSheetOptions(sheets);
            if (sheets.length > 0) {
                const defaultSheet = sheets[0];
                setSelectedSheet(defaultSheet);
                fetchSourceFileData(defaultSheet); // Call API with default value
            }
        }
    }, [fileDetails]);

    const handleSheetChange = (value) => {
        setSelectedSheet(value);
        fetchSourceFileData(value); // Call API on dropdown value change
    };

    return (
     <Modal
    title="File Details"
    open={isVisible}
    onCancel={onClose}
    footer={[
        <Button
            key="cancel"
            onClick={onClose}
            className={styles.outlinedBtn}
        >
            Cancel
        </Button>
    ]}
    width={'85%'}
    style={{height: '85vh'}}
    centered
>
    <div className={styles.modalContent}>
        {sheetOptions.length > 0 && (
            <div className={styles.sheetSelector}>
                <label><strong>Select Sheet Name:</strong></label>
                <Select
                    style={{ width: '200px', margin: '0px 10px' }}
                    value={selectedSheet}
                    onChange={handleSheetChange}
                >
                    {sheetOptions.map((sheet) => (
                        <Option key={sheet} value={sheet}>
                            {sheet}
                        </Option>
                    ))}
                </Select>
            </div>
        )}
        <div className={styles.tableContainer}>
            <DynamicTableComponents
                data={sourceFileData?.data}
                columns={sourceFileData?.columns}
                sticky
            />
        </div>
    </div>
</Modal>

    );
};
