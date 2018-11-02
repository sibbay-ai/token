
var SibbayHealthToken = artifacts.require("./SibbayHealthToken.sol");
const { increaseTime } = require("./utils/increaseTime.js");
const { latestTime } = require("./utils/latestTime.js");

contract("SibbayHealthToken-balance-extension", accounts => {
    const [sender, owner, fundAccount, spender, acc1, acc2, acc3] = accounts;
    const MAGNITUDE = 10 ** 18;
    const DAY = 3600 * 24;
    // sell price 0.001 ether
    let sellPrice = 10 ** 15;
    // buy price 0.1 ether
    let buyPrice = 10 ** 17;
    let sht;
    let time;

    beforeEach(async() => {
        sht = await SibbayHealthToken.new(owner, fundAccount);
        time = await latestTime();
    });

    it("available and locked balance should be normal", async() => {
        // transfer now + day
        await sht.transferByDate(acc1, [100 * MAGNITUDE, 100 * MAGNITUDE, 100 * MAGNITUDE], [time - DAY, time + DAY, time + 2*DAY], {from: owner});
        assert.equal(await sht.totalBalanceOf.call(acc1), 300 * MAGNITUDE);
        assert.equal(await sht.balanceOf.call(acc1), 100 * MAGNITUDE);
        assert.equal(await sht.lockedBalanceOf.call(acc1), 200 * MAGNITUDE);
        var res = await sht.accounts.call(acc1);
        assert.equal(res[0], 200 * MAGNITUDE);
        assert.equal(res[1], time + DAY);
        assert.equal(res[2], time + 2*DAY);
        res = await sht.lockedBalanceOfByDate(acc1, res[1]);
        assert.equal(res[0], 100 * MAGNITUDE);
        assert.equal(res[1], time + 2*DAY);
        res = await sht.lockedBalanceOfByDate(acc1, res[1]);
        assert.equal(res[0], 100 * MAGNITUDE);
        assert.equal(res[1], 0);
    })

    // same to above
    it("balance should be right without expired locked balance", async() => {
        // transfer now + day
        await sht.transferByDate(acc1, [100 * MAGNITUDE, 100 * MAGNITUDE, 100 * MAGNITUDE], [time - DAY, time + DAY, time + 2*DAY], {from: owner});
        assert.equal(await sht.totalBalanceOf.call(acc1), 300 * MAGNITUDE);
        assert.equal(await sht.balanceOf.call(acc1), 100 * MAGNITUDE);
        assert.equal(await sht.lockedBalanceOf.call(acc1), 200 * MAGNITUDE);
        var res = await sht.accounts.call(acc1);
        assert.equal(res[0], 200 * MAGNITUDE);
        assert.equal(res[1], time + DAY);
        assert.equal(res[2], time + 2*DAY);
        res = await sht.lockedBalanceOfByDate(acc1, res[1]);
        assert.equal(res[0], 100 * MAGNITUDE);
        assert.equal(res[1], time + 2*DAY);
        res = await sht.lockedBalanceOfByDate(acc1, res[1]);
        assert.equal(res[0], 100 * MAGNITUDE);
        assert.equal(res[1], 0);
    })

    it("balance should be right with part expired locked balance", async() => {
        // transfer now + day
        await sht.transferByDate(acc1, [100 * MAGNITUDE, 100 * MAGNITUDE, 100 * MAGNITUDE], [time - DAY, time + DAY, time + 2*DAY], {from: owner});
        assert.equal(await sht.totalBalanceOf.call(acc1), 300 * MAGNITUDE);
        assert.equal(await sht.balanceOf.call(acc1), 100 * MAGNITUDE);
        assert.equal(await sht.lockedBalanceOf.call(acc1), 200 * MAGNITUDE);
        var res = await sht.accounts.call(acc1);
        assert.equal(res[0], 200 * MAGNITUDE);
        assert.equal(res[1], time + DAY);
        assert.equal(res[2], time + 2*DAY);
        res = await sht.lockedBalanceOfByDate(acc1, res[1]);
        assert.equal(res[0], 100 * MAGNITUDE);
        assert.equal(res[1], time + 2*DAY);
        res = await sht.lockedBalanceOfByDate(acc1, res[1]);
        assert.equal(res[0], 100 * MAGNITUDE);
        assert.equal(res[1], 0);

        // increase one day
        await increaseTime(DAY);

        // balance
        assert.equal(await sht.totalBalanceOf.call(acc1), 300 * MAGNITUDE);
        assert.equal(await sht.balanceOf.call(acc1), 200 * MAGNITUDE);
        assert.equal(await sht.lockedBalanceOf.call(acc1), 100 * MAGNITUDE);
        var res = await sht.accounts.call(acc1);
        assert.equal(res[0], 200 * MAGNITUDE);
        assert.equal(res[1], time + DAY);
        assert.equal(res[2], time + 2*DAY);
        res = await sht.lockedBalanceOfByDate(acc1, res[1]);
        assert.equal(res[0], 100 * MAGNITUDE);
        assert.equal(res[1], time + 2*DAY);
        res = await sht.lockedBalanceOfByDate(acc1, res[1]);
        assert.equal(res[0], 100 * MAGNITUDE);
        assert.equal(res[1], 0);
    })

    it("balance should be right with all expired locked balance", async() => {
        // transfer now + day
        await sht.transferByDate(acc1, [100 * MAGNITUDE, 100 * MAGNITUDE, 100 * MAGNITUDE], [time - DAY, time + DAY, time + 2*DAY], {from: owner});
        assert.equal(await sht.totalBalanceOf.call(acc1), 300 * MAGNITUDE);
        assert.equal(await sht.balanceOf.call(acc1), 100 * MAGNITUDE);
        assert.equal(await sht.lockedBalanceOf.call(acc1), 200 * MAGNITUDE);
        var res = await sht.accounts.call(acc1);
        assert.equal(res[0], 200 * MAGNITUDE);
        assert.equal(res[1], time + DAY);
        assert.equal(res[2], time + 2*DAY);
        res = await sht.lockedBalanceOfByDate(acc1, res[1]);
        assert.equal(res[0], 100 * MAGNITUDE);
        assert.equal(res[1], time + 2*DAY);
        res = await sht.lockedBalanceOfByDate(acc1, res[1]);
        assert.equal(res[0], 100 * MAGNITUDE);
        assert.equal(res[1], 0);

        // increase 2 day
        await increaseTime(2*DAY);

        // balance
        assert.equal(await sht.totalBalanceOf.call(acc1), 300 * MAGNITUDE);
        assert.equal(await sht.balanceOf.call(acc1), 300 * MAGNITUDE);
        assert.equal(await sht.lockedBalanceOf.call(acc1), 0 * MAGNITUDE);
        var res = await sht.accounts.call(acc1);
        assert.equal(res[0], 200 * MAGNITUDE);
        assert.equal(res[1], time + DAY);
        assert.equal(res[2], time + 2*DAY);
        res = await sht.lockedBalanceOfByDate(acc1, res[1]);
        assert.equal(res[0], 100 * MAGNITUDE);
        assert.equal(res[1], time + 2*DAY);
        res = await sht.lockedBalanceOfByDate(acc1, res[1]);
        assert.equal(res[0], 100 * MAGNITUDE);
        assert.equal(res[1], 0);
    })
})
