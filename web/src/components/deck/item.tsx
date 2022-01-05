import React, { CSSProperties, useEffect, useRef, VFC } from 'react';
import { useCardLocation, useCardsInDeck, useHand } from 'src/hooks';
import { CARD_SIZE } from '../../constants';
import Card, { CardRef } from '../card';
import style from './style.module.scss';

interface ItemProps {
  card: Cards.Card;
}

const Item: VFC<ItemProps> = (props) => {
  const { card } = props;
  const [getLocation] = useCardLocation();
  const [, hasDealt] = useCardsInDeck();
  const [hand] = useHand(card.playerId)
  const isDealing = card.position === 'dealing';
  const cardRef = useRef<CardRef>(null);

  useEffect(
    () => {
      if (card.position === 'dealing' && cardRef.current && card.playerId === '0') {
        cardRef.current.flip();
        return;
      }
    },
    [card.position]
  );

  const move = (): CSSProperties => {
    if (cardRef.current) {
      const source = cardRef.current.getRect();
      const { playerId } = card;
      if (playerId && isDealing) {
        const target = hand.cards[0] === null ? 'left' : 'right';
        const destination = getLocation(playerId, target);
        if (destination) {
          const movingLeft = destination.x < source.x;
          return {
            position: 'absolute',
            top: destination.y,
            left: destination.x,
            transform: `rotate(${hand.rotation}deg)`
          }
        }
      }
      return {
        top: source.y,
        left: source.x,
      }
    }
    return {
      left: 0,
      right: 0,
      top: 0,
      transform: `rotate(0deg)`
    }
  };

  const size = () => {
    if (!isDealing || !hasDealt) {
      return CARD_SIZE.deck;
    }
    if (card.playerId === '0') {
      return CARD_SIZE.player;
    }
    return CARD_SIZE.opponent;
  }

  return (
    <div data-name="item" className={style.itemContainer} style={{ ...move() }}>
      <Card
        card={card}
        ref={cardRef}
        isFaceDown
        isRotated
        size={size()}
      />
    </div>
  );
};

export default Item;
