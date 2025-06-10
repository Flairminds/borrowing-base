import React from 'react';
import { UIComponents } from '../uiComponents';

export const DataMapping = ({ selectedFund, selectedDate, selectedFiles }) => {
  return (
    <div>
      <div style={{ fontWeight: 600, fontSize: 18, marginBottom: 16 }}>Data mapping</div>
      <div style={{ background: '#f6ffed', borderRadius: 8, padding: 16, marginBottom: 16 }}>
        <span>Fund: <span style={{ color: '#13c2c2', fontWeight: 600 }}>{selectedFund}</span></span>
        <span style={{ marginLeft: 24 }}>Report Date: <span style={{ color: '#13c2c2', fontWeight: 600 }}>{selectedDate ? selectedDate.format('YYYY-MM-DD') : ''}</span></span>
      </div>
      <div style={{ fontWeight: 500, marginBottom: 8 }}>Data mapping</div>
      <div>This is where the data mapping interface will go. You can design forms or tools to map fields from the selected files.</div>
      <ul style={{ marginTop: 8 }}>
        {selectedFiles.map(file => (
          <li key={file}>Mapping for: <a href="#">{file}</a></li>
        ))}
      </ul>
    </div>
  );
}; 