import React, { Fragment, VFC } from 'react';
import { useRecoilValue } from 'recoil';
import { CARD_SIZE } from '../../constants';
import { settings } from '../../state';
import Deck from '../deck';
import Hand from '../hand';
import PlaySpace from '../playSpace';
import style from './style.module.scss';

const Board: VFC = () => {
  const settingsState = useRecoilValue(settings);
  const hasFirst = settingsState.opponents >= 1;
  const hasSecond = settingsState.opponents >= 2;
  const hasThird = settingsState.opponents >= 3;
  const hasFourth = settingsState.opponents >= 4;

  if (!settingsState.inGame) {
    return null;
  }

  return (
    <Fragment>
      <div className={style.container}>
        <div className={style.opponentSide}>
          {hasFirst && <Hand playerId="1" size={CARD_SIZE.opponent} />}
          {hasThird && <Hand playerId="3" size={CARD_SIZE.opponent} />}
        </div>
        <PlaySpace />
        <div className={style.opponentSide}>
          {hasSecond && <Hand playerId="2" size={CARD_SIZE.opponent} />}
          {hasFourth && <Hand playerId="4" size={CARD_SIZE.opponent} />}
        </div>
      </div>
      <Deck />
    </Fragment>
  );
};

export default Board;
