from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import json

def select_currency(driver, currency_code):
    '''选择货币类型'''
    # 使用映射字典找到对应的中文名称
    currency_name = [name for name, code in currency_symbol_mapping.items() if code == currency_code][0]
    if not currency_name:
        raise ValueError(f"Currency code {currency_code} not found in mapping")

    # 点击货币下拉列表
    currency_dropdown = driver.find_element(By.NAME, "pjname")
    currency_dropdown.click()
    
    # 选择对应的货币
    try:
        currency_option = driver.find_element(By.XPATH, f"//option[contains(text(), '{currency_name}')]")
        currency_option.click()
    except Exception as e:
        raise Exception(f"Currency option {currency_name} not found on the website.")


def data_input(driver, data):
    '''输入日期'''
    # 开始日期
    data_input_start = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "erectDate")))
    data_input_start.clear()
    data_input_start.send_keys(data)
    data_input_start.click()
    driver.find_element(By.ID, "calendarClose").click()
    
    # 结束日期
    data_input_end = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "nothing")))
    data_input_end.clear()
    data_input_end.send_keys(data)
    data_input_start.click()
    driver.find_element(By.ID, "calendarClose").click()


def fetch_forex_rate(data, currency_code):
    '''获取外汇汇率'''
    driver = webdriver.Chrome()
    try:
        driver.get("https://www.boc.cn/sourcedb/whpj/")
        # 输入日期并关闭
        data_input(driver, data)
        # 输入货币代号
        select_currency(driver, currency_code)
        # 点击查询
        driver.find_element(By.XPATH, "//input[@onclick='executeSearch()']").click()
        # 等待结果出现
        value_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//tr[@class='odd'][1]/td[4]")))
        value = value_element.text
    finally:
        driver.quit()
    return value

def fetch_forex_rate(data, currency_code):
    '''获取外汇汇率'''
    driver = webdriver.Chrome()
    try:
        driver.get("https://www.boc.cn/sourcedb/whpj/")
        #输入日期并关闭
        data_input(driver, data)
        #输入货币代号
        select_currency(driver, currency_code)
        #点击查询
        driver.find_element(By.XPATH, "//input[@onclick='executeSearch()']").click()
        #获取现汇卖出价
        value = driver.find_element(By.XPATH, "//tr[@class='odd'][1]/td[4]").text
    finally:
        driver.quit()
    return value

def process_input_file(input_file, pattern):
    '''根据提供的模式处理输入文件'''
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    results = []
    if pattern == 'one_currency':
        currency_code = lines[0].strip()  # 假设第一行是货币代码
        dates = [line.strip() for line in lines[1:]]  # 其余行是日期
        for date in dates:
            rate = fetch_forex_rate(date, currency_code)
            results.append(f"{date}, {currency_code}: {rate}\n")

    elif pattern == 'one_date':
        date = lines[0].strip()  # 假设第一行是日期
        currency_codes = [line.strip() for line in lines[1:]]  # 其余行是货币代码
        for currency_code in currency_codes:
            rate = fetch_forex_rate(date, currency_code)
            results.append(f"{date}, {currency_code}: {rate}\n")

    elif pattern == 'multiple':
        for line in lines:
            date, currency_code = line.strip().split(',')
            rate = fetch_forex_rate(date, currency_code)
            results.append(f"{date}, {currency_code}: {rate}\n")

    # 将结果写入到输出文件
    with open('results.txt', 'a', encoding='utf-8') as file:
        for result in results:
            file.write(result)

def print_usage():
    print("Usage:")
    print("  Default mode: python3 yourcode.py YYYYMMDD CURRENCY_CODE")
    print("  Other modes:  python3 yourcode.py input.txt --pattern [one_currency|one_date|multiple]")
    sys.exit(1)

if __name__ == "__main__":
    # 读取映射字典
    with open('currency_symbol_mapping.json', 'r', encoding='utf-8') as file:
        currency_symbol_mapping = json.load(file)
    
    # 检查参数个数
    if len(sys.argv) not in [3, 4]:
        print_usage()

    # 默认模式
    if len(sys.argv) == 3:
        data, currency_code = sys.argv[1], sys.argv[2]
        forex_rate = fetch_forex_rate(data, currency_code)
        print(forex_rate)
        # 将汇率写入到文件
        with open('result.txt', 'a', encoding='utf-8') as file:
            file.write(f"{data}, {currency_code}: {forex_rate}\n")

    # 其他模式
    elif len(sys.argv) == 4 and sys.argv[2] == '--pattern':
        input_file = sys.argv[1]
        pattern = sys.argv[3]
        if pattern not in ['one_currency', 'one_date', 'multiple']:
            print("Error: Invalid pattern specified.")
            print_usage()
        process_input_file(input_file, pattern)
        
    else:
        print_usage()


