
var SibbayHealthToken = artifacts.require("./SibbayHealthToken.sol");
const { increaseTime } = require("./utils/increaseTime.js");
const { latestTime } = require("./utils/latestTime.js");

contract("SibbayHealthToken-batch-transfer-from-extension", accounts => {
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

    it("batch transfer from should be successful", async() => {
        // approve
        await sht.approve(spender, 300 * MAGNITUDE, {from: owner});
        assert.equal(await sht.allowance.call(owner, spender), 300 * MAGNITUDE);

        // batch transfer
        await sht.batchTransferFrom(owner, [acc1, acc2, acc3], [100 * MAGNITUDE, 100 * MAGNITUDE, 100 * MAGNITUDE], {from: spender});

        // spender
        assert.equal(await sht.allowance.call(owner, spender), 0);

        // acc1, acc2, acc3
        assert.equal(await sht.balanceOf.call(acc1), 100 * MAGNITUDE);
        assert.equal(await sht.balanceOf.call(acc2), 100 * MAGNITUDE);
        assert.equal(await sht.balanceOf.call(acc3), 100 * MAGNITUDE);
    })

    it("batch transfer from to fund acount should be failed", async() => {
        // approve
        await sht.approve(spender, 100 * MAGNITUDE, {from: owner});
        assert.equal(await sht.allowance.call(owner, spender), 100 * MAGNITUDE);

        // set fund and open buy/sell flag
        await sht.setSellPrice(sellPrice, {from: owner});
        await sht.setBuyPrice(buyPrice, {from: owner});
        await sht.addTokenToFund(owner, 100*MAGNITUDE, {from: owner});
        await sht.sendTransaction({from: owner, value: 1 * MAGNITUDE});
        await sht.openBuy({from: owner});
        assert.equal(await sht.buyFlag.call(), true);
        await sht.openSell({from: owner});
        assert.equal(await sht.sellFlag.call(), true);

        try {
            await sht.batchTransferFrom(owner, [fundAccount], [100 * MAGNITUDE], {from: spender});
            assert.fail();
        } catch (err){
            assert.ok(/revert/.test(err.message));
        }
    })

    it("batch transfer from to 0 acount should be failed", async() => {
        // approve
        await sht.approve(spender, 100 * MAGNITUDE, {from: owner});
        assert.equal(await sht.allowance.call(owner, spender), 100 * MAGNITUDE);

        try {
            await sht.batchTransferFrom(owner, [0x0], [100 * MAGNITUDE], {from: spender});
            assert.fail();
        } catch (err){
            assert.ok(/revert/.test(err.message));
        }
    })

    it("batch transfer from without enough approval should be failed", async() => {
        // approve
        await sht.approve(spender, 100 * MAGNITUDE, {from: owner});
        assert.equal(await sht.allowance.call(owner, spender), 100 * MAGNITUDE);

        try {
            await sht.batchTransferFrom(owner, [acc1, acc2], [100 * MAGNITUDE, 100 * MAGNITUDE], {from: spender});
            assert.fail();
        } catch (err){
            assert.ok(/revert/.test(err.message));
        }
    })

    it("batch transfer from exceeds avaliables without expired locked tokens should be failed", async() => {
        // approve
        await sht.approve(spender, 100 * MAGNITUDE, {from: owner});
        assert.equal(await sht.allowance.call(owner, spender), 100 * MAGNITUDE);

        // transfer now + day
        await sht.transferFromByDate(owner, acc1, [100 * MAGNITUDE], [time + DAY], {from: spender});

        // spender
        assert.equal(await sht.allowance.call(owner, spender), 0 * MAGNITUDE);

        // acc1
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

        // approve
        await sht.approve(spender, 100 * MAGNITUDE, {from: acc1});
        assert.equal(await sht.allowance.call(acc1, spender), 100 * MAGNITUDE);

        // tranfer
        try {
            await sht.batchTransferFrom(acc1, [acc2], [100 * MAGNITUDE], {from: spender});
            assert.fail();
        } catch (err){
            assert.ok(/revert/.test(err.message));
        }
    })

    it("batch transfer from exceeds avaliables without enough expired locked tokens should be failed", async() => {
        // approve
        await sht.approve(spender, 100 * MAGNITUDE, {from: owner});
        assert.equal(await sht.allowance.call(owner, spender), 100 * MAGNITUDE);

        // transfer now + day
        await sht.transferFromByDate(owner, acc1, [100 * MAGNITUDE], [time + DAY], {from: spender});

        // spender
        assert.equal(await sht.allowance.call(owner, spender), 0 * MAGNITUDE);

        // acc1
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

        // approve
        await sht.approve(spender, 100 * MAGNITUDE, {from: acc1});
        assert.equal(await sht.allowance.call(acc1, spender), 100 * MAGNITUDE);

        // tranfer
        try {
            await sht.batchTransferFrom(acc1, [acc2, acc3], [100 * MAGNITUDE, 100 * MAGNITUDE], {from: spender});
            assert.fail();
        } catch (err){
            assert.ok(/revert/.test(err.message));
        }
    })

    it("batch transfer from exceeds avaliables with enough expired locked tokens should be successful", async() => {
        // approve
        await sht.approve(spender, 100 * MAGNITUDE, {from: owner});
        assert.equal(await sht.allowance.call(owner, spender), 100 * MAGNITUDE);

        // transfer now + day
        await sht.transferFromByDate(owner, acc1, [100 * MAGNITUDE], [time + DAY], {from: spender});

        // spender
        assert.equal(await sht.allowance.call(owner, spender), 0 * MAGNITUDE);

        // acc1
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

        // approve
        await sht.approve(spender, 100 * MAGNITUDE, {from: acc1});
        assert.equal(await sht.allowance.call(acc1, spender), 100 * MAGNITUDE);

        // tranfer
        await sht.batchTransferFrom(acc1, [acc2], [100 * MAGNITUDE], {from: spender});

        assert.equal(await sht.balanceOf.call(acc1), 0 * MAGNITUDE);
        assert.equal(await sht.balanceOf.call(acc2), 100 * MAGNITUDE);
    })
})
