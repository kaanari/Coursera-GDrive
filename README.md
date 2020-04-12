
# Coursera Google Drive Downloader via Google Colab
[![PyPI](https://img.shields.io/pypi/v/coursera-GDrive?color=brightgreen)](https://pypi.org/project/coursera-GDrive)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/kaanaritr/Coursera-GDrive/issues)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/kaanaritr/Coursera-GDrive.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/kaanaritr/Coursera-GDrive/context:python)

This small project is helpful for downloading Coursera courses into your Google Drive via Google Colab. You can use it with given instruction below or given [Jupyter Notebook](https://github.com/kaanaritr/Coursera-GDrive/blob/master/extras/EasyDownloader.ipynb) file easily.
This module makes it easier to mount your google drive and download all enrolled courses from Coursera. 

All enrolled courses can be downloaded by the methods given below,(For more detailed explanations, see the section ''Usage''.)
* Calling download() function,
* Making a list that includes the course names,
* Reading from a text file that contains the course names,

## Getting Started
An overview of CGDD via Google Colab,how to download and use,some basic tips ,explanations and more.

### Prerequisites
- Coursera-dl Package ( version>=0.11.0 )
- You have to use [Google Colab](https://colab.research.google.com/). 
- If you have never experienced it , then I strongly recommend you to use this powerful and free platform.


### Installing

You can download it by using the command below in your terminal.

```
pip install Coursera-GDrive
```


## Usage

### How to use this package without writing code?

If you don't want to waste your time to read this documentation, then just download [Jupyter Notebook](https://github.com/kaanaritr/Coursera-GDrive/blob/master/extras/EasyDownloader.ipynb) file, follow the instructions in the given file and run it on your Google Colab.

### If you want to use this package by writing your own code;

First of all, you have to know the basics of Python to understand the given instructions below.

### Initializing

- #### Initialize the downloader object with default save folder (COURSERA).
	```
	downloader = CourseraDownloader() 
	```
- #### Initialize the downloader object with save folder <folder-name> in your Google Drive.
  - If downloader can't find given folder, it will automatically creates itself.

  ```
  downloader = CourseraDownloader(<folder-name>)

  # Example:
  # downloader = CourseraDownloader("coursera_files")
  ```

### Authentication and Authorization

Before we go further, we must authenticate ourselves first. For that purpose, we need to CAUTH token which is using for one of the main authentication method by Coursera.

- #### How to find your Coursera CAUTH token by using your browser?
	1. First login to `coursera.org` in your web browser :  
	1. For example, in chrome, Go to settings
	1. Advanced
	1. Privacy and Security
	1. Site Settings
	1. Cookies and Site Data
	1. See all cookies and site data
	1. coursera.org -> **CAUTH**
	1. Copy the content and Paste to **\<cauth-token>**
	

	```
	cauth = <cauth-token>

	# Example:
	# cauth = "t-w_itR2tML6ZWA_myKtQeC0JO97SJFkh3PgatWw32t4nrlZrHKsfe2sw"
	```
- #### How to login with your CAUTH Token?

	```
	downloader.login(cauth)
	```
### Courses Lists
Last one step before download, if you want to see some useful courses list, you have to read this section.

- #### How to see all enrolled Courses?

	```
	downloader.printEnrolledCourses() 
	# Prints all enrolled Courses.
	```
- #### How to see all available courses in Coursera?

	```
	downloader.printAllCourses() 
	# Prints all courses in Coursera.
	```

### Downloading the Courses

- ### How to download all of my enrolled course?
	It's very straight forward. Just call the download method.
	```
	downloader.download()
	# Downloads all enrolled courses.
	```
- ### How to download just one course?
	Make sure that the class name you are using corresponds to the resource name used in the URL for that class:
	 `https://www.coursera.org/learn/<course-name>/home/welcome`
	 
	**Example:**
	`https://www.coursera.org/learn/`**algorithmic-toolbox**`/home/welcome`

	```
	downloader.download("<course-name>") 
	# Downloads just <course-name>.

	# Example:
	# downloader.download("algorithmic-toolbox")
	```
- ### How to download one or more course?
	There are several methods to download multiple courses easily.
	- #### Multiple Course String Argument
	```
	downloader.download("<course1>","<course2>","<course3>",...) 
	# Downloads all the given courses.

	# Example:
	# downloader.download("algorithmic-toolbox","crypto","iot","python-ar")
	```
	- #### Python List Argument
	```
	course_list = ["<course1>","<course2>","<course3>",...]
	downloader.download(course_list) 
	# Downloads all courses in python list.

	# Example:
	# course_list = ["algorithmic-toolbox","crypto","iot","python-ar"]
	# downloader.download(course_list)
	```
	- #### Passing a text file as an argument
	Make sure that,
	1. Course names in text file are separated by a newline.
	2. Text file is in the save folder. ( Default: COURSERA )
	```
	downloader.download("<courselist.txt>") 
	# Downloads all courses in text file.

	# Example:
	# downloader.download("course_list.txt")
	```

	- #### Passing mixed arguments
	```
	course_list = ["<course-x>","<course-y>","<course-z>",...]
	downloader.download("<course1>","<course2>","<course3>","<courselist.txt>",course_list) 
	# Downloads all the given courses, courses in text file and courses in python list.
	```




## Built With

* [Python 3](https://www.python.org/) 
* [Google Colab](https://colab.research.google.com/) 

## Contributing

Please read [CONTRIBUTING.md](https://github.com/kaanaritr/Coursera-GDrive/blob/master/CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Authors

* 👤**Kaan ARI**  - [kaanaritr](https://github.com/kaanaritr)
 * 👤**Ayşe İDMAN**  - [viorq](https://github.com/viorq)


See also the list of [contributors](https://github.com/kaanaritr/Coursera-GDrive/graphs/contributors) who are participated in this project.

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](https://github.com/kaanaritr/Coursera-GDrive/blob/master/LICENSE) file for details.

## Acknowledgments

* Thanks to [Coursera Download](https://github.com/coursera-dl/coursera-dl) project for letting me to make this project real.
