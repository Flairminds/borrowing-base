import React from "react";
import { UIComponents } from "../../uiComponents";

export const ModalFooter = ({ onClickCancel = () => {}, onClickSubmit = () => {}, submitText = 'Submit', loading = false, key = 'footer-buttons', showCancel = true, showSubmit = true, submitBtnDisabled = false }) => {
	return (
		<div key={key}>
			{showCancel &&
				<UIComponents.Button key={'back'} onClick={onClickCancel} text={'Cancel'} />}
			{showSubmit &&
				<UIComponents.Button key={'submit'} type="primary" onClick={onClickSubmit} loading={loading} isFilled={true} text={submitText} btnDisabled={submitBtnDisabled} />}
		</div>
	);
};