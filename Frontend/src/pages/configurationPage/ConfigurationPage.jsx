import { Tabs } from 'antd';
import React, { useEffect, useRef, useState } from 'react';
import { useSearchParams } from "react-router-dom";
import { GenericDragnDropMapping } from '../../layouts/configurationPageTabs/genericDragnDropmapping/GenericDragnDropMapping';
import { SecurityMappingPage } from '../../layouts/configurationPageTabs/securityMappingPage/SecurityMappingPage';
import { uniqueMappingValues } from '../../utils/constants/configurationConstants';
import styles from './ConfigurationPage.module.css';
import { Icons } from '../../components/icons';

const TabPaneWrapper = ({
	children,
	description,
	...props
}) => {
	return (
		<div style={{padding: '0 10px'}} {...props}>
			<p style={{ color: '#909090', margin: '0 0 10px 0'}}>
				{/* <Icons.InfoIcon title='' style={{margin: '0 5px 0 0'}} /> */}
				{description}
			</p>
			<div>
				{children}
			</div>
		</div>
	);
};

const tabItemStyle = {
	fontSize: '14px',
	color: '#888',
	padding: '10px 20px',
	fontWeight: 'normal'
};

export const ConfigurationPage = () => {
	const [activeMappingType, setActiveMappingType] = useState(uniqueMappingValues["1"]);
	const [defaultKey, setDefaultKey] = useState(null);
	const [searchParams, setSearchParams] = useSearchParams();
	const selectedSecurities = useRef([]);


	const tabItems = [
		{
			key: "1",
			label: "Security Mapping",
			lookup: 'security_mapping',
			tabStyle: tabItemStyle,
			children: <TabPaneWrapper description={"Map the securities from the cashfile to the mastercomp source files to combine the data for base data extraction."}><SecurityMappingPage selectedSecurities={selectedSecurities} /></TabPaneWrapper>
		},
		{
			key: "2",
			label: "Loan Type Mapping",
			lookup: 'loan_type_mapping',
			children: <TabPaneWrapper description={"Map the different loan types from the source files to standardised master loan types."}><GenericDragnDropMapping activeMappingType={activeMappingType} /></TabPaneWrapper>
		},
		{
			key: "3",
			label: "Lien Type Mapping",
			lookup: 'lien_type_mapping',
			children: <TabPaneWrapper description={"Map the different lien types from the source files to standardised master lien types."}><GenericDragnDropMapping activeMappingType={activeMappingType} /></TabPaneWrapper>
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
		let temp = tabItems[0].lookup;
		if (searchParams.get('tab')) {
			temp = searchParams.get('tab');
		}
		const filteredItem = tabItems.filter(item => item.lookup === temp)[0];
		onChange(filteredItem.key);
		setDefaultKey(filteredItem.key);
	}, []);

	return (
		<div style={{padding: '10px'}}>
			{defaultKey &&
			<Tabs
				defaultActiveKey={defaultKey}
				items={tabItems}
				onChange={onChange}
				className={styles.configTabs}
			/>}
		</div>
	);
};
