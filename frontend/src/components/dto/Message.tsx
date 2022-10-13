export type EventType = 'tell' | 'initial' | 'connect' | 'change' | 'disconnect'

export type PayloadType = {
  new_price: string;
  trading_tool: string;
};

export type MessageType = {
  kind: EventType;
  payload: PayloadType;
};
