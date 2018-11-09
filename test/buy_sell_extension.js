
var SibbayHealthToken = artifacts.require("./SibbayHealthToken.sol");

contract("SibbayHealthToken-buy-sell-extension", accounts => {

    const [sender, owner, fundAccount, acc1, acc2, acc3] = accounts;
    const MAGNITUDE = 10 ** 18;
    // sell price 0.001 ether
    let sellPrice = 10 ** 15;
    // buy price 0.1 ether
    let buyPrice = 10 ** 17;
    let sht;

    beforeEach(async() => {
        sht = await SibbayHealthToken.new(owner, fundAccount);
    });

    it("set sell price should be successful", async() => {
        await sht.setSellPrice(sellPrice, {from: owner});
        assert.equal(await sht.sellPrice.call(), sellPrice);
    })

    it("set buy price should be successful", async() => {
        await sht.setBuyPrice(buyPrice, {from: owner});
        assert.equal(await sht.buyPrice.call(), buyPrice);
    })

    it("open buy/sell falg should be successful", async() => {
        await sht.setSellPrice(sellPrice, {from: owner});
        await sht.setBuyPrice(buyPrice, {from: owner});

        // buy flag
        await sht.openBuy({from: owner});
        assert.equal(await sht.buyFlag.call(), true);

        // sell flag
        await sht.openSell({from: owner});
        assert.equal(await sht.sellFlag.call(), true);
    })

    it("close buy/sell falg should be successful", async() => {
        await sht.setSellPrice(sellPrice, {from: owner});
        await sht.setBuyPrice(buyPrice, {from: owner});
        
        // buy flag
        await sht.openBuy({from: owner});
        assert.equal(await sht.buyFlag.call(), true);
        await sht.closeBuy({from: owner});
        assert.equal(await sht.buyFlag.call(), false);
        
        // sell flag
        await sht.openSell({from: owner});
        assert.equal(await sht.sellFlag.call(), true);
        await sht.closeSell({from: owner});
        assert.equal(await sht.sellFlag.call(), false);
    })

    it("buy tokens should be successful", async() => {
        await sht.setSellPrice(sellPrice, {from: owner});
        await sht.setBuyPrice(buyPrice, {from: owner});
        await sht.addTokenToFund(owner, 100*MAGNITUDE, {from: owner});
        assert.equal(await sht.balanceOf.call(fundAccount), 100 * MAGNITUDE);
        assert.equal(await sht.availableBalanceOf.call(fundAccount), 100 * MAGNITUDE);
        await sht.openBuy({from: owner});
        assert.equal(await sht.buyFlag.call(), true);

        await sht.buy({from: acc1, value: 10 * MAGNITUDE});
        assert.equal(await sht.balanceOf.call(acc1), 100 * MAGNITUDE);
        assert.equal(await sht.availableBalanceOf.call(acc1), 100 * MAGNITUDE);
        assert.equal(await sht.balanceOf.call(fundAccount), 0 * MAGNITUDE);
        assert.equal(await sht.availableBalanceOf.call(fundAccount), 0 * MAGNITUDE);
    })

    it("buy tokens should be successful-2", async() => {
        await sht.setBuyPrice(buyPrice, {from: owner});
        await sht.addTokenToFund(owner, 100*MAGNITUDE, {from: owner});
        assert.equal(await sht.balanceOf.call(fundAccount), 100 * MAGNITUDE);
        assert.equal(await sht.availableBalanceOf.call(fundAccount), 100 * MAGNITUDE);
        await sht.openBuy({from: owner});
        assert.equal(await sht.buyFlag.call(), true);

        await sht.buy({from: acc1, value: 10 * MAGNITUDE});
        assert.equal(await sht.balanceOf.call(acc1), 100 * MAGNITUDE);
        assert.equal(await sht.availableBalanceOf.call(acc1), 100 * MAGNITUDE);
        assert.equal(await sht.balanceOf.call(fundAccount), 0 * MAGNITUDE);
        assert.equal(await sht.availableBalanceOf.call(fundAccount), 0 * MAGNITUDE);
    })

    it("buy tokens without value should be failed", async() => {
        await sht.setSellPrice(sellPrice, {from: owner});
        await sht.setBuyPrice(buyPrice, {from: owner});
        await sht.addTokenToFund(owner, 100*MAGNITUDE, {from: owner});
        assert.equal(await sht.balanceOf.call(fundAccount), 100 * MAGNITUDE);
        assert.equal(await sht.availableBalanceOf.call(fundAccount), 100 * MAGNITUDE);
        await sht.openBuy({from: owner});
        assert.equal(await sht.buyFlag.call(), true);

        try {
            await sht.buy({from: acc1});
            assert.fail();
        } catch (err){
            assert.ok(/revert/.test(err.message));
        }
        assert.equal(await sht.balanceOf.call(fundAccount), 100 * MAGNITUDE);
        assert.equal(await sht.availableBalanceOf.call(fundAccount), 100 * MAGNITUDE);
    })

    it("sell tokens should be successful", async() => {
        await sht.setSellPrice(sellPrice, {from: owner});
        await sht.setBuyPrice(buyPrice, {from: owner});
        await sht.addTokenToFund(owner, 100*MAGNITUDE, {from: owner});
        assert.equal(await sht.balanceOf.call(fundAccount), 100 * MAGNITUDE);
        assert.equal(await sht.availableBalanceOf.call(fundAccount), 100 * MAGNITUDE);
        await sht.openBuy({from: owner});
        assert.equal(await sht.buyFlag.call(), true);
        await sht.openSell({from: owner});
        assert.equal(await sht.sellFlag.call(), true);

        await sht.buy({from: acc1, value: 10 * MAGNITUDE});
        assert.equal(await sht.balanceOf.call(acc1), 100 * MAGNITUDE);
        assert.equal(await sht.availableBalanceOf.call(acc1), 100 * MAGNITUDE);

        await sht.sendTransaction({from: owner, value: 1 * MAGNITUDE});

        await sht.sell(100 * MAGNITUDE, {from: acc1});
        assert.equal(await sht.balanceOf.call(acc1), 0 * MAGNITUDE);
        assert.equal(await sht.availableBalanceOf.call(acc1), 0 * MAGNITUDE);
    })

    it("sell tokens should be successful-2", async() => {
        await sht.setSellPrice(sellPrice, {from: owner});
        await sht.openSell({from: owner});
        assert.equal(await sht.sellFlag.call(), true);

        await sht.transfer(acc1, 100 * MAGNITUDE, {from: owner});
        assert.equal(await sht.balanceOf.call(acc1), 100 * MAGNITUDE);
        assert.equal(await sht.availableBalanceOf.call(acc1), 100 * MAGNITUDE);

        await sht.sendTransaction({from: owner, value: 1 * MAGNITUDE});

        await sht.sell(100 * MAGNITUDE, {from: acc1});
        assert.equal(await sht.balanceOf.call(acc1), 0 * MAGNITUDE);
        assert.equal(await sht.availableBalanceOf.call(acc1), 0 * MAGNITUDE);
    })
})
