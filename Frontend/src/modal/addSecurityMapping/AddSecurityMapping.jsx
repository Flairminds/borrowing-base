import Modal from "antd/es/modal/Modal";
import React, { useState } from "react";
import { CustomButton } from "../../components/custombutton/CustomButton";
import styles from "./AddSecurityMapping.module.css";

export const AddSecurityMapping = ({ isOpen, columns, onClose }) => {
    const [formValues, setFormValues] = useState({});

    const handleInputChange = (key, value) => {
        setFormValues((prev) => ({ ...prev, [key]: value }));
    };

    const handleSave = () => {
        setFormValues({});
        onClose();
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
