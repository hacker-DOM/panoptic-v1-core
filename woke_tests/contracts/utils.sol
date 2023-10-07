// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

import {PanopticMath} from "@libraries/PanopticMath.sol";

import {PanopticFactory} from "@contracts/PanopticFactory.sol";

import {SemiFungiblePositionManager} from "@contracts/SemiFungiblePositionManager.sol";
import {IUniswapV3Factory} from "univ3-core/interfaces/IUniswapV3Factory.sol";
import {IUniswapV3Pool} from "univ3-core/interfaces/IUniswapV3Pool.sol";

import {CallbackLib} from "@libraries/CallbackLib.sol";
import {Constants} from "@libraries/Constants.sol";
import {TickMath} from "univ3-core/libraries/TickMath.sol";
import {SafeTransferLib} from "@libraries/SafeTransferLib.sol";
import {PoolAddress} from "univ3-periphery/libraries/PoolAddress.sol";

//see PanopticFactory.t.sol

import "woke/console.sol";

contract PanopticFactoryHarness is PanopticFactory {
    constructor(
        address _WETH9,
        SemiFungiblePositionManager _SFPM,
        IUniswapV3Factory _univ3Factory,
        address poolReference,
        address collateralReference
    ) PanopticFactory(_WETH9, _SFPM, _univ3Factory, poolReference, collateralReference) {}

    function getPoolReference() external view returns (address) {
        return POOL_REFERENCE;
    }
}

contract Utils {
    address _WETH = 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2;
    uint128 constant FULL_RANGE_LIQUIDITY_AMOUNT_WETH = 0.1 ether;
    uint128 constant FULL_RANGE_LIQUIDITY_AMOUNT_TOKEN = 1e6;
    IUniswapV3Factory V3FACTORY = IUniswapV3Factory(0x1F98431c8aD98523631AE4a59f267346ea31F984);

    // Replicated from PanopticFactory.sol
    function getSalt(
        address v3Pool,
        address deployer,
        uint96 nonce
    ) external pure returns (bytes32) {
        return
            bytes32(
                abi.encodePacked(PanopticMath.getPoolId(v3Pool), uint64(uint160(deployer)), nonce)
            );
    }

    function predictDeterministicAddress(
        address implementation,
        bytes32 salt,
        address deployer
    ) external pure returns (address predicted) {
        assembly ("memory-safe") {
            let ptr := mload(0x40)
            mstore(add(ptr, 0x38), deployer)
            mstore(add(ptr, 0x24), 0x5af43d82803e903d91602b57fd5bf3ff)
            mstore(add(ptr, 0x14), implementation)
            mstore(ptr, 0x3d602d80600a3d3981f3363d3d373d3d3d363d73)
            mstore(add(ptr, 0x58), salt)
            mstore(add(ptr, 0x78), keccak256(add(ptr, 0x0c), 0x37))
            predicted := keccak256(add(ptr, 0x43), 0x55)
        }
    }

    /*//////////////////////////////////////////////////////////////
                COMPUTE FULL RANGE LIQUIDITY
    //////////////////////////////////////////////////////////////*/

    struct CallbackData {
        PoolAddress.PoolKey univ3poolKey;
        address payer;
    }

    /// Replicated logic from _mintFullRange in Panoptic Factory

    function computeFullRangeLiquidity(
        address panopticFactory,
        IUniswapV3Pool pool
    ) external returns (uint128 fullRangeLiquidity, uint256 amount0, uint256 amount1) {
        // get current tick
        (uint160 currentSqrtPriceX96, , , , , , ) = pool.slot0();

        // build callback data
        bytes memory mintdata = abi.encode(
            CallbackData({ // compute by reading values from univ3pool every time
                univ3poolKey: PoolAddress.PoolKey({
                    token0: pool.token0(),
                    token1: pool.token1(),
                    fee: pool.fee()
                }),
                payer: msg.sender
            })
        );

        // For full range: L = Δx * sqrt(P) = Δy / sqrt(P)
        // We start with fixed delta amounts and apply this equation to calculate the liquidity
        unchecked {
            // Since we know one of the tokens is WETH, we simply add 0.1 ETH + worth in tokens
            if (pool.token0() == _WETH) {
                fullRangeLiquidity = uint128(
                    (FULL_RANGE_LIQUIDITY_AMOUNT_WETH * currentSqrtPriceX96) / Constants.FP96
                );
            } else if (pool.token1() == _WETH) {
                fullRangeLiquidity = uint128(
                    (FULL_RANGE_LIQUIDITY_AMOUNT_WETH * Constants.FP96) / currentSqrtPriceX96
                );
            } else {
                // Find the resulting liquidity for providing 1e6 of both tokens
                uint128 liquidity0 = uint128(
                    (FULL_RANGE_LIQUIDITY_AMOUNT_TOKEN * currentSqrtPriceX96) / Constants.FP96
                );
                uint128 liquidity1 = uint128(
                    (FULL_RANGE_LIQUIDITY_AMOUNT_TOKEN * Constants.FP96) / currentSqrtPriceX96
                );

                // Pick the greater of the liquidities - i.e the more "expensive" option
                // This ensures that the liquidity added is sufficiently large
                fullRangeLiquidity = liquidity0 > liquidity1 ? liquidity0 : liquidity1;
            }

            // simulate the amounts minted in the uniswap pool
            // we will revert from woke
            (amount0, amount1) = IUniswapV3Pool(pool).mint(
                address(this),
                (TickMath.MIN_TICK / pool.tickSpacing()) * pool.tickSpacing(),
                (TickMath.MAX_TICK / pool.tickSpacing()) * pool.tickSpacing(),
                fullRangeLiquidity,
                mintdata
            );
        }
    }

    function uniswapV3MintCallback(
        uint256 amount0Owed,
        uint256 amount1Owed,
        bytes calldata data
    ) external {
        console.log("in callback");
        // Decode the mint callback data
        CallbackLib.CallbackData memory decoded = abi.decode(data, (CallbackLib.CallbackData));
        // Validate caller to ensure we got called from the AMM pool
        CallbackLib.validateCallback(msg.sender, address(V3FACTORY), decoded.poolFeatures);

        // Sends the amount0Owed and amount1Owed quantities provided
        if (amount0Owed > 0) {
            console.log("token 0", decoded.payer, msg.sender);
        }
        SafeTransferLib.safeTransferFrom(
            decoded.poolFeatures.token0,
            decoded.payer,
            msg.sender,
            amount0Owed
        );
        if (amount1Owed > 0) {
            console.log("token 1", decoded.payer, msg.sender);
        }
        SafeTransferLib.safeTransferFrom(
            decoded.poolFeatures.token1,
            decoded.payer,
            msg.sender,
            amount1Owed
        );
    }
}
