import { Modal } from "antd";
import React from "react";
import { LoaderSmall } from "../../components/uiComponents/loader/loader";

export const CellDetailsModal = ({ visible, onClose, cellDetails, isCellLoading }) => {
	return (
		<Modal style={{minWidth: '600px'}} title={!isCellLoading && cellDetails?.title} open={visible} onCancel={onClose} footer={null}>
			{isCellLoading ? <LoaderSmall /> :
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
			}
		</Modal>
	);
};

