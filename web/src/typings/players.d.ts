export interface Player {
  id: string;
  isShielded: boolean;
  isDead: boolean;
}

export type HandCards = [
  Cards.Card | null,
  Cards.Card | null,
];

export interface Hand {
  cards: HandCards;
  rotation: number;
}

export as namespace Players;
