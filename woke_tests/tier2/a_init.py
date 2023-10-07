from woke_tests.common import *

from pytypes.contracts.SemiFungiblePositionManager import SemiFungiblePositionManager
from pytypes.lib.v3core.contracts.interfaces.IUniswapV3Factory import IUniswapV3Factory
from pytypes.contracts.PanopticFactory import PanopticFactory
from pytypes.contracts.libraries.FeesCalc import FeesCalc
from pytypes.contracts.univ3libraries.TickMath import TickMath
from pytypes.contracts.univ3libraries.LiquidityAmounts import LiquidityAmounts
from pytypes.contracts.libraries.InteractionHelper import InteractionHelper
from pytypes.contracts.libraries.PanopticMath import PanopticMath

from woke_tests.framework.generators.random.fuzz_test import FuzzTest


class Init(FuzzTest):
    chain: Chain
    paccs: Tuple[Account, ...]
    users: Tuple[Account, ...]
    state: State  # pyright: ignore [reportUninitializedInstanceVariable]

    # put your contracts here
    # tokens: List[ERC20]
    sfpm: SemiFungiblePositionManager
    V3FACTORY: IUniswapV3Factory
    panopticFactory: PanopticFactory
    factory_owner: Account

    def __init__(s):
        # ===== Initialize accounts =====
        super().__init__()
        s.chain = default_chain
        s.paccs = tuple(s.chain.accounts[i] for i in range(NUM_PACCS))
        s.users = s.chain.accounts[NUM_PACCS : NUM_PACCS + NUM_USERS]

        # standup some libraries we need
        TickMath.deploy(from_=s.paccs[0])
        LiquidityAmounts.deploy(from_=s.paccs[0])
        FeesCalc.deploy(from_=s.paccs[0])
        InteractionHelper.deploy(from_=s.paccs[0])
        s.panoptic_math = PanopticMath.deploy(from_=s.paccs[0])
        # ===== Add labels =====
        for idx, usr in enumerate(s.users):
            usr.label = crypto_names[idx]
