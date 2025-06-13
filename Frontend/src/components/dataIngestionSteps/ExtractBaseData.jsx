import React, { useEffect, useState } from 'react';

export const ExtractBaseData = ({ selectedIds, uploadedFiles }) => {
	const [ selectedFiles, setSelectedFiles ] = useState([]);

	useEffect(() => {
		const selectedList = uploadedFiles?.data?.filter(item => {
			if (selectedIds?.current.includes(item.file_id)) return item;
		});
		setSelectedFiles(selectedList);
	}, []);

	return (
		<div>
			<div style={{ fontWeight: 600, fontSize: 18, marginBottom: 16 }}>Extract Base data</div>
			<div>Ready to extract base data for the selected files.</div>
			<ul style={{ marginTop: 8 }}>
				{selectedFiles?.map((file, key) => (
					<div key={key} style={{display: 'flex'}}>
						<li key={file}>{file.file_name}</li>
					</div>
				))}
			</ul>
		</div>
	);
};