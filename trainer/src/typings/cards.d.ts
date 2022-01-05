export type Type =
  | 'archer'
  | 'priest'
  | 'sword'
  | 'shield'
  | 'trebuchet'
  | 'mule'
  | 'joker'
  | 'crown';

type Rank =
  | 1
  | 2
  | 3
  | 4
  | 5
  | 6
  | 7
  | 8;

export interface Card {
  type: Type
  rank: Rank
}

export as namespace Cards;
