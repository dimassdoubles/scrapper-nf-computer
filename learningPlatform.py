from httplib2 import Credentials
import requests
from bs4 import BeautifulSoup
import warnings
import credentials

warnings.filterwarnings("ignore")

class LearningPlatform:  
    def __init__(self, url):
        self.__url = url
        self.__session = requests.Session()
        self.__user_id = ""

    def __navigate_to_dashborad(self):
        dashboard_url = self.__url + "my/"
        response = self.__session.get(dashboard_url, verify=False)
    
    def get_user_name(self):
        url_profile_page = self.__url + "user/profile.php?id=" + self.__user_id
        response = self.__session.get(url_profile_page, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")

        # format name is = {name}: Public Profile
        # we just split string with :
        return soup.title.text.split(":")[0]

    def login(self, username, password):
        login_url = self.__url + "login/index.php"

        response = self.__session.get(url=self.__url, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # get logintoken
        login_token = soup.find("input", {"name": "logintoken"}).get("value")

        body_request_parameter = { "anchor": "", 
                                   "logintoken": login_token, 
                                   "username": username, 
                                   "password": password,
                                  }
        
        # login
        try:
            # get user id
            login_response = self.__session.post(login_url, data=body_request_parameter)
            login_soup = BeautifulSoup(login_response.text, "html.parser")
            user_id = login_soup.find("div", {"data-userid": True}).get("data-userid")
            
            if user_id is None:
                return False
            self.__user_id = user_id
            return True
        except:
            return False

    # format course dict
    # {"id": "151", "name": "databse"}
    def get_tasks(self, list_course_dict):
        # should return list of dict with this format:
        # [{"id": "{course_id}+{task_id}", "title": "Mini Project", "type": "quiz", "description": "..."}]
        result = []
        
        url_base_course_page = self.__url + "course/view.php?id=" # will be add course id later
        url_base_assign_page = self.__url + "mod/assign/view.php?id=" # will be add task id later

        for course in list_course_dict:
            course_id = course["id"]
            url_course_page = url_base_course_page + course_id
            response = self.__session.get(url_course_page)
            soup = BeautifulSoup(response.text, "html.parser")

            # get quizes
            quizes = soup.find_all("li", {"class": "modtype_quiz"})
            for quiz in quizes:
                quiz_id = quiz.get("id").split("-")[-1]
                new_task = {
                    "id": course_id+quiz_id,
                    "title": course["name"] + " - " + quiz.text.split("\n")[0].split("Quiz")[0],
                    "type": "quiz",
                    "deadline": "",
                    "description": "",
                }
                result.append(new_task)


            # get assignment
            assignments = soup.find_all("li", {"class": "modtype_assign"})
            for assignment in assignments:
                assignment_id = assignment.get("id").split("-")[-1]
                url_assign_page = url_base_assign_page + assignment_id
                assignment_response = self.__session.get(url_assign_page)
                assignment_soup = BeautifulSoup(assignment_response.text, "html.parser")
                assignment_title = assignment_soup.find("h2", {"class": "ccnMdlHeading"}).text
                assignment_deadline = assignment_soup.find("div", {"data-region": "activity-dates"}).text.split("Due: ")[-1].split("\n")[0]
                assignment_description = assignment_soup.find("div", {"id": "intro"}).text

                new_task = {
                    "id": course_id+assignment_id,
                    "title": course["name"] + " - " + assignment_title,
                    "type": "assignment",
                    "deadline": assignment_deadline,
                    "description": assignment_description,
                }

                result.append(new_task)


        return result
