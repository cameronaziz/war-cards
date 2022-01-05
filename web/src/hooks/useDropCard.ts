import { useRecoilState } from 'recoil';
import { UI } from '../state';
import { isChooseOpponentCard } from '../utilities';

const useDropCard = () => {
  const [UIState, setUIState] = useRecoilState(UI);

  const onDropCard = (card: Cards.Card) => {
    if (isChooseOpponentCard(card)) {
      setUIState((state) => ({
        ...state,
        modalState: 'card',
      }));
    }
  };

  return [
    onDropCard,
  ]
};

export default useDropCard;
