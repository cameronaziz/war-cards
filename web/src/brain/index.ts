import { useSetRecoilState } from 'recoil';
import { players } from '../state';
// import { getHandSingle } from '../utilities';

interface BrainOptionsBase {
  rank: Cards.Rank;
  player: Players.Player;
  deck: State.Deck;
}

interface BrainOptionsOpponent extends BrainOptionsBase {
  rank: Cards.OpponentRank;
  // opponent: Players.Player;
}

interface BrainOptionsCard extends BrainOptionsOpponent {
  choice: Cards.Rank;
}

type BrainOptions<T extends Cards.Rank> =
  T extends Cards.OpponentCardRank ? BrainOptionsCard :
  T extends Cards.OpponentRank ? BrainOptionsOpponent : BrainOptionsBase;


const useBrain = <T extends Cards.Rank>(options: BrainOptions<T>) => {
  const setPlayersState = useSetRecoilState(players);
  const { rank, player, deck } = options;
  switch (options.rank) {
    case '1': {
      break;
    }
    case '2':
      break;
    case '3':
      // const opponentCard = getHandSingle(options.opponent, deck);
      // const playerCard = getHandSingle(player, deck);
      // const opponentRank = parseInt(opponentCard.rank);
      // const playerRank = parseInt(playerCard.rank);
      // if (playerRank > opponentRank) {
      //   return {
      //     killed: options.opponent.id
      //   }
      // }
      // if (opponentRank > playerRank) {
      //   return {
      //     killed: player.id
      //   }
      // }
      return {
        killed: null
      }
    case '5':
    case '6':
      break;
    case '4':
      player.isShielded = true;
      break;
    case '7':
      break;
    case '8':
      player.isDead = true;
      break;

  }
}

export default useBrain
