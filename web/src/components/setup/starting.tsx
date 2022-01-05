import React, { useEffect, VFC } from 'react';
import { useRecoilState } from 'recoil';
import { settings } from '../../state';

const Starting: VFC = () => {
  const [settingsState, setSettingsState] = useRecoilState(settings);

  useEffect(
    () => {
      possibleReset(settingsState)
    },
    [settingsState.opponents],
  );

  const possibleReset = (state: State.Settings) => {
    switch (state.starting) {
      case '0':
      case 'random':
        break;
      default:
        const starting = parseInt(state.starting, 10);
        if (state.opponents < starting) {
          reset();
        }
        break;
    }
  };

  const reset = () => {
    setSettingsState((state) => ({ ...state, starting: 'random' }));
  }


  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value as Settings.Starting;
    setSettingsState((state) => ({
      ...state,
      starting: value,
    }));
  };

  return (
    <tr>
      <th>
        Starting
      </th>
      <td>
        <div className="control">
          <label className="radio">
            <input
              type="radio"
              name="random"
              value="random"
              checked={settingsState.starting === 'random'}
              onChange={handleChange}
            />
            <span className="ml-2 mr-4" >Random</span>
          </label>
          <label className="radio">
            <input
              type="radio"
              name="player"
              value="0"
              checked={settingsState.starting === '0'}
              onChange={handleChange}
            />
            <span className="ml-2 mr-4" >You</span>
          </label>
          {Array
            .from({ length: settingsState.opponents })
            .map((_, i) =>
              <label key={i} className="radio">
                <input
                  type="radio"
                  name={`starting - ${i + 1}`}
                  value={i + 1}
                  onChange={handleChange}
                  checked={settingsState.starting === `${i + 1}`}
                />
                <span className="ml-2 mr-4" >Opponent {i + 1}</span>
              </label>
            )}
        </div>
      </td>
    </tr>
  );
};

export default Starting;
