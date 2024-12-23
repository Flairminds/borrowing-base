
export const convertToDropdownOptions = (dropdownValues) => {
    const resultArray = dropdownValues.map((value) => {
        return {
            value: value,
            label: value
        };
    });

    return resultArray;
};

export const getConcTestChnages = (oldData, newData) => {
    const changes = [];

    newData.data.forEach((newItem ,index) => {
        // const oldItem = oldData.data.find(item => item.fund_test_id === newItem.fund_test_id);
        // if (oldItem) {
            let diff = {};
            Object.keys(newItem).forEach(key => {
                if (newItem[key] !== oldData?.data[index][key] && key !== "fund_test_id") {
                    diff[key] = newItem[key];
                }
            });

            if (Object.keys(diff).length > 0) {
                changes.push({
                    fund_test_id: newItem.fund_test_id,
                    ...diff
                });
            }
        // }
    });

    return changes;
}

export const styledDropdownOptions = (data) => {
    const resultOptionArray = data.map((el) => ({
        label: el.test_name,
        description: el.description,
        fund_test_id: el.fund_test_id,
        value: `${el.test_name}||${el.fund_test_id}`
    }));

    return resultOptionArray;
}


export const ConcentrationTestTableData = {
    'data': [
        {
            testname: "Test 1",
            limitValue: 10,
            visibleOndashboard: true
        },
        {
            testname: "Test 2",
            limitValue: 20,
            visibleOndashboard: true
        },
        {
            testname: "Test 3",
            limitValue: 10,
            visibleOndashboard: true
        },
        {
            testname: "Test 4",
            limitValue: 10,
            visibleOndashboard: true
        },
        {
            testname: "Test 5",
            limitValue: 10,
            visibleOndashboard: true
        },
        {
            testname: "Test 6",
            limitValue: 10,
            visibleOndashboard: true
        }
    ],
    'columns': [
        {
            key: 'testname',
            label: "Test Name"
        },
        {
            key: 'limitValue',
            label: "Limit Value"
        },
        {
            key: 'visibleOndashboard',
            label: "Visible on Dashboard"
        }

    ]
};
