export interface Position {
  left: DOMRect | null;
  right: DOMRect | null;
}

type Hands = {
  [playerId: string]: Position;
}

type State = 'default' | 'over' | 'dragging';

type ModalState = 'opponent' | 'card';

type StateValues = {
  [key in State]: string;
}

export as namespace UI;
