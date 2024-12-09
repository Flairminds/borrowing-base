import React, { useState, useRef } from 'react';
import { Input, Space } from 'antd';

export const CurrencyInput = ({value, setValue, inputWidth, style ={}, reference }) => {
  // const [value, setValue] = useState("$");

  const customStyle = {
    width : inputWidth,
    outline : 'none',
    ...style
  }

  const formatWithCommas = (val) => {
    return val.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  };

  const onChangeFunc = (e) => {
    // Remove dollar sign and commas from the input to format the value correctly
    const inputValue = e.target.value.replace(/\$/g, "").replace(/,/g, "");
    setValue(`$${formatWithCommas(inputValue)}`);
  };

  return (
    <div>
        <Input ref={reference} value={value} onChange={(e) => onChangeFunc(e)} style={customStyle} />
    </div>
  );
};
