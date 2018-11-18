
var SibbayHealthToken = artifacts.require("./SibbayHealthToken.sol");
const { increaseTime } = require("./utils/increaseTime.js");
const { latestTime } = require("./utils/latestTime.js");
var log4js = require('log4js');

contract("SibbayHealthToken-auto-free-extension", accounts => {

    const [sender, owner, fundAccount, acc1, acc2, acc3] = accounts;
    const MAGNITUDE = 10 ** 18;
    const DAY = 3600 * 24;
    // sell price 0.001 ether
    let sellPrice = 10 ** 15;
    let sht;
    let time;

    // logger
    var logger = log4js.getLogger();
    logger.level = 'info';

    beforeEach(async() => {
        sht = await SibbayHealthToken.new(owner, fundAccount);
        time = await latestTime();
    });

    it("auto free is normal", async() => {
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

        // refresh
        await sht.refresh(acc1, {from: owner});

        assert.equal(await sht.balanceOf.call(acc1), 100 * MAGNITUDE);
        assert.equal(await sht.availableBalanceOf.call(acc1), 100 * MAGNITUDE);
        assert.equal(await sht.lockedBalanceOf.call(acc1), 0 * MAGNITUDE);
        var res = await sht.accounts.call(acc1);
        assert.equal(res[0], 0);
        assert.equal(res[1], 0);
        assert.equal(res[2], 0);

    })

    it("can't free lock balance when auto free is closed", async() => {
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

        // close auto free
        await sht.closeAutoFree(acc1, {from: owner});
        assert.equal(await sht.autoFreeLockBalance.call(acc1), true);

        // increase time
        await increaseTime(DAY);

        // refresh
        await sht.refresh(acc1, {from: owner});
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

    })

    it("free lock balance when force auto free is opened", async() => {
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

        // close auto free
        await sht.closeAutoFree(acc1, {from: owner});
        assert.equal(await sht.autoFreeLockBalance.call(acc1), true);

        // open force auto free
        await sht.openForceAutoFree(acc1, {from: owner});
        assert.equal(await sht.forceAutoFreeLockBalance.call(acc1), true);

        // increase time
        await increaseTime(DAY);

        // refresh
        await sht.refresh(acc1, {from: owner});
        assert.equal(await sht.balanceOf.call(acc1), 100 * MAGNITUDE);
        assert.equal(await sht.availableBalanceOf.call(acc1), 100 * MAGNITUDE);
        assert.equal(await sht.lockedBalanceOf.call(acc1), 0 * MAGNITUDE);
        var res = await sht.accounts.call(acc1);
        assert.equal(res[0], 0);
        assert.equal(res[1], 0);
        assert.equal(res[2], 0);
    })

})
