
var SibbayHealthToken = artifacts.require("./SibbayHealthToken.sol");

contract("SibbayHealthToken-erc20-sht", accounts => {

    const [owner, acc1, acc2, acc3] = accounts;
    const MAGNITUDE = 10 ** 18;
    let sht;

    beforeEach(async() => {
        sht = await SibbayHealthToken.new();
    });

    it("should have name Sibbay Health Token", async() => {
        assert.equal(await sht.name.call(), "Sibbay Health Token");
    });

    it("should have symbol SHT", async() => {
        assert.equal(await sht.symbol.call(), "SHT");
    });

    it("should have decimals 18", async() => {
        assert.equal(await sht.decimals.call(), 18);
    });

    it("total supply should be 1000000000 * (10 ** 18) ", async() => {
        assert.equal(await sht.totalSupply.call(), 1000000000 * MAGNITUDE);
    })

    it("balance of account should be right", async() => {
        assert.equal(await sht.balanceOf.call(owner), 1000000000 * MAGNITUDE);
        assert.equal(await sht.balanceOf.call(acc1), 0);
        assert.equal(await sht.balanceOf.call(acc2), 0);
        assert.equal(await sht.balanceOf.call(acc3), 0);
    })

    it("transfer 100 tokens should be successful", async() => {
        await sht.transfer(acc1, 100 * MAGNITUDE, {from: owner});
        assert.equal(await sht.balanceOf.call(owner), (1000000000 - 100) * MAGNITUDE);
        assert.equal(await sht.balanceOf.call(acc1), 100 * MAGNITUDE);
    })

    it("approve 100 tokens should be successful", async() => {
        await sht.approve(acc1, 100 * MAGNITUDE, {from: owner});
        assert.equal(await sht.allowance(owner, acc1), 100 * MAGNITUDE);
    })

    // same to approve
    it("allowance of account should be successful", async() => {
        await sht.approve(acc1, 100 * MAGNITUDE, {from: owner});
        assert.equal(await sht.allowance(owner, acc1), 100 * MAGNITUDE);
    })

    it("increase apporval 100 tokens should be successful", async() => {
        await sht.increaseApproval(acc1, 100 * MAGNITUDE, {from: owner});
        assert.equal(await sht.allowance(owner, acc1), 100 * MAGNITUDE);
    })

    it("decrease approval 100 tokens should be successful", async() => {
        await sht.approve(acc1, 100 * MAGNITUDE, {from: owner});
        await sht.decreaseApproval(acc1, 100 * MAGNITUDE, {from: owner});
        assert.equal(await sht.allowance(owner, acc1), 0);
    })

    it("transfer from 100 tokens should be successful", async() => {
        await sht.approve(acc1, 100 * MAGNITUDE, {from: owner});
        await sht.transferFrom(owner, acc2, 100*MAGNITUDE, {from: acc1});
        assert.equal(await sht.allowance(owner, acc1), 0 * MAGNITUDE);
        assert.equal(await sht.balanceOf.call(acc1), 0);
        assert.equal(await sht.balanceOf.call(owner), (1000000000 - 100) * MAGNITUDE);
        assert.equal(await sht.balanceOf.call(acc2), 100 * MAGNITUDE);
    })
})
