import React from 'react';
import { UIComponents } from '../uiComponents';

export const DataMapping = ({ selectedFund, selectedDate, selectedFiles }) => {
  return (
    <div>
      <div style={{ fontWeight: 600, fontSize: 18, marginBottom: 16 }}>Data mapping</div>
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