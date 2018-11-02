
var SibbayHealthToken = artifacts.require("./SibbayHealthToken.sol");
const { increaseTime } = require("./utils/increaseTime.js");
const { latestTime } = require("./utils/latestTime.js");

contract("SibbayHealthToken-transfer-from-by-date-extension", accounts => {

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

    it("transfer from by date should be successful", async() => {
        // approve
        await sht.approve(spender, 100 * MAGNITUDE, {from: owner});
        assert.equal(await sht.allowance.call(owner, spender), 100 * MAGNITUDE);

        // tranfer
        await sht.transferFromByDate(owner, acc1, [100 * MAGNITUDE], [time + DAY], {from: spender});

        // spender
        assert.equal(await sht.allowance.call(owner, spender), 0);

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
    })

    it("transfer from by date to fund account should be failed", async() => {
        // approve
        await sht.approve(spender, 100 * MAGNITUDE, {from: owner});
        assert.equal(await sht.allowance.call(owner, spender), 100 * MAGNITUDE);

        // set fund and open buy/sell flag
        await sht.setSellPrice(sellPrice, {from: owner});
        await sht.setBuyPrice(buyPrice, {from: owner});
        await sht.addTokenToFund(100*MAGNITUDE, {from: owner});
        await sht.sendTransaction({from: owner, value: 1 * MAGNITUDE});
        await sht.openBuy({from: owner});
        assert.equal(await sht.buyFlag.call(), true);
        await sht.openSell({from: owner});
        assert.equal(await sht.sellFlag.call(), true);

        // transfer by date to fund account
        try {
            await sht.transferFromByDate(owner, fundAccount, [100 * MAGNITUDE], [time + DAY], {from: spender});
            assert.fail();
        } catch (err){
            assert.ok(/revert/.test(err.message));
        }
    })

    it("transfer from by date to 0 account should be failed", async() => {
        // approve
        await sht.approve(spender, 100 * MAGNITUDE, {from: owner});
        assert.equal(await sht.allowance.call(owner, spender), 100 * MAGNITUDE);

        try {
            await sht.transferFromByDate(owner, 0x0, [100 * MAGNITUDE], [time + DAY], {from: spender});
            assert.fail();
        } catch (err){
            assert.ok(/revert/.test(err.message));
        }
    })

    it("transfer from by date without enough approval should be failed", async() => {
        // approve
        await sht.approve(spender, 100 * MAGNITUDE, {from: owner});
        assert.equal(await sht.allowance.call(owner, spender), 100 * MAGNITUDE);

        try {
            await sht.transferFromByDate(owner, acc1, [200 * MAGNITUDE], [time + DAY], {from: spender});
            assert.fail();
        } catch (err){
            assert.ok(/revert/.test(err.message));
        }
    })

    it("transfer from by date 0 tokens should be no effect", async() => {
        // approve
        await sht.approve(spender, 100 * MAGNITUDE, {from: owner});
        assert.equal(await sht.allowance.call(owner, spender), 100 * MAGNITUDE);

        await sht.transferFromByDate(owner, acc1, [0], [time + DAY], {from: spender});

        // spender
        assert.equal(await sht.allowance.call(owner, spender), 100 * MAGNITUDE);

        // acc1
        assert.equal(await sht.totalBalanceOf.call(acc1), 0);
        assert.equal(await sht.balanceOf.call(acc1), 0);
        assert.equal(await sht.lockedBalanceOf.call(acc1), 0);
        var res = await sht.accounts.call(acc1);
        assert.equal(res[0], 0);
        assert.equal(res[1], 0);
        assert.equal(res[2], 0);
    })

    it("transfer from by date with date earlier than now should same tranfer", async() => {
        // approve
        await sht.approve(spender, 100 * MAGNITUDE, {from: owner});
        assert.equal(await sht.allowance.call(owner, spender), 100 * MAGNITUDE);

        await sht.transferFromByDate(owner, acc1, [100 * MAGNITUDE], [time - DAY], {from: spender});

        // spender
        assert.equal(await sht.allowance.call(owner, spender), 0 * MAGNITUDE);

        // acc1
        assert.equal(await sht.totalBalanceOf.call(acc1), 100 * MAGNITUDE);
        assert.equal(await sht.balanceOf.call(acc1), 100 * MAGNITUDE);
        assert.equal(await sht.lockedBalanceOf.call(acc1), 0 * MAGNITUDE);
        var res = await sht.accounts.call(acc1);
        assert.equal(res[0], 0);
        assert.equal(res[1], 0);
        assert.equal(res[2], 0);
    })

    it("transfer from by date with date is the first should be successful", async() => {
        // approve
        await sht.approve(spender, 100 * MAGNITUDE, {from: owner});
        assert.equal(await sht.allowance.call(owner, spender), 100 * MAGNITUDE);

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
    })

    it("transfer from by date with date with same old should be successful", async() => {
        // approve
        await sht.approve(spender, 200 * MAGNITUDE, {from: owner});
        assert.equal(await sht.allowance.call(owner, spender), 200 * MAGNITUDE);

        await sht.transferFromByDate(owner, acc1, [100 * MAGNITUDE], [time + DAY], {from: spender});

        // spender
        assert.equal(await sht.allowance.call(owner, spender), 100 * MAGNITUDE);

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

        // transfer by date again
        await sht.transferFromByDate(owner, acc1, [100 * MAGNITUDE], [time + DAY], {from: spender});

        // spender
        assert.equal(await sht.allowance.call(owner, spender), 0 * MAGNITUDE);

        // acc1
        assert.equal(await sht.totalBalanceOf.call(acc1), 200 * MAGNITUDE);
        assert.equal(await sht.balanceOf.call(acc1), 0 * MAGNITUDE);
        assert.equal(await sht.lockedBalanceOf.call(acc1), 200 * MAGNITUDE);
        var res = await sht.accounts.call(acc1);
        assert.equal(res[0], 200 * MAGNITUDE);
        assert.equal(res[1], time + DAY);
        assert.equal(res[2], time + DAY);
        var res2 = await sht.lockedBalanceOfByDate(acc1, res[1]);
        assert.equal(res2[0], 200 * MAGNITUDE);
        assert.equal(res2[1], 0);
    })

    it("transfer from by date with date earlier than frist should be successful", async() => {
        // approve
        await sht.approve(spender, 200 * MAGNITUDE, {from: owner});
        assert.equal(await sht.allowance.call(owner, spender), 200 * MAGNITUDE);

        // transfer now + 2day
        await sht.transferFromByDate(owner, acc1, [100 * MAGNITUDE], [time + 2*DAY], {from: spender});

        // spender
        assert.equal(await sht.allowance.call(owner, spender), 100 * MAGNITUDE);

        assert.equal(await sht.totalBalanceOf.call(acc1), 100 * MAGNITUDE);
        assert.equal(await sht.balanceOf.call(acc1), 0 * MAGNITUDE);
        assert.equal(await sht.lockedBalanceOf.call(acc1), 100 * MAGNITUDE);
        var res = await sht.accounts.call(acc1);
        assert.equal(res[0], 100 * MAGNITUDE);
        assert.equal(res[1], time + 2*DAY);
        assert.equal(res[2], time + 2*DAY);
        var res2 = await sht.lockedBalanceOfByDate(acc1, res[1]);
        assert.equal(res2[0], 100 * MAGNITUDE);
        assert.equal(res2[1], 0);

        // tranfer now + day
        await sht.transferFromByDate(owner, acc1, [100 * MAGNITUDE], [time + DAY], {from: spender});

        // spender
        assert.equal(await sht.allowance.call(owner, spender), 0 * MAGNITUDE);

        // acc1
        assert.equal(await sht.totalBalanceOf.call(acc1), 200 * MAGNITUDE);
        assert.equal(await sht.balanceOf.call(acc1), 0 * MAGNITUDE);
        assert.equal(await sht.lockedBalanceOf.call(acc1), 200 * MAGNITUDE);
        var res = await sht.accounts.call(acc1);
        assert.equal(res[0], 200 * MAGNITUDE);
        assert.equal(res[1], time + DAY);
        assert.equal(res[2], time + 2*DAY);
        var res2 = await sht.lockedBalanceOfByDate(acc1, res[1]);
        assert.equal(res2[0], 100 * MAGNITUDE);
        assert.equal(res2[1], time + 2*DAY);
        res2 = await sht.lockedBalanceOfByDate(acc1, res2[1]);
        assert.equal(res2[0], 100 * MAGNITUDE);
        assert.equal(res2[1], 0);
    })

    it("transfer from by date with date later than last should be successful", async() => {
        // approve
        await sht.approve(spender, 200 * MAGNITUDE, {from: owner});
        assert.equal(await sht.allowance.call(owner, spender), 200 * MAGNITUDE);

        // transfer now + day
        await sht.transferFromByDate(owner, acc1, [100 * MAGNITUDE], [time + DAY], {from: spender});

        // spender
        assert.equal(await sht.allowance.call(owner, spender), 100 * MAGNITUDE);

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

        // transfer now + 2*day
        await sht.transferFromByDate(owner, acc1, [100 * MAGNITUDE], [time + 2*DAY], {from: spender});

        // spender
        assert.equal(await sht.allowance.call(owner, spender), 0 * MAGNITUDE);

        // acc1
        assert.equal(await sht.totalBalanceOf.call(acc1), 200 * MAGNITUDE);
        assert.equal(await sht.balanceOf.call(acc1), 0 * MAGNITUDE);
        assert.equal(await sht.lockedBalanceOf.call(acc1), 200 * MAGNITUDE);
        res = await sht.accounts.call(acc1);
        assert.equal(res[0], 200 * MAGNITUDE);
        assert.equal(res[1], time + DAY);
        assert.equal(res[2], time + 2*DAY);
        res2 = await sht.lockedBalanceOfByDate(acc1, res[1]);
        assert.equal(res2[0], 100 * MAGNITUDE);
        assert.equal(res2[1], time + 2*DAY);
        res2 = await sht.lockedBalanceOfByDate(acc1, res2[1]);
        assert.equal(res2[0], 100 * MAGNITUDE);
        assert.equal(res2[1], 0);
    })

    it("transfer from by date with date between frist and last should be successful", async() => {
        // approve
        await sht.approve(spender, 300 * MAGNITUDE, {from: owner});
        assert.equal(await sht.allowance.call(owner, spender), 300 * MAGNITUDE);

        // transfer now + day
        await sht.transferFromByDate(owner, acc1, [100 * MAGNITUDE], [time + DAY], {from: spender});

        // spender
        assert.equal(await sht.allowance.call(owner, spender), 200 * MAGNITUDE);

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

        // transfer now + 3*day
        await sht.transferFromByDate(owner, acc1, [100 * MAGNITUDE], [time + 3*DAY], {from: spender});

        // spender
        assert.equal(await sht.allowance.call(owner, spender), 100 * MAGNITUDE);

        // acc1
        assert.equal(await sht.totalBalanceOf.call(acc1), 200 * MAGNITUDE);
        assert.equal(await sht.balanceOf.call(acc1), 0 * MAGNITUDE);
        assert.equal(await sht.lockedBalanceOf.call(acc1), 200 * MAGNITUDE);
        var res = await sht.accounts.call(acc1);
        assert.equal(res[0], 200 * MAGNITUDE);
        assert.equal(res[1], time + DAY);
        assert.equal(res[2], time + 3*DAY);
        var res2 = await sht.lockedBalanceOfByDate(acc1, res[1]);
        assert.equal(res2[0], 100 * MAGNITUDE);
        assert.equal(res2[1], time + 3*DAY);
        res2 = await sht.lockedBalanceOfByDate(acc1, res2[1]);
        assert.equal(res2[0], 100 * MAGNITUDE);
        assert.equal(res2[1], 0);

        // transfer now + 2*day
        await sht.transferFromByDate(owner, acc1, [100 * MAGNITUDE], [time + 2*DAY], {from: spender});

        // spender
        assert.equal(await sht.allowance.call(owner, spender), 0 * MAGNITUDE);

        // acc1
        assert.equal(await sht.totalBalanceOf.call(acc1), 300 * MAGNITUDE);
        assert.equal(await sht.balanceOf.call(acc1), 0 * MAGNITUDE);
        assert.equal(await sht.lockedBalanceOf.call(acc1), 300 * MAGNITUDE);
        var res = await sht.accounts.call(acc1);
        assert.equal(res[0], 300 * MAGNITUDE);
        assert.equal(res[1], time + DAY);
        assert.equal(res[2], time + 3*DAY);
        var res2 = await sht.lockedBalanceOfByDate(acc1, res[1]);
        assert.equal(res2[0], 100 * MAGNITUDE);
        assert.equal(res2[1], time + 2*DAY);
        res2 = await sht.lockedBalanceOfByDate(acc1, res2[1]);
        assert.equal(res2[0], 100 * MAGNITUDE);
        assert.equal(res2[1], time + 3*DAY);
        res2 = await sht.lockedBalanceOfByDate(acc1, res2[1]);
        assert.equal(res2[0], 100 * MAGNITUDE);
        assert.equal(res2[1], 0);
    })

    it("transfer from by date exceeds avaliables without expired locked tokens should be failed", async() => {
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

        // tranfer bydate to acc2
        try {
            await sht.transferFromByDate(acc1, acc2, [100 * MAGNITUDE], [time + DAY], {from: spender});
            assert.fail();
        } catch (err){
            assert.ok(/revert/.test(err.message));
        }
    })

    it("transfer from by date exceeds avaliables without enough expired locked tokens should be failed", async() => {
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

        // transfer 200 tokens
        try {
            await sht.transferFromByDate(acc1, acc2, [200 * MAGNITUDE], [time + DAY], {from: spender});
            assert.fail();
        } catch (err){
            assert.ok(/revert/.test(err.message));
        }
    })

    it("transfer from by date exceeds avaliables with enough expired locked tokens should be successful", async() => {
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

        // transfer now + day
        await sht.transferFromByDate(acc1, acc2, [100 * MAGNITUDE], [time + DAY], {from: spender});

        // acc1
        assert.equal(await sht.totalBalanceOf.call(acc1), 0 * MAGNITUDE);
        assert.equal(await sht.balanceOf.call(acc1), 0 * MAGNITUDE);
        assert.equal(await sht.lockedBalanceOf.call(acc1), 0 * MAGNITUDE);
        var res = await sht.accounts.call(acc1);
        assert.equal(res[0], 0 * MAGNITUDE);
        assert.equal(res[1], 0);
        assert.equal(res[2], 0);

        // acc2
        assert.equal(await sht.totalBalanceOf.call(acc2), 100 * MAGNITUDE);
        assert.equal(await sht.balanceOf.call(acc2), 0 * MAGNITUDE);
        assert.equal(await sht.lockedBalanceOf.call(acc2), 100 * MAGNITUDE);
        res = await sht.accounts.call(acc2);
        assert.equal(res[0], 100 * MAGNITUDE);
        assert.equal(res[1], time + DAY);
        assert.equal(res[2], time + DAY);
        res2 = await sht.lockedBalanceOfByDate(acc2, res[1]);
        assert.equal(res2[0], 100 * MAGNITUDE);
        assert.equal(res2[1], 0);

    })

    // same to above
    it("available balance of should be right", async() => {
        // approve
        await sht.approve(spender, 200 * MAGNITUDE, {from: owner});
        assert.equal(await sht.allowance.call(owner, spender), 200 * MAGNITUDE);

        // transfer now + day
        await sht.transferFromByDate(owner, acc1, [100 * MAGNITUDE, 100 * MAGNITUDE], [time - DAY, time + DAY], {from: spender});

        // spender
        assert.equal(await sht.allowance.call(owner, spender), 0 * MAGNITUDE);

        // acc1
        assert.equal(await sht.totalBalanceOf.call(acc1), 200 * MAGNITUDE);
        assert.equal(await sht.balanceOf.call(acc1), 100 * MAGNITUDE);
        assert.equal(await sht.lockedBalanceOf.call(acc1), 100 * MAGNITUDE);
        var res = await sht.accounts.call(acc1);
        assert.equal(res[0], 100 * MAGNITUDE);
        assert.equal(res[1], time + DAY);
        assert.equal(res[2], time + DAY);
        var res2 = await sht.lockedBalanceOfByDate(acc1, res[1]);
        assert.equal(res2[0], 100 * MAGNITUDE);
        assert.equal(res2[1], 0);
    })

    // same to above
    it("locked balance of should be right", async() => {
        // approve
        await sht.approve(spender, 200 * MAGNITUDE, {from: owner});
        assert.equal(await sht.allowance.call(owner, spender), 200 * MAGNITUDE);

        // transfer now + day
        await sht.transferFromByDate(owner, acc1, [100 * MAGNITUDE, 100 * MAGNITUDE], [time - DAY, time + DAY], {from: spender});

        // spender
        assert.equal(await sht.allowance.call(owner, spender), 0 * MAGNITUDE);

        // acc1
        assert.equal(await sht.totalBalanceOf.call(acc1), 200 * MAGNITUDE);
        assert.equal(await sht.balanceOf.call(acc1), 100 * MAGNITUDE);
        assert.equal(await sht.lockedBalanceOf.call(acc1), 100 * MAGNITUDE);
        var res = await sht.accounts.call(acc1);
        assert.equal(res[0], 100 * MAGNITUDE);
        assert.equal(res[1], time + DAY);
        assert.equal(res[2], time + DAY);
        var res2 = await sht.lockedBalanceOfByDate(acc1, res[1]);
        assert.equal(res2[0], 100 * MAGNITUDE);
        assert.equal(res2[1], 0);
    })

    // same to above
    it("locked balance of by date should be right", async() => {
        // approve
        await sht.approve(spender, 200 * MAGNITUDE, {from: owner});
        assert.equal(await sht.allowance.call(owner, spender), 200 * MAGNITUDE);

        // transfer now + day
        await sht.transferFromByDate(owner, acc1, [100 * MAGNITUDE, 100 * MAGNITUDE], [time - DAY, time + DAY], {from: spender});

        // spender
        assert.equal(await sht.allowance.call(owner, spender), 0 * MAGNITUDE);

        // acc1
        assert.equal(await sht.totalBalanceOf.call(acc1), 200 * MAGNITUDE);
        assert.equal(await sht.balanceOf.call(acc1), 100 * MAGNITUDE);
        assert.equal(await sht.lockedBalanceOf.call(acc1), 100 * MAGNITUDE);
        var res = await sht.accounts.call(acc1);
        assert.equal(res[0], 100 * MAGNITUDE);
        assert.equal(res[1], time + DAY);
        assert.equal(res[2], time + DAY);
        var res2 = await sht.lockedBalanceOfByDate(acc1, res[1]);
        assert.equal(res2[0], 100 * MAGNITUDE);
        assert.equal(res2[1], 0);
    })
})
