type Result<T extends boolean> = T extends true ? Cards.Card : [Cards.Card, Cards.Card]

export const getHand = <T extends boolean>(player: Players.Player, deck: State.Deck, first?: T): Result<T> => {
  const cardInHand = deck.filter((card) => card.playerId === player.id);

  if (first) {
    if (cardInHand.length === 0 || cardInHand.length > 1) {
      throw new Error('There is no card in hand');
    }
    return cardInHand[0] as Result<T>;
  }

  return cardInHand as Result<T>;
};

export const getHandSingle = (player: Players.Player, deck: State.Deck) => getHand(player, deck, true);

export const getHandRotation = (playerId?: string) => {
  if (playerId === '0' || !playerId) {
    return 0;
  }
  const playerNumber = parseInt(playerId, 10);
  const odd = playerNumber % 2 === 0;
  return odd ? -90 : 90;
};
