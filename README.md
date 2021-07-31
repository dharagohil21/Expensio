# Expensio (Online Expense Management Platform)

The aim of Expensio is to promote better financial planning by providing users an easy-touse platform that makes expense tracking easier and non-frustrating. Expensio will enable users to categorize their incomes and expenses so that they can identify the expenses that they can cut down on. Apart from the monthly reports Expensio also provide interactive visualizations that will provide users with a better understanding of the cash flow.
<br/>
This project is the backend of the expensio-platform.

-   _Date Created_: 07 JUNE 2021
-   _Last Modification Date_: 31 JULY 2021
-   _URL_: [GitLab] <https://git.cs.dal.ca/rushikesh/group16-5709-project.git>
-   _Frontend URL_: [Heroku] <https://expensio-app.herokuapp.com/>
-   _Backend URL_: [Heroku] <https://expensio-app.herokuapp.com/>

## Authors

-   [Nachiket Niranjanbhai Panchal](mailto:nc784795@dal.ca) - _(Full-stack developer)_
-   [Rushikesh Patel](mailto:rushikesh.patel@dal.ca) - _(Full-stack developer)_
-   [Jaspreet Kaur Gill](mailto:js523380@dal.ca) - _(Full-stack developer)_
-   [Sravani Pinninti](mailto:sravani.pinninti@dal.ca) - _(Full-stack developer)_
-   [Dharaben Thakorbhai Gohil](mailto:dh447205@dal.ca) - _(Full-stack developer)_

## Getting Started

### Prerequisites

```
- Python 3.8.x
```

### Installing

Here are some steps which will help you to install and run application in your local machine.

```
1. Install pip - [Installation - pip documentation v21.1.2](https://pip.pypa.io/en/stable/installing/)
2. Install [virtualenv](https://pypi.org/project/virtualenv/) - `pip install virtualenv`
3. Install [Git](https://git-scm.com/)
4. Clone the project `git clone https://git.cs.dal.ca/rushikesh/group16_expensio`
5. `cd group16_expensio`
6. Setup python virtualenv - `virtualenv --python=python38 env`
7. Activate virtualenv
    *nix -`env/bin/activate`
    windows - `.\env\Scripts\Activate`
8. Install application dependencies - `pip install -r requirements`
9. Run application - `flask run`
```

## Deployment

To deploy the project on heroku:

1. Signup on [Heroku](https://www.heroku.com/)
2. Create a new app. Note the git url from Settings tab of the application.
3. Install [Heroku Cli](https://devcenter.heroku.com/articles/heroku-cli)
4. Login into Heroku cli - `heroku login`
5. Add the heroku git url as a remote in your project - `git remote add heroku <heroku-app-git-url>`
6. Deploy - `git push heroku master`
