from .a_init import *

from pytypes.contracts.PanopticPool import PanopticPool
from pytypes.contracts.CollateralTracker import CollateralTracker


from pytypes.contracts.tokens.interfaces.IERC20Partial import IERC20Partial
from pytypes.lib.v3core.contracts.interfaces.IUniswapV3Pool import IUniswapV3Pool
from pytypes.woke_tests.contracts.utils import Utils, PanopticFactoryHarness


class Helpers(Init):
    def random_user(s) -> Account:
        return random.choice(s.users)

    def random_v3_pool(s) -> IUniswapV3Pool:
        return random.choice(s.v3_pools)

    # def random_token(s) -> ERC20:
    #     return random.choice(s.tokens)

    def _deploy(s):
        s.V3FACTORY = IUniswapV3Factory(V3FACTORY_ADDRESS)

        s.utils = Utils.deploy(from_=s.paccs[0])

        print("Deploy SFPM")
        s.sfpm = SemiFungiblePositionManager.deploy(s.V3FACTORY, from_=s.paccs[0])
        print("Deployed")
        pool = PanopticPool.deploy(s.sfpm, from_=s.paccs[0])
        col = CollateralTracker.deploy(from_=s.paccs[0])
        s.factory_owner = s.paccs[0]
        s.panopticFactory = PanopticFactoryHarness.deploy(
            WETH, s.sfpm, V3FACTORY_ADDRESS, pool, col, from_=s.factory_owner
        )
        WETHE = IERC20Partial(WETH)  # "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48")
        mint_erc20_(WETH, s.paccs[0], 100000)

        print("balance is", IERC20Partial(WETH).balanceOf(s.paccs[0]))
        s.v3_pools = [IUniswapV3Pool(0x88E6A0C2DDD26FEEB64F039A2C41296FCB3F5640)]

    def _deploy_pool(s, pool: IUniswapV3Pool, owner: Account):

        token0 = pool.token0()
        token1 = pool.token1()
        fee = pool.fee()
        tickSpacing = pool.tickSpacing()

        # give test contract a sufficient amount of tokens to deploy a new pool

        mint_erc20_(token0, owner, INITIAL_MOCK_TOKENS)
        mint_erc20_(token1, owner, INITIAL_MOCK_TOKENS)
        IERC20Partial(token0).approve(
            s.panopticFactory, INITIAL_MOCK_TOKENS, from_=owner
        )
        IERC20Partial(token1).approve(
            s.panopticFactory, INITIAL_MOCK_TOKENS, from_=owner
        )
        IERC20Partial(token0).approve(s.sfpm, INITIAL_MOCK_TOKENS, from_=owner)
        IERC20Partial(token1).approve(s.sfpm, INITIAL_MOCK_TOKENS, from_=owner)
        #
        # assertEq(IERC20Partial(token0).balanceOf(address(this)), INITIAL_MOCK_TOKENS);
        # assertEq(IERC20Partial(token1).balanceOf(address(this)), INITIAL_MOCK_TOKENS);


#
# // approve factory to move tokens, on behalf of the test contract
# IERC20Partial(token0).approve(address(panopticFactory), INITIAL_MOCK_TOKENS);
# IERC20Partial(token1).approve(address(panopticFactory), INITIAL_MOCK_TOKENS);
#
# // approve sfpm to move tokens, on behalf of the test contract
# IERC20Partial(token0).approve(address(sfpm), INITIAL_MOCK_TOKENS);
# IERC20Partial(token1).approve(address(sfpm), INITIAL_MOCK_TOKENS);
#
# // approve self
# IERC20Partial(token0).approve(address(this), INITIAL_MOCK_TOKENS);
# IERC20Partial(token1).approve(address(this), INITIAL_MOCK_TOKENS);
