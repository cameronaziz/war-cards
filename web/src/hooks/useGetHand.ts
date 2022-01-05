import { useRecoilValue } from 'recoil';
import { deck } from '../state';
import { getHandRotation } from '../utilities';

interface GetHand {
  (playerId: string): Players.Hand;
}

interface UseGetHand {
  (): [GetHand];
}

const useGetHand: UseGetHand = () => {
  const deckState = useRecoilValue(deck);

  const getHand: GetHand = (playerId) => {
    const [first, second] = deckState.filter((card) => card.playerId === playerId);
    const hand: Players.Hand = {
      rotation: getHandRotation(playerId),
      cards: [
        first ? first : null,
        second ? second : null,
      ]
    }
    return hand;
  }

  return [
    getHand,
  ];
}

export default useGetHand;
