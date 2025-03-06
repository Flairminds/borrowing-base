import React from "react";

export const ModalTitle = ({ title = 'Title', description = 'description', showDescription = false }) => {
	return (
		<div>
			<h4>{title}</h4>
			{showDescription && <p style={{ color: '#909090'}}>{description}</p>}
		</div>
	);
};