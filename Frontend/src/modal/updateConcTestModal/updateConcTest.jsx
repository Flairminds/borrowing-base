/* eslint-disable react/react-in-jsx-scope */
import { Modal, Radio } from "antd";
import { useState } from 'react';
import { UIComponents } from "../../components/uiComponents";

const UpdateConcTestModal = ({isUpdatedModalOpen, setIsUpdatedModalOpen, onSubmit, setSubmitBtnLoading, loading}) => {
	const [selectedOption, setSelectedOption] = useState('new');

	const handleCancel = () => {
		setIsUpdatedModalOpen(false);
		setSubmitBtnLoading(false);
	};

	return (
		<Modal
			title="Choose to update records"
			open={isUpdatedModalOpen}
			onCancel={handleCancel}
			footer={null}
		>
			<Radio.Group
				onChange={(e) => setSelectedOption(e.target.value)}
				value={selectedOption}
				style={{ display: 'flex', gap: '8px' }}
			>
				<Radio value="new">Update new records</Radio>
				<Radio value="both">Update new and old records</Radio>
			</Radio.Group>

			<div style={{ marginTop: 24, display: 'flex', justifyContent: 'flex-end', gap: 8 }}>
				<UIComponents.Button onClick={handleCancel} text = 'Cancel' />
				<UIComponents.Button
					isFilled = {true}
					text = 'Continue'
					onClick = {() => onSubmit(selectedOption)}
					loading = {loading}
				/>
			</div>
		</Modal>
	);
};

export default UpdateConcTestModal;