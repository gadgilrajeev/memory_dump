# Memory Dump Heatmap
### Introduction
The Memory Dump Heatmap Presentation project is a web application developed using Flask, a Python web framework, to visualize memory dumps in the form of heatmaps. The project allows users to generate and view heatmaps of binary files representing memory dumps, providing insights into the distribution and values of memory addresses.
### Project Setup
To set up and run the Memory Dump Heatmap Presentation project, please follow the instructions below:

### Installation
* Clone the project repository from the desired location.
* Make sure you have Python installed on your system (Python 3.6 or higher).
* Create a virtual environment (optional but recommended).
* Navigate to the project directory using the command line.
### Required Libraries
* Install the required libraries by running the following command:
```bash
pip install -r requirements.txt
```
### Running the Application
* Once the required libraries are installed, run the Flask application by executing the following command:
```bash
python app.py
```
This will start the Flask development server.

* Access the application by opening a web browser and entering the following URL:
```bash
http://localhost:5000/
```
This will open the home page of the application.

### Application Structure
The Memory Dump Heatmap Presentation project follows the following structure:

* app.py: The main Flask application file that contains the application logic.
* templates/: Directory containing HTML templates for different pages of the application.
  * index.html: Home page template.
  * generate_files.html: Template for generating memory dump files.
  * heatmap.html: Template for displaying the memory dump heatmaps.
* bin_files/: Directory for storing generated memory dump binary files.
* memdump.c: C source code file for generating memory dump files.
* requirements.txt: Text file specifying the required Python libraries for the project.

### Functionality
#### Generating Memory Dump Files
The application provides a page generate_files.html where users can specify the start address, end address, interval, and number of iterations to generate memory dump files. The C source code file memdump.c is responsible for generating the memory dump files based on the provided parameters.

Enter the following parameters :

start address = 2, end address=2222, interval=4, and iterations = 2


#### Viewing Memory Dump Heatmaps
Users can view the generated memory dump files as heatmaps on the heatmap.html page. The heatmaps display the memory values as colors, providing a visual representation of memory distribution. Users can select a base memory dump file and compare it with other memory dump files.

select dump_0.bin as a base memory dump file and select dump_1.bin as a second memory dump file
* Selecting Base File: On the heatmap.html page, users can select a base memory dump file from the available options. select dump_0.bin 
* Comparing Files: Then select second memory dump files to compare with the base file. select dump_1.bin .The application generates heatmaps for selected file and highlights the differences between the values of the base file and the compared files.
* Pagination: The heatmaps are displayed in chunks, and users can navigate through the chunks using pagination buttons.
* Heatmap Details: Users can hover over each memory cell in the heatmap to view the address and value details.

#### Thank you 
