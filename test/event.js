
var SibbayHealthToken = artifacts.require("./SibbayHealthToken.sol");
const { latestTime } = require("./utils/latestTime.js");
const { increaseTime } = require("./utils/increaseTime.js");
var log4js = require('log4js');

contract("SibbayHealthToken event test", accounts => {

    const [sender, owner, fundAccount, spender, acc1, acc2, acc3] = accounts;
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
        sht = await SibbayHealthToken.new(owner, fundAccount);
        time = await latestTime();
    });

    it("event Transfer should be triggerred", async() => {
        var { logs }= await sht.transfer(acc1, 100 * MAGNITUDE, {from: owner});
        // assert logs
        assert.equal(logs.length, 1);
        assert.equal(logs[0].event, "Transfer");
        assert.equal(logs[0].args.from, owner);
        assert.equal(logs[0].args.to, acc1);
        assert.equal(logs[0].args.value, 100 * MAGNITUDE);
    });

    it("event Transfer of batchTransfer should be triggerred", async() => {
        var { logs } = await sht.batchTransfer([acc1, acc2, acc3], [100 * MAGNITUDE, 100 * MAGNITUDE, 100 * MAGNITUDE], {from: owner});
        // assert logs
        assert.equal(logs.length, 3);
        assert.equal(logs[0].event, "Transfer");
        assert.equal(logs[0].args.from, owner);
        assert.equal(logs[0].args.to, acc1);
        assert.equal(logs[0].args.value, 100 * MAGNITUDE);
        assert.equal(logs[1].event, "Transfer");
        assert.equal(logs[1].args.from, owner);
        assert.equal(logs[1].args.to, acc2);
        assert.equal(logs[1].args.value, 100 * MAGNITUDE);
        assert.equal(logs[2].event, "Transfer");
        assert.equal(logs[2].args.from, owner);
        assert.equal(logs[2].args.to, acc3);
        assert.equal(logs[2].args.value, 100 * MAGNITUDE);
    });

    it("event Approval should be triggerred", async() => {
        var { logs } = await sht.approve(spender, 100 * MAGNITUDE, {from: owner});
        // assert logs
        assert.equal(logs.length, 1);
        assert.equal(logs[0].event, "Approval");
        assert.equal(logs[0].args.owner, owner);
        assert.equal(logs[0].args.spender, spender);
        assert.equal(logs[0].args.value, 100 * MAGNITUDE);
    });

    it("event Approval of increaseApproval should be triggerred", async() => {
        var { logs } = await sht.increaseApproval(spender, 100 * MAGNITUDE, {from: owner});
        // assert logs
        assert.equal(logs.length, 1);
        assert.equal(logs[0].event, "Approval");
        assert.equal(logs[0].args.owner, owner);
        assert.equal(logs[0].args.spender, spender);
        assert.equal(logs[0].args.value, 100 * MAGNITUDE);
    });

    it("event Approval of decreaseApproval should be triggerred", async() => {
        var { logs } = await sht.decreaseApproval(spender, 100 * MAGNITUDE, {from: owner});
        // assert logs
        assert.equal(logs.length, 1);
        assert.equal(logs[0].event, "Approval");
        assert.equal(logs[0].args.owner, owner);
        assert.equal(logs[0].args.spender, spender);
        assert.equal(logs[0].args.value, 0 * MAGNITUDE);
    });

    it("event TransferFrom should be triggerred", async() => {
        await sht.approve(spender, 100 * MAGNITUDE, {from: owner});
        var { logs } = await sht.transferFrom(owner, acc1, 100*MAGNITUDE, {from: spender});
        // assert logs
        assert.equal(logs.length, 1);
        assert.equal(logs[0].event, "TransferFrom");
        assert.equal(logs[0].args.spender, spender);
        assert.equal(logs[0].args.from, owner);
        assert.equal(logs[0].args.to, acc1);
        assert.equal(logs[0].args.value, 100 * MAGNITUDE);
    });

    it("event TransferFrom of batchTransferFrom should be triggerred", async() => {
        await sht.approve(spender, 300 * MAGNITUDE, {from: owner});
        var { logs } = await sht.batchTransferFrom(owner, [acc1, acc2, acc3], [100 * MAGNITUDE, 100 * MAGNITUDE, 100 * MAGNITUDE], {from: spender});
        // assert logs
        assert.equal(logs.length, 3);
        assert.equal(logs[0].event, "TransferFrom");
        assert.equal(logs[0].args.spender, spender);
        assert.equal(logs[0].args.from, owner);
        assert.equal(logs[0].args.to, acc1);
        assert.equal(logs[0].args.value, 100 * MAGNITUDE);
        assert.equal(logs[1].event, "TransferFrom");
        assert.equal(logs[1].args.spender, spender);
        assert.equal(logs[1].args.from, owner);
        assert.equal(logs[1].args.to, acc2);
        assert.equal(logs[1].args.value, 100 * MAGNITUDE);
        assert.equal(logs[2].event, "TransferFrom");
        assert.equal(logs[2].args.spender, spender);
        assert.equal(logs[2].args.from, owner);
        assert.equal(logs[2].args.to, acc3);
        assert.equal(logs[2].args.value, 100 * MAGNITUDE);
    });

    it("event Pause/Unpause should be triggerred", async() => {
        var { logs } = await sht.pause({from: owner});
        // assert logs
        assert.equal(logs.length, 1);
        assert.equal(logs[0].event, "Pause");

        var { logs } = await sht.unpause({from: owner});
        // assert logs
        assert.equal(logs.length, 1);
        assert.equal(logs[0].event, "Unpause");
    });

    it("event Froze/Unfroze should be triggerred", async() => {
        var { logs } = await sht.froze(acc1, {from: owner});
        // assert logs
        assert.equal(logs.length, 1);
        assert.equal(logs[0].event, "Froze");
        assert.equal(logs[0].args.admin, owner);
        assert.equal(logs[0].args.who, acc1);

        var { logs } = await sht.unfroze(acc1, {from: owner});
        // assert logs
        assert.equal(logs.length, 1);
        assert.equal(logs[0].event, "Unfroze");
        assert.equal(logs[0].args.admin, owner);
        assert.equal(logs[0].args.who, acc1);
    });

    it("event AddAdministrator/DelAdministrator should be triggerred", async() => {
        var { logs } =await sht.addAdministrator(acc1, {from: owner});
        // assert logs
        assert.equal(logs.length, 1);
        assert.equal(logs[0].event, "AddAdministrator");
        assert.equal(logs[0].args.admin, acc1);

        var { logs } =await sht.delAdministrator(acc1, {from: owner});
        // assert logs
        assert.equal(logs.length, 1);
        assert.equal(logs[0].event, "DelAdministrator");
        assert.equal(logs[0].args.admin, acc1);
    });

    it("event SetSellPrice should be triggerred", async() => {
        var { logs } = await sht.setSellPrice(sellPrice, {from: owner});
        // assert logs
        assert.equal(logs.length, 1);
        assert.equal(logs[0].event, "SetSellPrice");
        assert.equal(logs[0].args.admin, owner);
        assert.equal(logs[0].args.price, sellPrice);
    });

    it("event SetBuyPrice should be triggerred", async() => {
        var { logs } = await sht.setBuyPrice(buyPrice, {from: owner});
        // assert logs
        assert.equal(logs.length, 1);
        assert.equal(logs[0].event, "SetBuyPrice");
        assert.equal(logs[0].args.admin, owner);
        assert.equal(logs[0].args.price, buyPrice);
    });

    it("event TransferByDate should be triggerred", async() => {
        var { logs } = await sht.transferByDate(acc1, [100 * MAGNITUDE], [time + DAY], {from: owner});
        // assert logs
        assert.equal(logs.length, 1);
        assert.equal(logs[0].event, "TransferByDate");
        assert.equal(logs[0].args.from, owner);
        assert.equal(logs[0].args.to, acc1);
        assert.equal(logs[0].args.values[0], 100 * MAGNITUDE);
        assert.equal(logs[0].args.dates[0], time + DAY);

        var { logs } = await sht.transferByDate(acc1, [100 * MAGNITUDE, 100 * MAGNITUDE], [time - DAY, time + DAY], {from: owner});
        // assert logs
        assert.equal(logs.length, 2);
        assert.equal(logs[0].event, "Transfer");
        assert.equal(logs[0].args.from, owner);
        assert.equal(logs[0].args.to, acc1);
        assert.equal(logs[0].args.value, 100 * MAGNITUDE);
        assert.equal(logs[1].event, "TransferByDate");
        assert.equal(logs[1].args.from, owner);
        assert.equal(logs[1].args.to, acc1);
        assert.equal(logs[1].args.values[0], 100 * MAGNITUDE);
        assert.equal(logs[1].args.values[1], 100 * MAGNITUDE);
        assert.equal(logs[1].args.dates[0], time - DAY);
        assert.equal(logs[1].args.dates[1], time + DAY);
    });

    it("event TransferFromByDate should be triggerred", async() => {
        // approve and transferFromByDate
        await sht.approve(spender, 100 * MAGNITUDE, {from: owner});
        var { logs } = await sht.transferFromByDate(owner, acc1, [100 * MAGNITUDE], [time + DAY], {from: spender});
        // assert logs
        assert.equal(logs.length, 1);
        assert.equal(logs[0].event, "TransferFromByDate");
        assert.equal(logs[0].args.spender, spender);
        assert.equal(logs[0].args.from, owner);
        assert.equal(logs[0].args.to, acc1);
        assert.equal(logs[0].args.values[0], 100 * MAGNITUDE);
        assert.equal(logs[0].args.dates[0], time + DAY);

        // approve and transferFromByDate
        await sht.approve(spender, 200 * MAGNITUDE, {from: owner});
        var { logs } = await sht.transferFromByDate(owner, acc1, [100 * MAGNITUDE, 100 * MAGNITUDE], [time - DAY, time + DAY], {from: spender});
        // assert logs
        assert.equal(logs.length, 2);
        assert.equal(logs[0].event, "TransferFrom");
        assert.equal(logs[0].args.spender, spender);
        assert.equal(logs[0].args.from, owner);
        assert.equal(logs[0].args.to, acc1);
        assert.equal(logs[0].args.value, 100 * MAGNITUDE);
        assert.equal(logs[1].event, "TransferFromByDate");
        assert.equal(logs[1].args.spender, spender);
        assert.equal(logs[1].args.from, owner);
        assert.equal(logs[1].args.to, acc1);
        assert.equal(logs[1].args.values[0], 100 * MAGNITUDE);
        assert.equal(logs[1].args.values[1], 100 * MAGNITUDE);
        assert.equal(logs[1].args.dates[0], time - DAY);
        assert.equal(logs[1].args.dates[1], time + DAY);
    });

    it("event OpenBuy should be triggerred", async() => {
        await sht.setBuyPrice(buyPrice, {from: owner});
        await sht.addTokenToFund(100*MAGNITUDE, {from: owner});
        var { logs } = await sht.openBuy({from: owner});
        // assert logs
        assert.equal(logs.length, 1);
        assert.equal(logs[0].event, "OpenBuy");
        assert.equal(logs[0].args.who, owner);
    });

    it("event CloseBuy should be triggerred", async() => {
        await sht.setBuyPrice(buyPrice, {from: owner});
        await sht.addTokenToFund(100*MAGNITUDE, {from: owner});
        await sht.openBuy({from: owner});
        var { logs } = await sht.closeBuy({from: owner});
        // assert logs
        assert.equal(logs.length, 1);
        assert.equal(logs[0].event, "CloseBuy");
        assert.equal(logs[0].args.who, owner);
    });

    it("event OpenSell should be triggerred", async() => {
        await sht.setSellPrice(sellPrice, {from: owner});
        var { logs } = await sht.openSell({from: owner});
        // assert logs
        assert.equal(logs.length, 1);
        assert.equal(logs[0].event, "OpenSell");
        assert.equal(logs[0].args.who, owner);
    });

    it("event CloseSell should be triggerred", async() => {
        await sht.setSellPrice(sellPrice, {from: owner});
        await sht.openSell({from: owner});
        var { logs } = await sht.closeSell({from: owner});
        // assert logs
        assert.equal(logs.length, 1);
        assert.equal(logs[0].event, "CloseSell");
        assert.equal(logs[0].args.who, owner);
    });

    it("event Buy should be triggerred", async() => {
        await sht.setBuyPrice(buyPrice, {from: owner});
        await sht.addTokenToFund(100*MAGNITUDE, {from: owner});
        await sht.openBuy({from: owner});
        var { logs } = await sht.buy({from: acc1, value: 10 * MAGNITUDE});
        // assert logs
        assert.equal(logs.length, 2);
        assert.equal(logs[0].event, "TransferFrom");
        assert.equal(logs[0].args.spender, acc1);
        assert.equal(logs[0].args.from, fundAccount);
        assert.equal(logs[0].args.to, acc1);
        assert.equal(logs[0].args.value, 100 * MAGNITUDE);
        assert.equal(logs[1].event, "Buy");
        assert.equal(logs[1].args.who, acc1);
        assert.equal(logs[1].args.etherValue, 10 * MAGNITUDE);
        assert.equal(logs[1].args.tokenValue, 100 * MAGNITUDE);
    });

    it("event Sell should be triggerred", async() => {
        await sht.setSellPrice(sellPrice, {from: owner});
        await sht.openSell({from: owner});
        await sht.transfer(acc1, 1000 * MAGNITUDE, {from: owner});
        await sht.sendTransaction({from: owner, value: 1 * MAGNITUDE});
        var { logs } = await sht.sell(1000 * MAGNITUDE, {from: acc1});
        // assert logs
        assert.equal(logs.length, 2);
        assert.equal(logs[0].event, "Transfer");
        assert.equal(logs[0].args.from, acc1);
        assert.equal(logs[0].args.to, fundAccount);
        assert.equal(logs[0].args.value, 1000 * MAGNITUDE);
        assert.equal(logs[1].event, "Sell");
        assert.equal(logs[1].args.from, acc1);
        assert.equal(logs[1].args.to, fundAccount);
        assert.equal(logs[1].args.tokenValue, 1000 * MAGNITUDE);
        assert.equal(logs[1].args.etherValue, 1 * MAGNITUDE);
    });

    it("event Withdraw should be triggerred", async() => {
        await sht.sendTransaction({from: owner, value: 1 * MAGNITUDE});
        var { logs } = await sht.withdraw({from: owner});
        // assert logs
        assert.equal(logs.length, 1);
        assert.equal(logs[0].event, "Withdraw");
        assert.equal(logs[0].args.who, owner);
        assert.equal(logs[0].args.etherValue, 1 * MAGNITUDE);
    });

    it("event AddTokenToFund should be triggerred", async() => {
        var { logs } = await sht.addTokenToFund(100*MAGNITUDE, {from: owner});
        // assert logs
        assert.equal(logs.length, 2);
        assert.equal(logs[0].event, "Transfer");
        assert.equal(logs[0].args.from, owner);
        assert.equal(logs[0].args.to, fundAccount);
        assert.equal(logs[0].args.value, 100 * MAGNITUDE);
        assert.equal(logs[1].event, "AddTokenToFund");
        assert.equal(logs[1].args.who, owner);
        assert.equal(logs[1].args.value, 100 * MAGNITUDE);
    });

    it("event Refresh should be triggerred", async() => {
        await sht.transferByDate(acc1, [100 * MAGNITUDE], [time + DAY], {from: owner});
        var { logs } = await sht.refresh(acc1, {from: owner});
        // assert logs
        assert.equal(logs.length, 1);
        assert.equal(logs[0].event, "Refresh");
        assert.equal(logs[0].args.from, owner);
        assert.equal(logs[0].args.who, acc1);
    });

})
