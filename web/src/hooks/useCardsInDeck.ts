import { useRecoilValue } from 'recoil';
import { deck } from '../state';

interface UseCardsInDeck {
  (): [Cards.Card[], boolean]
}

const useCardsInDeck: UseCardsInDeck = () => {
  const deckState = useRecoilValue(deck);
  const cards = deckState.filter((card) => card.position === 'deck' || card.position === 'dealing');
  const hasDealt = cards.length !== deckState.length;

  return [
    cards,
    hasDealt,
  ];
};

export default useCardsInDeck;
