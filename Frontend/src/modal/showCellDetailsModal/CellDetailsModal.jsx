import { Modal } from "antd";
import React from "react";

export const CellDetailsModal = ({ visible, onClose, cellDetails }) => {
	return (
		<Modal title={cellDetails?.title} open={visible} onCancel={onClose} footer={null}>
			{cellDetails && cellDetails.data && Object.keys(cellDetails?.data).map((k, i) => {
				return (
					<>
						<div>
							<strong>{k}:</strong> {cellDetails.data[k]}
						</div>
					</>
				);
			})}
		</Modal>
	);
};

