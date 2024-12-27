import React, { useState } from 'react';
import stylesUload from "./ParameterChange.module.css";
import { ebitdaColumns, leverageColumns } from "../../utils/Options";
import ButtonStyles from "../../components/Buttons/ButtonStyle.module.css";
import tickIcon from "../../assets/NavbarIcons/tick.svg";
import crossIcon from "../../assets/NavbarIcons/cross.svg";

export const ParameterChange = ({ parameterList, selectedOptionUpdateValue, setParameterList, selectedIndexes, setSelectedIndexes }) => {
    const [allInputValue, setAllInputValue] = useState('');
    const OptionsColumns = selectedOptionUpdateValue === "Ebitda" ? ebitdaColumns : leverageColumns;

    const handleInputChange = (index, enteredValue) => {
        const updatedOptions = [...parameterList.data];
        const inputValue = enteredValue;
        updatedOptions[index].percent = inputValue;

        if (selectedOptionUpdateValue == "Ebitda") {
            const ebitdaValue = updatedOptions[index].Ebitda;
            const leverageValue = updatedOptions[index].Leverage;
            const inputValueFloat = parseFloat(enteredValue);

            const updateEbita = isNaN(inputValueFloat) ? '' : (ebitdaValue * (1 + inputValueFloat / 100));
            const updateLeverage = (ebitdaValue * leverageValue) / updateEbita;

            updatedOptions[index].updated_ebitda = updateEbita.toFixed(2);
            updatedOptions[index].updated_leverage = updateLeverage.toFixed(2);
        } else {
            const ebitdaValue = updatedOptions[index].Ebitda;
            const leverageValue = updatedOptions[index].Leverage;
            const inputValueFloat = parseFloat(enteredValue);

            const updateLeverage = isNaN(inputValueFloat) ? '' : (leverageValue * (1 + inputValueFloat / 100));
            const updateEbita = (ebitdaValue * leverageValue) / updateLeverage;

            updatedOptions[index].updated_leverage = updateLeverage.toFixed(2);
            updatedOptions[index].updated_ebitda = updateEbita.toFixed(2);
        }
        setParameterList({...parameterList, data: updatedOptions});

        if (selectedIndexes.includes(index)) {
            setSelectedIndexes(selectedIndexes.filter(i => i !== index));
        }
    };

    const handleSelectAll = () => {
        if (selectedIndexes?.length === parameterList?.data.length) {
            setSelectedIndexes([]);
        } else {
            const allIndexes = parameterList?.data?.map((_, index) => index);
            setSelectedIndexes(allIndexes);
        }
    };

    const handleCheckboxChange = (index) => {
        if (selectedIndexes.includes(index)) {
            setSelectedIndexes(selectedIndexes.filter(i => i !== index));
        } else {
            setSelectedIndexes([...selectedIndexes, index]);
        }
    };

    const handleCrossButtonClick = () => {
        setAllInputValue('');
    };

    const handleAddButtonClick = () => {
        const updatedOptions = parameterList.data.map((asset, index) => {
            if (selectedIndexes.includes(index)) {
                const inputValue = allInputValue;
                const inputValueFloat = parseFloat(allInputValue);
                let updateEbita, updateLeverage;

                if (selectedOptionUpdateValue == "Ebitda") {
                    const ebitdaValue = asset.Ebitda;
                    const leverageValue = asset.Leverage;
                    updateEbita = isNaN(inputValueFloat) ? '' : (ebitdaValue * (1 + inputValueFloat / 100));
                    updateLeverage = (ebitdaValue * leverageValue) / updateEbita;
                } else {
                    const ebitdaValue = asset.Ebitda;
                    const leverageValue = asset.Leverage;
                    updateLeverage = isNaN(inputValueFloat) ? '' : (leverageValue * (1 + inputValueFloat / 100));
                    updateEbita = (ebitdaValue * leverageValue) / updateLeverage;
                }

                return {
                    ...asset,
                    percent: inputValue,
                    updated_ebitda: updateEbita.toFixed(2),
                    updated_leverage: updateLeverage.toFixed(2)
                };
            }
            return asset;
        });
        setParameterList({...parameterList, data: updatedOptions});
        setAllInputValue('');
        setSelectedIndexes([]);
    };

    return (
        <div>
            <div style={{ display: "flex", justifyContent: "start", padding: "0rem 0 0.5rem 0rem", alignItems: "center" }}>
                <span>Additive Leverage Change in selected investment (%):</span>
                <input
                    placeholder='Range: -99% to 100%'
                    value={allInputValue}
                    onChange={e => setAllInputValue(e.target.value)}
                    style={{ padding: "6px", border: "none", outline: "none", borderBottom: "1px solid rgb(84 79 79)" }}
                />
                <button style={{ marginLeft: "0px", border: "none", background: "transparent" }} onClick={handleAddButtonClick}>
                    <img src={tickIcon} alt="tick" />
                </button>
                <button style={{ marginLeft: "0px", border: "none", background: "transparent" }} onClick={handleCrossButtonClick}>
                    <img src={crossIcon} alt="cross" />
                </button>
            </div>
            <div className={stylesUload.tableContainer}>
                <table className={stylesUload.table}>
                    <thead className={stylesUload.stickyHeader}>
                        <tr className={stylesUload.headRow}>
                            <th className={stylesUload.th}>
                                <input
                                    type="checkbox"
                                    checked={selectedIndexes?.length === parameterList?.data.length}
                                    onChange={handleSelectAll}
                                />
                            </th>
                            {parameterList?.columns?.map(column => (
                                <th key={column.key} className={stylesUload.th}>
                                    {column.label}
                                </th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {parameterList?.data?.map((asset, index) => (
                            <tr key={index}>
                                <td className={stylesUload.td}>
                                    <input
                                        type="checkbox"
                                        checked={selectedIndexes.includes(index)}
                                        onChange={() => handleCheckboxChange(index)}
                                    />
                                </td>
                                {parameterList?.columns?.map(column => (
                                <>
                                {
                                    column.key == 'percent' ?
                                    <td className={stylesUload.td} style={{ backgroundColor: '#EEF6FC', padding: '10px' }}>
                                        <input
                                            style={{ border: "none", padding: "3px", outline: "none", width: "100%", backgroundColor: "#EEF6FC" }}
                                            value={asset[column.key]}
                                            placeholder='Update Values'
                                            onChange={e => handleInputChange(index, e.target.value)}
                                        />
                                    </td>
                                    :
                                    <td className={stylesUload.td}>
                                        {asset[column.key]}
                                    </td>

                                }
                                </>
                                ))}
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};
