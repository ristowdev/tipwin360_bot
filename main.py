from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import os

def get_active_sports_links():
    """get all live sports"""

    option = webdriver.ChromeOptions()
    option.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    option.add_argument("--headless")
    option.add_argument("--no-sandobx")
    option.add_argument("--disable-dev-sh-usage")

    # browser = webdriver.Chrome(executable_path='chromedriver', chrome_options=option)
    browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=option)

    browser.get("https://m.betx360.com/?Key=0_0_0_0_0_0_4_0#type=InPlay")
    
    time.sleep(5)
    
    select = Select(browser.find_element(By.CLASS_NAME, 'hpf-select'))
    select.select_by_value('1')

    time.sleep(3)
    browser.get("https://m.betx360.com/?Key=0_0_0_0_0_0_4_0#type=InPlay")
    browser.implicitly_wait(60) # seconds 
    browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    live_sports = []
    active_sports = browser.find_elements(By.CLASS_NAME, 'ipo-Classification')
    WebDriverWait(browser, 10).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'ipo-Classification')))
    sport_len = len(active_sports)
    sport = 0
    while sport < sport_len: 
        # active_sports = browser.find_elements(By.CLASS_NAME, 'ipo-Classification')
        active_sports = WebDriverWait(browser, 10).until(
            EC.visibility_of_all_elements_located((By.CLASS_NAME, "ipo-Classification"))
        )
        sport_len = len(active_sports)
        sport_name = active_sports[sport].find_element(By.CLASS_NAME, 'ipo-Classification_Name').text
        if str(sport_name) == 'Virtual Soccer':
            sport = sport + 1
            sport_name = active_sports[sport].find_element(By.CLASS_NAME, 'ipo-Classification_Name').text
        browser.execute_script("arguments[0].click();", active_sports[sport])
        WebDriverWait(browser, 10).until(
            EC.visibility_of_all_elements_located((By.CLASS_NAME, "ipo-Classification"))
        )
        all_events = WebDriverWait(browser, 10).until(
            EC.visibility_of_all_elements_located((By.CLASS_NAME, "ipo-Event"))
        )
        newlen = len(all_events)
        print(str(sport_name) + str("\n"))
        i = 0
        events_list = []
        while i < newlen:
            all_events = WebDriverWait(browser, 10).until(
                EC.visibility_of_all_elements_located((By.CLASS_NAME, "ipo-Event"))
            )
            newlen = len(all_events)
            teams = WebDriverWait(all_events[i], 10).until(
                EC.visibility_of_all_elements_located((By.CLASS_NAME, "ipo-TeamsText"))
            )
            team_1 = teams[0].text
            team_2 = teams[1].text
            print(str("Teams:") + str(team_1) + str(" - ") + str(team_2))
            browser.execute_script("arguments[0].click();", all_events[i])
            event_url = browser.current_url
            print(event_url)
            event_back = WebDriverWait(browser, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "ipe-EventViewTitle_Back"))
            )
            browser.execute_script("arguments[0].click();", event_back)
            events_list.append({'team_1': team_1, 'team_2': team_2, 'url': event_url})
            i += 1
        sport_url = browser.current_url
        live_sports.append({'sport_name': sport_name, 'sport_url': sport_url, 'sport_fixtures': events_list})
        sport += 1
    return live_sports


def data_load():
    live_sports = get_active_sports_links()

    print(live_sports)
    # go throw all sports
    for sport in live_sports:
        sport_fixutres = sport['sport_fixtures']
        # go throw all fixture in sports
        for fixture in sport_fixutres:
            team_1 = fixture['team_1']
            team_2 = fixture['team_2']
            url = fixture['url'] 


            # check if event is new
            # if Events.objects.filter(event_url=url).exists():
                #if events exists in database update its time
                # Events.objects.filter(event_url=url).values_list('event_last_update', flat=True).update(event_last_update=timezone.now())
            # else:
                # print("New events")
                #if events doesnt exist in db write event
                # Events.objects.create(event_url=url, event_team_1=team_1, event_team_2=team_2, event_team2_1='none', event_team2_2='none', event_added=timezone.now(), event_sport=sport['sport_name'], event_last_update=timezone.now())
                # print(url)

data_load()