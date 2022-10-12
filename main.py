import credentials
from firebaseController import pushData
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

    nf_computer = LearningPlatform(url=login_url)
    
    isLogin = nf_computer.login(username=username, password=password)
    if isLogin:
        name = nf_computer.get_user_name()
        print("Selamat Datang " + name + "\n")

        print("[+] Mencoba mengekstrak data")
        tasks = nf_computer.get_tasks(list_course_dict=list_course_dict)
        print("[+] Melakukan push data")
        pushData(tasks=tasks)
        print("[+] Push data selesai")
    else: 
        print("[-] Maaf, terjadi kesalahan saat login")

if __name__ == "__main__":
    main()
