import React, { forwardRef, useEffect, useImperativeHandle, useRef, useState } from 'react';
import { useRecoilState } from 'recoil';
import { useDropCard } from '../../hooks';
import { UI } from '../../state';
import * as utilities from './utilities';

interface CardProps {
  card: Cards.Card | null;
  isDraggable?: boolean
  isAbsolute?: boolean;
  isFaceDown?: boolean;
  isRotated?: boolean
  rotateAmount?: number;
  size?: Cards.Size;
}

export interface CardRef {
  flip(): void;
  getRect(): DOMRect;
}

const CURSOR: UI.StateValues = {
  default: 'default',
  over: 'grab',
  dragging: 'grabbing',
};

const Card = forwardRef<CardRef, CardProps>((props, ref) => {
  const { card, size, isAbsolute, isFaceDown, isRotated, rotateAmount, isDraggable } = props;
  const transformationRef = useRef(utilities.getTransform(isRotated, rotateAmount))
  const containerRef = useRef<HTMLDivElement>(null);
  const [UIState, setUIState] = useRecoilState(UI);
  const [isFlipping, setIsFlipping] = useState(false);
  const [onDropCard] = useDropCard();

  useImperativeHandle(
    ref,
    () => ({
      flip,
      getRect,
    }),
  );

  const getRect = () => {
    if (!containerRef.current) {
      const fake = document.createElement('div');
      return fake.getBoundingClientRect();
    }
    return containerRef.current.getBoundingClientRect();
  }

  const flip = () => {
    setIsFlipping((flipping) => !flipping);
  };


  const lightCard = !isFaceDown && !card?.rank

  useEffect(
    () => {
      if (containerRef.current) {
        containerRef.current.addEventListener('dragstart', dragstart);
        containerRef.current.addEventListener('dragend', dragend);
      }

      return () => {
        if (containerRef.current) {
          containerRef.current.removeEventListener('dragstart', dragstart);
          containerRef.current.removeEventListener('dragend', dragend);
        }
      }
    },
    [containerRef.current, UIState.dragState],
  );

  const dragstart = (e: DragEvent) => {
    if (!isDraggable) {
      e.preventDefault();
      return;
    }

    if (card) {
      setUIState((prevUI) => ({
        ...prevUI,
        draggingCardId: card.id,
      }));
    }
  };

  const dragend = (e: DragEvent) => {
    if (card && UIState.dragState === 'over') {
      onDropCard(card);
    }

    setUIState((prevUI) => ({
      ...prevUI,
      draggingCardId: null,
      dragState: 'default',
    }));
  };

  return (
    <div
      ref={containerRef}
      className={utilities.getContainerClassName(isFlipping, isAbsolute)}
      draggable={isDraggable ? 'true' : 'false'}
      style={{
        cursor: CURSOR[UIState.dragState],
        transform: transformationRef.current,
        opacity: lightCard ? 0 : 1,
      }}
    >
      <img
        src={utilities.cardImage({
          rank: card ? card.rank : undefined,
          isFaceDown,
          isPlayer: card?.playerId === '0',
          size,
        })}
        alt={`card face for ${card?.rank || 'unknown'} rank`}
      />
    </div>
  );
})

export default Card;
