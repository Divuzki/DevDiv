# DevDiv News

## Overview

Welcome to DevDiv, a cutting-edge and innovative news aggregation platform. DevDiv is designed to scrape headlines from various sources, clean the data, and store it in a database. Users can also post their own news articles, which are clearly identified as user-generated content. With DevDiv, stay informed with curated news content while enabling users to contribute their own stories.

## Features

- **Headline Scraping**: DevDiv automatically scrapes headlines from various sources, ensuring a wide range of news coverage.
- **Data Cleaning**: The scraped data is meticulously cleaned to provide accurate and reliable information.
- **User News Submission**: Users can post their own news articles, allowing for community-driven content.
- **Database Storage**: All scraped and user-generated content is securely stored in a database for easy access and retrieval.

## Installation

To install and run DevDiv, follow these steps:
#### 1. Clone the repository: 
```
git clone https://github.com/Divuzki/DevDiv-A-Web-News-Complex-Scraper.git
```

#### 2. Creating a Python Environment with virtualenv (Optional)

In DevDiv, we provide optional steps to create a Python environment using virtualenv. A virtual environment helps isolate project dependencies and ensures consistent package installations across different projects. If you prefer to use virtualenv, follow the steps below:

1. Install virtualenv, if it's not already installed:
   ```
   pip install virtualenv
   ```

2. Create a new virtual environment:
   ```
   virtualenv env
   ```

3. Activate the virtual environment:
   - For Windows:
     ```
     .\env\Scripts\activate
     ```
   - For macOS/Linux:
     ```
     source env/bin/activate
     ```

   You should see the virtual environment's name in your terminal prompt.

4. Install project dependencies:
   ```
   pip install -r requirements.txt
   ```

Now you have a Python environment set up with virtualenv, and you can proceed with running and developing the DevDiv project.

Note: Using virtualenv is completely optional. If you prefer to install project dependencies globally or use an alternative method, feel free to skip these steps.

If you decide not to use virtualenv, make sure you have the necessary dependencies installed globally to run the DevDiv project.

---

By following these optional steps, you can create a dedicated Python environment using virtualenv to manage your project's dependencies. However, remember that using virtualenv is not a requirement, and you are free to choose an alternative approach based on your preference or project needs.

#### 3. Install dependencies: 
```
pip install -r requirements.txt
```
#### 4. Apply database migrations: 
```
python manage.py migrate
```
#### 5. Start the development server: 
```
python manage.py runserver
```

## Usage

Once DevDiv is installed and running, you can:

1. Browse and read the latest scraped news headlines.
2. Post your own news articles and contribute to the platform.
3. Search for specific news topics or keywords.
4. Interact with user-generated content through comments or upvotes.

## Technologies Used

- Django: A powerful Python web framework for building the backend of the application.
- BeautifulSoup: Used for web scraping and extracting data from HTML.
- PostgreSQL: A robust and reliable database management system.
- Bootstrap: A popular CSS framework for responsive and appealing user interfaces.

## License

DevDiv is released under the MIT License. For more details, please see the [LICENSE](https://github.com/Divuzki/DevDiv/blob/master/LICENSE) file.

## Contact

For any inquiries or questions, please reach out to me at divuzki@gmail.com.

---

Thank you for your interest in DevDiv. I hope this platform brings you valuable news content while fostering a community of knowledge sharing. Happy reading and contributing!
