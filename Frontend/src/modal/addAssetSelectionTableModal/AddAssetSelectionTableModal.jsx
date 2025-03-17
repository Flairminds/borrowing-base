import { Modal } from 'antd';
import { useEffect, useState } from 'preact/hooks';
import React from 'react';
import { AddAssetDynamicTable } from '../../components/addAssetDynamicTable/AddAssetDynamicTable';
// import ButtonStyles from "../../components/uiComponents/Button/ButtonStyle.module.css";
// import {Whatif_Columns,Whatif_data} from "../../utils/Whatif_Data"
import buttonStyle from '../../components/uiComponents/Button/ButtonStyle.module.css';
import { generateAssetFormData, generateEmptyAssetFormData } from '../../utils/helperFunctions/addAssetFormData';
import { CreateAssetModal } from '../createAssetModal/CreateAssetModal';
import { UIComponents } from '../../components/uiComponents';

export const AddAssetSelectionTableModal = ({previewModal, isPreviewModal, previewColumns, previewData, setPreviewData, setAddAssetSelectedData}) => {
	const handleCancel = () => {
		isPreviewModal(false);
	};

	const [createAssetModalOpen, setCreateAssetModalOpen] = useState(false);
	const [createAssetFormData, setCreateAssetFormData] = useState();
	const [modificationData, setModificationData] = useState({
		data: '',
		index: ''
	});


	const [selectedAssets, setSelectedAssets] = useState([]);
	const [showModifyButton, setShowModifyButton] = useState(true);


	useEffect(() => {
		setSelectedAssets(Array(previewData?.length).fill(true));
	}, [previewData]);

	const modifyAssetsData = (index, data) => {
		if (index != -1) {
			const previewDataArray = previewData;
			previewDataArray[index] = data;
			setPreviewData(previewDataArray);
		} else {
			setPreviewData([data, ...previewData]);
		}

	};

	const handleCreateAsset = () => {
		const modifiedData = generateEmptyAssetFormData();
		setShowModifyButton(false);
		setCreateAssetFormData(modifiedData);
		setCreateAssetModalOpen(true);
	};

	const handleSubmit = () => {
		const selectedData = [];
		for (let i = 0; i < previewData.length; i++) {
			if (selectedAssets[i] == true) {
				selectedData.push(previewData[i]);
			}

		}
		setAddAssetSelectedData(selectedData);
		isPreviewModal(false);
	};


	return (

		<div>
			<Modal
				title={<span style={{ color: '#909090', fontWeight: '500', fontSize: '14px', padding: '0 0 0 3%' }}></span>}
				centered
				open={previewModal}
				onOk={handleCancel}
				onCancel={handleCancel}
				width={'70%'}
				footer={[

				]}
			>
				<div style={{textAlign: 'end', padding: '1rem'}} >
					<UIComponents.Button onClick={handleCreateAsset} text='Create Asset' />
				</div>

				<div style={{height: "70vh"}}>
					<AddAssetDynamicTable data={previewData} columns={previewColumns} selectedAssets={selectedAssets} setSelectedAssets={setSelectedAssets} setModificationData={setModificationData} setCreateAssetModalOpen={setCreateAssetModalOpen} setCreateAssetFormData={setCreateAssetFormData}/>
				</div>

				<div style={{margin: '1rem', textAlign: 'end'}}>
					<UIComponents.Button onClick={handleSubmit} isFilled={true} text='Submit' />
				</div>

				<CreateAssetModal
					createAssetModalOpen={createAssetModalOpen}
					setCreateAssetModalOpen={setCreateAssetModalOpen}
					createAssetFormData={createAssetFormData}
					setCreateAssetFormData={setCreateAssetFormData}
					modifyAssetsData={modifyAssetsData}
					modificationData={modificationData}
					setModificationData={setModificationData}
					showModifyButton={showModifyButton}
					setShowModifyButton={setShowModifyButton}
				/>

			</Modal>

		</div>
	);
};
