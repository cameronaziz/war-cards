import { atom } from 'recoil';

const SETTINGS_DEFAULT: State.Settings = {
  opponents: 2,
  starting: 'random',
  inGame: false,
};

const settings = atom({
  key: 'settingsState',
  default: SETTINGS_DEFAULT,
});

export default settings;
