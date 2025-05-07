import { Progress } from 'antd';
import React from 'react';
import Styles from './ProgressBar.module.css';

export const ProgressBar = ({progressBarPercent}) => {
	return (
		<div className={Styles.progressContainer}>
			<Progress
				type="circle"
				percent={progressBarPercent}
				size={200}
				strokeColor={'#1EBEA5'}
				steps={{ count: 2, gap: 10 }}
				trailColor="rgba(012, 43, 0534, 0.06)"
				strokeWidth={20}
			/>
			<div className={Styles.progressStatus}>
				{progressBarPercent < 50 ?
					<>
						step 1/2 : Validating your file
					</>
					: progressBarPercent == 50 ?
						<>
							Validation Complete
						</>
						: progressBarPercent > 50 && progressBarPercent < 100 ?
							<>
								step 2/2 : Generating results
							</>
							: progressBarPercent == 100 ?
								<>
									Processing Complete
								</>
								: null}
			</div>
		</div>
	);
};
