**训练crf++**  
-f: 使用属性不少于INT  
-p: 线程数  
-m: 迭代次数  
-c: 代价函数，默认1.0 过大会过拟合  
template: 特征模板文件  
model:输出模型文件   
crf_learn -f 4 -p 3 -m 500 -c 3 template ./CRF_data/train_.txt model

**生成测试文件**
crf_test -m model ./data/test.txt > ./data/test.rst
