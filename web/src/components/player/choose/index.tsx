import React, { VFC } from 'react';
import { useRecoilState } from 'recoil';
import { UI } from '../../../state';
import style from './style.module.scss';

const Choose: VFC = (props) => {
  const [settingsState, setSettingsState] = useRecoilState(UI);

  const submit = () => {

  }

  if (settingsState.modalState === null) {
    return null;
  }

  return (
    <div className="modal is-active">
      <div className={style.background} />
      <div className="modal-card">
        <header className="modal-card-head">
          <p className="modal-card-title">
            Pick an
          </p>
        </header>
        <div className="modal-card-body">
          Pick
        </div>
        <footer className="modal-card-foot" />
      </div>
    </div >
  );
};

export default Choose;
