import { Button, Select } from 'antd';
import React, { useEffect, useState } from 'react';
import { toast } from 'react-toastify';
import backArrowIcon from "../../assets/assestSelection/back.svg";
import filterIcon from "../../assets/NavbarIcons/filter.svg";
import ButtonStyles from '../../components/Buttons/ButtonStyle.module.css';
import { ColumnSelectionPopup } from '../../modal/columnSelectionPopup/ColumnSelectionPopup';
import { uploadInitialFile } from '../../services/api';
import Styles from './AssetSelectionPage.module.css';
import { useNavigate } from 'react-router';

export const AssetSelectionPage = ({
    assetSelectionData,
    setAssetSelectionData,
    setTablesData,
    baseFile,
    selectedAssets,
    setSelectedAssets,
    setIsAnalysisModalOpen,
    setConstDate,
    fundType
}) => {
    const [loading, setLoading] = useState(false);
    const [isSelectAll, setIsSelectAll] = useState(true);
    const [selectOptions, setSelectOptions] = useState({});
    const [filters, setFilters] = useState({});
    const [columnSelectionPopupOpen, setColumnSelectionPopupOpen] = useState(false); // State for column selection popup
    const selectionIdentifier = assetSelectionData?.assetSelectionList?.identifier;
    const navigate = useNavigate();

    useEffect(() => {
        setIsSelectAll(selectedAssets.every(asset => asset));

        if (assetSelectionData.assetSelectionList?.columns) {
            const options = {};
            assetSelectionData.assetSelectionList.columns.forEach((col) => {
                const uniqueValues = [...new Set(assetSelectionData.assetSelectionList.data.map(item => item[col.key]))];
                options[col.key] = [
                    { label: 'All', value: '' },
                    ...uniqueValues.map(value => ({
                        label: value,
                        value: value
                    }))
                ];
            });
            setSelectOptions(options);
        }
    }, [selectedAssets, assetSelectionData]);

    const handleCheckBoxClick = (index) => {
        const newValues = [...selectedAssets];
        newValues[index] = !newValues[index];

        setSelectedAssets(newValues);
        setIsSelectAll(newValues.every(asset => asset));
    };

    const handleSelectAllClick = () => {
        const newSelectAll = !isSelectAll;
        setIsSelectAll(newSelectAll);
        setSelectedAssets(assetSelectionData.assetSelectionList?.data.map(() => newSelectAll));
    };

    const handleFilterChange = (key, value) => {
        setFilters(prevFilters => ({ ...prevFilters, [key]: value }));
    };

    const filteredData = assetSelectionData.assetSelectionList?.data.filter(row => {
        return Object.keys(filters).every(key => {
            return filters[key] ? row[key] === filters[key] : true;
        });
    });

    const openColumnSelectionPopup = () => {
        setColumnSelectionPopupOpen(true);
    };

    const CalculateResults = async () => {
        setLoading(true);
        setIsAnalysisModalOpen(false);
        const selectedAssetsList = [];
        for (let i = 0; i < assetSelectionData.assetSelectionList?.data.length; i++) {
            if (selectedAssets[i]) {
                const assetData = assetSelectionData.assetSelectionList?.data[i];
                selectedAssetsList.push(assetData[selectionIdentifier]);
            }
        }

        try {
            const fileData = {
                'base_data_file': assetSelectionData.file_name,
                'base_data_file_id': assetSelectionData.base_data_file_id,
                'user_id': assetSelectionData.user_id,
                'selected_assets': selectedAssetsList
            };
            const tableDataResponse = await uploadInitialFile(fileData);
            if (tableDataResponse.status === 200) {
                setTablesData(tableDataResponse?.data);
                setConstDate(tableDataResponse.data.closing_date);
                navigate('/');
                toast.success("Results Generated");
            }
        } catch (err) {
            setLoading(false);
            toast.error("Error in running the data.")
        }
        setLoading(false);
    };

    const backToDashboard = () => {
        navigate('/');
    };

    return (
        <>
            <div className={Styles.headingContainer}>
                <div className={Styles.backButton} onClick={backToDashboard}>
                    <img src={backArrowIcon} className={Styles.img} />
                </div>
                <h2 className={Styles.heading}>Select Assets to Calculate Borrowing Base</h2>
            </div>

            <div className={Styles.filtersContainer}>
                {assetSelectionData.assetSelectionList?.columns.map((col, index) => (
                    <div key={index} className={Styles.filterItem}>
                        <label style={{ color: "rgb(144, 144, 144)" }}>{col.label}</label>
                        <Select
                            defaultValue=""
                            style={{ width: '100%' }}
                            suffixIcon={<img style={{ width: "100%", height: "100%" }} src={filterIcon} alt="Filter Icon" />}
                            options={selectOptions[col.key]}
                            placeholder={`Select ${col.label}`}
                            onChange={(value) => handleFilterChange(col.key, value)}
                        />
                    </div>
                ))}
            </div>

            <div className={Styles.tableContainer}>
                {filteredData.length > 0 ? (
                    <table className={Styles.table}>
                        <thead>
                            <tr className={Styles.headRow}>
                                    <th className={Styles.th}>
                                        <input
                                            style={{ margin: '0rem 0.3rem' }}
                                            type="checkbox"
                                            checked={isSelectAll}
                                            onChange={handleSelectAllClick}
                                        />
                                    </th>
                                {assetSelectionData.assetSelectionList?.columns.map((col, index) => (
                                    <th key={index} className={Styles.th}>
                                        {col.label}
                                    </th>
                                ))}
                                <th style={{ cursor: "pointer" }} className={Styles.th} onClick={openColumnSelectionPopup}>
                                    +
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                            {filteredData.map((row, rowIndex) => (
                                <tr key={rowIndex}>
                                        <td style={{ paddingLeft: "0.6rem" }}>
                                            <input
                                                onClick={() => handleCheckBoxClick(assetSelectionData.assetSelectionList.data.indexOf(row))}
                                                value={selectedAssets[assetSelectionData.assetSelectionList.data.indexOf(row)]}
                                                style={{ margin: '0rem 0.3rem' }}
                                                type="checkbox"
                                                checked={selectedAssets[assetSelectionData.assetSelectionList.data.indexOf(row)]}
                                            />
                                        </td>
                                    {assetSelectionData.assetSelectionList?.columns.map((col) => (
                                        <td key={col.key} className={Styles.td}>
                                            {row[col.key]}
                                        </td>
                                    ))}
                                </tr>
                            ))}
                        </tbody>
                    </table>
                ) : (
                    <div className={Styles.heading}>No Data</div>
                )}
            </div>

            <ColumnSelectionPopup
                setAssetSelectionData={setAssetSelectionData}
                assetSelectionData={assetSelectionData}
                setSelectedAssets={setSelectedAssets}
                baseFile={baseFile}
                columnSelectionPopupOpen={columnSelectionPopupOpen}
                setColumnSelectionPopupOpen={setColumnSelectionPopupOpen}
                fundType={fundType}
            />

            <div style={{ textAlign: 'center', margin: '2rem 0rem' }}>
                <Button onClick={CalculateResults} style={{ padding: '0.2rem 0.7rem' }} loading={loading} className={ButtonStyles.filledBtn}>View Results</Button>
            </div>
        </>
    );
};
