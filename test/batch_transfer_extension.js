
var SibbayHealthToken = artifacts.require("./SibbayHealthToken.sol");
const { increaseTime } = require("./utils/increaseTime.js");
const { latestTime } = require("./utils/latestTime.js");

contract("SibbayHealthToken-batch-transfer-extension", accounts => {
    const [owner, fundAccount, acc1, acc2, acc3] = accounts;
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

    it("batch transfer should be successful", async() => {
        await sht.batchTransfer([acc1, acc2, acc3], [100 * MAGNITUDE, 100 * MAGNITUDE, 100 * MAGNITUDE], {from: owner});
        assert.equal(await sht.balanceOf.call(acc1), 100 * MAGNITUDE);
        assert.equal(await sht.balanceOf.call(acc2), 100 * MAGNITUDE);
        assert.equal(await sht.balanceOf.call(acc3), 100 * MAGNITUDE);
    })

    it("batch transfer to fund acount should be failed", async() => {
        // set fund and open buy/sell flag
        await sht.setSellPrice(sellPrice, {from: owner});
        await sht.setBuyPrice(buyPrice, {from: owner});
        await sht.addTokenToFund(100*MAGNITUDE, {from: owner});
        await sht.sendTransaction({from: owner, value: 1 * MAGNITUDE});
        await sht.openBuy({from: owner});
        assert.equal(await sht.buyFlag.call(), true);
        await sht.openSell({from: owner});
        assert.equal(await sht.sellFlag.call(), true);

        try {
            await sht.batchTransfer([fundAccount], [100 * MAGNITUDE], {from: owner});
            assert.fail();
        } catch (err){
            assert.ok(/revert/.test(err.message));
        }
    })

    it("batch transfer to 0 acount should be failed", async() => {
        try {
            await sht.batchTransfer([0x0], [100 * MAGNITUDE], {from: owner});
            assert.fail();
        } catch (err){
            assert.ok(/revert/.test(err.message));
        }
    })

    it("batch transfer exceeds avaliables without expired locked tokens should be failed", async() => {
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
            await sht.batchTransfer([acc2], [100 * MAGNITUDE], {from: acc1});
            assert.fail();
        } catch (err){
            assert.ok(/revert/.test(err.message));
        }
    })

    it("batch transfer exceeds avaliables without enough expired locked tokens should be failed", async() => {
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

        // transfer 200 tokens
        try {
            await sht.batchTransfer([acc2, acc3], [100 * MAGNITUDE, 100 * MAGNITUDE], {from: acc1});
            assert.fail();
        } catch (err){
            assert.ok(/revert/.test(err.message));
        }
    })

    it("batch transfer exceeds avaliables with enough expired locked tokens should be successful", async() => {
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

        // transfer now + day
        await sht.batchTransfer([acc2, acc3], [50 * MAGNITUDE, 50 * MAGNITUDE], {from: acc1});

        // acc1
        assert.equal(await sht.balanceOf.call(acc1), 0 * MAGNITUDE);
        assert.equal(await sht.availableBalanceOf.call(acc1), 0 * MAGNITUDE);
        assert.equal(await sht.lockedBalanceOf.call(acc1), 0 * MAGNITUDE);
        var res = await sht.accounts.call(acc1);
        assert.equal(res[0], 0 * MAGNITUDE);
        assert.equal(res[1], 0);
        assert.equal(res[2], 0);

        // acc2
        assert.equal(await sht.balanceOf.call(acc2), 50 * MAGNITUDE);
        assert.equal(await sht.availableBalanceOf.call(acc2), 50 * MAGNITUDE);
        assert.equal(await sht.lockedBalanceOf.call(acc2), 0 * MAGNITUDE);

        // acc3
        assert.equal(await sht.balanceOf.call(acc3), 50 * MAGNITUDE);
        assert.equal(await sht.availableBalanceOf.call(acc3), 50 * MAGNITUDE);
        assert.equal(await sht.lockedBalanceOf.call(acc3), 0 * MAGNITUDE);
    })
})
