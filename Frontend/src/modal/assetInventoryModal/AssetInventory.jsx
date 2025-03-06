import { Modal } from 'antd';
import React, { useState } from 'react';
import ButtonStyles from "../../components/uiComponents/Button/ButtonStyle.module.css";
import { assetInventory } from "../../utils/asset";
import styles from "./AssestInventory.module.css";
import { ModalComponents } from '../../components/modalComponents';

export const AssetInventory = ({ isAssetInventoryModal, setIsAssetInventoryModal }) => {
	const [selectedSheet, setSelectedSheet] = useState('Included');

	const handleCancel = () => {
		setIsAssetInventoryModal(false);
	};

	const previewSheets = Object.keys(assetInventory);

	const { columns, data } = assetInventory[selectedSheet];

	return (
		<div>
			<Modal
				title={<ModalComponents.Title title='Asset Inventory' />}
				centered
				visible={isAssetInventoryModal}
				width={'70%'}
				footer={[<ModalComponents.Footer key='footer-buttons' onClickCancel={handleCancel} showSubmit={false} />
				]}
			>
				<div className={styles.tabsContainer}>
					{previewSheets.map(sheet => (
						<button
							key={sheet}
							onClick={() => setSelectedSheet(sheet)}
							className={selectedSheet === sheet ? styles.activeTab : styles.tab}
						>
							{sheet}
						</button>
					))}
				</div>

				<div className={styles.tableContainer}>
					<table className={styles.table}>
						<thead className={styles.stickyHeader}>
							<tr className={styles.headRow}>
								{columns.map((column, index) => (
									<th key={index} className={styles.th}>{column.title}</th>
								))}
							</tr>
						</thead>
						<tbody>
							{data.map((row, rowIndex) => (
								<tr key={rowIndex} className={rowIndex === data.length - 1 ? `${styles.totalRow} ${styles.lastRow}` : styles.td}>
									{columns.map((column, colIndex) => (
										<td key={colIndex} className={styles.td}>{row[column.key]}</td>
									))}
								</tr>
							))}
						</tbody>
					</table>
				</div>
			</Modal>
		</div>
	);
};

export default AssetInventory;