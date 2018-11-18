
var SibbayHealthToken = artifacts.require("./SibbayHealthToken.sol");
const { latestTime } = require("./utils/latestTime.js");
const { increaseTime } = require("./utils/increaseTime.js");
var log4js = require('log4js');

contract("SibbayHealthToken add token to fund test", accounts => {

    const [sender, owner, fundAccount, spender, acc1, acc2, acc3] = accounts;
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

    it("add token to fund should be success", async() => {
        await sht.addTokenToFund(owner, 100*MAGNITUDE, {from: owner});
        assert.equal(await sht.balanceOf.call(fundAccount), 100 * MAGNITUDE);
    });

    it("add token to fund by from should be success", async() => {
        await sht.approve(acc1, 100 * MAGNITUDE, {from: owner});
        await sht.addTokenToFund(owner, 100*MAGNITUDE, {from: acc1});
        assert.equal(await sht.balanceOf.call(fundAccount), 100 * MAGNITUDE);
    });

    it("add token to fund by from should be success", async() => {
        await sht.transfer(acc1, 100 * MAGNITUDE, {from: owner});
        await sht.addTokenToFund(acc1, 100*MAGNITUDE, {from: acc1});
        assert.equal(await sht.balanceOf.call(fundAccount), 100 * MAGNITUDE);
    });


})
