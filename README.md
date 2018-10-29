# token  
Sibbay Health Token  

## 部署方法 -- 1 部署脚本(推荐)
注意配置钱包地址和fundAccount地址
最简单的方法：详见 tools/ToolREADME.MD中的deploy_contract

## 部署方法 -- 2 truffle (不推荐)
```
注意在2_deploy.js中配置fund地址
truffle compile
truffle migration
```

## truffle test  
```  
$ truffle compile  
$ npm install  
$ truffle test  
```  

## python 单元测试运行方法  
1. 准备 python3 环境  
2. 安装 python 包  
```  
pip install -r test/requirements.txt  
```  
3. test/template_test.py 是一个单元测试的示例文件，不能直接运行   
test 目录下其他的 *_test.py 是智能合约的单元测试文件可以通过如下方法运行  
```  
python test/<file_name>.py  
```

智能合约的操作都是需要挖矿确认的，所以需要比较久的时间    
  
4. 可以通过如下命令运行所有单元测试  

```  
bash test.sh  
```  
