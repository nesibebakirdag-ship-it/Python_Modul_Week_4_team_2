# Python_Modul_Week_4

# Library Project
- In this project, we want you to write a library program using the Python information you have learned so far, error catching - file operations, especially the Json module and file information.
- In a library; There are two main parts: Membership transactions and Book transactions.
- Membership transactions include information on adding a member, deleting a member, checking a member, giving a book to a member, and receiving a returned book from a member. A database or file where membership data is recorded is also required.
- We can say similar things about book transactions.

#### To detail the project:
 * It will consist of main.py, Kitap_transactions.py, Member_Transactions.py, Zaman.py files.
##### Main.py:
* The main file of our project will be the main.py file. Operations will be executed from this file, other Python files will be called from this section as a module. For example, adding a book, deleting a book, adding a member, giving a book to a member, and member control will be done here.

![image](https://github.com/user-attachments/assets/a27bdecd-d799-4868-8241-cd559c560747)

 

* Below you will see a run output of this project. You can run the functions in the book_transactions and membership_transactions modules via inputs on the main page.




##### book_transactions.py :
* In this module, you will write book information (registered books and total number), add, delete, search and update functions. We will save our data in the book.json file. The Kitap.json file will be given to you (you can create it yourself if you wish). File control must be done with the Os Module. Below you can find function examples for book transactions, but you do not have to follow them, you can make your own planning.

 ![image](https://github.com/werhereitacademy/week_4/assets/141542413/753abd94-38de-417e-afd8-0540ba8aa591)

* There is a lot of data in the Kitap.json file. We will work with the following data. We will use these as basis when adding new data or searching.

 ![image](https://github.com/werhereitacademy/week_4/assets/141542413/ff5f0b47-5244-4b58-b8ae-7c5dff092a73)

##### Book.json :
sample output is as follows

![image](https://github.com/werhereitacademy/week_4/assets/141542413/caaecfd5-db10-4bc7-985b-0f1a4fb208d4)

##### Membership_transactions.py:
* Here, operations such as member information (member names and total number of members), member updating, adding members, searching for members, deleting members, lending books and returning books will be performed. Additionally, members must be saved in the uye.Json file. When lending a book, it is absolutely
* - The date and time the book was lent and the date to return it after 2 weeks should be added and this information should be saved in the taksi.json file.

![image](https://github.com/werhereitacademy/week_4/assets/141542413/6728d7fa-2aa2-49a8-b843-cccd9a397311)

* We will do this from the py module when we create it ourselves.
* - After being saved in the taksi.json file, the loaned book should be deleted from Kitap.json so that it does not appear when someone else wants to buy it.
##### Note: You will create the user.json and tracking.json file yourself.

![image](https://github.com/werhereitacademy/week_4/assets/141542413/49f04d87-bece-4493-b62f-022cfa3d9201)

* The data you will save to Uye.json should be as follows:

 ![image](https://github.com/werhereitacademy/week_4/assets/141542413/8761111e-11f6-47ba-9605-cc8b33be84b3)

##### time.py :
* We lend our books to our members for 2 weeks. Therefore, we will record the time and date of the loan and the date when it should be returned, thanks to this module.
When we run this module, we want it to return the current time and the time 2 weeks later.

![image](https://github.com/werhereitacademy/week_4/assets/141542413/7a7c7274-32ef-42e9-b3c7-9d2094752893)

##### The data you will save in tracking.json should be as follows:

![image](https://github.com/werhereitacademy/week_4/assets/141542413/3948f87d-bf87-49a6-a9d6-75bcdf155afd)

## Hackerrank Questions

1. Diagonal Difference: https://www.hackerrank.com/challenges/diagonal-difference/problem

2. Left Rotation: https://www.hackerrank.com/challenges/array-left-rotation/problem

3. Counter game: https://www.hackerrank.com/challenges/counter-game/problem

4. Time Delta: https://www.hackerrank.com/challenges/python-time-delta/problem
