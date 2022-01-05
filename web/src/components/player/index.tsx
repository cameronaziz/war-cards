import React, { VFC } from 'react';
import { CARD_SIZE } from '../../constants';
import Hand from '../hand';
import Choose from './choose';
import style from './style.module.scss';

const Player: VFC = () => {
  return (
    <div className={style.container}>
      <Hand playerId="0" isPlayer size={CARD_SIZE.player} />
      <Choose />
    </div>
  );
};

export default Player;

