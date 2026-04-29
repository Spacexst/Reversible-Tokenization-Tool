REVERSIBLE TOKENIZATION TOOL

## USER GUIDE
Reversible Tokenization System- User Guide 
Version 1.0
Audience: End-Users, Testers, Researchers
Purpose: This guide explains how to install, navigate and use the Reversible Tokenization System through its Graphical User Interface.
1.	Introduction
The Reversible Tokenization System is a tool designed to convert text into tokenized form and reconstruct the original text from tokens when required by authorized users. It is designed primarily to protect data privacy when interacting with AI Systems, by replacing sensitive information with tokens. This allows users to process or analyze text securely without exposing personal or confidential data.
This user guide will help you:
•	Understand the system’s features 
•	Navigate the Graphical User Interface
•	Perform tokenization and detokenization
•	Manage files and outputs
•	Troubleshoot common issues

2.	System Requirements

Hardware
•	Minimum 4 GB RAM
•	200 MB free disk space
•	Standard keyboard and mouse
           Software
•	Windows/macOS/Linux
•	Python and required libraries

3.	Installation

3.1	Downloading the Application
•	Visit the official download page or repository
•	Download the latest version for your operating system

3.2	Installation steps
Windows: Run the .exe installer and follow onscreen instructions
macOS: Drag the application into the applications folder
Linux: Extract the package and run the executable or install via terminal
3.3	First Launch
When you first open the application for the first time, the system displays the login window. Users must authenticate before accessing the main interface. After a successful login, the application loads the default settings and initializes the tokenization engine in the background.

4.	Getting Started with the Interface
4.1. Main Window Overview
The main interface of the Reversible Tokenization System is designed to be simple and task focused. The following components appear from top to bottom and left-to right within GUI
1.	Select a file-Upload a text file for processing

2.	File dialog box-Uploaded file can be seen


3.	Protect data-Tokenizes the sensitive information in the text file

4.	Ask AI-Sends the protected text to AI systems for processing


5.	Restore data-Converts the tokenized text back to its readable form

6.	Clear-Removes all text and resets the interface


7.	Admin Tools-Provides access to admin/auditors (RBAC)

8.	Status bar-Shows system messages and progress updates



5.	Core Features

5.1	Tokenization

To tokenize text:
•	Select a file
•	Click on Protect data button
•	View the tokenized file


5.2	Detokenization

To detokenize text:
•	Select a tokenized text file
•	Click on Restore data button
•	View the detokenized file

5.3	Ask AI (choose AI)
To send protected text to an AI system
•	Click on Ask AI button
•	Select the AI service from the Choose AI window 
•	Wait for the AI response to appear in the output area
     
     5.4.  Clear files
To clear the file from the panel
•	Click on clear button
    
5.4	Admin Tools
Only authorized users can access the admin tools (auditors, admin)
Logged in admin can view and open:
•	Token Mappings
•	Audit Logs
•	Search for a token
 Logged in auditor can view and open:
•	Audit Logs

6.	Trouble shooting
Issue: Tokenization failed
Check if the input text contains unsupported characters
Restart the application if the tokenizer engine stalls

Issue: Detokenization produced incomplete text
Ensure the token list is complete and formatted

Issue: Application freezes
Close and reopen the program

7.	Contact and Support
For bug reports, feature requests or support contact the development team or visit repository.

## Use cases
-Protecting sensitive data (email id, phone number, credit card numbers)
-Health care data anonymization
-Financial data, for e.g. banks
-Secure data sharing and analysis
-Research requiring reversible anonymization
-Proecting data while interacting with AI systems


## OVERVIEW
  This project set out to address a significant industry challenge: the secure handling of sensitive data when interacting with the artifical intelligence systems. To mitigate the risk of exposing Personally Identifiable Information (PIIs) and other confidential information like Financial data to external AI platforms, the project designed and implemented a 'Reversible Tokenization Solution' that detects ans tokenizes sensitive data, stores token mappings securely in embedded database and enables controlled detokenization for authorized users.

  The system combines:
  -Regex for structured pattern detection (e.g. emails, phone numbers, credit card numbers, currency )
  -spaCy NLP module for NER (Named Entity Recognition) for detection and tokenization of entities such as names
  -UUIDv4-based token generation for secure and unique identifiers
  -SQLite database for secure persistent token to original mapping

## Key Features
  -Fully reversible Tokenization of sensitive data
  -UUIDv4-based secure token generation
  -Hybrid NLP pipeline (spaCy + Regex)
  -Persistent SQLite mapping storage
  -No <UNK> token usage (no data loss)

## System Architecture
Flowchart
  A[Input Text]--> B[Regex Pattern Detection]
  B--> C[Spacy Tokenization]
  C--> D[UUID Token Generation]
  D--> E[SQLite Storage]
  E--> F[Tokenized output]
  F--> G[Detokenization process]
  G--> H[Original Text restored]

  ![alt text](image.png)

  ### Example Usage
    Original Text: John Doe is a bachelor of IT student. The funds allocated are $100,000
    Tokenized Text: TKN_0b6bb4f0  is a bachelor of IT stufdent. The funds allocated are TKN_0cc6786b
    Detokenized (Reconstructed output)Text:  John Doe is a bachelor of IT student. The funds allocated are $100,000

## Screenshots
### Tokenization Process
![Tokenization](Screenshots/Tokenization.png)

### SQLite Database Mapping
![Database](Screenshots/database.png)

### Detokenization Output
![Detokenization](Screenshots/Detokenization.png)

## Technologies used
  Programming languages: Python and all of its relevant libraries
  Cryptographic Techniques-AES (Fernet)
  spaCy(NLP processing)
  Regex(pattern matching)
  UUIDv4(secure token generation)
  SQLite(Database storage)

## Project Structure
  Reversible Tokenization/
  |
  |--gui.py (handles user interface and main application logic)
  |
  |--pii_tokenizer.py (handles tokenization and detokenization logic)
  |
  |--encryption_utils.py (handles cryptographic functions-turns the sensitive data into cipher text before storing in data base)
  |
  |--db.py (handles database logic)
  |
  |--audit_logger.py (logs the tokenization and detokenization events for traceability and accountability)
  |
  |--README.md
  |
  |--LICENSE
  |
  |--Tests
  |--Screenshots (capturing the core operations like tokenization, detokenization and stored token-value mappings)

## How it Works
  1. Input text is processed using Regex to detect structured sensitive data
  2. spaCy performs linguistic tokenization
  3. Each detected sensitive value is replaced with a unique UUID identifier
  4. The mappings between UUID tokens and original values are stored in SQLite database
  5. During reversal original values are restored through cryptographic tools
  6. The original values are fully restored without loss

## Limitations
  1. Local key storage limitations. No backup or key rotation
  2. Not suitable for multi user environments
  3. Created in Tkinter lacks visual flexibility or responsiveness to screen sizes like that in web frameworks

## Future Improvements
 Include:
  1.  Extending the system to a client-server or web-based architecture 
  2.  Integrate external "Key Management Services" or Hardware Security Modules (HSMs), key rotation mechanisms
  3.  More advanced GUI frameworks for better visual flexibility and user-experience

## Author
  Anuradha Mangalpalli
  Bachelor of Applied Information Technology student
  Whitecliffe

  Reversible Tokenization Tool-AI
  Developed for Academic Research 

## Citation
  This project is archived in zenodo:
   https://doi.org/10.5281/zenodo.19881601




 











  





