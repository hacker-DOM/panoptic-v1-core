from woke_tests.tier2.g_issues import Issues
from woke.testing.core import default_chain
from woke.development.core import Account
from woke_tests.runner import get_address
from woke.development.transactions import must_revert
from pytypes.contracts.libraries.Errors import Errors
from pytypes.lib.v3core.contracts.interfaces.IUniswapV3Pool import IUniswapV3Pool

user_addr = "0x15d34aaf54267db7d7c367839aaf71a00a2c6a65"

from woke_tests.runner import unit_test


@default_chain.connect()
def test_owner():
    issues = Issues()
    unit_test(
        issues,
        flow_name="set_owner",
        params={"random_user": Account(user_addr)},
    )


@default_chain.connect()
def test_deploy_pool():
    issues = Issues()
    unit_test(
        issues,
        flow_name="deploy_panoptic_pool",
        params={
            "random_v3_pool": IUniswapV3Pool(
                "0x88e6A0c2dDD26FEEb64F039a2c41296FcB3f5640"
            ),
            "random_user": Account(user_addr),
            "random_salt": 55,
        },
    )


@default_chain.connect()
def test_deploy_pool_unsupported():
    # test_Fail_deployNewPool_UnsupportedPool
    issues = Issues()
    with must_revert(Errors.UniswapPoolNotSupported):
        unit_test(
            issues,
            flow_name="deploy_panoptic_pool",
            params={
                "random_v3_pool": IUniswapV3Pool(
                    "0x5777d92f208679DB4b9778590Fa3CAB3aC9e2168"
                ),
                "random_user": Account(user_addr),
                "random_salt": 55,
            },
        )
