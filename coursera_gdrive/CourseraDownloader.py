import os,pkg_resources
import io
import time
import subprocess
import sys
from coursera.coursera_dl import get_session

FINISHED_COURSES_FILE = 'finishedCourses.log'
ENROLLED_COURSES_API = 'https://api.coursera.org/api/memberships.v1?includes=courseId,courses.v1&q=me&showHidden=true&filter=current,preEnrolled'
ALL_COURSES_API = 'https://api.coursera.org/api/courses.v1?limit=10000'

DEFAULT_GDRIVE_PATH = '/content/drive/My Drive/'

DEFAULT_SAVE_FOLDER = 'COURSERA'

COURSERA_DL_PARAMETERS = [
                         '--download-delay 0',
                         '--video-resolution 720p',
                         '--about',
                         '--download-notebooks',
                         '--download-quizzes'
                         ]


class CourseraDownloader:
    """
    Downloader Class which makes all process.
    """

    def __init__(self, save_folder=DEFAULT_SAVE_FOLDER):

        try:
            from google.colab import drive
            drive.mount('/content/drive')
            self._checkGoogleDrive(save_folder)
            self._inColab = True
        except ModuleNotFoundError:
            print("You have to use Google Colab!")
            self._inColab = False


        self._debug = False
        self._loginFlag = False
        self._totalCourses = 0
        self._totalEnrolled = 0
        self._subtitleLangs = "all"
        self.cauth = ""
        self.savePath = DEFAULT_GDRIVE_PATH + DEFAULT_SAVE_FOLDER
        self.enrolledCoursesList = {}
        self.allCoursesList = {}

        library_package = __name__
        library_path = '/'.join(('lib', 'language_codes.csv'))

        with pkg_resources.resource_stream(library_package, library_path) as langList:
            self._langList = langList.read().decode("utf8").splitlines()[1:]
            self._langList = {lang.split(",")[0]: lang.split(",")[1][:] for lang in self._langList}

    def __str__(self):
        rowLen = 80
        currentConfigs = "="*rowLen + "\n"
        currentConfigs += "| Current Configs :".ljust(rowLen-1) +"|"+"\n"
        currentConfigs += "|"+"="* (rowLen-2) + "|\n"

        if(len(self.cauth) > rowLen - 14):
            currentConfigs += "| 1) CAUTH: {}...".format(self.cauth[0:rowLen-17]).ljust(rowLen - 1) + "|" + "\n"
        else:
            currentConfigs += "| 1) CAUTH: {}".format(self.cauth).ljust(rowLen-1) +"|"+"\n"

        currentConfigs += "|"+"-"* (rowLen-2) + "|\n"
        currentConfigs += "| 2) SAVE PATH: {}".format(self.savePath).ljust(rowLen-1) +"|"+"\n"
        currentConfigs += "|"+"-"* (rowLen-2) + "|\n"
        currentConfigs += "| 3) TOTAL ENROLLED COURSES: {}".format(self._totalEnrolled).ljust(rowLen-1) +"|"+"\n"
        currentConfigs += "|"+"-"* (rowLen-2) + "|\n"
        currentConfigs += "| 4) TOTAL COURSERA COURSES: {}".format(self._totalCourses).ljust(rowLen-1) +"|"+"\n"
        currentConfigs += "="*rowLen + "\n"

        return currentConfigs

    def _checkGoogleDrive(self, save_folder):
        """
        Checks if Google Drive is mounted properly.

        @param  : args: Gets Save Folder <class 'str'>
        @return : None
        """

        if os.path.exists(DEFAULT_GDRIVE_PATH):
            print("Google Drive is mounted successfully.")
            os.chdir(DEFAULT_GDRIVE_PATH)

            if save_folder.endswith("/"):
                save_folder = save_folder[:-1]

            if save_folder.startswith("/"):
                save_folder = save_folder[1:]

            self.savePath = DEFAULT_GDRIVE_PATH + save_folder

            if os.path.exists(self.savePath):
                print("Folder is found.")
                os.chdir(save_folder)
            else:
                print("{} is created.".format(save_folder))
                cmd = "mkdir -p {}".format(save_folder)
                os.system(cmd)
                os.chdir(save_folder)

            print("Ready to Login. Use login() method.")

        else:
            print("There is a problem. Please try again.")

    def setSubtitles(self,*args,commonAlternative = "en"):
        """
        Sets the subtitle choice.

        @param  : args: Gets Subtitle Language List <class 'str'>
        @return : None
        """

        if len(args) != 0: # Check if there is any argument is given.
            self._subtitleLangs = ""
            print("SUBTITLE LANGUAGE(S):")
            for lang in args:

                if ("|" not in lang) and lang != commonAlternative:
                    lang+="|"+commonAlternative


                if lang.split("|")[0] in self._langList.keys():
                    print(" - {} is added.".format(self._langList[lang.split("|")[0]]))
                else:
                    print(" - Unknown language is added. ({})".format(lang.split("|")[0]))

                self._subtitleLangs+=lang+","

            self._subtitleLangs = self._subtitleLangs[:-1] # Discard the last comma.

            print("Common alternative language is ",end="")
            if commonAlternative in self._langList.keys():
                print(self._langList[commonAlternative]+".")
            else:
                print("unknown. ({})".format(commonAlternative))


    def showLanguages(self):
        """
        Gives the list of 2 character language codes of some widely used languages.
        There may be other codes that is used in Coursera.
        To learn more, https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes

        @param  : None
        @return : None
        """

        print("========================")
        print(" List of Language Codes ")
        print("========================")

        for num,lang in enumerate(self._langList):
            print(str(num+1)+") "+lang+" | "+self._langList[lang])


    def login(self, cauth):
        """
        Login function creates an authorized TLS session.

        @param  : args: It takes CAUTH <class 'str'> Token to make user authorized.
        @return : <class 'bool'> which indicates to success of the process.
        """
        if (not self._inColab) and (not self._debug):
            return False

        self.cauth = cauth
        self.session = get_session()
        self.session.cookies.set('CAUTH', self.cauth)

        if (self._enrolledCourses()):
            print("=" * 100)
            print("You have enrolled {} course.".format(self._totalEnrolled))
            print("If you want to see enrolled courses call printEnrolledCourses() method!\n")
            self._loginFlag = True
            self._allCourses()
            print("Coursera has {} courses now.".format(self._totalCourses))
            print("If you want to see all courses call printAllCourses() method!")
            print("=" * 100, end="\n\n")

        else:
            print("Login Error!")
            self._loginFlag = False

    def _enrolledCourses(self):
        """
        Finds all enrolled courses in Coursera and adds them to Dictionary.

        @param  : args: None
        @return : <class 'bool'> which indicates success of process.
        """

        response = self.session.get(ENROLLED_COURSES_API)
        if (response.status_code != 200):
            return False

        json = response.json()
        enrolledCoursesList = json['linked']['courses.v1']
        self._totalEnrolled = json["paging"]["total"]
        enrolledCoursesList = [(course["slug"], course["name"]) for course in enrolledCoursesList]
        enrolledCoursesList.sort(key=lambda tup: tup[0])

        self.enrolledCoursesList = dict(enrolledCoursesList)

        return True

    def _allCourses(self):
        """
        Finds all courses in Coursera and adds them to Dictionary.

        @param  : args: None
        @return : <class 'bool'> which indicates to success of the process.
        """

        if (not self._loginFlag) and (not self._debug):
            return False

        response = self.session.get(ALL_COURSES_API)
        if (response.status_code != 200):
            return False

        allCoursesList = response.json()["elements"]
        self._totalCourses = len(allCoursesList)
        allCoursesList = [(course["slug"], course["name"]) for course in allCoursesList]
        allCoursesList.sort(key=lambda tup: tup[0])
        self.allCoursesList = dict(allCoursesList)

        return True


    def download(self, *args):
        """
        Downloads all requested classes and checks if they are exist and properly authorized.

        @param  : args: It can be multiple list, course names, a single course name or empty.
        @return : <class 'bool'> which indicates to success of the process.
        """

        if (not self._loginFlag) and (not self._debug):
            return False

        if len(args) == 0:
            self._downloadList = self.enrolledCoursesList.keys()

        else:
            self._downloadList = []
            for arg_index,arg in enumerate(args):

                if type(arg) == list:
                    print("Argument {} : Checking list.".format(arg_index+1))
                    self._checkCourseExist(arg)

                elif type(arg) == str:
                    if ".txt" in arg:

                        try:
                            coursesListFile = open(arg, "r")
                            courseList = coursesListFile.read().splitlines()
                            coursesListFile.close()
                            print("Argument {} : {} file opened:".format(arg_index+1, arg))
                            self._checkCourseExist(courseList)

                        except FileNotFoundError:
                            print("Argument {} : {} file does not exist!".format(arg_index+1, arg))
                            continue
                    else:

                        print("Argument {} : Checking existence.".format(arg_index+1))
                        self._checkCourseExist(arg)

                else:
                    print("Wrong Parameter Type: {}".format(type(arg)))
                    return False

            self._downloadList.sort()

        self._startDownload()

    def _settings(self):
        
        """
        Make configs to coursera-dl.conf file.

        @param  : None
        @return : None
        """
        
        with open('coursera-dl.conf', "w") as configFile:
            for config in COURSERA_DL_PARAMETERS:
                configFile.write(config)
                configFile.write("\n")

            configFile.write("--cauth ")
            configFile.write(self.cauth)


    def _checkCourseExist(self, course_names):
        """
        Checks if the course exists in Coursera to make sure that there is not any wrong course name in the download queue.

        @param  : args: Course names list or Course names.
        @return : <class 'bool'> which indicates to success of the process.
        """

        if type(course_names) == list:
            for course in course_names:
                if course in self.allCoursesList.keys():
                    print("- [{}] is added to download queue.".format(course))
                    self._downloadList.append(course)
                else:
                    print("- [{}] Wrong course id.".format(course))

        elif type(course_names) == str:
            if course_names in self.allCoursesList.keys():
                print("- [{}] is added to download queue.".format(course_names))
                self._downloadList.append(course_names)
            else:
                print("- [{}] Wrong course id.".format(course_names))

        else:
            print("Wrong Parameter Type: {}".format(type(course_names)))
            return False

    def _startDownload(self):

        """
        Starts download process.

        @param  : None
        @return : None
        """

        self._settings()  # Creates Coursera-dl Configs.

        try:
            with open(FINISHED_COURSES_FILE, 'r') as finishedCoursesLog:
                self.finishedCourses = finishedCoursesLog.read().splitlines()

            self.finishedCoursesLog = open(FINISHED_COURSES_FILE, "a")

        except FileNotFoundError:
            self.finishedCoursesLog = open(FINISHED_COURSES_FILE, 'w')
            self.finishedCourses = []


        try:
            downloadQueue = list(set(self._downloadList) - set(self.finishedCourses))  # Finds undownloaded courses.
            downloadQueue.sort()

            if len(downloadQueue) == 0:
                print("=" * 100)
                print("All Courses is already downloaded.".center(100), )
                print("=" * 100)
                self.finishedCoursesLog.close()
                return False

            for course_name in downloadQueue:
                print("=" * 100)
                courseLog = '{}.log'.format(course_name)

                with io.open(courseLog, 'wb') as writer, io.open(courseLog, 'rb', 1) as reader:
                    process = subprocess.Popen(['coursera-dl', course_name,"-sl",self._subtitleLangs], stderr=writer)

                    while process.poll() is None:
                        sys.stdout.write(reader.read().decode('utf-8'))
                        time.sleep(0.1)

                    sys.stdout.write(reader.read().decode('utf-8'))

                self.finishedCoursesLog.write(course_name)
                self.finishedCoursesLog.write("\n")

            self.finishedCoursesLog.close()

            print("=" * 100)
            print("Downloading is done!".center(100))
            print("=" * 100)
            return True

        except KeyboardInterrupt:
            self.finishedCoursesLog.close()
            print("=" * 100)
            print("Downloader is paused.".center(100))
            print("=" * 100)

        except:
            print("=" * 100)
            print("There is an unexpected error! Please report it. [https://github.com/kaanaritr/Coursera-GDrive]".center(100))
            print("=" * 100)


    def printEnrolledCourses(self):
        """
        Prints all enrolled courses in Coursera.

        @param  : args: None
        @return : None
        """
        if (not self._inColab) and (not self._debug):
            return False

        if self._loginFlag:
            seq = 1
            print("=" * 100)
            for slug, name in self.enrolledCoursesList.items():
                print("{}) {} : {}".format(seq, slug, name))
                seq += 1
            print("=" * 100)
            print("{} enrolled course listed.".format(self._totalEnrolled).center(100))
            print("=" * 100, end="\n\n")

        else:
            print("You must login first!\n")

    def printAllCourses(self):
        """
        Prints all available courses in Coursera.

        @param  : args: None
        @return : None
        """

        if (not self._inColab) and (not self._debug):
            return False

        if self._loginFlag and self._totalCourses != 0:
            seq = 1
            print("=" * 100)
            for slug, name in self.allCoursesList.items():
                print("{}) {} : {}".format(seq, slug, name))
                seq += 1
            print("=" * 100)
            print("{} course listed.".format(self._totalCourses).center(100))
            print("=" * 100, end="\n\n")

        else:
            print("You must login first!\n")