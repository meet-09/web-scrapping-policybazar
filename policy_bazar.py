import sys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as cond
from selenium.webdriver.common.by import By
import time
import random
import string
import pprint
import csv
import datetime


def getVariant(variant_list, input_variant):
    # v_count = 0
    variant_xpath = ''
    # for variant in variant_list:
    #     v_count += 1

    #     print(variant.text.split("(")[0].lower())
    #     if(variant.text.split("(")[0].lower().strip() == input_variant.lower()):
    #         variant_xpath = '//*[@id="variantScroll"]/li[' + str(v_count) + ']/span'
    # for i in range(0,len(variant_list)):
    v_num = random.randint(1,len(variant_list))
    variant_xpath = '//*[@id="variantScroll"]/li[' + str(v_num) + ']/span'

    # print(variant_xpath)
    return variant_xpath


def getRegYear(input_reg_year):
    r_count = 0
    reg_year_xpath = ''
    year_dict = {
        '2018':'1',
        '2017':'2',
        '2016':'3',
        '2015':'4',
        '2014':'5',
        '2013':'6',
    }

    # for reg_year in reg_year_list:
    #     r_count += 1

    #     print(reg_year.text)
        # if(reg_year.text == input_reg_year):
        #     reg_year_xpath = '//*[@id="dvRegYear"]/ul/div/li[' + str(r_count) + ']/span'
            # //*[@id="dvRegYear"]/ul/div/li[6]/span - 2013
            # //*[@id="dvRegYear"]/ul/div/li[5]/span
            # //*[@id="dvRegYear"]/ul/div/li[1]/span
    reg_year_xpath = '//*[@id="dvRegYear"]/ul/div/li[' + year_dict[input_reg_year] + ']/span'
    return reg_year_xpath

# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
# driver = webdriver.Chrome(options=chrome_options,executable_path=r"C:\webdrivers\chromedriver")
# driver.get('https://ci.policybazaar.com/questions?utm_source=&utm_term=&utm_campaign=&utm_medium=&ishome=true')


