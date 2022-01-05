import React, { useEffect, VFC } from 'react';
import { useRecoilState, useSetRecoilState } from 'recoil';
import { deck, players, settings } from '../../state';
import Opponents from './opponents';
import Starting from './starting';
import style from './style.module.scss';
import { createPlayers, shuffleDeck } from './utilities';

const Setup: VFC = () => {
  const setPlayersState = useSetRecoilState(players);
  const [deckState, setDeckState] = useRecoilState(deck);
  const [settingsState, setSettingsState] = useRecoilState(settings);

  useEffect(
    () => {
      window.addEventListener('keypress', keypress);

      return () => {
        window.removeEventListener('keypress', keypress);
      }
    },
    [],
  );

  const keypress = (e: KeyboardEvent) => {
    if (e.key === 'Enter') {
      startGame();
    }
  };

  const startGame = () => {
    const players = createPlayers(settingsState);
    const deck = shuffleDeck(deckState);
    setDeckState(deck);
    setPlayersState(players);
    setSettingsState({ ...settingsState, inGame: true });
  };


  if (settingsState.inGame) {
    return null
  }

  return (
    <div className="modal is-active">
      <div className={style.background}></div>
      <div className="modal-card">
        <header className="modal-card-head">
          <p className="modal-card-title">
            War Cards
          </p>
        </header>
        <div className="modal-card-body">
          <table className="table">
            <tbody>
              <Opponents />
              <Starting />
            </tbody>
          </table>
        </div>
        <footer className="modal-card-foot">
          <button onClick={startGame} className="button is-success">Start</button>
        </footer>
      </div>
    </div>
  );
};

export default Setup;
