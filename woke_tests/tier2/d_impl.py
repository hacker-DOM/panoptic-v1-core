from .c_hooks import *

from woke_tests.runner import get_address


class Impl(Hooks):
    def impl_deploy_panoptic_pool(s, v3pool: IUniswapV3Pool, owner: Account, salt: int):
        token0 = v3pool.token0()
        token1 = v3pool.token1()
        fee = v3pool.fee()
        tickSpacing = v3pool.tickSpacing()

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
        pool_salt = s.utils.getSalt(v3pool, owner, salt)
        preComputedPool = s.utils.predictDeterministicAddress(
            s.panopticFactory.getPoolReference(), pool_salt, s.panopticFactory
        )

        liquidityBefore = v3pool.liquidity()
        balance0Before = IERC20Partial(token0).balanceOf(owner)
        balance1Before = IERC20Partial(token1).balanceOf(owner)

        IERC20Partial(token0).approve(s.utils, INITIAL_MOCK_TOKENS, from_=owner)
        IERC20Partial(token1).approve(s.utils, INITIAL_MOCK_TOKENS, from_=owner)

        fullRangeLiquidity = 0
        # compute is doing an on chain mint that needs to be reverted
        with snapshot_and_revert_fix(default_chain):
            tx = s.utils.computeFullRangeLiquidity(
                s.panopticFactory, v3pool, from_=owner
            )
            fullRangeLiquidity = tx.return_value[0]

        tx = s.panopticFactory.deployNewPool(token0, token1, fee, salt, from_=owner)
        deployedPool = tx.return_value

        assert get_address(s.panopticFactory.getPanopticPool(v3pool)) == get_address(
            deployedPool
        )
        assert get_address(v3pool) == get_address(
            PanopticPool(preComputedPool).univ3pool()
        ), f"v3 pool address {get_address(v3pool)} != linked {get_address(PanopticPool(preComputedPool).univ3pool())} "

        #
        #        /* Liquidity checks */
        #        // Amount of liquidity in univ3 pool after Panoptic Pool deployment
        liquidityAfter = v3pool.liquidity()
        #        // ensure liquidity in pool now is sum of liquidity before and user deployed amount
        assert (
            liquidityAfter - liquidityBefore == fullRangeLiquidity
        ), f"liquidity delta {liquidityAfter - liquidityBefore} != full range {fullRangeLiquidity}"
