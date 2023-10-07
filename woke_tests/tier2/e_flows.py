from .d_impl import *

from woke_tests.framework import get_address


class Flows(Impl):
    def random_salt(s) -> int:
        return generators.random_int(min=0, max=2**96 - 1)

    def random_rarity(s) -> int:
        return generators.random_int(min=1, max=2)

    @flow()
    def set_owner(s, random_user: Account):

        s.panopticFactory.setOwner(random_user, from_=s.panopticFactory.factoryOwner())
        assert get_address(random_user) == s.panopticFactory.factoryOwner()

    @flow()
    def deploy_panoptic_pool(
        s, random_v3_pool: IUniswapV3Pool, random_user: Account, random_salt: int
    ):
        print("deploy v3 pool", random_v3_pool, "salt", random_salt)
        s.impl_deploy_panoptic_pool(random_v3_pool, random_user, random_salt)

    @flow()
    def deploy_panoptic_pool_rarity(
        s,
        random_v3_pool: IUniswapV3Pool,
        random_user: Account,
        random_salt: int,
        random_rarity: int,
    ):
        print("deploy v3 pool", random_v3_pool, "salt", random_salt, random_rarity)
        s.impl_deploy_panoptic_pool(
            random_v3_pool, random_user, random_salt, random_rarity
        )
