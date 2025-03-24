import { Tabs } from 'antd';
import React, { useEffect, useRef, useState } from 'react';
import { useSearchParams } from "react-router-dom";
import { GenericDragnDropMapping } from '../../layouts/configurationPageTabs/genericDragnDropmapping/GenericDragnDropMapping';
import { uniqueMappingValues } from '../../utils/constants/configurationConstants';
import styles from './ConfigurationPage.module.css';
import { SecurityMappingPage } from '../../layouts/configurationPageTabs/securityMappingPage/SecurityMappingPage';

export const ConfigurationPage = () => {
	const [activeMappingType, setActiveMappingType] = useState(uniqueMappingValues["1"]);
	const [searchParams, setSearchParams] = useSearchParams();
	const selectedSecurities = useRef([]);


	const tabItems = [
		{
			key: "1",
			label: "Security Mapping",
			lookup: 'security_mapping',
			children: <SecurityMappingPage selectedSecurities={selectedSecurities} />
		},
		{
			key: "2",
			label: "Loan Type Mapping",
			lookup: 'loan_type_mapping',
			children: <GenericDragnDropMapping activeMappingType={activeMappingType} />
		},
		{
			key: "3",
			label: "Lien Type Mapping",
			lookup: 'lien_type_mapping',
			children: <GenericDragnDropMapping activeMappingType={activeMappingType} />
		}
	];

	const onChange = (key) => {
		if (uniqueMappingValues[key]) {
			setActiveMappingType(uniqueMappingValues[key]);
		}
		const filteredItem = tabItems.filter(item => item.key === key)[0];
		setSearchParams({tab: filteredItem.lookup});
	};

	useEffect(() => {
		setSearchParams({tab: 'security_mapping'});
	}, []);

	return (
		<div style={{padding: '15px'}}>
			<Tabs
				type="card"
				defaultActiveKey="1"
				items={tabItems}
				onChange={onChange}
				className={styles.configTabs}
			/>
		</div>
	);
};
