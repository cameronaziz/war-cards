import { createPlayer } from '../../utilities';

export const createPlayers = (settingsState: State.Settings): Players.Player[] => {
  const opponents: Players.Player[] = Array
    .from(
      { length: settingsState.opponents },
      (_, i) => createPlayer(`${i + 1}`),
    );
  const players: Players.Player[] = [
    ...opponents,
    createPlayer('0'),
  ];

  return players;
};

export const shuffleDeck = (deck: Cards.Card[]): Cards.Card[] => {
  const shuffled = [...deck];
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }
  return shuffled;
}
