import { atom } from 'recoil';
import { createPlayer } from '../utilities';

const PLAYERS_DEFAULT: State.Players = [
  createPlayer('0'),
];

const players = atom({
  key: 'playerState',
  default: PLAYERS_DEFAULT,
});

export default players;
