import { useRecoilValue } from 'recoil';
import { deck } from '../state';
import { getHandRotation } from '../utilities';
import useDraw, { UseDraw } from './useDraw';

interface UseHand {
  (playerId?: string): [Players.Hand, ReturnType<UseDraw>[0]];
}

const useHand: UseHand = (playerId?: string) => {
  const deckState = useRecoilValue(deck);
  const [draw] = useDraw();

  const [first, second] = playerId ? deckState.filter((card) => card.playerId === playerId && card.position === 'hand') : [null, null]

  const hand: Players.Hand = {
    rotation: getHandRotation(playerId),
    cards: [
      first ? first : null,
      second ? second : null,
    ],
  };

  return [
    hand,
    draw
  ];
}

export default useHand;
