var SibbayHealthToken = artifacts.require("SibbayHealthToken");

var owner = "0xee21ebb177539f247d4c9cc6255facf2af21e6b4";
var fund = "0x28b7a7fd5e876e5e2ac50dbb66860d80b2e2db3a";

module.exports = function(deployer) {
    deployer.deploy(SibbayHealthToken, owner, fund);
}
