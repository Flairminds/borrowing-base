import React from 'react';
import { UIComponents } from '../uiComponents';
import { fundOptionsArray } from '../../utils/constants/constants';
import { DatePicker } from 'antd';

export const SelectFundDate = ({ selectedFund, setSelectedFund, selectedDate, setSelectedDate }) => {
  return (
    <div>
      <div style={{ fontWeight: 600, fontSize: 18, marginBottom: 16 }}>Select Fund and Report Date</div>
      <div style={{ marginBottom: 10 }}>Select Fund</div>
      <select 
        value={selectedFund || ''} 
        style={{ width: '100%', marginBottom: 16, padding: '8px' }}
        onChange={(e) => setSelectedFund(e.target.value)}
      >
        {fundOptionsArray.map(option => (
          <option key={option.value} value={option.label}>{option.label}</option>
        ))}
      </select>
      <div style={{ marginBottom: 10 }}>Report Date</div>
      <DatePicker
        format="DD-MM-YYYY"
        style={{ width: '100%' }}
        placeholder="dd-mm-yyyy"
        value={selectedDate}
        onChange={setSelectedDate}
      />
    </div>
  );
}; 