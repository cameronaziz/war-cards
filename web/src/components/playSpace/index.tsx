import React, { useEffect, useRef, VFC } from 'react';
import { useRecoilState } from 'recoil';
import { UI } from '../../state';
import style from './style.module.scss';

const BACKGROUND_COLORS: UI.StateValues = {
  default: '#49504d',
  over: '#35654d',
  dragging: '#646335',
};

const PlaySpace: VFC = () => {
  const playSpaceRef = useRef<HTMLDivElement>(null);
  const [UIState, setUIState] = useRecoilState(UI);

  useEffect(
    () => {
      if (playSpaceRef.current) {
        playSpaceRef.current.addEventListener('dragover', dragover);
        playSpaceRef.current.addEventListener('dragleave', dragleave);
      }

      return () => {
        if (playSpaceRef.current) {
          playSpaceRef.current.removeEventListener('dragover', dragover);
          playSpaceRef.current.removeEventListener('dragleave', dragleave);
        }
      }
    },
    [playSpaceRef.current],
  );

  useEffect(
    () => {
      if (UIState.draggingCardId !== null && UIState.dragState === 'default') {
        setUIState((prevUI) => ({
          ...prevUI,
          dragState: 'dragging',
        }));
        return
      }
      if (UIState.draggingCardId === null && UIState.dragState === 'dragging') {
        setUIState((prevUI) => ({
          ...prevUI,
          dragState: 'default',
        }));
      }
    },
    [UIState.draggingCardId],
  );

  const dragover = (event: DragEvent) => {
    event.preventDefault();
    if (UIState.dragState !== 'over') {
      setUIState((prevUI) => ({
        ...prevUI,
        dragState: 'over',
      }));
    }
  };

  const dragleave = (event: DragEvent) => {
    event.preventDefault();
    if (UIState.dragState !== 'over') {
      setUIState((prevUI) => ({
        ...prevUI,
        dragState: 'dragging',
      }));
    }
  };

  return (
    <div
      ref={playSpaceRef}
      className={style.container}
    >
      <div
        className={style.playSpace}
        style={{
          backgroundColor: BACKGROUND_COLORS[UIState.dragState],
        }}
      />
    </div>
  );
};

export default PlaySpace;
