import Modal from "antd/es/modal/Modal";
import React, {useState } from "react";
import { CustomButton } from "../../components/custombutton/CustomButton";
import {postAddSecurityMapping } from "../../services/dataIngestionApi";
import { showToast } from "../../utils/helperFunctions/toastUtils";
import styles from "./AddSecurityMapping.module.css";

export const AddSecurityMapping = ({ isOpen, columns, onClose, getMappingData }) => {
    const [formValues, setFormValues] = useState({});
    const handleInputChange = (key, value) => {
        setFormValues((prev) => ({ ...prev, [key]: value }));
    };

    const handleSave = async () => {
        try {
            const payload = formValues;
            const response = await postAddSecurityMapping(payload);

            if (response.data.success) {

                const successMessage = response.data.message || 'Security mapping added successfully';
                showToast('success', successMessage);
                getMappingData();
                setFormValues({});
                onClose();
            }
        } catch (error) {
            showToast('error', error.response.data.message || 'Error: Failed to add security mapping');
        }
    };



    const handleCancel = () => {
        setFormValues({});
        onClose();
    };

    return (
        <Modal
            open={isOpen}
            onCancel={handleCancel}
            footer={null}
            width={'50%'}
        >
            <h5 style={{ textAlign: "center" }}>Add Security Mapping</h5>
            {columns.map((col) => (
                <div key={col.key} className={styles.inputContainer}>
                    <label>{col.label}</label>
                    <input
                        type="text"
                        value={formValues[col.key] || ""}
                        onChange={(e) => handleInputChange(col.key, e.target.value)}
                        required={columns.isRequired}
                    />
                </div>
            ))}
            <div className={styles.buttonContainer}>
                <CustomButton isFilled={true} text="Save" onClick={handleSave} />
                <CustomButton isFilled={false} text="Cancel" onClick={handleCancel} />
            </div>
        </Modal>
    );
};
