import React, { VFC } from 'react';
import { useCardsInDeck, useDraw } from '../../hooks';
import Item from './item';
import style from './style.module.scss';

const Deck: VFC = () => {
  const [draw, deal] = useDraw();
  const [cards, hasDealt] = useCardsInDeck();

  const onClick = () => {
    if (hasDealt) {
      draw('0');
      return;
    }
    deal();
  };

  return (
    <div onClick={onClick} className={hasDealt ? style.deckContainerDealt : style.deckContainer}>
      <div className={style.deckInner}>
        <div className={hasDealt ? style.dummy : style.dummyDealt} />
        <div className={style.deckStack}>
          {cards.reverse().map((card, i) =>
            <Item
              card={card}
              key={i}
            />
          )}
        </div>
      </div>
      <div className={hasDealt ? style.dummyDealt : style.dummy} />
    </div>
  );
};

export default Deck;
