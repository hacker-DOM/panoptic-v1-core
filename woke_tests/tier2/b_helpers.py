from .a_init import *

from pytypes.contracts.PanopticPool import PanopticPool
from pytypes.contracts.CollateralTracker import CollateralTracker


class Helpers(Init):
    def random_user(s) -> Account:
        return random.choice(s.users)

    # def random_token(s) -> ERC20:
    #     return random.choice(s.tokens)

    def _deploy(s):
        s.V3FACTORY = IUniswapV3Factory(V3FACTORY_ADDRESS)

        print("Deploy SFPM")
        s.sfpm = SemiFungiblePositionManager.deploy(s.V3FACTORY, from_=s.paccs[0])
        print("Deployed")
        pool = PanopticPool.deploy(s.sfpm, from_=s.paccs[0])
        col = CollateralTracker.deploy(from_=s.paccs[0])
        s.factory_owner = s.paccs[0]
        s.panopticFactory = PanopticFactory.deploy(
            _WETH, s.sfpm, V3FACTORY, pool, col, from_=s.factory_owner
        )
