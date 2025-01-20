import { updateAssetDefaultColumnsData } from "../constants/constants";

export const updateDataAfterChange = (data, investment_name, colKey, sheetname, updatedValue) => {
    if (data?.table_data[sheetname]) {
        data?.table_data[sheetname].data.forEach(element => {
            if (element[updateAssetDefaultColumnsData[sheetname]] == investment_name) {
                element[colKey] = updatedValue;
            }
        });
    }
    return data;
};

export const addAssetAtIndex = (data, effectiveIndex, uniqueValue, uniqueKey, selectedSheet) => {
    const tableData = data;

    const keys = tableData.table_data[selectedSheet].columns.map(column => column.key);
    const newInvestment = {};
    keys.forEach(key => {
        newInvestment[key] = key === uniqueKey ? uniqueValue : "";
    });

    const updatedData = {
        ...data,
        table_data: {
            ...data.table_data,
            [selectedSheet]: {
                ...data.table_data[selectedSheet],
                data: [...data.table_data[selectedSheet].data]
            }
        }
    };

    updatedData.table_data[selectedSheet].data.splice(effectiveIndex, 0, newInvestment);

    return updatedData;

};


export const deleteAssetAtIndex = (data, effectiveIndex, uniqueKey, selectedSheet) => {
    const updatedData = {
        ...data,
        table_data: {
            ...data.table_data,
            [selectedSheet]: {
                ...data.table_data[selectedSheet],
                data: [...data.table_data[selectedSheet].data]
            }
        }
    };

    const valueToreturn = updatedData.table_data[selectedSheet].data[effectiveIndex][uniqueKey];

    updatedData.table_data[selectedSheet].data.splice(effectiveIndex, 1);

    return {
        updatedData: updatedData,
        rowName: valueToreturn
    };
};

export const duplicateAsset = (data, effectiveIndex, uniqueValue, uniqueKey, selectedSheet) => {
    const tableData = data;
    const duplicatedAssetIndex = effectiveIndex - 1;

    const changesArray = [];

    const keys = tableData.table_data[selectedSheet].columns.map(column => column.key);
    const colNames = tableData.table_data[selectedSheet].columns.map(column => column.label);
    const newInvestment = {};
    keys.forEach((key, index) => {
        newInvestment[key] = key === uniqueKey ? uniqueValue : tableData.table_data[selectedSheet].data[duplicatedAssetIndex][key];
        changesArray.push({
            row_name: uniqueValue,
            column_name: colNames[index],
            updated_value: tableData.table_data[selectedSheet].data[duplicatedAssetIndex][key]
        });
    });

    const updatedData = {
        ...data,
        table_data: {
            ...data.table_data,
            [selectedSheet]: {
                ...data.table_data[selectedSheet],
                data: [...data.table_data[selectedSheet].data]
            }
        }
    };

    updatedData.table_data[selectedSheet].data.splice(effectiveIndex, 0, newInvestment);


    return {
        updatedTableData: updatedData,
        duplicatechangesArray: changesArray
    };
};

export const getLatestPrevValue = (PrevChanges, currdata, rowName, columnName) => {
        let latestEntry = null;
        let data = [];

        if (PrevChanges) {
            data = [...PrevChanges, ...currdata];
        } else {
            data = currdata;
        }
        data.forEach(entry => {
            if (entry.row_name === rowName && entry.column_name === columnName) {
                latestEntry = entry;
            }
        });

        if (latestEntry) {
            const prevValue = isNaN(latestEntry.prev_value) ? latestEntry.prev_value?.replace(/,/g, '') : latestEntry.prev_value;
            const updatedValue = isNaN(latestEntry.updated_value) ? latestEntry.updated_value?.replace(/,/g, '') : latestEntry.updated_value;

            if (prevValue && updatedValue && !isNaN(prevValue) && !isNaN(updatedValue)) {
                const prevNumber = parseFloat(prevValue);
                const updatedNumber = parseFloat(updatedValue);

                if (updatedNumber !== 0) {
                    const percentageChange = ((updatedNumber - prevNumber) / updatedNumber) * 100;
                    return `${latestEntry.prev_value} | ${percentageChange.toFixed(2)}%`;
                }
            }

            return latestEntry.prev_value ? latestEntry.prev_value : null;
        }
        return null;
    };