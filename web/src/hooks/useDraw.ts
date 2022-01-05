import { useRecoilValue, useSetRecoilState } from 'recoil';
import { deck, players } from '../state';
import useGetHand from './useGetHand';

export interface UseDraw {
  (): [(playerId: string) => void, () => Promise<void>];
}

const useDraw: UseDraw = () => {
  const setDeckState = useSetRecoilState(deck);
  const playersState = useRecoilValue(players);
  const [getHand] = useGetHand();

  const delayed = (index: number) => {
    setDeckState((prevDeck) => {
      const cards = [...prevDeck];
      const card = cards[index];
      const nextCard: Cards.Card = {
        ...card,
        position: 'hand',
      };
      cards.splice(index, 1, nextCard);
      return cards;
    });
  }

  const draw = (playerId: string) => {
    const hand = getHand(playerId);
    if (hand.cards.every((card) => card !== null)) {
      return;
    }

    setDeckState((prevDeck) => {
      const cards = [...prevDeck];
      const firstInDeck = cards.findIndex((card) => card.position === 'deck');
      const card = cards[firstInDeck];
      const nextCard: Cards.Card = {
        ...card,
        playerId,
        isFaceUp: playerId === '0',
        position: 'dealing',
      };
      cards.splice(firstInDeck, 1, nextCard);
      setTimeout(() => {
        delayed(firstInDeck);
      }, 900);
      return cards;
    });
  };

  const deal = async () => {
    for (let player of playersState) {
      draw(player.id);
      await new Promise((resolve) => setTimeout(resolve, 500));
    }
  }

  return [
    draw,
    deal,
  ];
}

export default useDraw;
