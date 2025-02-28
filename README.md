# Data and ML Platform

<div align="center">

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io/your-app-url)
[![Python 3.7+](https://img.shields.io/badge/Python-3.7+-blue.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![Google Sheets](https://img.shields.io/badge/Google_Sheets-API-green.svg?style=flat&logo=google-sheets&logoColor=white)](https://developers.google.com/sheets/api)
[![Google Drive](https://img.shields.io/badge/Google_Drive-API-4285F4.svg?style=flat&logo=google-drive&logoColor=white)](https://developers.google.com/drive)

</div>

## 📋 Project Overview

The GDG On Campus PUP Data and ML System is a comprehensive web application designed to serve as the digital infrastructure for the Google Developer Group at the Polytechnic University of the Philippines. This platform facilitates student engagement with data science and machine learning initiatives through an intuitive interface built on modern web technologies.

## 🛠️ Technology Stack

<table>
  <tr>
    <td>
      <img src="https://raw.githubusercontent.com/streamlit/streamlit/develop/docs/_static/favicon.png" width="40" height="40" />
    </td>
    <td>
      <strong>Streamlit</strong><br/>
      Powers the reactive web interface with minimal development overhead
    </td>
  </tr>
  <tr>
    <td>
      <img src="https://www.gstatic.com/images/branding/product/2x/sheets_48dp.png" width="40" height="40" />
    </td>
    <td>
      <strong>Google Sheets API</strong><br/>
      Primary database system for storing and retrieving user data
    </td>
  </tr>
  <tr>
    <td>
      <img src="https://www.gstatic.com/images/branding/product/2x/drive_48dp.png" width="40" height="40" />
    </td>
    <td>
      <strong>Google Drive API</strong><br/>
      Manages access to resources and documentation
    </td>
  </tr>
  <tr>
    <td>
      <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/1869px-Python-logo-notext.svg.png" width="40" height="40" />
    </td>
    <td>
      <strong>Python</strong><br/>
      Core programming language for both frontend and backend functionality
    </td>
  </tr>
</table>

## 📊 Interactive Pages

<details>
<summary><b>🏠 Home Page</b></summary>
<br>

- **Welcome Hub**: Central information repository about GDG On Campus PUP
- **Tech Focus**: Deep dive into our Data and ML initiatives and mission
- **Quick Links**: Access to important resources and community guidelines

</details>

<details>
<summary><b>📅 Events Page</b></summary>
<br>

- **Workshop Archive**: Access recordings of past workshops and study jams
- **Resource Library**: Comprehensive collection of learning materials
- **Event Timeline**: Browse our complete history of tech events

</details>

<details>
<summary><b>🏆 Leaderboard Page</b></summary>
<br>

- **XParky Tracker**: Check your current point status and level
- **Community Rankings**: See how you stack up against fellow members
- **Top Performers**: Spotlight on the most active community members

</details>

<details>
<summary><b>🎓 Certificates Page</b></summary>
<br>

- **Quick Certificate Access**: Enter your email to download earned certificates
- **Event Verification**: Certificates for workshop attendance and evaluation completion

</details>

<details>
<summary><b>📝 Submission Page</b></summary>
<br>

- **Activity Submissions**: Submit completed challenges to earn XParky points
- **Level-Up System**: Complete activities to advance through skill levels
- **Secure Verification**: Email and student number authentication
- **Progress Tracking**: Monitor submission status and feedback

</details>

## 🚀 Getting Started

### Prerequisites

```
Python 3.7+
Google Cloud Platform account with API access
Required Python packages (see requirements.txt)
```

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/gdg-pup/data-ml-system.git](https://github.com/gdg-pup/data-ml-system.git)
    ```
2.  **Navigate to the project directory:**
    ```bash
    cd data-ml-system
    ```
3.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate  # On Windows
    # source venv/bin/activate # On macOS and Linux
    ```
4.  **Upgrade pip (if necessary):**
    ```bash
    python -m pip install --upgrade pip
    ```
5.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Google API Credentials

1.  Download your `credentials.json` file from the Google Cloud Console.
2.  Place the `credentials.json` file in the root directory of the project.

## Running the Application

```bash
streamlit run app.py
```

## 👨‍💻 Development Team

<div align="center">
  <table>
    <tr>
      <td align="center">
        <a href="https://github.com/JpCurada">
          <img src="https://github.com/JpCurada.png" width="100px;" alt=""/>
          <br /><sub><b>John Paul Curada</b></sub>
        </a>
      </td> 
      <td align="center">
        <a href="https://github.com/cytojen">
          <img src="https://github.com/cytojen.png" width="100px;" alt=""/>
          <br /><sub><b>Jen Patrick Nataba</b></sub>
        </a>
      </td> 
      <td align="center">
        <a href="https://github.com/thatjohnlagman">
          <img src="https://github.com/thatjohnlagman.png" width="100px;" alt=""/>
          <br /><sub><b>John Ferry Lagman</b></sub>
        </a>
      </td>
      <td align="center">
        <a href="https://github.com/definitelynotredd">
          <img src="https://github.com/definitelynotredd.png" width="100px;" alt=""/>
          <br /><sub><b>Redd Lawrence Reyes</b></sub>
        </a>
      </td>
      <td align="center">
        <a href="https://github.com/paisenpai">
          <img src="https://github.com/paisenpai.png" width="100px;" alt=""/>
          <br /><sub><b>John Gavin Deposoy</b></sub>
        </a>
      </td>
    </tr>
  </table>
</div>

## 📜 License

This project is proprietary and maintained by GDG On Campus PUP.

---

<div align="center">
<i>Developed for Google Developer Group on Campus - Polytechnic University of the Philippines</i>
</div>
