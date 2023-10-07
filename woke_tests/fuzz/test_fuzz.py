from woke_tests.tier2.g_issues import Issues
from woke.testing.core import default_chain
from woke.development.core import Account
from woke_tests.runner import get_address
from woke.development.transactions import must_revert
from pytypes.contracts.libraries.Errors import Errors
from pytypes.lib.v3core.contracts.interfaces.IUniswapV3Pool import IUniswapV3Pool

user_addr = "0x15d34aaf54267db7d7c367839aaf71a00a2c6a65"


from woke_tests.runner import fuzz_test


@default_chain.connect()
def test_owner():
    print("deploy_pool")
    print("===================")
    issues = Issues()
    fuzz_test(issues, sequences_count=0, flow_name=["set_owner"])


@default_chain.connect()
def test_deploy_pool():
    print("deploy_pool")
    print("===================")
    issues = Issues()
    fuzz_test(issues, sequences_count=0, flow_name=["deploy_panoptic_pool"])


@default_chain.connect()
def test_deploy_rarity():
    print("deploy_pool")
    print("===================")
    issues = Issues()
    fuzz_test(issues, sequences_count=10, flow_name=["deploy_panoptic_pool_rarity"])
