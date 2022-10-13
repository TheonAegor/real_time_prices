import { useEffect, useState } from 'react';
import useWebSocket, { ReadyState } from 'react-use-websocket';
import BasicSelect from './components/BasicSelect/BasicSelect';
import { Chart, registerables } from 'chart.js';
import { Line } from 'react-chartjs-2';
import 'chartjs-adapter-luxon';
import StreamingPlugin from 'chartjs-plugin-streaming';
import { SelectChangeEvent } from '@mui/material/Select';

Chart.register(StreamingPlugin, ...registerables);

const App = () => {
  const socketUrl = 'ws://localhost:8080/connect';
  const { sendMessage, lastMessage, readyState } = useWebSocket(socketUrl);
  const [data, setData] = useState([]);
  const [tradingInstr, setTradingInstr] = useState([]);
  const [tradingTool, setTradingTool] = useState('');
  const [id, setId] = useState('');

  let currPrice = 0;
  let currTS = 0;

  const onSelectPick = (event: SelectChangeEvent) => {
    setTradingTool(event.target.value as string);
    const tt = event.target.value;
    if (tt !== tradingTool) {
      sendMessage(
        JSON.stringify({
          kind: 'change',
          payload: { id: id, trading_tool: tt },
        })
      );
    }
  };

  if (lastMessage !== null) {
    // console.log('lastMessage is not null');
    const full_data: any = JSON.parse(lastMessage?.data);
    if (full_data.kind === 'initial') {
    }
    if (full_data.kind === 'tell') {
      if (full_data.payload.new_price) {
        currPrice = full_data.payload.new_price.value;
        console.log(currPrice);
        currTS = full_data.payload.full_info.timestamp;
      }
    }
  }

  useEffect(() => {
    if (lastMessage !== null) {
      const full_data: any = JSON.parse(lastMessage?.data);
      if (full_data.kind === 'initial') {
        setTradingInstr(full_data.payload.trading_tools);
        setId(full_data.payload.id);
      }
    }
  }, [lastMessage]);

  return (
    <div>
      <BasicSelect variants={tradingInstr} onSelectPick={onSelectPick} />
      <Line
        data={{
          datasets: [
            {
              data: data,
            },
          ],
        }}
        options={{
          scales: {
            x: {
              type: 'realtime',
              realtime: {
                delay: 2000,
                onRefresh: (chart) => {
                  chart.data.datasets.forEach((dataset) => {
                    dataset.data.push({
                      x: currTS,
                      y: currPrice,
                    });
                  });
                },
              },
            },
            y: {
              min: -100, // minimum value
              max: 100, // maximum value
            },
          },
        }}
      />
    </div>
  );
};

export default App;
