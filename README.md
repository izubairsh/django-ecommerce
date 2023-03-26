# Project Name: Butcher Shop POS System

## Description
This is a Point of Sale (POS) system built using Django framework, with the purpose of helping a butcher shop to manage their sales and inventory. The system allows the shop owner to add, edit and delete products, view sales history, and generate reports. 

## Languages Used
- Python
- JavaScript
- HTML
- CSS
- Bootstrap

## Installation and Setup
1. Clone the repository from GitHub using the following command:
`git clone https://github.com/your_username/butcher_shop_pos.git`

2. Create a virtual environment and activate it:
`python3 -m venv env`
`source env/bin/activate`

3. Install the required dependencies:
`pip install -r requirements.txt`

4. Create the database tables:
`python manage.py migrate`

5. Load sample data (optional):
`python manage.py loaddata fixtures/sample_data.json`

6. Start the development server:
`python manage.py runserver`

7. Open a web browser and navigate to `http://localhost:8000` to access the system.

## Usage
- Login using the credentials provided by the shop owner.
- Use the navigation bar to access the various functionalities of the system, such as adding/editing products, viewing sales history and generating reports.
- The system automatically updates the inventory levels when a sale is made.
- Use the logout button to exit the system.

## License
This project is licensed under the MIT License. See the `LICENSE` file for more information.
