# token
Sibbay Health Token


## 单元测试运行方法
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
