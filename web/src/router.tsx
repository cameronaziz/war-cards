import React, { Fragment, VFC } from 'react';
import { useRecoilValue } from 'recoil';
import { Board, Player, Setup } from './components';
import { settings } from './state';

const Router: VFC = () => {
  const settingsState = useRecoilValue(settings);

  if (settingsState.inGame) {
    return (
      <Fragment>
        <Board />
        <Player />
      </Fragment>
    );
  }

  return (
    <Setup />
  );
};

export default Router;
