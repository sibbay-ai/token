
var SibbayHealthToken = artifacts.require("./SibbayHealthToken.sol");

contract("SibbayHealthToken-sell-extension", accounts => {

    const [sender, owner, fundAccount, acc1, acc2, acc3] = accounts;
    const MAGNITUDE = 10 ** 18;
    // sell price 0.001 ether
    let sellPrice = 10 ** 15;
    let sht;

    beforeEach(async() => {
        sht = await SibbayHealthToken.new(owner, fundAccount);
    });

    it("set sell price should be successful", async() => {
        await sht.setSellPrice(sellPrice, {from: owner});
        assert.equal(await sht.sellPrice.call(), sellPrice);
    })

    it("close sell falg should be successful", async() => {
        await sht.setSellPrice(sellPrice, {from: owner});
        
        // sell flag
        await sht.closeSell({from: owner});
        assert.equal(await sht.sellFlag.call(), false);
    })

    it("sell tokens should be successful", async() => {
        await sht.setSellPrice(sellPrice, {from: owner});
        await sht.addTokenToFund(owner, 100*MAGNITUDE, {from: owner});
        assert.equal(await sht.balanceOf.call(fundAccount), 100 * MAGNITUDE);
        assert.equal(await sht.availableBalanceOf.call(fundAccount), 100 * MAGNITUDE);
        assert.equal(await sht.sellFlag.call(), true);

        await sht.transfer(acc1, 100 * MAGNITUDE, {from: owner});
        assert.equal(await sht.balanceOf.call(acc1), 100 * MAGNITUDE);
        assert.equal(await sht.availableBalanceOf.call(acc1), 100 * MAGNITUDE);

        await sht.sendTransaction({from: owner, value: 1 * MAGNITUDE});

        await sht.sell(100 * MAGNITUDE, {from: acc1});
        assert.equal(await sht.balanceOf.call(acc1), 0 * MAGNITUDE);
        assert.equal(await sht.availableBalanceOf.call(acc1), 0 * MAGNITUDE);
    })

    it("sell tokens should be successful-2", async() => {
        await sht.setSellPrice(sellPrice, {from: owner});

        await sht.transfer(acc1, 100 * MAGNITUDE, {from: owner});
        assert.equal(await sht.balanceOf.call(acc1), 100 * MAGNITUDE);
        assert.equal(await sht.availableBalanceOf.call(acc1), 100 * MAGNITUDE);

        await sht.sendTransaction({from: owner, value: 1 * MAGNITUDE});

        await sht.sell(100 * MAGNITUDE, {from: acc1});
        assert.equal(await sht.balanceOf.call(acc1), 0 * MAGNITUDE);
        assert.equal(await sht.availableBalanceOf.call(acc1), 0 * MAGNITUDE);
    })

    it("sell tokens should be failed when close sell", async() => {
        // set sell price
        await sht.setSellPrice(sellPrice, {from: owner});
        await sht.transfer(acc1, 100 * MAGNITUDE, {from: owner});
        assert.equal(await sht.balanceOf.call(acc1), 100 * MAGNITUDE);
        assert.equal(await sht.availableBalanceOf.call(acc1), 100 * MAGNITUDE);

        await sht.sendTransaction({from: owner, value: 1 * MAGNITUDE});

        // close sell
        await sht.closeSell({from: owner});
        assert.equal(await sht.sellFlag.call(), false);

        try{
            await sht.sell(100 * MAGNITUDE, {from: acc1});
            assert.fail();
        } catch (err) {
            assert.ok(/revert/.test(err.message));
        }

        assert.equal(await sht.balanceOf.call(acc1), 100 * MAGNITUDE);
        assert.equal(await sht.availableBalanceOf.call(acc1), 100 * MAGNITUDE);

        try{
            await sht.transfer(fundAccount, 100 * MAGNITUDE, {from: acc1});
            assert.fail();
        } catch (err) {
            assert.ok(/revert/.test(err.message));
        }

        assert.equal(await sht.balanceOf.call(acc1), 100 * MAGNITUDE);
        assert.equal(await sht.availableBalanceOf.call(acc1), 100 * MAGNITUDE);
    })
})
