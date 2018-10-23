

/*
 * 测试样板
 * 仅供truffle testcase使用
 * */

/*
 * 包含必要的合约文件
 */
var SibbayHealthToken = artifacts.require("./SibbayHealthToken.sol");

/*
 * latestTime 获取最近出块时间，替代Date.now()
 * increaseTime 增加时间，用于使锁定期快速到期的方法
 * log4js 用于日志打印
 */
const { latestTime } = require("./utils/latestTime.js");
const { increaseTime } = require("./utils/increaseTime.js");
var log4js = require('log4js');

/*
 * 合约测试开始
 */
contract("sample of beginning to test", accounts => {

    /*
     * 1. 获取账户方法，一共10个账户
     * 2. 小数点位数，方便计算，也可以用1e18简单表示
     * 3. 一天的秒数
     */
    const [owner, spender, acc1, acc2, acc3] = accounts;
    const MAGNITUDE = 10 ** 18;
    const DAY = 3600 * 24;

    /*
     * logger 实例，实现js的简单日志输出
     */
    var logger = log4js.getLogger();
    logger.level = 'info';

    /*
     * 全局变量，所有case都要使用
     */
    let sht;
    let time;

    /*
     * 所有case之前都要执行的内容:
     * 1. 生成新的合约
     * 2. 获取最新块的时间
     */
    beforeEach(async() => {
        sht = await SibbayHealthToken.new();
        time = await latestTime();
    });

    /*
     * 所有测试用例都用异步的方法实现
     * 1. 查询类的接口用 function.call()来实现
     * 2. 修改类的接口直接使用函数名发送交易
     */
    it("sample case 1", async() => {
        /*
         * 查询类接口
         */
        assert.equal(await sht.name.call(), "Sibbay Health Token");
        assert.equal(await sht.symbol.call(), "SHT");

        /*
         * 修改类接口
         */
        await sht.transfer(acc1, 100 * MAGNITUDE, {from: owner});
        await sht.approve(spender, 100 * MAGNITUDE, {from: owner});

        /*
         * 向合约发送1个以太币
         */
        await sht.sendTransaction({from: owner, value: 1 * MAGNITUDE});

        /*
         * 接口失败调用的判断方法
         * 使用 try catch，并revert交易
         */
        try {
            await sht.transfer(0x0, 100 * MAGNITUDE, {from: owner});
            assert.fail();
        } catch (err){
            assert.ok(/revert/.test(err.message));
        }

        /*
         * 更新出块时间 now + DAY
         */
        await increaseTime(DAY);

        /*
         * 打印日志
         */
        logger.info("name is", await sht.name.call());
    });

    /*
     * 同上，添加其它case
     */
    it("sample case 2", async() => {
        /*
         * 事件验证
         */
        var { logs } = await sht.transfer(acc1, 100 * MAGNITUDE, {from: owner});
        //logger.info("logs is", logs);
        assert.equal(logs.length, 1);
        assert.equal(logs[0].event, "Transfer");
        assert.equal(logs[0].args.from, owner);
        assert.equal(logs[0].args.to, acc1);
        assert.equal(logs[0].args.value, 100 * MAGNITUDE);
    });
})
