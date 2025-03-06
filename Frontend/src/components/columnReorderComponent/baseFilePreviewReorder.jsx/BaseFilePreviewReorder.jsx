import { MenuOutlined } from '@ant-design/icons';
import React, { useState } from 'react';
import { DndProvider, useDrag, useDrop } from 'react-dnd';
import { HTML5Backend } from 'react-dnd-html5-backend';
import { updateColumnsOrder } from '../../../services/dataIngestionApi';
import { showToast } from '../../../utils/helperFunctions/toastUtils';
import { CustomButton } from '../../uiComponents/Button/CustomButton';
import styles from './BaseFilePreviewReorder.module.css';

const ItemType = "COLUMN";

const DraggableColumn = ({ column, index, moveColumn }) => {
	const [, ref, drag] = useDrag({
		type: ItemType,
		item: { index }
	});

	const [, drop] = useDrop({
		accept: ItemType,
		hover: (item) => {
			if (item.index !== index) {
				moveColumn(item.index, index);
				item.index = index;
			}
		}
	});

	return (
		<div
			ref={(node) => drop(ref(node))}
			className={styles.columnItem}
			style={{
				display: "flex",
				justifyContent: "space-between",
				alignItems: "center",
				padding: "8px",
				border: "1px solid #ddd",
				marginBottom: "4px",
				backgroundColor: "#f9f9f9",
				cursor: "pointer"
			}}
		>
			<span>{column}</span>
			<MenuOutlined
				style={{ margin: "5px 7px", cursor: "grab" }}
				ref={drag}
			/>
		</div>
	);
};


export const BaseFilePreviewReorder = ({selectedColumns, totalColumnsData, refreshDataFunction}) => {

	const [columns, setColumns] = useState(selectedColumns);

	const reorderColumns = async() => {
		const updatedColumnOrder = columns.map((col, index) => {
			const columnMatchingData = totalColumnsData.find((c) => c.label == col);
			const columnData = {
				"bdm_id": columnMatchingData?.bdm_id,
				"sequence": index + 1,
				"col_name": columnMatchingData.label
			};
			return columnData;
		});

		try {
			const res = await updateColumnsOrder(updatedColumnOrder);
			refreshDataFunction();
			showToast("success", res.data.message);
		} catch (err) {
			console.error(err);
			showToast('error', err.response?.data?.message || 'Failed to Update');
		}
	};

	const moveColumn = (fromIndex, toIndex) => {
		const updatedColumns = [...columns];
		const [moved] = updatedColumns.splice(fromIndex, 1);
		updatedColumns.splice(toIndex, 0, moved);
		setColumns(updatedColumns);
	};


	return (
		<DndProvider backend={HTML5Backend}>
			<div className={styles.orderColumnContainer}>
				{columns.map((column, index) => (
					<DraggableColumn
						key={column}
						column={column}
						index={index}
						moveColumn={moveColumn}
					/>
				))}
			</div>
			<div className={styles.reorderBtnContainer}>
				<CustomButton text="Reorder" isFilled={true} onClick={reorderColumns} />
			</div>
		</DndProvider>
	);
};
