# Forex_rate
本项目利用web自动化在中国银行外汇牌价网站（https://www.boc.cn/sourcedb/whpj/）上自动查询某时间下某货币对人民币的现汇卖出价，拥有四种模式，默认为给某一日期和某一货币标准符号，输出的结果保存在result.txt中,其他三种模式为不同的批处理模式，输出的结果保存在results.txt中。
## Getting Started
### Prerequisites
Python带有selenium的环境即可
### Introduction
currency_symbol_mapping.json文件为prepare_mapping.py文件的运行结果
该文件给出了一个包含所有以中国银行能查到的外汇货币的中文名称为键和以其标准符号为值的字典，prepare_mapping.py文件中包含取数据逻辑。

input.txt为三种批处理模式的输入文件

search_forex_rate.py文件为查询时运行的文件

标准符号大部分来自https://www.11meigui.com/tools/currency，该网站上没有的部分来自搜索引擎。
## Running the tests
### Default
在终端运行如下命令：

```bash
python3 ./search_forex_rate.py YYYYMMDD USD
```

即可获得YYYYMMDD日期当天的某时间的美元汇率输出在result.txt文件中。
### One_date
输入文件input.txt文件格式：

第一行为日期YYYYMMDD，其余行每行都是一个货币标准符号。

在终端运行如下命令：

```bash
python3 ./search_forex_rate.py input.txt --pattern one_date
```

即可获得YYYYMMDD日期当天的某时间的所有输入货币类型的汇率输出在results.txt文件中。
### One_currency
输入文件input.txt文件格式：

第一行为一个货币标准符号，其余每行都是一个日期YYYYMMDD。

在终端运行如下命令：

```bash
python3 ./search_forex_rate.py input.txt --pattern one_currency
```

即可获得该外汇货币在所有输入日期的汇率输出在results.txt文件中。
### Multiple
输入文件input.txt文件格式：

每一行都是以逗号分隔的某一日期和某一货币标准符号，例如YYYYMMDD,USD

在终端运行如下命令

```bash
python3 ./search_forex_rate.py input.txt --pattern multiple
```

即可获得所有不同搭配的汇率输出在results.txt文件中。

