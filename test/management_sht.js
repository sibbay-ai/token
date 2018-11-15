
var SibbayHealthToken = artifacts.require("./SibbayHealthToken.sol");

contract("SibbayHealthToken-management-sht", accounts => {

    const [sender, owner, fundAccount, acc1, acc2, acc3] = accounts;
    const MAGNITUDE = 10 ** 18;
    let sht;

    beforeEach(async() => {
        sht = await SibbayHealthToken.new(owner, fundAccount);
    });

    it("add administrator should be successful", async() => {
        await sht.addAdministrator(acc1, {from: owner});
        assert.equal(await sht.adminList.call(acc1), true);
    });

    it("del administrator should be successful", async() => {
        await sht.addAdministrator(acc1, {from: owner});
        assert.equal(await sht.adminList.call(acc1), true);
        await sht.delAdministrator(acc1, {from: owner});
        assert.equal(await sht.adminList.call(acc1), false);
    })

    it("pause contract should be successful", async() => {
        await sht.pause({from: owner});
        assert.equal(await sht.paused.call(), true);
    })

    it("unpause contract should be successful", async() => {
        await sht.pause({from: owner});
        assert.equal(await sht.paused.call(), true);
        await sht.unpause({from: owner});
        assert.equal(await sht.paused.call(), false);
    })

    it("open autoFreeLockBalance be successful", async() => {
        await sht.openAutoFree(acc1, {from: owner});
        assert.equal(await sht.autoFreeLockBalance.call(acc1), false);
    })

    it("close autoFreeLockBalance be successful", async() => {
        await sht.closeAutoFree(acc1, {from: owner});
        assert.equal(await sht.autoFreeLockBalance.call(acc1), true);
    })

    it("open froceAutoFreeLockBalance be successful", async() => {
        await sht.openForceAutoFree(acc1, {from: owner});
        assert.equal(await sht.forceAutoFreeLockBalance.call(acc1), true);
    })

})
