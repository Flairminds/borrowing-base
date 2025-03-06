import { Modal } from 'antd';
import React, { useState } from 'react';
import ButtonStyles from "../../components/Buttons/ButtonStyle.module.css";
import { assetInventory } from "../../utils/asset";
import styles from "./AssestInventory.module.css";

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
          title={<span style={{ color: '#909090', fontWeight: '500', fontSize: '14px', padding: '0 0 0 3%' }}>Asset Inventory</span>}
          centered
          visible={isAssetInventoryModal}
          width={'70%'}
          footer={[
            <div key="footer-buttons" className="px-4">
              <button key="cancel" onClick={handleCancel} className={ButtonStyles.outlinedBtn}>
                Cancel
              </button>
            </div>
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