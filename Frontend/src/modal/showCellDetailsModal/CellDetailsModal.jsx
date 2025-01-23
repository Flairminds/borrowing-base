import { Modal } from "antd";
import React from "react";

export const CellDetailsModal = ({ visible, onClose, cellDetails }) => {
	return (
		<Modal style={{minWidth: '600px'}} title={cellDetails?.title} open={visible} onCancel={onClose} footer={null}>
			<div style={{padding: '1rem'}}>
				{cellDetails && cellDetails.data && Object.keys(cellDetails?.data).map((k, i) => {
					return (
						<>
							<div>
								<strong>{k}:</strong> {cellDetails.data[k]}
							</div>
						</>
					);
				})}
				<div>
					{cellDetails?.htmlRender ? cellDetails.htmlRender : <></>}
				</div>
			</div>
		</Modal>
	);
};

