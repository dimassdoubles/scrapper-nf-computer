from asyncio import current_task
import json
import credentials
from firebaseController import FirebaseController, pushData
from learningPlatform import LearningPlatform

def main():
    # format url must "https://blablabla/"
    login_url = "https://learn.nurulfikri.com/"
    list_course_dict = [
        {"id": "152", "name": "Soft Skill"},
        {"id": "126", "name": "Daspro"},
        {"id": "127", "name": "Database"},
        {"id": "129", "name": "Code Versioning"},
        {"id": "119", "name": "UI/UX"},
        {"id": "128", "name": "Design Pattern"},
        {"id": "153", "name": "Orientation Class"},
        {"id": "130", "name": "Pemrograman Mobile"},
        {"id": "131", "name": "Final Project"},
    ]

    username = credentials.username
    password = credentials.password
    collection = "tasks"
    nf_computer = LearningPlatform(url=login_url)
    firebase_controller = FirebaseController(collection=collection)
    
    isLogin = nf_computer.login(username=username, password=password)
    if isLogin:
        name = nf_computer.get_user_name()
        print("Welcome Datang " + name + "\n")

        print("[+] Try to extract data from website")
        new_tasks = nf_computer.get_tasks(list_course_dict=list_course_dict)

        print("[+] Cek if there is new task")
        with open("tasks.json") as file:
            json_object =json.load(file)

        current_tasks = json_object["data"]

        print(f"    - Current tasks length   : {len(current_tasks)} tasks")
        print(f"    - Extracted tasks length : {len(new_tasks)} tasks")

        if len(current_tasks) != len(new_tasks):
            print("[+] Try to push data to firestore")
            firebase_controller.push_tasks(new_tasks)
            print("[+] Transaction completed")
        else:
            print("[+] There is no new task, transaction completed")
    else: 
        print("[-] Sorry, there is a problem when login")
    
    print("")

if __name__ == "__main__":
    main()
