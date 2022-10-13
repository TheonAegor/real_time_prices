export class Connection {
  connection: WebSocket;

  constructor(
    path: URL,
    onOpen: any,
    onMessage: any,
    onClose: any,
    onError: any
  ) {
    this.connection = new WebSocket(path);
    this.connection.onmessage = onMessage;
    this.connection.onclose = onClose;
    this.connection.onerror = onError;
  }

  push = (kind: any, data: any) => {
    this.connection.send(JSON.stringify({ kind: kind, payload: data }));
  };
}
