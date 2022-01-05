export type Rank =
  | '1'
  | '2'
  | '3'
  | '4'
  | '5'
  | '6'
  | '7'
  | '8';

export type OpponentRank =
  | '1'
  | '2'
  | '3'
  | '5'
  | '6';

export type OpponentCardRank =
  '1';

type Position = 'deck' | 'discard' | 'hand' | 'dealing';
type Size = '0.5' | '0.75' | '1' | '2' | '3';

export interface Card {
  id: string;
  playerId?: string;
  rank: Rank;
  position: Position;
  isFaceUp: boolean;
}

export interface CardAgainstOpponent extends Card {
  rank: OpponentRank;
}

export interface CardWithChoice extends Card {
  rank: OpponentCardRank;
}

export interface OpponentCard extends Card {
  rank: Extract<Rank, '1' | '2' | '3' | '5' | '6'>;
}

export as namespace Cards;
