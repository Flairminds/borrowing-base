import {Modal } from 'antd';
import { useEffect, useState } from 'preact/hooks';
import React from 'react';
import ButtonStyles from "../../components/Buttons/ButtonStyle.module.css";
import { intermediateMetricsTable } from '../../services/api';
import { PreviewTable } from '../previewModal/PreviewTable';

export const AboutModal = ({isAboutModalState, aboutModalState, baseFile}) => {

	const [intermediateMetrics, setIntermediateMetrics] = useState();

	const handleCancel = () => {
		isAboutModalState(false);
	};

	useEffect(() => {
		const getMediateMetrics = async () => {
			try {
				const res = await intermediateMetricsTable(baseFile.id);
				setIntermediateMetrics(res.data);
			} catch (err) {
				console.error(err);
			}
		};
		getMediateMetrics();
	}, []);

	return (
		<>
			<Modal
				title={<span style={{ color: '#909090', fontWeight: '500', fontSize: '14px', padding: '0 0 0 3%' }}></span>}
				centered
				open={aboutModalState}
				// onOk={handleOk}
				onCancel={handleCancel}
				width={'50%'}
				footer={[
					<div key="footer-buttons" className="px-4">
						<button key="back" onClick={handleCancel} className={ButtonStyles.outlinedBtn}>
							Cancel
						</button>
					</div>
				]}
			>
				<>
					<PreviewTable />
				</>
			</Modal>
		</>
	);
};
