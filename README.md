# Sharding
University of Messina A.Y. 2024/2025 | Computer System Security

## Description
This project focuses on implementing a secure solution for the transmission of PDF files through the use of sharding and symmetric encryption. The system divides each PDF file into three parts, also called "shards", which are individually encrypted using symmetric keys. The encrypted shards are then distributed across three separate containers that act like servers. The shards can be retrieved from the containers to recompose the original file.

## 🛠️ Used Tools
To achieve the project's goal, the following tools are used:
* Python3: Language used for the project
* XAMPP: To connect to MySQL database
* Docker: Used for creating some containers that act as servers
* Flask: Allows to expose RESTful endpoints via HTTP

## 📝 How to Run the Project
This is a brief instruction list to run the project:
* First clone the repo:
```
git clone https://github.com/Andrewww00/Sharding.git
```
* Once done, start Docker Desktop, then move to the directory:
```
cd Sharding
docker compose up -d
```
* As last step, just run the main.py and follow the instruction on terminal:
```
python3 main.py
```

Credits:
* Longo Andrea
* Musmeci Edoardo
