import React, { useState } from 'react';
import { DynamicInputComponent } from '../../components/reusableComponents/dynamicInputsComponent/DynamicInputComponent';
import { UIComponents } from '../../components/uiComponents';
import { getCompanyInfo } from '../../services/api';
import styles from './PortfolioInsights.module.css';

const fetchCompanyInfo = async (companyName, setCompanyInfo, setLoading) => {
	setLoading(true);
	try {
		const response = await getCompanyInfo({ "company_name": companyName });
		if (!response) {
			setCompanyInfo({ error: true, "error_message": 'No response from API' });
			setLoading(false);
			return;
		}
		try {
			setCompanyInfo(response.data.result.data);
		} catch (e) {
			setCompanyInfo({ error: true, error_message: 'Failed to parse company info.' });
		}
	} catch (error) {
		setCompanyInfo({ error: true, error_message: 'Error fetching data.' });
	}
	setLoading(false);
};

const PortfolioInsights = () => {
	const [companyName, setCompanyName] = useState('');
	const [companyInfo, setCompanyInfo] = useState(null);
	const [loading, setLoading] = useState(false);

	const handleSearch = () => {
		if (companyName.trim()) {
			fetchCompanyInfo(companyName, setCompanyInfo, setLoading);
		}
	};

	return (
		<div className={styles.container}>
			<div className={styles.header}>
				<div className={styles.title}>Portfolio Company Insights</div>
			</div>
			<div className={styles.searchRow}>
				<DynamicInputComponent
					inputType="text"
					placeholder="Enter company name"
					inputValue={companyName}
					onInputChange={e => setCompanyName(e.target.value)}
					autoFocusInput={true}
				/>
				<UIComponents.Button
					text="Search"
					isFilled={true}
					onClick={handleSearch}
					loading={loading}
				/>
			</div>
			{loading ? <UIComponents.LoaderSmall /> :
				<>
					{companyInfo && (
						<div>
							<p style={{fontSize: '13px'}}><i>*This content is generated using OpenAI for information purpose and may be subject to errors or omissions. Please verify independently.</i></p>
							{companyInfo.error ? (
								companyInfo.suggestions && companyInfo.suggestions.length > 0 ? (
									<div className={styles.suggestions}>
										<b>Multiple matches found. Please specify company name:</b>
										<ol>
											{companyInfo.suggestions.map((s, i) => (
												<li key={i}>{s}</li>
											))}
										</ol>
									</div>
								) : (
									<div className={styles.error}>{companyInfo.error_message}</div>
								)
							) : (
								<>
									<div className={styles.companyInfo}>
										<div className={styles.infoBlock}>
											<UIComponents.StatsCard cardData={{ key: 'company', label: 'Company Name', value: companyInfo.company_name }} />
										</div>
										<div className={styles.infoBlock}>
											<UIComponents.StatsCard cardData={{ key: 'industry', label: 'Industry', value: companyInfo.industry }} />
										</div>
										{companyInfo.parent_company && (
											<div className={styles.infoBlock}>
												<UIComponents.StatsCard cardData={{ key: 'parent', label: 'Parent Company', value: companyInfo.parent_company }} />
											</div>
										)}
									</div>
									{companyInfo.products_and_services && companyInfo.products_and_services.length > 0 && (
										<div className={styles.companyInfo}>
											<div>
												<b>Products and Services:</b>
												<ol style={{ margin: '8px 0 0 16px' }}>
													{companyInfo.products_and_services.map((p, i) => (
														<li key={i}>{p}</li>
													))}
												</ol>
											</div>
										</div>
									)}
									{companyInfo.ownership_history && companyInfo.ownership_history.length > 0 && (
										<div className={styles.companyInfo}>
											<div>
												<b>Ownership History:</b>
												<ol style={{ margin: '8px 0 0 16px' }}>
													{companyInfo.ownership_history.map((p, i) => (
														<li key={i}>
															<div>{p.date}</div>
															<div>Acquired by - {p.acquirer}</div>
															<div>{p.details}</div>
														</li>
													))}
												</ol>
											</div>
										</div>
									)}
									{companyInfo.acquisitions_history && companyInfo.acquisitions_history.length > 0 && (
										<div className={styles.companyInfo}>
											<div>
												<b>Acquisitions:</b>
												<ol style={{ margin: '8px 0 0 16px' }}>
													{companyInfo.acquisitions_history.map((p, i) => (
														<li key={i}>
															<div>{p.date}</div>
															<div>{p.details}</div>
														</li>
													))}
												</ol>
											</div>
										</div>
									)}
									{companyInfo.key_milestones && companyInfo.key_milestones.length > 0 && (
										<div className={styles.companyInfo}>
											<div>
												<b>Key Milestones:</b>
												<ol style={{ margin: '8px 0 0 16px' }}>
													{companyInfo.key_milestones.map((p, i) => (
														<li key={i}>
															<div>{p.date}</div>
															<div>{p.event}</div>
														</li>
													))}
												</ol>
											</div>
										</div>
									)}
									{companyInfo.subsidiaries && companyInfo.subsidiaries.length > 0 && (
										<div className={styles.companyInfo}>
											<div>
												<b>Subsidiaries:</b>
												<ol style={{ margin: '8px 0 0 16px' }}>
													{companyInfo.subsidiaries.map((p, i) => (
														<li key={i}>{p}</li>
													))}
												</ol>
											</div>
										</div>
									)}
									{companyInfo.sister_companies && companyInfo.sister_companies.length > 0 && (
										<div className={styles.companyInfo}>
											<div>
												<b>Other Related Companies:</b>
												<ol style={{ margin: '8px 0 0 16px' }}>
													{companyInfo.sister_companies.map((p, i) => (
														<li key={i}>{p}</li>
													))}
												</ol>
											</div>
										</div>
									)}
									{companyInfo.latest_news_links && companyInfo.latest_news_links.length > 0 && (
										<div className={styles.companyInfo}>
											<div>
												<b>Latest News:</b>
												<ol style={{ margin: '8px 0 0 16px' }}>
													{companyInfo.latest_news_links.map((p, i) => (
														<li key={i}>
															<div>{p.date}</div>
															<div><a href={p.link} target="_blank" rel="noreferrer">{p.link}</a></div>
														</li>
													))}
												</ol>
											</div>
										</div>
									)}
								</>
							)}
						</div>
					)}
				</>}
		</div>
	);
};

export default PortfolioInsights;
