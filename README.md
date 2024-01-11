<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/AnhHuy007/MailBox">
    <img src="demoImg/icon.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">MailBox app</h3>

  <p align="center">
    This app sends and recieves email through SMPT and POP3 protocol !!!
    <br />
  </p>
</div>


## About The Project

![MailBox app!](/demoImg/main.png "Main screen")

MailBox is an app for send and recieve email by SMTP (Simple Mail Transfer Protocol) and POP3 (Post Office Protocol 3). This app serves educational purpose only.

## Credit
We would like to extend our sincere thanks to the creators of the server jar file used in this app. The server jar file is sourced from the [Test-mail-server](https://github.com/eugenehr/test-mail-server) on GitHub. We are committed to honoring the open-source licensing terms and providing proper credit to the original creators.


### Built With

* [![Python][Python.js]][Python-url]



<!-- GETTING STARTED -->

## Getting Started

### Prerequisites
1. Java version 8

The server is suitable for older version of java and java 8 is recommended,
Install Java 8 from [this link](https://www.java.com/download/ie_manual.jsp "Java download link").

### Installation

1. Clone the repo
    ```sh
    git clone https://github.com/anhhuy007/MailBox.git
    ```
    

<!-- USAGE EXAMPLES -->

## Usage

1. Navigate to the project folder
2. Run the server .jar file by open terminal and enter this code
	```
	java-jar test-mail-server-1.0.jar -s 2225 -p 3335 -m./
	```
 
 If there is more than one java version in your computer, enter the path leads to java file in folder bin of java version 8, for example

	"C:\Program Files\Java\jdk-1.8\bin\java" -jar test-mail-server-1.0.jar -s 2225 -p 3335 -m ./

 
 3. Run the mail.py file in the project to start
 4. App automatically logins with default mail, you can change the mail by click in the avatar at top right corner to sign out
![Sign Out Screen](/demoImg/signout.png "Sign Out screen")
 5. After sign out, the app will close. We run file mail.py again and login screen appear (any password)
![Login Screen](/demoImg/login.png "Login screen")



<!-- CONTACT -->

## Contact

Anh Huy Huynh - [@anhhuy007](https://twitter.com/anhhuy007) - imanhhuy007@gmail.com

Project Link: [https://github.com/anhhuy007/MailBox](https://github.com/anhhuy007/MailBox)






[Python.js]: https://img.shields.io/badge/python-ffff00?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/
