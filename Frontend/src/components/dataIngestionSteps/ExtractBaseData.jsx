import React from 'react';
import { UIComponents } from '../uiComponents';

export const ExtractBaseData = ({ selectedFund, selectedDate, selectedFiles }) => {
  return (
    <div>
      <div style={{ fontWeight: 600, fontSize: 18, marginBottom: 16 }}>Extract Base data</div>
      <div style={{ background: '#f6ffed', borderRadius: 8, padding: 16, marginBottom: 16 }}>
        <span>Fund: <span style={{ color: '#13c2c2', fontWeight: 600 }}>{selectedFund}</span></span>
        <span style={{ marginLeft: 24 }}>Report Date: <span style={{ color: '#13c2c2', fontWeight: 600 }}>{selectedDate ? selectedDate.format('YYYY-MM-DD') : ''}</span></span>
      </div>
      <div>Ready to extract base data for the selected files.</div>
      <ul style={{ marginTop: 8 }}>
        {selectedFiles.map(file => (
          <li key={file}>{file}</li>
        ))}
      </ul>
    </div>
  );
}; 