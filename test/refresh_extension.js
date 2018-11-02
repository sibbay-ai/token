var SibbayHealthToken = artifacts.require("./SibbayHealthToken.sol");
const { increaseTime } = require("./utils/increaseTime.js");
const { latestTime } = require("./utils/latestTime.js");

contract("SibbayHealthToken-refresh-extension", accounts => {

    const [sender, owner, fundAccount, acc1, acc2, acc3] = accounts;
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

    it("refresh should be successful", async() => {
        await sht.transferByDate(acc1, [100 * MAGNITUDE, 100 * MAGNITUDE], [time + DAY, time + 2*DAY], {from: owner});
        assert.equal(await sht.totalBalanceOf.call(acc1), 200 * MAGNITUDE);
        assert.equal(await sht.balanceOf.call(acc1), 0 * MAGNITUDE);
        assert.equal(await sht.lockedBalanceOf.call(acc1), 200 * MAGNITUDE);
        var res = await sht.accounts.call(acc1);
        assert.equal(res[0], 200 * MAGNITUDE);
        assert.equal(res[1], time + DAY);
        assert.equal(res[2], time + 2*DAY);
        res = await sht.lockedBalanceOfByDate(acc1, res[1]);
        assert.equal(res[0], 100 * MAGNITUDE);
        assert.equal(res[1], time+2*DAY);
        res = await sht.lockedBalanceOfByDate(acc1, res[1]);
        assert.equal(res[0], 100 * MAGNITUDE);
        assert.equal(res[1], 0);

        // increase time
        await increaseTime(DAY);

        // refresh
        await sht.refresh(acc1, {from: owner});

        // balance
        res = await sht.accounts.call(acc1);
        assert.equal(res[0], 100 * MAGNITUDE);
        assert.equal(res[1], time + 2*DAY);
        assert.equal(res[2], time + 2*DAY);
        res = await sht.lockedBalanceOfByDate(acc1, res[1]);
        assert.equal(res[0], 100 * MAGNITUDE);
        assert.equal(res[1], 0);
    })

    it("refresh should be failedi when paused", async() => {
        await sht.transferByDate(acc1, [100 * MAGNITUDE, 100 * MAGNITUDE], [time + DAY, time + 2*DAY], {from: owner});
        assert.equal(await sht.totalBalanceOf.call(acc1), 200 * MAGNITUDE);
        assert.equal(await sht.balanceOf.call(acc1), 0 * MAGNITUDE);
        assert.equal(await sht.lockedBalanceOf.call(acc1), 200 * MAGNITUDE);
        var res = await sht.accounts.call(acc1);
        assert.equal(res[0], 200 * MAGNITUDE);
        assert.equal(res[1], time + DAY);
        assert.equal(res[2], time + 2*DAY);
        res = await sht.lockedBalanceOfByDate(acc1, res[1]);
        assert.equal(res[0], 100 * MAGNITUDE);
        assert.equal(res[1], time+2*DAY);
        res = await sht.lockedBalanceOfByDate(acc1, res[1]);
        assert.equal(res[0], 100 * MAGNITUDE);
        assert.equal(res[1], 0);

        // pause contract
        await sht.pause({from: owner});
        // increase time
        await increaseTime(DAY);

        // refresh
        try {
            await sht.refresh(acc1, {from: owner});
            assert.fail();
        } catch (err){
            assert.ok(/revert/.test(err.message));
        }

        // balance
        res = await sht.accounts.call(acc1);
        assert.equal(res[0], 200 * MAGNITUDE);
        assert.equal(res[1], time + DAY);
        assert.equal(res[2], time + 2*DAY);
        res = await sht.lockedBalanceOfByDate(acc1, res[1]);
        assert.equal(res[0], 100 * MAGNITUDE);
        assert.equal(res[1], time+2*DAY);
        res = await sht.lockedBalanceOfByDate(acc1, res[1]);
        assert.equal(res[0], 100 * MAGNITUDE);
        assert.equal(res[1], 0);
    })

})
