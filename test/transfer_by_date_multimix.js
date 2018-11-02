var SibbayHealthToken = artifacts.require("./SibbayHealthToken.sol");
var log4js = require('log4js');
const { increaseTime } = require("./utils/increaseTime.js");
const { latestTime } = require("./utils/latestTime.js");

contract("SibbayHealthToken", accounts => {

    var logger = log4js.getLogger();
    logger.level = 'info';
    const [owner, fundAccount, acc1, acc2, acc3, acc4] = accounts;
    const MAGNITUDE = 10 ** 18;
    const DAY = 3600 * 24;
    // sell price 0.001 ether
    let sellPrice = 10 ** 15;
    // buy price 0.1 ether
    let buyPrice = 10 ** 17;
    let sht;
    let time;

    beforeEach(async() => {
        sht = await SibbayHealthToken.new(owner, fundAccount);
        time = await latestTime();
    });

    it("transfer by date 日期更新", async() => {
        await sht.transferByDate(acc3, [1 * MAGNITUDE, 2*MAGNITUDE, 3*MAGNITUDE], [time + DAY,time + 2*DAY,time + 3*DAY], {from: owner});
        await sht.transferByDate(acc3, [1 * MAGNITUDE, 2*MAGNITUDE, 3*MAGNITUDE], [time + 5,time + 2*3600,time + 24*3600], {from: owner});
        var res = await sht.accounts.call(acc3)
        var first = res[1]
        assert.equal(first, time + 5);
        // increase time
        await increaseTime(6);

        res = await sht.accounts.call(acc3)
        first = res[1]
        assert.equal(first, time + 5);
        await sht.refresh(acc3)
        res = await sht.accounts.call(acc3)
        first = res[1]
        assert.equal(first, time + 2*3600);

    })

    it("transfer by date 大量压力", async() => {
        var times = 30
        let i = 0
        while (i<times){
            i += 1;
            await sht.transferByDate(acc4, [MAGNITUDE], [time + i*100], {from: owner});
        }
        i = 0
        while (i<times){
            i += 1;
            await sht.transferByDate(acc4, [MAGNITUDE], [time + i*200], {from: owner});
        }
        i = 0
        while (i<times){
            i += 1;
            await sht.transferByDate(acc4, [MAGNITUDE], [time + i*300], {from: owner});
        }

        var res = await sht.accounts.call(acc4)
        var next = res[1]
        //logger.info(next);
        i = 0
        while (next > 0){
            i += 1
            res = await sht.lockedBalanceOfByDate.call(acc4, next)
            //logger.info(i,res[0]);
            next = res[1]
        }
        assert.equal(i , times*2);
    })


    it("transfer by date 相同日期重叠相加", async() => {
        await sht.transferByDate(acc1, [1 * MAGNITUDE], [time + DAY], {from: owner});
        await sht.transferByDate(acc1, [0.3 * MAGNITUDE], [time + DAY], {from: owner});

        var res = await sht.accounts.call(acc1)
        var first = res[1]
        assert.equal(first, time +  DAY);
        var res = await sht.lockedBalanceOfByDate.call(acc1, first)
        assert.equal(res[1], 0);
        assert.equal(res[0], 1.3 * MAGNITUDE);

    })

    it("transfer by date 时间交错+叠加", async() => {
        await sht.transferByDate(acc2, [1 * MAGNITUDE, 2*MAGNITUDE, 3*MAGNITUDE], [time + 3*DAY,time + 2*DAY,time + 1*DAY], {from: owner});
        await sht.transferByDate(acc2, [0.1 * MAGNITUDE, 0.2*MAGNITUDE, 0.3*MAGNITUDE], [time + 1*DAY,time + 2*3600,time + 1*3600], {from: owner});

        var res = await sht.accounts.call(acc2)
        var first = res[1]
        assert.equal(first, time +  1*3600);
        var res = await sht.lockedBalanceOfByDate.call(acc2, first)
        assert.equal(res[1], time + 2*3600);
        res = await sht.lockedBalanceOfByDate.call(acc2, res[1])
        assert.equal(res[1], time + 1*DAY);
        res = await sht.lockedBalanceOfByDate.call(acc2, res[1])
        assert.equal(res[0], 3.1*MAGNITUDE);

    })

})
