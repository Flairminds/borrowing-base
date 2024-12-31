import React, { useEffect, useState } from "react";
import CrossIcon from '../../assets/CrossIcon.svg';
import RightIcon from '../../assets/RightIcon.svg';
import { getSecurityMappingData, editPfltSecMapping } from "../../services/dataIngestionApi";
import { showToast } from "../../utils/helperFunctions/toastUtils";
import styles from "./SecurityMapping.module.css";

export const SecurityMapping = () => {
    const [data, setData] = useState([]);
    const [columns, setColumns] = useState([]);
    const [editingCell, setEditingCell] = useState(null);
    const [tempValue, setTempValue] = useState("");

    // Fetch mapping data
    const getMappingData = async () => {
        try {
            const mappingRes = await getSecurityMappingData();
            const { data, columns } = mappingRes.data.result;
            setData(data);
            setColumns(columns);
        } catch (err) {
            showToast("error", err?.response?.data?.message || "Failed to load data");
        }
    };

    // Initialize data on component mount
    useEffect(() => {
        getMappingData();
    }, []);

    // Handle cell click to start editing
    const handleCellEdit = (rowIndex, colKey, currentValue) => {
        setEditingCell({ rowIndex, colKey });
        setTempValue(currentValue);
    };

    // Handle input value change during editing
    const handleCellChange = (e) => {
        setTempValue(e.target.value);
    };

    // Save changes to the cell
    const handleSaveEdit = async () => {
        const { rowIndex, colKey } = editingCell;
        const updatedData = [...data];
        const changes = [
            {
                id: updatedData[rowIndex].id,
                [colKey]: tempValue
            }
        ];

        try {
            await editPfltSecMapping(changes);
            updatedData[rowIndex][colKey] = tempValue;
            setData(updatedData);
            setEditingCell(null);
            setTempValue("");
            showToast("success", "Data updated successfully");
        } catch (error) {
            showToast("error", error?.response?.data?.message || "Failed to update data");
        }
    };

    // Cancel editing without saving
    const handleCancelEdit = () => {
        setEditingCell(null);
        setTempValue("");
    };

    return (
        <div className={styles.pageContainer}>
            <div className={styles.soiMappingPage}>
                <div className={styles.tableContainer}>
                    <table className={styles.table}>
                        <thead>
                            <tr className={styles.headRow}>
                                {columns?.map((col, index) => (
                                    <th key={index} className={styles.th}>
                                        {col.label}
                                    </th>
                                ))}
                            </tr>
                        </thead>
                        <tbody>
                            {data?.map((row, rowIndex) => (
                                <tr key={rowIndex}>
                                    {columns?.map((col) => {
                                        const isEditable =
                                            col.key === "family_name" || col.key === "cashfile_security_name";
                                        const isValueEmpty =
                                            (col.key === "family_name" || col.key === "cashfile_security_name") &&
                                            !row[col.key];

                                        return (
                                            <td
                                                key={col.key}
                                                className={`${styles.td} ${isValueEmpty ? styles.emptyValue : ""}`}
                                                onClick={() =>
                                                    isEditable &&
                                                    !editingCell &&
                                                    handleCellEdit(rowIndex, col.key, row[col.key])
                                                }
                                            >
                                                {editingCell?.rowIndex === rowIndex &&
                                                    editingCell?.colKey === col.key ? (
                                                    <div className={styles.editIconsContainer}>
                                                        <input
                                                            type="text"
                                                            value={tempValue}
                                                            onChange={handleCellChange}
                                                            className={styles.updateInput}
                                                            autoFocus
                                                        />
                                                        <img
                                                            src={RightIcon}
                                                            alt="Save"
                                                            className={styles.iconButton}
                                                            onClick={handleSaveEdit}
                                                        />
                                                        <img
                                                            src={CrossIcon}
                                                            alt="Cancel"
                                                            className={styles.iconButton}
                                                            onClick={handleCancelEdit}
                                                        />
                                                    </div>
                                                ) : (
                                                    row[col.key]
                                                )}
                                            </td>
                                        );
                                    })}
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};
