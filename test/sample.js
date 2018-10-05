
var SibbayHealthToken = artifacts.require("./SibbayHealthToken.sol");
var log4js = require('log4js');

contract("SibbayHealthToken", accounts => {

    const [owner, acc1, acc2, acc3] = accounts;
    const MAGNITUDE = 10 ** 18;
    let sht;
    var logger = log4js.getLogger();
    logger.level = 'info';

    beforeEach(async() => {
        sht = await SibbayHealthToken.new();
    });

    it("should have name Sibbay Health Token", async() => {
        assert.equal(await sht.name.call(), "Sibbay Health Token");
        logger.info("\nname is", await sht.name.call());
    });

    it("should have symbol SHT", async() => {
        assert.equal(await sht.symbol.call(), "SHT");
        logger.info("\nsymbole is", await sht.symbol.call());
    });

})
