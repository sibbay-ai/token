var SibbayHealthToken = artifacts.require("SibbayHealthToken");

var fund = "0xee21ebb177539f247d4c9cc6255facf2af21e6b4";

module.exports = function(deployer) {
    deployer.deploy(SibbayHealthToken, fund);
}
