export interface Settings {
  opponents: Settings.Opponents;
  starting: Settings.Starting;
  inGame: boolean;
}

export interface UI {
  hands: UI.Hands;
  draggingCardId: string | null;
  dragState: UI.State;
  playSpace: DOMRect | null;
  modalState: UI.ModalState | null;
}

export type Players = Players.Player[];

export type Deck = Cards.Card[]

export as namespace State;
