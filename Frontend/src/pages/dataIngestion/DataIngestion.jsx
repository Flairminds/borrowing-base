
import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { BaseDataTab } from '../../layouts/dataIngestion/BaseData';
import { SourceFilesTab } from '../../layouts/dataIngestion/SourceFile';
import styles from './DataIngestionPage.module.css';

const tabItems = [
	{ key: 'baseData', label: 'Base Data', children: <BaseDataTab />, query: 'base-data' },
	{ key: 'sourceFiles', label: 'Source Files', children: <SourceFilesTab />, query: 'source-files' }
];

const DataIngestion = () => {
	const [searchParams, setSearchParams] = useSearchParams();
	const [activeKey, setActiveKey] = useState('baseData');

	useEffect(() => {
		const selectedTab = tabItems.find(tab => tab.key === activeKey);
		if (selectedTab) {
			const currentTabInUrl = searchParams.get('tab');
			if (currentTabInUrl !== selectedTab.query) {
				setSearchParams({ tab: selectedTab.query });
			}
		}
	}, [activeKey, searchParams, setSearchParams]);

	return (
		<div className={styles.dataIngestionPageContainer}>
			<div className={styles.tabs}>
				{tabItems.map(tab => (
					<div
						key={tab.key}
						className={`${styles.tab} ${activeKey === tab.key ? styles.activeTab : ''}`}
						onClick={() => setActiveKey(tab.key)}
					>
						{tab.label}
					</div>
				))}
			</div>
			<div className={styles.tabContent}>
				{tabItems.find(tab => tab.key === activeKey)?.children}
			</div>
		</div>
	);
};

export default DataIngestion;