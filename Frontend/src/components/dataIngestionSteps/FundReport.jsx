import React from 'react';

const FundReport = ({selectedFund, selectedDate}) => {
	return (
		<div
			style={{
				backgroundColor: '#f5f6f8',
				borderRadius: 8,
				padding: '8px 16px',
				display: 'flex',
				alignItems: 'center',
				justifyContent: 'center',
				fontWeight: 500,
				fontSize: 18,
				marginBottom: '0.8rem'
			}}
		>
			<span style={{ marginRight: 16 }}>
				Fund: <span style={{ color: '#00a99d', fontWeight: 'bold' }}>{selectedFund}</span>
			</span>
			<span>
				Report Date: <span style={{ color: '#00a99d', fontWeight: 'bold' }}>{selectedDate.format('MM-DD-YYYY')}</span>
			</span>
		</div>
	);
};

export default FundReport