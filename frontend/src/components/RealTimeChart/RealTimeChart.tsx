import React, { Component } from 'react';
import { Chart, registerables } from 'chart.js';
import { Line, Chart as ReactChart } from 'react-chartjs-2';
import 'chartjs-adapter-luxon';
import StreamingPlugin from 'chartjs-plugin-streaming';

Chart.register(StreamingPlugin, ...registerables);

const RealTimeChart = (props: any) => {
  console.log('Building RealTimeChart');
  const { val, date, data } = props;
  return (
    <Line
      data={{
        datasets: [
          {
            data: [],
          },
        ],
      }}
      options={{
        scales: {
          x: {
            type: 'realtime',
            realtime: {
              delay: 1000,
              onRefresh: (chart) => {
                chart.data.datasets.forEach((dataset) => {
                  dataset.data.push({
                    x: Date.now(),
                    y: Math.random(),
                  });
                });
              },
            },
          },
        },
      }}
    />
  );
};

export default RealTimeChart;
