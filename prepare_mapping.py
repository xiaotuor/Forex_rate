from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import json

currency_symbol_mapping = {}#中国银行网站的外汇货币类型与货币符号的映射字典

def fetch_currency_type():
    """从中国银行获取所有可选的外汇货币类型"""
    driver = webdriver.Chrome()
    try:
        driver.get("https://www.boc.cn/sourcedb/whpj/")
        select_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "pjname")))
        select = Select(select_element)
        options_text = [option.text for option in select.options][1:] # 去除“选择货币”选项
        print(options_text)
    finally:
        driver.quit()

    return options_text

def init_currency_symbol_mapping():
    """初始化货币符号映射"""
    currency_type = fetch_currency_type()
    all_currency_symbol_mapping = {} # 对照网站中所有的外汇货币类型与货币符号的映射字典
    driver = webdriver.Chrome()
    try:
        driver.get('https://www.11meigui.com/tools/currency')

        #分大洲获取所有的货币符号
        continents = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//table/tbody/tr[2]/td/table[position()>=1]")))
        for continent in continents:
            for currency in continent.find_elements(By.XPATH, "./tbody/tr[position()>=3]"):
                all_currency_symbol_mapping[currency.find_element(By.XPATH, "./td[2]").text] = currency.find_element(By.XPATH, "./td[5]").text
        #print(all_currency_symbol_mapping)

        # 对照网站中名字不一样但是货币符号一样的别名
        alias_mapping = {
            '港币': '港元',
            '日元': '日圆',
            '加拿大元': '加元',
            '泰国铢': '泰铢',
            '林吉特': '马元',
            '西班牙比塞塔': '比塞塔',
            '意大利里拉': '里拉',
            '印尼卢比': '盾',
            '印度卢比': '卢比',
            '南非兰特': '兰特',
        }
        # 对照网站中没有或者不匹配的货币符号（搜索得到）
        all_currency_symbol_mapping['韩元'] = 'KRW'
        all_currency_symbol_mapping['新台币'] = 'NT$'
        all_currency_symbol_mapping['巴西里亚尔'] = 'BRL'
        all_currency_symbol_mapping['阿联酋迪拉姆'] = 'AED'
        all_currency_symbol_mapping['沙特里亚尔'] = 'SAR'
        all_currency_symbol_mapping['土耳其里拉'] = 'TRY'

        for currency in currency_type:
            try:
                # 如果currency直接在映射中，使用它
                if currency in all_currency_symbol_mapping:
                    currency_symbol_mapping[currency] = all_currency_symbol_mapping[currency]
                # 否则检查是否存在别名
                elif currency in alias_mapping and alias_mapping[currency] in all_currency_symbol_mapping:
                    currency_symbol_mapping[currency] = all_currency_symbol_mapping[alias_mapping[currency]]
                else:
                    # 如果找不到货币及其别名，打印错误消息(一次性找到所有错误)
                    print(f"Error: Currency {currency} not found in mapping.")
            except KeyError as e:
                # 打印异常消息
                print(f"KeyError: {e}")
        #sys.exit()
                
    finally:
        driver.quit()
    print(currency_symbol_mapping)


if __name__ == "__main__":
    init_currency_symbol_mapping()

    # 将映射字典保存到文件
    with open('currency_symbol_mapping.json', 'w', encoding= 'utf-8') as file:
        json.dump(currency_symbol_mapping, file, ensure_ascii=False, indent=4)
