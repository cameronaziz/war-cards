export const isChooseOpponentCard = (card: Cards.Card): card is Cards.CardAgainstOpponent =>
  card.rank === '1' || card.rank === '2' || card.rank === '3' || card.rank === '5' || card.rank === '6';

export const isCardWithChoice = (card: Cards.Card): card is Cards.CardWithChoice =>
  card.rank === '1';
