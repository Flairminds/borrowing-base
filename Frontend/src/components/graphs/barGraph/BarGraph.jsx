import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { formatNumber } from '../../../utils/helperFunctions/numberFormatting';
import { THEME } from '../../../utils/styles';

export const BarGraph = ({ chartsData, yAxis }) => {

	// const hasUnadjustedBB = chartsData?.some(data => data.hasOwnProperty('Unadjusted BB'));
	// const hasUpdatedUnadjustedBB = chartsData?.some(data => data.hasOwnProperty('Updated unadjusted BB'));
	// const hasBB = chartsData?.some(data => data.hasOwnProperty('BB'));
	// const hasUpdatedBB = chartsData?.some(data => data.hasOwnProperty('Updated BB'));

	return (
		<div style={{ height: "100%", width: "100%" }}>
			<ResponsiveContainer width="100%" height="100%" style={{ backgroundColor: "#f5f5f5" }}>
				<BarChart
					data={chartsData}
					margin={{
						top: 5,
						right: 30,
						left: 30,
						bottom: 5
					}}
				>
					<CartesianGrid strokeDasharray="3 3" />
					<XAxis dataKey="name" />
					<YAxis tickFormatter={formatNumber} />
					<Tooltip formatter={(value) => formatNumber(value)} />
					<Legend />
					{yAxis?.map((segment, index) => {
						return (
							<Bar key={index} dataKey={segment} fill={THEME.PRIMARY_BG_COLOR} />
						);
					})}
				</BarChart>
			</ResponsiveContainer>
		</div>
	);
};
