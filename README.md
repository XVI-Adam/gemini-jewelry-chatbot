# Oro Latino Jewelry Store – AI-Powered Virtual Shopping Assistant

Welcome to the Oro Latino Jewelry Store virtual assistant application. This AI-driven system allows users to browse gold jewelry, add items to a virtual cart, receive live inventory feedback, and visualize their orders through AI-generated images. It’s built using Google's Gemini API, Firestore, and Taipy GUI.

---

## Features

- Conversational AI chatbot to assist customers with shopping  
- Real-time inventory checks and cart adjustments  
- Sales and inventory dashboard with visualizations  
- AI-generated images of ordered items  
- Firebase Firestore integration for persistent data storage  
- Interactive GUI with page navigation for a complete shopping experience  

---

## Tech Stack

- Python
- Google Generative AI (Gemini)
- Firebase Firestore
- Taipy GUI
- dotenv
- base64

---

## File Overview

| File | Description |
|------|-------------|
| `proj2.py` | Main application handling chatbot, order processing, and GUI pages |
| `prompt.py` | System instruction for the Gemini-powered chatbot |
| `proj2_image_gen.py` | AI image generator for visualizing customer orders |
| `inventory.py` | GUI for viewing inventory and sales analytics |
| `firestore_db.py` | Initializes Firestore and seeds inventory and sales data |
| `tap_to_pay.png`, `thank_you.jpg` | Image assets used in the application UI |

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/oro-latino-jewelry-assistant.git
cd oro-latino-jewelry-assistant
```
### 2. Install Python Dependencies

Install the required libraries:
```bash
pip install taipy firebase-admin python-dotenv google-generativeai
```
### 3. Configure Environment Variables

Create a .env file in the root directory:
```bash
GEMINI_API_KEY=your_google_generative_ai_key
```
