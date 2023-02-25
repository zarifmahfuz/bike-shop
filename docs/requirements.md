# Intro
I started off the project by brainstorming and compiling a list of fundamental requirements for the bike shop app. To make my life easier, I made a few assumptions before coming up with the requirements. The assumptions and requirements are specified below.

## Assumptions 
* There is only one actor of the system - the store admin.
* This is meant to be used as an internal tool for a single bike shop. As a result, the system represents one bike shop.
* The requirement “The admin of the store would like to be able to populate the database through the system. As any other sales system, it should allow sales to be entered manually.” tells me that the store admin would like to manually record sales transactions of the bikes through this system for bookkeeping purposes. This means that the system is essentially an accounting tool.
* All sales entered will be in the Canadian Dollars currency.

## Requirements Specification
### Bikes
* Ability for the admin to add new bikes to the database, including bike details such as name, model, price, and stock levels.
* Ability to add images for each bike.
* Ability to view and update existing bike records.
* Ability to view the list of all bikes and search for bikes by their name/model.

### Sales
* Ability to manually enter sales transactions for bikes, including customer information and payment details.
* Ability to view and edit existing sales transactions, including refunding a sales transaction.
* Ability to delete a sales transaction.
* Ability to apply discounts to sales transactions based on criteria such as total purchase amount.
* Ability to add multiple bikes in a single sales transaction.
* Ability to view the list of previous sales

### Analytics
* Ability to view sales trends over time
* Ability to view lifetime sales statistics
* Ability to see the top selling bikes

### User Management [Not Implemented]
* Ability to create and manage users and their roles and permissions.
* Ability to assign sales transactions to individual salespeople.
* Ability to track user activity and auditing.
