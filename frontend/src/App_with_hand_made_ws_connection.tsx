import React, { useState, useEffect, useCallback } from 'react';
import { Connection } from './components/network';
import './App.css';

function App() {
  const path: URL = new URL('wss://localhost:8080/connect');
  path.protocol = 'ws';
  const conn = new Connection(path, onOpen, onMessage, onClose, onError);

  function onOpen(this: WebSocket, ev: MessageEvent<any>) {
    console.log('ws connection opened');
  }

  function onMessage(event: any): void {}

  function onError(event: any): void {
    console.log(JSON.stringify(event.data));
  }

  function onClose(event: any): void {
    console.log(JSON.stringify(event.data));
  }

  const sendMsgToWs = () => {
    conn.push('change', { payload: { value: 'hello' } });
  };

  return (
    <div className="App">
      <button
        onClick={sendMsgToWs}
        // disabled={readyState !== ReadyState.OPEN}
      >
        Click Me to send 'Hello'
      </button>
    </div>
  );
}

export default App;
