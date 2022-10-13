import React, { useState, useCallback, useEffect, useRef } from 'react';
import useWebSocket, { ReadyState } from 'react-use-websocket';
import BasicSelect from './components/BasicSelect/BasicSelect';
import BasicTextField from './components/BasicTextField/BasicTextField';
import RealTimeChart from './components/RealTimeChart/RealTimeChart';
import { SelectChangeEvent } from '@mui/material/Select';
import { Chart, registerables } from 'chart.js';
import { Line, Chart as ReactChart } from 'react-chartjs-2';
import 'chartjs-adapter-luxon';
import StreamingPlugin from 'chartjs-plugin-streaming';

Chart.register(StreamingPlugin, ...registerables);

const App = () => {
  //Public API that will echo messages sent to it back to the client
  const [socketUrl, setSocketUrl] = useState('ws://localhost:8080/connect');
  const [id, setId] = useState('');
  const [tradingTool, setTradingTool] = useState('');
  const [tradingInstr, setTradingInstr] = useState([]);
  let currPrice = 0;
  let currTimeStamp = 0;
  const dataset = useRef([] as any)

  //   const [currPrice, setCurrPrice] = useState(0);
  //   const [date, setDate] = useState('');
  //   const [messageHistory, setMessageHistory] = useState([]);
//   const [dataset, setDataset] = useState([] as any);

  const { sendMessage, lastMessage, readyState } = useWebSocket(socketUrl);

  //   console.log('App started.');

  const handleClickSendMessage = useCallback(() => sendMessage('Hello'), []);

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

  const connectionStatus = {
    [ReadyState.CONNECTING]: 'Connecting',
    [ReadyState.OPEN]: 'Open',
    [ReadyState.CLOSING]: 'Closing',
    [ReadyState.CLOSED]: 'Closed',
    [ReadyState.UNINSTANTIATED]: 'Uninstantiated',
  }[readyState];

  useEffect(() => {
    if (lastMessage !== null) {
      //   setMessageHistory((prev: any) => prev.concat(lastMessage));

      let data = JSON.parse(lastMessage.data);
      if (data.kind === 'initial') {
        console.log(data);
        setTradingInstr(data.payload.trading_tools);
        setId(data.payload.id);
        console.log(data.payload.trading_tools);
      }
      //   setCurrPrice(data.payload.new_price);
      if (data.kind === 'tell') {
        if (data.payload.new_price) {
          currPrice = data.payload.new_price.value;
          currTimeStamp = data.payload.full_info.timestamp;
          //   x = data.payload.full_info.timestamp;
          //   y = data.payload.new_price.value;
            dataset.current.push({
              x: data.payload.full_info.timestamp,
              y: data.payload.new_price.value,
            });
          if (tradingTool !== data.payload.trading_tool) {
            console.log(tradingTool);
            console.log(data.payload.trading_tool);
            setTradingTool(data.payload.trading_tool);
          }
        }
      }
    }
  }, [lastMessage]);
  return (
    <div>
      <button
        onClick={handleClickSendMessage}
        disabled={readyState !== ReadyState.OPEN}
      >
        Click Me to send 'Hello'
      </button>
      <span>The WebSocket is currently {connectionStatus}</span>
      <BasicSelect variants={tradingInstr} onSelectPick={onSelectPick} />
      {/* <RealTimeChart val={currPrice.current} date={currTimeStamp.current} /> */}
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
      {/* <BasicTextField value={currPrice.current} /> */}
      {/* {lastMessage ? <span>Last message: {lastMessage.data}</span> : null}
      <ul>
        {messageHistory.map((message: any, idx) => (
          <span key={idx}>{message ? message.data : null}</span>
        ))}
      </ul> */}
    </div>
  );
};

export default App;
