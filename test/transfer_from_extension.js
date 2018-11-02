
var SibbayHealthToken = artifacts.require("./SibbayHealthToken.sol");
const { increaseTime } = require("./utils/increaseTime.js");
const { latestTime } = require("./utils/latestTime.js");

contract("SibbayHealthToken-transfer-from-extension", accounts => {

    const [owner, fundAccount, spender, acc1, acc2, acc3] = accounts;
    const MAGNITUDE = 10 ** 18;
    const DAY = 3600 * 24;
    // sell price 0.001 ether
    let sellPrice = 10 ** 15;
    // buy price 0.1 ether
    let buyPrice = 10 ** 17;
    let sht;
    let time;

    beforeEach(async() => {
        sht = await SibbayHealthToken.new(fundAccount);
        time = await latestTime();
    });

    it("transfer from 100 tokens to fund account and get eth should be failed", async() => {
        await sht.setSellPrice(sellPrice, {from: owner});
        await sht.setBuyPrice(buyPrice, {from: owner});
        await sht.addTokenToFund(100*MAGNITUDE, {from: owner});
        await sht.sendTransaction({from: owner, value: 1 * MAGNITUDE});
        await sht.openBuy({from: owner});
        assert.equal(await sht.buyFlag.call(), true);
        await sht.openSell({from: owner});
        assert.equal(await sht.sellFlag.call(), true);

        await sht.transfer(acc1, 100 * MAGNITUDE, {from: owner});
        assert.equal(await sht.totalBalanceOf.call(acc1), 100 * MAGNITUDE);

        // approve
        await sht.approve(spender, 100 * MAGNITUDE, {from: acc1});
        assert.equal(await sht.allowance.call(acc1, spender), 100 * MAGNITUDE);

        try{
            await sht.transferFrom(acc1, fundAccount, 100 * MAGNITUDE, {from: spender});
            assert.fail();
        } catch (err) {
            assert.ok(/revert/.test(err.message));
        }
    })

    it("transfer from 100 tokens to 0 account should be failed", async() => {
        // approve
        await sht.approve(spender, 100 * MAGNITUDE, {from: owner});
        assert.equal(await sht.allowance.call(owner, spender), 100 * MAGNITUDE);

        try{
            await sht.transferFrom(owner, 0x0, 100 *MAGNITUDE, {from: spender});
            assert.fail();
        } catch (err) {
            assert.ok(/revert/.test(err.message));
        }
    })

    it("frozen account transfers from 100 tokens to normal account should be failed", async() => {
        // transfer
        await sht.transfer(acc1, 100 * MAGNITUDE, {from: owner});
        assert.equal(await sht.totalBalanceOf.call(acc1), 100 * MAGNITUDE);

        // approve
        await sht.approve(spender, 100 * MAGNITUDE, {from: acc1});
        assert.equal(await sht.allowance.call(acc1, spender), 100 * MAGNITUDE);

        await sht.froze(acc1, {from: owner});
        try{
            await sht.transferFrom(acc1, acc2, 100 *MAGNITUDE, {from: spender});
            assert.fail();
        } catch (err) {
            assert.ok(/revert/.test(err.message));
        }
    })

    it("frozen account transfers from 100 tokens to 0 account should be failed", async() => {
        // set fund and open buy/sell flag
        await sht.setSellPrice(sellPrice, {from: owner});
        await sht.setBuyPrice(buyPrice, {from: owner});
        await sht.addTokenToFund(100*MAGNITUDE, {from: owner});
        await sht.sendTransaction({from: owner, value: 1 * MAGNITUDE});
        await sht.openBuy({from: owner});
        assert.equal(await sht.buyFlag.call(), true);
        await sht.openSell({from: owner});
        assert.equal(await sht.sellFlag.call(), true);

        await sht.transfer(acc1, 100 * MAGNITUDE, {from: owner});
        assert.equal(await sht.totalBalanceOf.call(acc1), 100 * MAGNITUDE);

        // approve
        await sht.approve(spender, 100 * MAGNITUDE, {from: acc1});
        assert.equal(await sht.allowance.call(acc1, spender), 100 * MAGNITUDE);

        await sht.froze(acc1, {from: owner});

        try{
            await sht.transferFrom(acc1, 0x0, 100 *MAGNITUDE, {from: spender});
            assert.fail();
        } catch (err) {
            assert.ok(/revert/.test(err.message));
        }
    })

    it("transfer from 100 tokens without enough approval should be failed", async() => {
        // approve
        await sht.approve(spender, 100 * MAGNITUDE, {from: owner});
        assert.equal(await sht.allowance.call(owner, spender), 100 * MAGNITUDE);

        try {
            await sht.transferFrom(owner, acc1, 200 * MAGNITUDE, {from: spender});
            assert.fail();
        } catch (err){
            assert.ok(/revert/.test(err.message));
        }
    })

    it("transfer from 100 tokens exceeds avaliables without expired locked tokens should be failed", async() => {
        // approve
        await sht.approve(spender, 100 * MAGNITUDE, {from: owner});
        assert.equal(await sht.allowance.call(owner, spender), 100 * MAGNITUDE);

        // transfer now + day
        await sht.transferFromByDate(owner, acc1, [100 * MAGNITUDE], [time + DAY], {from: spender});

        // spender
        assert.equal(await sht.allowance.call(owner, spender), 0 * MAGNITUDE);

        // acc1
        assert.equal(await sht.totalBalanceOf.call(acc1), 100 * MAGNITUDE);
        assert.equal(await sht.balanceOf.call(acc1), 0 * MAGNITUDE);
        assert.equal(await sht.lockedBalanceOf.call(acc1), 100 * MAGNITUDE);
        var res = await sht.accounts.call(acc1);
        assert.equal(res[0], 100 * MAGNITUDE);
        assert.equal(res[1], time + DAY);
        assert.equal(res[2], time + DAY);
        var res2 = await sht.lockedBalanceOfByDate(acc1, res[1]);
        assert.equal(res2[0], 100 * MAGNITUDE);
        assert.equal(res2[1], 0);

        // approve
        await sht.approve(spender, 100 * MAGNITUDE, {from: acc1});
        assert.equal(await sht.allowance.call(acc1, spender), 100 * MAGNITUDE);

        // tranfer
        try {
            await sht.transferFrom(acc1, acc2, 100 * MAGNITUDE, {from: spender});
            assert.fail();
        } catch (err){
            assert.ok(/revert/.test(err.message));
        }
    })

    it("transfer from 100 tokens exceeds avaliables without enough expired locked tokens should be failed", async() => {
        // approve
        await sht.approve(spender, 100 * MAGNITUDE, {from: owner});
        assert.equal(await sht.allowance.call(owner, spender), 100 * MAGNITUDE);

        // transfer now + day
        await sht.transferFromByDate(owner, acc1, [100 * MAGNITUDE], [time + DAY], {from: spender});

        // spender
        assert.equal(await sht.allowance.call(owner, spender), 0 * MAGNITUDE);

        // acc1
        assert.equal(await sht.totalBalanceOf.call(acc1), 100 * MAGNITUDE);
        assert.equal(await sht.balanceOf.call(acc1), 0 * MAGNITUDE);
        assert.equal(await sht.lockedBalanceOf.call(acc1), 100 * MAGNITUDE);
        var res = await sht.accounts.call(acc1);
        assert.equal(res[0], 100 * MAGNITUDE);
        assert.equal(res[1], time + DAY);
        assert.equal(res[2], time + DAY);
        var res2 = await sht.lockedBalanceOfByDate(acc1, res[1]);
        assert.equal(res2[0], 100 * MAGNITUDE);
        assert.equal(res2[1], 0);

        // increase time
        await increaseTime(DAY);
        time = time + DAY;

        // approve
        await sht.approve(spender, 100 * MAGNITUDE, {from: acc1});
        assert.equal(await sht.allowance.call(acc1, spender), 100 * MAGNITUDE);

        // tranfer
        try {
            await sht.transferFrom(acc1, acc2, 200 * MAGNITUDE, {from: spender});
            assert.fail();
        } catch (err){
            assert.ok(/revert/.test(err.message));
        }
    })

    it("transfer from 100 tokens exceeds avaliables with enough expired locked tokens should be successful", async() => {
        // approve
        await sht.approve(spender, 100 * MAGNITUDE, {from: owner});
        assert.equal(await sht.allowance.call(owner, spender), 100 * MAGNITUDE);

        // transfer now + day
        await sht.transferFromByDate(owner, acc1, [100 * MAGNITUDE], [time + DAY], {from: spender});

        // spender
        assert.equal(await sht.allowance.call(owner, spender), 0 * MAGNITUDE);

        // acc1
        assert.equal(await sht.totalBalanceOf.call(acc1), 100 * MAGNITUDE);
        assert.equal(await sht.balanceOf.call(acc1), 0 * MAGNITUDE);
        assert.equal(await sht.lockedBalanceOf.call(acc1), 100 * MAGNITUDE);
        var res = await sht.accounts.call(acc1);
        assert.equal(res[0], 100 * MAGNITUDE);
        assert.equal(res[1], time + DAY);
        assert.equal(res[2], time + DAY);
        var res2 = await sht.lockedBalanceOfByDate(acc1, res[1]);
        assert.equal(res2[0], 100 * MAGNITUDE);
        assert.equal(res2[1], 0);

        // increase time
        await increaseTime(DAY);
        time = time + DAY;

        // approve
        await sht.approve(spender, 100 * MAGNITUDE, {from: acc1});
        assert.equal(await sht.allowance.call(acc1, spender), 100 * MAGNITUDE);

        // tranfer
        await sht.transferFrom(acc1, acc2, 100 * MAGNITUDE, {from: spender});

        // spender
        assert.equal(await sht.allowance.call(acc1, spender), 0 * MAGNITUDE);

        // acc1, acc2
        assert.equal(await sht.totalBalanceOf.call(acc1), 0);
        assert.equal(await sht.totalBalanceOf.call(acc2), 100 * MAGNITUDE);
    })
})
