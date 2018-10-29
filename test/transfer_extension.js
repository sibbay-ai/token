
var SibbayHealthToken = artifacts.require("./SibbayHealthToken.sol");
const { increaseTime } = require("./utils/increaseTime.js");
const { latestTime } = require("./utils/latestTime.js");
var log4js = require('log4js');

contract("SibbayHealthToken-transfer-extension", accounts => {

    const [owner, fundAccount, acc1, acc2, acc3] = accounts;
    const MAGNITUDE = 10 ** 18;
    const DAY = 3600 * 24;
    // sell price 0.001 ether
    let sellPrice = 10 ** 15;
    // buy price 0.1 ether
    let buyPrice = 10 ** 17;
    let sht;
    let time;

    // logger
    var logger = log4js.getLogger();
    logger.level = 'info';

    beforeEach(async() => {
        sht = await SibbayHealthToken.new(fundAccount);
        time = await latestTime();
    });

    it("transfer 100 tokens to fund account and get eth should be successful", async() => {
        await sht.setSellPrice(sellPrice, {from: owner});
        await sht.setBuyPrice(buyPrice, {from: owner});
        await sht.addTokenToFund(100*MAGNITUDE, {from: owner});
        await sht.sendTransaction({from: owner, value: 1 * MAGNITUDE});
        await sht.openBuy({from: owner});
        assert.equal(await sht.buyFlag.call(), true);
        await sht.openSell({from: owner});
        assert.equal(await sht.sellFlag.call(), true);

        await sht.transfer(acc1, 100 * MAGNITUDE, {from: owner});
        assert.equal(await sht.balanceOf.call(acc1), 100 * MAGNITUDE);

        await sht.transfer(fundAccount, 100 * MAGNITUDE, {from: acc1});
        assert.equal(await sht.balanceOf.call(acc1), 0 * MAGNITUDE);
    })

    it("transfer 100 tokens to 0 account should be failed", async() => {
        try{
            await sht.transfer(0x0, 100 *MAGNITUDE, {from: owner});
            assert.fail();
        } catch (err) {
            assert.ok(/revert/.test(err.message));
        }
    })

    it("frozen account transfers 100 tokens to normal account should be failed", async() => {
        await sht.transfer(acc1, 100 * MAGNITUDE, {from: owner});
        assert.equal(await sht.balanceOf.call(acc1), 100 * MAGNITUDE);

        await sht.froze(acc1, {from: owner});
        try{
            await sht.transfer(acc2, 100 *MAGNITUDE, {from: acc1});
            assert.fail();
        } catch (err) {
            assert.ok(/revert/.test(err.message));
        }
    })

    it("frozen account transfers 100 tokens to 0 account should be successful", async() => {
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
        assert.equal(await sht.balanceOf.call(acc1), 100 * MAGNITUDE);

        await sht.froze(acc1, {from: owner});

        await sht.transfer(0x0, 100 *MAGNITUDE, {from: acc1});
        assert.equal(await sht.balanceOf.call(acc1), 0 * MAGNITUDE);
        assert.equal(await sht.balanceOf.call(0x0), 100 * MAGNITUDE);
    })

    it("transfer 100 tokens exceeds avaliables without expired locked tokens should be failed", async() => {
        // transfer now + day
        await sht.transferByDate(acc1, [100 * MAGNITUDE], [time + DAY], {from: owner});
        assert.equal(await sht.balanceOf.call(acc1), 100 * MAGNITUDE);
        assert.equal(await sht.availableBalanceOf.call(acc1), 0 * MAGNITUDE);
        assert.equal(await sht.lockedBalanceOf.call(acc1), 100 * MAGNITUDE);
        var res = await sht.accounts.call(acc1);
        assert.equal(res[0], 100 * MAGNITUDE);
        assert.equal(res[1], time + DAY);
        assert.equal(res[2], time + DAY);
        var res2 = await sht.lockedBalanceOfByDate(acc1, res[1]);
        assert.equal(res2[0], 100 * MAGNITUDE);
        assert.equal(res2[1], 0);

        // tranfer bydate to acc2
        try {
            await sht.transfer(acc2, 100 * MAGNITUDE, {from: acc1});
            assert.fail();
        } catch (err){
            assert.ok(/revert/.test(err.message));
        }
    })

    it("transfer 100 tokens exceeds avaliables without enough expired locked tokens should be failed", async() => {
        // transfer now + day
        await sht.transferByDate(acc1, [100 * MAGNITUDE], [time + DAY], {from: owner});
        assert.equal(await sht.balanceOf.call(acc1), 100 * MAGNITUDE);
        assert.equal(await sht.availableBalanceOf.call(acc1), 0 * MAGNITUDE);
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

        // tranfer bydate to acc2
        try {
            await sht.transfer(acc2, 200 * MAGNITUDE, {from: acc1});
            assert.fail();
        } catch (err){
            assert.ok(/revert/.test(err.message));
        }
    })

    it("transfer 100 tokens exceeds avaliables with enough expired locked tokens should be successful", async() => {
        // transfer now + day
        await sht.transferByDate(acc1, [100 * MAGNITUDE], [time + DAY], {from: owner});
        assert.equal(await sht.balanceOf.call(acc1), 100 * MAGNITUDE);
        assert.equal(await sht.availableBalanceOf.call(acc1), 0 * MAGNITUDE);
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

        await sht.transfer(acc2, 100 * MAGNITUDE, {from: acc1});

        assert.equal(await sht.balanceOf.call(acc1), 0);
        assert.equal(await sht.balanceOf.call(acc2), 100 * MAGNITUDE);
    })

})
