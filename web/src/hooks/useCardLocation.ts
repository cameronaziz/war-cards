import { useRecoilState } from 'recoil';
import { UI } from '../state';

interface SetLocation {
  (playerId: string, position: keyof UI.Position, rect: DOMRect): void
}

interface GetLocation {
  (playerId: string, position: keyof UI.Position): DOMRect | null;
}

interface UseCardLocation {
  (): [GetLocation, SetLocation];
}

const useCardLocation: UseCardLocation = () => {
  const [uiState, setUIState] = useRecoilState(UI);

  const getLocation = (playerId: string, position: keyof UI.Position) => {
    const { left, right } = uiState.hands[playerId];
    return position === 'left' ? left : right;
  };

  const setLocation = (playerId: string, position: keyof UI.Position, rect: DOMRect) => {
    if (uiState.hands[playerId] && uiState.hands[playerId][position] !== null) {
      return;
    }

    setUIState((ui) => {
      const nextHand = {
        ...ui.hands[playerId]
      };
      nextHand[position] = rect;

      return {
        ...ui,
        hands: {
          ...ui.hands,
          [playerId]: nextHand,
        }
      };
    });
  }

  return [
    getLocation,
    setLocation,
  ]
};

export default useCardLocation;
