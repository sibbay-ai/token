
var SibbayHealthToken = artifacts.require("./SibbayHealthToken.sol");
const { increaseTime } = require("./utils/increaseTime.js");
const { latestTime } = require("./utils/latestTime.js");
var log4js = require('log4js');

contract("SibbayHealthToken-vault-of-owner", accounts => {

    const [owner, fundAccount, spender, acc1, acc2, acc3] = accounts;
    const MAGNITUDE = 10 ** 18;
    const DAY = 3600 * 24;
    const YEAR = 3600 * 24 * 365;
    // sell price 0.001 ether
    let sellPrice = 10 ** 15;
    // buy price 0.1 ether
    let buyPrice = 10 ** 17;
    let sht;
    let time;

    /*
     * logger 实例，实现js的简单日志输出
     */
    var logger = log4js.getLogger();
    logger.level = 'info';

    beforeEach(async() => {
        sht = await SibbayHealthToken.new();
        time = await latestTime();
    });

    it("transfer less/equal than 10% of owner's balance should be success", async() => {

        // get 6% of owner's balance
        let balance = await sht.balanceOf.call(owner);
        let value = balance * 0.06;

        // transfer 6% should be success
        await sht.transfer(acc1, value, {from: owner});
        assert.equal(await sht.balanceOf.call(acc1), value);
        assert.equal(await sht.balanceOf.call(owner), balance - value);

        // transfer +4% should be success
        let value_2 = balance * 0.04;
        await sht.transfer(acc1, value_2, {from: owner});
        assert.equal(await sht.balanceOf.call(acc1), value + value_2);
        assert.equal(await sht.balanceOf.call(owner), balance - value - value_2);
    })

    it("transfer more than 10% of owner's balance should be failed", async() => {

        // get 10% + 1 of owner's balance
        let balance = await sht.balanceOf.call(owner);
        let value = balance * 0.1 + 1e10;

        try{
            // transfer should be failed
            await sht.transfer(acc1, value, {from: owner});
            assert.fail();
        } catch (err) {
            assert.ok(/revert/.test(err.message));
        }
    })

    it("vault should be right", async() => {
        // get vault
        let vault = await sht.vault.call();
        assert.equal(vault, 1e26);

        // get balance of owner
        let balance = await sht.balanceOf.call(owner);

        // increase time
        await increaseTime(YEAR);
        time = time + YEAR;

        // get vault
        vault = await sht.vault.call();
        assert.equal(vault, balance * 0.1);

        // transfer 10% should be success
        await sht.transfer(acc1, vault, {from: owner});
        assert.equal(await sht.balanceOf.call(acc1), balance * 0.1);
        //assert.equal(await sht.balanceOf.call(acc1), vault);
        assert.equal(await sht.balanceOf.call(owner), balance - vault);
        assert.equal(await sht.vault.call(), 0);

        // update var
        balance = balance - vault;
        vault = balance * 0.1;

        // increase time
        await increaseTime(YEAR);
        time = time + YEAR;

        // transfer 10% should be success
        await sht.transfer(acc2, vault, {from: owner});
        assert.equal(await sht.balanceOf.call(acc2), vault);
        assert.equal(await sht.balanceOf.call(owner), balance - vault);
        assert.equal(await sht.vault.call(), 0);

    })

    it("transfer from less/equal than 10% of owner's balance should be success", async() => {

        // get balance of owner
        let balance = await sht.balanceOf.call(owner);

        // get vault
        let vault = await sht.vault.call();
        assert.equal(vault, balance * 0.1);

        // approve
        await sht.approve(spender, vault * 2, {from: owner});
        assert.equal(await sht.allowance.call(owner, spender), vault * 2);

        // transfer 6% should be success
        let value = balance * 0.06;
        await sht.transferFrom(owner, acc1, value, {from: spender});
        assert.equal(await sht.balanceOf.call(acc1), value);
        assert.equal(await sht.balanceOf.call(owner), balance - value);

        // transfer +4% should be success
        let value_2 = balance * 0.04;
        await sht.transferFrom(owner, acc1, value_2, {from: spender});
        assert.equal(await sht.balanceOf.call(acc1), value + value_2);
        assert.equal(await sht.balanceOf.call(owner), balance - value - value_2);
    })

    it("transfer from more than 10% of owner's balance should be failed", async() => {

        // get balance of owner
        let balance = await sht.balanceOf.call(owner);

        // get vault
        let vault = await sht.vault.call();
        assert.equal(vault, balance * 0.1);

        // approve
        await sht.approve(spender, vault * 2, {from: owner});
        assert.equal(await sht.allowance.call(owner, spender), vault * 2);

        let value = balance * 0.1 + 1e10;

        try{
            // transfer should be failed
            await sht.transferFrom(owner, acc1, value, {from: spender});
            assert.fail();
        } catch (err) {
            assert.ok(/revert/.test(err.message));
        }
    })

    it("batch transfer less/equal than 10% of owner's balance should be success", async() => {

        // get 6% of owner's balance
        let balance = await sht.balanceOf.call(owner);
        let value = balance * 0.06;

        // transfer 6% should be success
        await sht.batchTransfer([acc1], [value], {from: owner});
        assert.equal(await sht.balanceOf.call(acc1), value);
        assert.equal(await sht.balanceOf.call(owner), balance - value);

        // transfer +4% should be success
        let value_2 = balance * 0.04;
        await sht.batchTransfer([acc1], [value_2], {from: owner});
        assert.equal(await sht.balanceOf.call(acc1), value + value_2);
        assert.equal(await sht.balanceOf.call(owner), balance - value - value_2);
    })

    it("batch transfer more than 10% of owner's balance should be failed", async() => {

        // get 10% + 1 of owner's balance
        let balance = await sht.balanceOf.call(owner);
        let value = balance * 0.1 + 1e10;

        try{
            // transfer should be failed
            await sht.batchTransfer([acc1], [value], {from: owner});
            assert.fail();
        } catch (err) {
            assert.ok(/revert/.test(err.message));
        }
    })

    it("batch transfer from less/equal than 10% of owner's balance should be success", async() => {

        // get balance of owner
        let balance = await sht.balanceOf.call(owner);

        // get vault
        let vault = await sht.vault.call();
        assert.equal(vault, balance * 0.1);

        // approve
        await sht.approve(spender, vault * 2, {from: owner});
        assert.equal(await sht.allowance.call(owner, spender), vault * 2);

        // transfer 6% should be success
        let value = balance * 0.06;
        await sht.batchTransferFrom(owner, [acc1], [value], {from: spender});
        assert.equal(await sht.balanceOf.call(acc1), value);
        assert.equal(await sht.balanceOf.call(owner), balance - value);

        // transfer +4% should be success
        let value_2 = balance * 0.04;
        await sht.batchTransferFrom(owner, [acc1], [value_2], {from: spender});
        assert.equal(await sht.balanceOf.call(acc1), value + value_2);
        assert.equal(await sht.balanceOf.call(owner), balance - value - value_2);
    })

    it("batch transfer from more than 10% of owner's balance should be failed", async() => {

        // get balance of owner
        let balance = await sht.balanceOf.call(owner);

        // get vault
        let vault = await sht.vault.call();
        assert.equal(vault, balance * 0.1);

        // approve
        await sht.approve(spender, vault * 2, {from: owner});
        assert.equal(await sht.allowance.call(owner, spender), vault * 2);

        let value = balance * 0.1 + 1e10;

        try{
            // transfer should be failed
            await sht.batchTransferFrom(owner, [acc1], [value], {from: spender});
            assert.fail();
        } catch (err) {
            assert.ok(/revert/.test(err.message));
        }
    })

    it("transfer by date less/equal than 10% of owner's balance should be success", async() => {

        // get 6% of owner's balance
        let balance = await sht.balanceOf.call(owner);
        let value = balance * 0.06;

        // transfer 6% should be success
        await sht.transferByDate(acc1, [value], [time + DAY], {from: owner});
        assert.equal(await sht.balanceOf.call(acc1), value);
        assert.equal(await sht.balanceOf.call(owner), balance - value);

        // transfer +4% should be success
        let value_2 = balance * 0.04;
        await sht.transferByDate(acc1, [value_2], [time + DAY], {from: owner});
        assert.equal(await sht.balanceOf.call(acc1), value + value_2);
        assert.equal(await sht.balanceOf.call(owner), balance - value - value_2);
    })

    it("transfer from by date more than 10% of owner's balance should be failed", async() => {

        // get 10% + 1 of owner's balance
        let balance = await sht.balanceOf.call(owner);
        let value = balance * 0.1 + 1e10;

        try{
            // transfer should be failed
            await sht.transferByDate(acc1, [value], [time + DAY], {from: owner});
            assert.fail();
        } catch (err) {
            assert.ok(/revert/.test(err.message));
        }
    })

    it("transfer from by date less/equal than 10% of owner's balance should be success", async() => {

        // get balance of owner
        let balance = await sht.balanceOf.call(owner);

        // get vault
        let vault = await sht.vault.call();
        assert.equal(vault, balance * 0.1);

        // approve
        await sht.approve(spender, vault * 2, {from: owner});
        assert.equal(await sht.allowance.call(owner, spender), vault * 2);

        // transfer 6% should be success
        let value = balance * 0.06;
        await sht.transferFromByDate(owner, acc1, [value], [time + DAY], {from: spender});
        assert.equal(await sht.balanceOf.call(acc1), value);
        assert.equal(await sht.balanceOf.call(owner), balance - value);

        // transfer +4% should be success
        let value_2 = balance * 0.04;
        await sht.transferFromByDate(owner, acc1, [value_2], [time + 2 * DAY], {from: spender});
        assert.equal(await sht.balanceOf.call(acc1), value + value_2);
        assert.equal(await sht.balanceOf.call(owner), balance - value - value_2);
    })

    it("transfer from by date more than 10% of owner's balance should be failed", async() => {

        // get balance of owner
        let balance = await sht.balanceOf.call(owner);

        // get vault
        let vault = await sht.vault.call();
        assert.equal(vault, balance * 0.1);

        // approve
        await sht.approve(spender, vault * 2, {from: owner});
        assert.equal(await sht.allowance.call(owner, spender), vault * 2);

        let value = balance * 0.1 + 1e10;

        try{
            // transfer should be failed
            await sht.transferFromByDate(owner, acc1, [value], [time + DAY], {from: spender});
            assert.fail();
        } catch (err) {
            assert.ok(/revert/.test(err.message));
        }
    })

})
