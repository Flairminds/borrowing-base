import { Modal } from 'antd';
import React from 'react';
import { WhatifTable } from '../WhatifTable/WhatifTable';

export const WhatIfAnalysisLib = ({
	tableModal,
	handleOk,
	handleCancel,
	setTableModal,
	whatIfAnalysisListData,
	Whatif_Columns,
	setTablesData,
	setWhatifAnalysisPerformed,
	selectedRow,
	setSelectedRow,
	simulationType,
	setSimulationType,
	whatIfAnalysisId,
	whatIfAnalysisType
}) => {
	return (
		<Modal title="What if Analysis Library"
			open={tableModal}
			onOk={handleOk}
			onCancel={handleCancel}
			width={'85%'}
			footer={[
				// <div key="footer-buttons" className="px-4">
				// <button key="back" onClick={()=>setTableModal(false)} className={ButtonStyles.outlinedBtn}>
				//     Cancel
				// </button>
				// <Button className={ButtonStyles.filledBtn} loading={loading}
				//      key="submit" type="primary" style={{ backgroundColor: '#0EB198' }}
				// >
				//     Use
				// </Button>
				// </div>
			]}
		>
			<WhatifTable setTableModal={setTableModal} whatIfAnalysisListData={whatIfAnalysisListData} data={whatIfAnalysisListData} columns={Whatif_Columns}
				setTablesData={setTablesData} setWhatifAnalysisPerformed={setWhatifAnalysisPerformed} selectedRow={selectedRow} setSelectedRow={setSelectedRow} simulationType={simulationType} setSimulationType={setSimulationType}
				whatIfAnalysisId={whatIfAnalysisId} whatIfAnalysisType={whatIfAnalysisType}
			/>
		</Modal>
	);
};
