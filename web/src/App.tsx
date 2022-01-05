import React from 'react';
import { RecoilRoot } from 'recoil';
import Router from './router';
import style from './style.module.scss';

const App = () => {
  return (
    <RecoilRoot>
      <div className={style.app}>
        <Router />
      </div>
    </RecoilRoot>
  );
}

export default App;