def calculatePolicy(area,model,fuel_type,input_variant,input_reg_year,input_policy_expiry,input_claim_choice):
    
    try:
        error = False
        
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(options=chrome_options,executable_path=r"C:\webdrivers\chromedriver")
        driver.get('https://ci.policybazaar.com/questions?utm_source=&utm_term=&utm_campaign=&utm_medium=&ishome=true')

        info_dict = {
                'model' : '',
                'variant' : '',
                'RTO' : '',
                'Fuel Type':'',
                'policy_expiry_time' : '',
                'NCB_value' : '',
                'car_bought_year' : '',
                'Did you Claim' : '',
                'supplier-1':'',
                'supplier-2':'',
                'supplier-3':'',
                'supplier-4':'',
                'supplier-5':'',
                'supplier-6':'',
                'supplier-7':'',
                'supplier-8':'',
                'supplier-9':'',
                'supplier-10':'',
            }

        time.sleep(2)
        rto_search = driver.find_element_by_tag_name('input')
        rto_search.send_keys(area)
        

        time.sleep(1)
        rto_select = driver.find_element_by_id('react-autowhatever-1').click()
        info_dict['RTO'] = area

        time.sleep(1)
        model_search = driver.find_element_by_tag_name('input')
        model_search.send_keys(model)

        time.sleep(1)
        model_select = driver.find_element_by_id('react-autowhatever-1').click()
        info_dict['model'] = model

        if(fuel_type.lower() == 'diesel'):
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="Diesel"]').click()
        else:
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="Petrol"]').click()

        info_dict['Fuel Type'] = fuel_type
        
        time.sleep(2)
        div_variant = driver.find_element_by_id('variantScroll')
        variant_list = div_variant.find_elements_by_tag_name('li')
        variant_xpath = getVariant(variant_list, input_variant)
        variant = driver.find_element_by_xpath(variant_xpath).text
        driver.find_element_by_xpath(variant_xpath).click()
        info_dict['variant'] = variant

        time.sleep(2)
        # div_reg_year = driver.find_elements_by_class_name('row')
        # reg_year_list = div_reg_year[1].find_elements_by_tag_name('li')
        # reg_year_list = driver.find_elements_by_xpath("//*[contains(@class, 'col-sm-4') and contains(@class ,'col-xs-4')]")
        reg_year = getRegYear(input_reg_year)
        driver.find_element_by_xpath(reg_year).click()
        info_dict['car_bought_year'] = input_reg_year

        time.sleep(2)
        input_name = driver.find_element_by_id('name')
        input_name.send_keys('Dexter')
        input_email = driver.find_element_by_id('email')
        input_email.send_keys('dexter@gmail.com')
        input_mob_no = driver.find_element_by_id('mobileNo')
        input_mob_no.send_keys('9898123451')

        time.sleep(1)
        driver.find_element_by_id('btnLeadDetails').click()

        time.sleep(2)
        appearing_lower_month = driver.find_element_by_xpath('//*[@id="datepicker"]/div/div[1]/div/div/span[1]').text
        appearing_lower_year = driver.find_element_by_xpath('//*[@id="datepicker"]/div/div[1]/div/div/span[2]').text
        appearing_higher_month = driver.find_element_by_xpath('//*[@id="datepicker"]/div/div[2]/div/div/span[1]').text
        appearing_higher_year = driver.find_element_by_xpath('//*[@id="datepicker"]/div/div[2]/div/div/span[2]').text

        appearing_lower_date = datetime.datetime.strptime((appearing_lower_month + "-" + appearing_lower_year),"%B-%Y")
        appearing_higher_date = datetime.datetime.strptime((appearing_higher_month + "-" + appearing_higher_year),"%B-%Y")

        input_date = datetime.datetime.strptime(input_policy_expiry,"%d/%m/%Y")

        if(input_date < appearing_lower_date):
            driver.find_element_by_xpath('//*[@id="datepicker"]/div/div[1]/div/a').click()
            time.sleep(2)
            date_list = driver.find_elements_by_tag_name('td')
            for date in date_list:
                if(date.get_attribute('data-month') == str(int(input_policy_expiry.split('/')[1])-1) and date.get_attribute('data-year') == input_policy_expiry.split('/')[2]):
                    d = date.find_element_by_tag_name('a')
                    if(d.text == input_policy_expiry.split('/')[0]):
                        d.click()
                        break
        elif(input_date > appearing_higher_date):
            driver.find_element_by_xpath('//*[@id="datepicker"]/div/div[2]/div/a').click()
            time.sleep(2)
            date_list = driver.find_elements_by_tag_name('td')
            for date in date_list:
                if(date.get_attribute('data-month') == str(int(input_policy_expiry.split('/')[1])-1) and date.get_attribute('data-year') == input_policy_expiry.split('/')[2]):
                    d = date.find_element_by_tag_name('a')
                    if(d.text == input_policy_expiry.split('/')[0]):
                        d.click()
                        break
        else:
            time.sleep(2)
            date_list = driver.find_elements_by_tag_name('td')
            for date in date_list:
                if(date.get_attribute('data-month') == str(int(input_policy_expiry.split('-')[1])-1) and date.get_attribute('data-year') == input_policy_expiry.split('-')[2]):
                    d = date.find_element_by_tag_name('a')
                    if(d.text == input_policy_expiry.split('-')[0]):
                        d.click()
                        break

        info_dict['policy_expiry_time'] = input_policy_expiry

        if(input_claim_choice.lower() == 'yes'):
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="rightSection"]/div/div/div[1]/div[2]/div/button[1]').click()
        elif(input_claim_choice.lower() == 'no'):
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="rightSection"]/div/div/div[1]/div[2]/div/button[2]').click()
            

        info_dict['Did you Claim'] = input_claim_choice.lower()

        time.sleep(10)
        ncb_val = driver.find_element_by_xpath('//*[@id="quotes-top"]/div[3]/div[1]/div[1]/div[2]/div[1]/p[2]/em').text
        # print("ncb val :",ncb_val)
        info_dict['NCB_value'] = ncb_val

        div_for_data = driver.find_element_by_id('dvQuoteList')
        quotes_list = div_for_data.find_elements_by_xpath("//*[contains(@class, 'quote-tile')]")

        count = 0

        for quotes in quotes_list:
            idv_value = 0
            premium_plan_value = 0

            count += 1

            # print(quotes.get_attribute('class'))
            quote_class = quotes.get_attribute('class').split(' ')
            for q in quote_class:
                if(q.split('-')[0].lower() == 'supplierid'):
                    supplier_id = q.split('-')[1]
            # print("supplier id :",supplier_id)
            
            idv_xpath = '//*[@id="' + str(supplier_id) + '"]/ul/li[2]/div[2]/div[2]/div/div[1]/div[2]'
            idv_value = driver.find_element_by_xpath(idv_xpath).text
            # print("idv Val :",idv_value)

            premium_xpath = '//*[@id="' + str(supplier_id) + '"]/ul/li[3]/div[2]/a/span'
            premium_plan_value = driver.find_element_by_xpath(premium_xpath).text
            # print("Premium Val :",premium_plan_value)

            data = [supplier_id,idv_value,premium_plan_value]

            info_dict['supplier-' + str(count)] = data
            
            if(count == 10):
                break

        return [info_dict,error]

    except Exception as ex:
        print(ex)
        error = True
        
        info_dict['model'] = model
        return [info_dict,error]


if __name__ == "__main__":
    input_file = csv.DictReader(open('./input-folder/Sample Input for Meet.csv'))

    with open("./output-folder/Sample output for Meet.csv","w",newline='',encoding="utf-8") as f:
        field_names = ['model','variant','RTO','Fuel Type','policy_expiry_time','NCB_value','car_bought_year','Did you Claim','supplier-1','supplier-2','supplier-3','supplier-4','supplier-5','supplier-6','supplier-7','supplier-8','supplier-9','supplier-10']
        writer = csv.DictWriter(f,fieldnames=field_names)
        writer.writeheader()

        for row in input_file:
            # calculatePolicy('KA01','Dzire','petrol','VXI (1298 cc)','2017','29-06-2019','YES')
            policy_information = calculatePolicy(row['RTO and City'],row['Model'],row['Fuel Type'],row['Variant'],row['Registration Year'],row['When does you policy expire'],row['Did you claim '])
            # pprint.pprint(policy_information)
            if(policy_information[1] == True):
                print("Error occured for Model : " + row['Model'] + " , Variant : " + policy_information[0]['variant'])
                writer.writerow(policy_information[0])
                f.flush()
            else:
                pprint.pprint(policy_information[0])
                writer.writerow(policy_information[0])
                f.flush()
        