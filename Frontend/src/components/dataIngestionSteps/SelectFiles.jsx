import React from 'react';
import { DynamicTableComponents } from '../reusableComponents/dynamicTableComponent/DynamicTableComponents';

export const SelectFiles = ({ uploadedFiles, selectedFiles, setSelectedFiles }) => {
  const columns = [
    { key: 'select', label: 'SELECT', isEditable: false },
    { key: 'date', label: 'REPORT DATE', isEditable: false },
    { key: 'fund', label: 'FUND', isEditable: false },
    { key: 'name', label: 'FILE NAME', isEditable: false },
    { key: 'uploadedBy', label: 'UPLOADED BY', isEditable: false }
  ];

  const handleCheckboxClick = (name) => {
    if (selectedFiles.includes(name)) {
      setSelectedFiles(selectedFiles.filter(f => f !== name));
    } else {
      setSelectedFiles([...selectedFiles, name]);
    }
  };

  const data = uploadedFiles.map(file => ({
    ...file,
    select: {
      value: selectedFiles.includes(file.name),
      meta_info: {
        isEditable: true,
        display_value: <input 
          type="checkbox" 
          checked={selectedFiles.includes(file.name)}
          onChange={() => handleCheckboxClick(file.name)}
        />
      }
    }
  }));

  return (
    <div>
      <div style={{ fontWeight: 600, fontSize: 18, marginBottom: 16 }}>Select files for extraction</div>
      <DynamicTableComponents
        data={data}
        columns={columns}
        showSettings={false}
      />
    </div>
  );
}; 