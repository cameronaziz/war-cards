import { useRecoilState } from 'recoil';
import { deck } from '../state';

interface UseCardPosition {
  (cardId?: string): [Cards.Position | null, (position: Cards.Position) => void];
}

const useCardPosition: UseCardPosition = (cardId?: string) => {
  const [deckState, setDeckState] = useRecoilState(deck);
  const card = cardId ? deckState.find((card) => card.id === cardId) : null;

  const setPosition = (position: Cards.Position) => {
    if (card) {
      setDeckState((state) => {
        const nextState = [...state];
        const index = nextState.findIndex((card) => card.id === cardId);
        nextState[index] = {
          ...card,
          position,
        };
        return nextState;
      });
    }
  }

  return [
    card?.position || null,
    setPosition,
  ];

};

export default useCardPosition;
