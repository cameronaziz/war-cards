import { atom } from 'recoil';
import { UUID } from '../utilities';

const ranks = {
  '1': 4,
  '2': 2,
  '3': 2,
  '4': 2,
  '5': 2,
  '6': 1,
  '7': 1,
  '8': 1,
};

const DECK = Object
  .entries(ranks)
  .reduce(
    (acc, cur) => {
      const cards = Array
        .from(
          { length: cur[1] },
          (_, i): Cards.Card => ({
            id: UUID(),
            isFaceUp: false,
            rank: cur[0] as Cards.Rank,
            position: 'deck',
          }),
        );
      const next = [...acc, ...cards];
      return next;
    },
    [] as Cards.Card[],
  );

const deck = atom({
  key: 'deckState',
  default: DECK,
});

export default deck;
