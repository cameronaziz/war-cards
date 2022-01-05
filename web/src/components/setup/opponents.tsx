import React, { VFC } from 'react';
import { useRecoilState } from 'recoil';
import { settings } from '../../state';

const Opponents: VFC = () => {
  const [settingsState, setSettingsState] = useRecoilState(settings);


  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = parseInt(e.target.value, 10);
    switch (value) {
      case 1:
      case 2:
      case 3:
      case 4:
        setSettingsState((state) => ({
          ...state,
          opponents: value,
        }));
    }
  };

  return (
    <tr>
      <th>
        Opponents
      </th>
      <td>
        <div className="control">
          {Array
            .from({ length: 4 })
            .map((_, i) =>
              <label key={i} className="radio">
                <input
                  type="radio"
                  name={`opponents - ${i + 1}`}
                  value={i + 1}
                  onChange={handleChange}
                  checked={settingsState.opponents === i + 1}
                />
                <span className="ml-2 mr-4" >{i + 1}</span>
              </label>
            )}
        </div>
      </td>
    </tr>
  );
};

export default Opponents;
