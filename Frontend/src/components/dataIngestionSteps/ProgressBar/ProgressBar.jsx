import { CalendarOutlined, UploadOutlined, FolderOpenOutlined, ProfileOutlined, SettingOutlined } from '@ant-design/icons';
import React from 'react';
import styles from './ProgressBar.module.css';

const ProgressBar = ({ currentStep }) => {
	const steps = [
		{ icon: <CalendarOutlined />, label: 'Select Fund & Date' },
		{ icon: <UploadOutlined />, label: 'Upload source files' },
		{ icon: <FolderOpenOutlined />, label: 'Select files for extraction' },
		{ icon: <ProfileOutlined />, label: 'Data mapping' },
		{ icon: <SettingOutlined />, label: 'Extract Base data' },
	];

	const getStepStatus = (index) => {
		if (index === currentStep) return 'active';
		if (index < currentStep) return 'completed';
		return '';
	};

	// Calculate positions for line segments
	const getLineSegments = () => {
		const segments = [];
		const stepWidth = 80 / (steps.length - 1); // Width between each step

		// Add a segment for each completed step
		for (let i = 0; i < currentStep; i++) {
			const segmentStart = i * stepWidth + 10;
			segments.push({
				left: `${segmentStart}%`,
				width: `${stepWidth}%`
			});
		}

		return segments;
	};

	return (
		<div className={styles.progressBar}>
			<div className={styles.progressLine} />
			{getLineSegments().map((segment, index) => (
				<div
					key={index}
					className={styles.progressLineSegment}
					style={{
						left: segment.left,
						width: segment.width
					}}
				/>
			))}
			{steps.map((step, index) => (
				<div key={index} className={styles.progressStep}>
					<div className={styles.stepIconContainer}>
						<div className={`${styles.stepIcon} ${styles[getStepStatus(index)]}`}>
							{step.icon}
						</div>
					</div>
					<div className={`${styles.stepLabel} ${currentStep === index ? styles.active : ''}`}>
						{step.label}
					</div>
				</div>
			))}
		</div>
	);
};

export default ProgressBar;