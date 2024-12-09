import React from 'react'
import { BarChart, Bar, Rectangle, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ReferenceLine, Cell } from 'recharts';
import { formatNumber } from '../../utils/helperFunctions/numberFormatting';


export const StackedBarGraph = ({StackedGraphData}) => {

    // const COLORS = {
        const BB= ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#AF19FF', '#FF6666', '#6699FF']
        const Updated_BB= ['#FF8042', '#AF19FF', '#FFBB28', '#FF6666', '#6699FF', '#0088FE', '#00C49F']
    //   };

  return (
    <div style={{height: "100%", width: "100%"}}>
        <BarChart
          width={500}
          height={300}
          data={StackedGraphData}
          margin={{
            top: 20,
            right: 30,
            left: 20,
            bottom: 5,
          }}
        >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis tickFormatter={formatNumber} />
            <Tooltip formatter={(value) => formatNumber(value)} />
            <Legend />
            {StackedGraphData?.map((item, index) => (
            <Bar
            key={item.name}
            dataKey={Object.keys(item).slice(1)} // Get all data keys except name
            stackId={index}
            fill={BB[index % BB.length]} // Use color based on index
            >
              {StackedGraphData?.map((d, i) => (
                <Cell key={i} fill={BB[index % BB.length]} /> // Ensure cells have the same color
              ))}
            </Bar>
          ))}
            
        </BarChart>
   </div>
  )
}
