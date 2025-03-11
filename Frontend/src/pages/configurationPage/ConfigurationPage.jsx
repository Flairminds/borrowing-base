import { Tabs } from 'antd';
import React from 'react';
import { configurationTabs } from '../../utils/constants/configurationConstants';
import styles from './ConfigurationPage.module.css';

export const ConfigurationPage = () => {

	const onChange = (key) => {
		console.info(key);
	};

	return (
		<div style={{padding: '15px'}}>
			<Tabs
				type="card"
				defaultActiveKey="2"
				items={configurationTabs}
				onChange={onChange}
				className={styles.configTabs}
			/>
		</div>
	);
};
