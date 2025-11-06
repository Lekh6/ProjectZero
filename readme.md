# Task Flow

#### Video Demo: https://youtu.be/205YhH4h5WA
## **Description**:

Task Flow is a minimalist productivity app designed for users who want decent control over their tasks at hand and need a tool for them to organize it all. This app combines simplicity and usefulness into one, effortlessly displaying all that the user requires, in the homepage, with further depth accessible, at the tap of a finger.
Including quick notes and statistics along with the usual tasks helps the user gain insight into their tasks at hand through visualization while letting them jot down quick notes and saving for them to view it later, along with the tasks they created. 

Since the app uses an user-account system, each user has their own data which can only be accessed with their passkey, so that the user gains some privacy.

This project was created as part of cs50x's final project requirement, following the course's rules and requirements.

## **Overview**

Personal organization through this app can be achieved using:
1. Task management: Add and update tasks at will to avoid forgetting important goals in real life.
2. Visualization: Gain insight into ur past and present, using visualizations based on ur tasks, helping u understand more about their completion.
3. Quick Notes: Jot down thoughts as soon as they appear in your mind, in the quick notes section of the app, saving them for you to view it later.

Each user gets their own personal spaces, powered by basic and simple SQL-tables in tandem with secure Flask sessions.

## **Technicality**

Core languages used:
1. Flask(python)
2. SQL
3. HTML, CSS, Javascript

## **Core components:**
### **```app.py```**

the website contains seven core routes which are essential in its proper working:

1.``` /login ``` - Authenticates users with the use of hashed passwords powered by Werkzeug.

2.``` /register ``` - Creates a new user and sets up the required tables in the database while assigning the a new session for them.

3.``` / ``` - The main page - the homepage that displays three key elements - pie chart - showing the tasks at hand, a task list and a quick notes field.

4.``` /timeline ``` - Generates a dual-line graph that displays tasks created and done over a specific period of time.

5.``` /notes ``` - Manages note creation and displays notes in reverse chronological order.

6.``` /overview ``` - Categorizes and displays four quadrants that showcase the task category based on the period left to complete them.

7.``` /logout ``` - Clears the session data, and lets another user login safely.


### **Templates:**

#### ```homepage.html```

This file is rendered for the route '/' and serves as the main page for the app, consisting of key elements:
    1. A pie chart, representing three main categories of priority: ['low', 'medium', 'high'], showing the tasks at hand.
    2. A panel in the center, comprising of tasks remaining, in the order of due date first.
    3. A quick notes field on the right, that lets the user jot down notes and save them without hassle.
    4. A Add button(+) at the bottom of the page that lets the user create a new task instantly.
    5. And finally, a sidebar built into all pages of the site, that lets the user navigate through the webpage.

#### ```overview.html```

This file is rendered for the route '/overview' and serves the basic idea of a 'eisenhower matrix' that implements four categories namely:
1. Now- Tasks that are due by today
2. Later - Tasks that are due by the week.
3. Flexible - Task that are due by anytime in a month's time.
4. Indefinite - Tasks that do not have a specific deadline.

#### ```timeline.html```

This page renders a dual-line graph that showcases the task creation and deletion stats over time, customized by a filter at the top of the page. It uses a chart.js for quick and lightweight visualization.

#### ```login.html``` and ```register.html```

These two pages render only for the sake of the user registering and logging into the sites. Doing the task of:
1. Storing credentials.
2. Creating respective tasks and notes tables.
3. Creating sessions to avoid redundant logins.
4. User convenience for organization of tasks anywhere.

#### ```notes.html```

This page renders a simple box layout that contains two elements taking up the screen:
1. The notes field on the left, that lets the user type and format their notes, before saving them and,
2. The panel on the right, that lets the user view what notes they have just saved.

### **Database:**

The backend uses cs50's SQLite3 for storing and accessing of data as such:
For every user registered, two tables are created as:
    
```data_<uid>```
```notes_<uid>```

the tables store key data such as the task title, due date, description, creation data and so on. Same goes with the notes table.
And the total user data for all users, is stored in another table called:
```users```

This table stores data about the various users logged into the website, their usernames, passwords(hashed) and their userid.


#### **UI and design:**

Task Flow's UI features extremely simple and minimalistic gradients of dark red theme showcasing aesthetics such as:

- Dark gradient with a subtle pop of crimson red.

- Blurred backgrounds during menu openings to allow for user focus and UI richness.

- Smooth animations for sidebar opening and task creation.

- Compact and clean layout- Easy to understand.


#### **Future and potential improvements:**

This webapp has a lot of room to grow, allowing for the addition of features such as:

- Analytics Expansion: Showing completion rates and average task durations.
- User preferences: Adding preferences and themes for user customization.
- API integration: Possible using of google calendar's API for effortless flow of task updation.
- Updation and deletion of tasks.


### **Design Choices:**

- Using flask and SQL : I chose to use basic languages such as Flask and SQL in order to acquire knowledge at a base level first.

- Using only html,css and js: Since these are the core of frontend languages, i decided to go ahead with these to get a good foundation knowledge.

- Use of multiple tables: Since this is a small-scale project, i figured the use of seperate tables for users wouldn't hinder my webpage's function.

- Use of sessions: Using sessions to store user-data temporarily and avoiding redundancy in logging in, is what i wanted to achieve.


### **How to run:**

1. **Clone or download the required files through the repository**
    ```bash
    git clone https://github.com/Lekh6/ProjectZero.git
    cd fp

2. **Install dependencies**
    ```bash
    pip install -r requirements.txt

3. **Start the Flask app**
    ```bash
    flask run

4. **Open in browser**
    ```bash
    http://127.0.0.1:5000/




