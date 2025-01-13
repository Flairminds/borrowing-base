import React, { useEffect, useState } from "react";
import { useNavigate } from 'react-router';
import CrossIcon from '../../assets/CrossIcon.svg';
import RightIcon from '../../assets/RightIcon.svg';
import { BackOption } from '../../components/BackOption/BackOption';
import { CustomButton } from "../../components/custombutton/CustomButton";
import { DynamicTableComponents } from '../../components/reusableComponents/dynamicTableComponent/DynamicTableComponents';
import { AddSecurityMapping } from "../../modal/addSecurityMapping/AddSecurityMapping";
import { getSecurityMappingData, editPfltSecMapping } from "../../services/dataIngestionApi";
import { showToast } from "../../utils/helperFunctions/toastUtils";
import styles from "./SecurityMapping.module.css";

export const SecurityMapping = () => {
    const navigate = useNavigate();
    const [data, setData] = useState([]);
    const [columns, setColumns] = useState([]);
    const [editingCell, setEditingCell] = useState(null);
    const [tempValue, setTempValue] = useState("");
    const [unmappedSecurities, setUnmappedSecurities] = useState([]);
    const [filteredData, setFilteredData] = useState([]);
    const [isModalOpen, setIsModalOpen] = useState(false);

    // Fetch mapping data
    const getMappingData = async () => {
        try {
            const mappingRes = await getSecurityMappingData();
            const { data, columns, unmapped_securities } = mappingRes.data.result;
            setData(data);
            setFilteredData(data);
            setColumns(columns);
            setUnmappedSecurities(unmapped_securities);
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
        const updatedData = [...filteredData];
        const changes = [
            {
                id: updatedData[rowIndex].id,
                [colKey]: tempValue
            }
        ];

        try {
            await editPfltSecMapping(changes);
            updatedData[rowIndex][colKey] = tempValue;
            setFilteredData(updatedData);
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

    const filterData = (val) => {
        const temp = data.filter(d => (d.cashfile_security_name && d.cashfile_security_name.toLowerCase().includes(val.toLowerCase())) || (d.master_comp_security_name && d.master_comp_security_name.toLowerCase().includes(val.toLowerCase())));
        setFilteredData(temp);
    };

    return (
        <div className={styles.pageContainer}>
            <div className={styles.soiMappingPage}>
                <div style={{ display: 'flex' }}>
                    <div className={styles.mappingContainer}>
                        <div className={styles.navContainer}>
                            <div className={styles.backOptionContainer}>
                                <BackOption onClick={() => navigate('/base-data-list')}
                                    text={`<- Base Data`} />
                            </div>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', minWidth: '300px' }}>
                                <input type="text" style={{ outline: 'none', border: '1px solid #DCDEDE', borderRadius: '5px', width: '100%', fontSize: 'small', padding: '0.5rem' }} onChange={(e) => filterData(e.target.value)} placeholder="Search by security name" />
                                <CustomButton isFilled={true} text="Add" onClick={() => setIsModalOpen(true)} />
                            </div>
                        </div>
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
                                    {filteredData?.map((row, rowIndex) => (
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
                                                        title={row[col.key]}
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
                    <div style={{ margin: '0 2rem', border: '1px solid #DCDEDE' }}>
                        <DynamicTableComponents data={unmappedSecurities} columns={[{ 'key': 'cashfile_securities', 'label': 'Unmapped Cashfile Securities' }]} />
                    </div>
                </div>
            </div>
            <AddSecurityMapping isOpen={isModalOpen} columns={columns} onClose={() => setIsModalOpen(false)} getMappingData={getMappingData}/>
        </div>
    );
};
