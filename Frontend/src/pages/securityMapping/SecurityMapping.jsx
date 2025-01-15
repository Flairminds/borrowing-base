import React, { useEffect, useState } from "react";
import { useNavigate } from 'react-router';
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
    const [unmappedSecurities, setUnmappedSecurities] = useState([]);
    const [filteredData, setFilteredData] = useState([]);
    const [isModalOpen, setIsModalOpen] = useState(false);

    // const tempColumnData = [
    //     {
    //         "key": "soi_name",
    //         "label": "Soi name",
    //         "isEditable": false
    //     },
    //     {
    //         "key": "master_comp_security_name",
    //         "label": "Master comp security name",
    //         "isEditable": false
    //     },
    //     {
    //         "key": "family_name",
    //         "label": "Family name",
    //         "isEditable": true
    //     },
    //     {
    //         "key": "security_type",
    //         "label": "Security type",
    //         "isEditable": false
    //     },
    //     {
    //         "key": "cashfile_security_name",
    //         "label": "Cash file security name",
    //         "isEditable": true
    //     }
    // ];


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

    // Save changes to the cell
    const handleSaveEdit = async (rowIndex, columnkey, inputValue) => {
        const updatedData = [...filteredData];
        const changes = [
            {
                id: updatedData[rowIndex].id,
                [columnkey]: inputValue
            }
        ];

        try {
            await editPfltSecMapping(changes);
            updatedData[rowIndex][columnkey] = inputValue;
            setFilteredData(updatedData);
            return {success: "failure", msg: "Update success"};
        } catch (error) {
            showToast("error", error?.response?.data?.message || "Failed to update data");
            return {success: "failure", msg: error?.response?.data?.message || "Failed to update data"};
        }
    };

    const filterData = (val) => {
        const temp = data.filter(d => (d.cashfile_security_name && d.cashfile_security_name.toLowerCase().includes(val.toLowerCase())) || (d.master_comp_security_name && d.master_comp_security_name.toLowerCase().includes(val.toLowerCase())) || (d.family_name && d.family_name.toLowerCase().includes(val.toLowerCase())) || (d.soi_name && d.soi_name.toLowerCase().includes(val.toLowerCase())));
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
                                <CustomButton isFilled={true} text="+ Add" onClick={() => setIsModalOpen(true)} />
                            </div>
                        </div>
                        <div className={styles.tableContainer}>
                            <DynamicTableComponents
                                data={filteredData && filteredData}
                                setData ={setFilteredData}
                                columns={columns}
                                enableSecurityMapping={true}
                                enableColumnEditing={true}
                                onChangeSave={handleSaveEdit}
                            />
                        </div>
                    </div>
                    <div style={{ margin: '0 2rem', border: '1px solid #DCDEDE', height: '80vh', overflow: 'auto' }}>
                        <DynamicTableComponents data={unmappedSecurities} columns={[{ 'key': 'cashfile_securities', 'label': `${unmappedSecurities.length} Unmapped Cashfile Securities` }]} />
                    </div>
                </div>
            </div>
            <AddSecurityMapping isOpen={isModalOpen} columns={columns} onClose={() => setIsModalOpen(false)} getMappingData={getMappingData}/>
        </div>
    );
};
