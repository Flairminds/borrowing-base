import React from 'react'
import { CartesianGrid, Legend, Line, LineChart, ResponsiveContainer, XAxis, YAxis,Tooltip } from 'recharts';
import { formatNumber } from '../../utils/helperFunctions/numberFormatting';

export const TrendGraph = ({lineChartDisplaydata}) => {
const colors = ["#FA8A6C", "#24cccc", "#6554C0"]; 
  return (
    <div style={{width:'100%', height:"100%"}}> 
         <ResponsiveContainer width="100%" height="100%" 
         style={{backgroundColor:"#f5f5f5"}}
         >
            <LineChart
                // width={'100%'}
                // height={'100%'}
                data={lineChartDisplaydata?.trend_graph_data}
                margin={{
                    top: 5,
                    right: 30,
                    left: 20,
                    bottom: 5,
                }}
            >
                    <CartesianGrid vertical={false}  strokeDasharray="1 3" />
                    <XAxis dataKey="date" />
                    <YAxis  tickFormatter={formatNumber}  />
                    <Tooltip formatter={(value) => formatNumber(value)} />
                    <Legend />
                    {lineChartDisplaydata?.x_axis?.map((key, index) => (
                      <Line
                        key={key}
                        type="linear"
                        dataKey={key}
                        stroke={colors[index % colors.length]} 
                        dot={false}
                        activeDot={{ r: 5 }}
                      />
                    ))}
                    {/* <Line type="linear" dataKey="Tot BB" stroke="#FA8A6C" dot={false} activeDot={{ r: 5 }} />
                    <Line type="linear" dataKey="Lev BB" stroke="#24cccc" dot={false} activeDot={{ r: 5 }}  />
                    <Line type="linear" dataKey="Sub BB" stroke="#6554C0" dot={false} activeDot={{ r: 5 }} /> */}

                </LineChart>
             </ResponsiveContainer>
    </div>
  )
}
