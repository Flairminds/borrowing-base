import { Tabs } from 'antd';
import React, { useState } from 'react';
import { uniqueMappingValues } from '../../utils/constants/configurationConstants';
import { GenericDragnDropMapping } from '../configurationPageTabs/genericDragnDropmapping/GenericDragnDropMapping';
import styles from './ConfigurationPage.module.css';

export const ConfigurationPage = () => {
	const [activeMappingType, setActiveMappingType] = useState(uniqueMappingValues["2"]);

	const onChange = (key) => {
		if (uniqueMappingValues[key]) {
			setActiveMappingType(uniqueMappingValues[key]);
		}
	};

	return (
		<div style={{padding: '15px'}}>
			<Tabs
				type="card"
				defaultActiveKey="2"
				items={[
					{
						key: "1",
						label: "Security Mapping",
						children: "Security Mapping UI"
					},
					{
						key: "2",
						label: "Loan Type Mapping",
						children: <GenericDragnDropMapping activeMappingType={activeMappingType} />
					},
					{
						key: "3",
						label: "Lien Type Mapping",
						children: <GenericDragnDropMapping activeMappingType={activeMappingType} />
					}
				]}
				onChange={onChange}
				className={styles.configTabs}
			/>
		</div>
	);
};
