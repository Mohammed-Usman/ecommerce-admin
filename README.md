# E-commerce Admin API

The E-commerce Admin API is a backend service that powers the web admin dashboard for e-commerce managers. It provides features for managing sales data, revenue analysis, inventory, and more.

## Getting Started

Follow these instructions to set up and run the E-commerce Admin API locally.

### Prerequisites

Before you begin, ensure you have the following dependencies installed:

- [Python](https://www.python.org/) (version 3.7 or higher)
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [MySQL](https://www.mysql.com/) or another supported relational database

### Installation
1. Create Database:
 
   ```
   CREATE DATABASE IF NOT EXISTS ecommerce;

   ```

2. Clone the repository:

   ```bash
   git clone https://github.com/Mohammed-Usman/ecommerce-admin.git
   cd ecommerce-admin

   python -m venv venv 
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

   pip install -r requirements.txt
   
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    ```
    Starting the FastApi server will create all required tables with columns with the help of  SqlAlchemy ORM.

## Version: 0.1.0

### /api/sales

#### GET
##### Summary:

Get Sales Data

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| start_date | query | ISO format datetime string  | No |  |
| end_date | query | ISO format datetime string | No |  |
| product | query |  | No |  |
| category | query |  | No |  |
| limit | query |  | No |  |
| offset | query |  | No |  |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /api/sales/revenue

#### GET
##### Summary:

Analyze Revenue

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| start_date | query | ISO format datetime string | No |  |
| end_date | query | ISO format datetime string | No |  |
| product | query |  | No |  |
| category | query |  | No |  |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /api/inventory

#### GET
##### Summary:

Get Inventory Status

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| start_date | query | ISO format datetime string | No |  |
| end_date | query | ISO format datetime string | No |  |
| product | query |  | No |  |
| category | query |  | No |  |
| limit | query |  | No |  |
| offset | query |  | No |  |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /api/products

#### POST
##### Summary:

Register Product

##### Responses

| Code | Description |
| ---- | ----------- |
| 201 | Successful Response |
| 422 | Validation Error |

#
# Database Schema Documentation

This document provides a comprehensive overview of the database schema for a dynamic Inventory and Sales Management System. The schema comprises several interconnected tables designed to facilitate efficient tracking of inventory, product categories, sales transactions, and more.

## Tables and Their Purposes

### `inventory`
- **Purpose**: This table serves as a real-time inventory tracker, maintaining the quantity of each product in stock.
- **Columns**:
  - `id`: Unique identifier for each inventory item.
  - `quantity`: The current stock quantity of the product.
  - `created_at`: Timestamp indicating when the inventory item was added.
  - `updated_at`: Timestamp indicating the last update to the inventory item.

### `product_category`
- **Purpose**: This table stores vital information about product categories, helping to organize and classify products.
- **Columns**:
  - `id`: Unique identifier for each product category.
  - `name`: The name of the product category (e.g., Electronics, Clothing).
  - `description`: A brief description of the product category.
  - `created_at`: Timestamp indicating when the product category was created.
  - `updated_at`: Timestamp indicating the last modification to the product category.

### `products`
- **Purpose**: Contains detailed information about individual products, including their names, descriptions, prices, and associations with categories and inventory.
- **Columns**:
  - `id`: Unique identifier for each product.
  - `name`: The name of the product.
  - `description`: A detailed description of the product.
  - `category_id`: A foreign key linking the product to its respective category in the `product_category` table.
  - `inventory_id`: A foreign key connecting the product to its inventory item in the `inventory` table.
  - `price`: The price of the product.
  - `created_at`: Timestamp indicating when the product was added.
  - `updated_at`: Timestamp indicating the last update to the product.
- **Relationships**:
  - Each product belongs to a specific product category.
  - Each product is associated with a particular inventory item.

### `sales`
- **Purpose**: This table records essential details about sales transactions, including the user responsible for the sale and the total sale amount.
- **Columns**:
  - `id`: Unique identifier for each sale.
  - `user_id`: Identifier for the user who initiated the sale.
  - `total`: The total amount of the sale.
  - `created_at`: Timestamp indicating when the sale was recorded.

### `sale_items`
- **Purpose**: Used to track individual items sold within each sale, enabling a granular view of product sales.
- **Columns**:
  - `id`: Unique identifier for each sale item.
  - `sale_id`: A foreign key linking the sale item to the corresponding sale in the `sales` table.
  - `product_id`: A foreign key connecting the sale item to the specific product sold in the `products` table.
  - `quantity`: The quantity of the product sold in the sale item.
  - `created_at`: Timestamp indicating when the sale item was recorded.
- **Relationships**:
  - Each sale item is associated with a particular sale.
  - Each sale item represents a product sold from the `products` table.

### Inserting dummy data

SQL queries for inserting dummy data can be found at the root level of this project
named: dummy_data.txt

## Conclusion

This thoughtfully designed schema efficiently manages inventory, categorizes products, records sales transactions, and associates sold items with specific products and sales. The interplay between these tables forms the backbone of the Inventory and Sales Management System, ensuring accurate and timely data tracking and analysis.
