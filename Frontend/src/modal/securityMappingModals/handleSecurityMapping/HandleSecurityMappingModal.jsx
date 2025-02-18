import { Modal } from 'antd';
import React, { useEffect, useState } from 'react';
import { DynamicTableComponents } from '../../../components/reusableComponents/dynamicTableComponent/DynamicTableComponents';
import { editPfltSecMapping, getProbableSecuritiesData } from '../../../services/dataIngestionApi';
import { showToast } from '../../../utils/helperFunctions/toastUtils';
import styles from './HandleSecurityMappingModal.module.css';

export const HandleSecurityMappingModal = ({isOpen, setIsOpen, activeSecurity}) => {

	const [probableEntriesData, setProbableEntriesData] = useState();

	const handleCancel = () => {
		setIsOpen(false);
	};

	const handleMapSecurity = async (secId, cashSecurity) => {
		const mappingData = {
			"id": secId,
			"cashfile_security_name": cashSecurity
		};
		try {
			const res = await editPfltSecMapping([mappingData]);
			showToast('success', res?.data?.message);
		} catch (error) {
			showToast("error", error?.response?.data?.message || "Failed to update data");
		}
		setProbableEntriesData(null);
		setIsOpen(false);
	};

	const additionalColumns = [{
		key: "",
		label: "",
		'render': (value, row) => <div onClick={() => handleMapSecurity(row.id, activeSecurity)} style={{textAlign: 'center'}}> Use </div>
	}];

	const getProbableMappings = async() => {
		const res = await getProbableSecuritiesData(activeSecurity);
		setProbableEntriesData(res.data.result);
	};

	useEffect(() => {
		if (isOpen) {
			getProbableMappings();
		}
	}, [activeSecurity]);


	return (
		<Modal open={isOpen} onCancel={handleCancel} footer={null} width={"90%"}>
			<h5>{activeSecurity}</h5>
			<DynamicTableComponents data={probableEntriesData?.data} columns={probableEntriesData?.columns} additionalColumns={additionalColumns} />


		</Modal>
	);
};
