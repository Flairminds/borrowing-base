import { OptionArray } from "../../utils/SampleOptionsArray";

export const arrayOfObjects = (OptionArray) => {
    return OptionArray.map((value, index) => ({ InvestmentName: value.InvestmentName, previousValue: value.previousValue, updatedValue: '' , alternateValue:value.previousEbitda?value.previousEbitda: value.previousLeverage}));
};

const res = arrayOfObjects(OptionArray)