import React, { VFC } from 'react';
import { useHand } from '../../hooks';
import Item from './item';
import style from './style.module.scss';

interface HandProps {
  playerId: string;
  isPlayer?: boolean;
  size?: Cards.Size;
}

const Hand: VFC<HandProps> = (props) => {
  const { playerId, isPlayer, size } = props;
  const [hand] = useHand(playerId);

  const { cards } = hand;

  return (
    <div className={style.container} style={{ transform: `rotate(${hand.rotation}deg)` }}>
      <Item
        isLeft
        size={size}
        card={cards[0]}
        playerId={playerId}
      />
      {cards[0] !== null &&
        <Item
          size={size}
          card={cards[1]}
          playerId={playerId}
        />
      }
    </div>
  );
};

export default Hand;

