import React, { useEffect, useRef, VFC } from 'react';
import { useCardLocation, useHand } from '../../hooks';
import Card, { CardRef } from '../card';

interface ItemProps {
  card: Cards.Card | null;
  isPlayer?: boolean;
  playerId: string;
  size?: Cards.Size;
  isLeft?: boolean;
}

const Item: VFC<ItemProps> = (props) => {
  const { card, size, isPlayer, playerId, isLeft } = props;
  const cardRef = useRef<CardRef>(null);
  const [, setLocation] = useCardLocation()
  const [hand] = useHand(playerId);

  const { id } = card || {};

  useEffect(
    () => {
      if (cardRef.current) {
        const rect = cardRef.current.getRect();
        setLocation(playerId, isLeft ? 'left' : 'right', rect);
      };
    },
    [cardRef.current],
  );

  // if (!card && i !== 0 && !isPlayer) {
  //   return null
  // }

  const isDraggable = hand.cards.every((card) => card !== null);

  return (
    <Card
      key={id}
      ref={cardRef}
      card={card}
      size={size}
      isDraggable={isDraggable}
    />
  )
};

export default Item;

