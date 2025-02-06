# Python scripts for different use cases

## Log Analyzer

A Python script to analyze Nginx web server logs and extract useful insights such as:
- Top 5 IP addresses with the most requests.
- Most frequent HTTP errors (4xx and 5xx status codes).
- Average response size in bytes.

### Usage

Run the script with the path to a log file as an argument:

```
python log_analyzer.py access.log
```


## XML to JSON Converter

A Python script for parsing XML files containing product data, converts it into JSON format, and saves the output to a different directory.

- Parses multiple XML files in a given directory.
- Extracts product data from `<product>` elements inside `<products>`.
- Converts valid XML data to JSON format.
- Saves JSON files to the output directory.

### Usage

Run the script while providing input and output directories:

```
python xml_to_json.py --input-dir /path/to/xml --output-dir /path/to/json
```

If no arguments are provided, it defaults to:

./input for XML files
./output for JSON files

## Task Manager


A Python script that implements a simple task management system using **TinyDB** as a lightweight database. The program allows users to add, update, delete, and list tasks via a command-line interface (CLI).

- Add a new task with a **title**, **description**, **due date**, and **status**.
- Update the status of a task (`pending`, `in_progress`, `completed`).
- Delete a task by title.
- List all tasks, sorted by **due date**.
- Uses **argparse** for command-line interaction.
- Logs all operations to `task_manager.log`.

### Prerequisites

Install dependencies using:

```
pip install tinydb
```
### Usage

Run the script with the desired command:

#### Add a Task
```
python task_manager.py add "Buy groceries" "Milk, eggs, bread" 2025-02-10
```
#### Update a Task Status
```
python task_manager.py update "Buy groceries" "completed"
```
#### Delete a Task
```
python task_manager.py delete "Buy groceries"
```
#### List All Tasks
```
python task_manager.py list
```

## API Data Fetcher
### Prerequisites

Install dependencies using:

```
pip install aiohttp
```
### Usage
```
python fetch_posts.py
```
