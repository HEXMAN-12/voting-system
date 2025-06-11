# PMS Voting System

A complete web-based voting system built with Flask and SQLite, featuring a modern UI and comprehensive functionality.

## 🚀 Features

- **User Registration & Authentication**: Secure user registration with CNIC validation
- **Vote Casting**: Clean interface for selecting and casting votes
- **Real-time Results**: Live voting results with statistics
- **Admin Panel**: Comprehensive admin dashboard with user management
- **Database**: SQLite database for storing users, votes, and statistics
- **Responsive Design**: Works on desktop and mobile devices
- **Security**: Password hashing and session management

## 📋 Requirements

- Python 3.7 or higher
- Windows OS (for the batch file)

## 🔧 Installation & Setup

### Option 1: One-Click Setup (Recommended)

**🚀 For immediate setup and launch:**
1. **Double-click `quick-start.bat`**
   - Automatically creates virtual environment
   - Installs all dependencies
   - Starts the server in background
   - Opens your web browser automatically
   - Perfect for end users

**🔧 For development and monitoring:**
1. **Double-click `run.bat`**
   - Complete setup with detailed console output
   - Starts the server with visible logs
   - Keeps console window open for debugging
   - Better for development work

**⚙️ For setup without running:**
1. **Double-click `setup-only.bat`**
   - Only sets up the environment and dependencies
   - Doesn't start the server
   - Good for initial setup or troubleshooting

**📊 To check system status:**
1. **Double-click `check-status.bat`**
   - Shows environment status
   - Checks if server is running
   - Displays helpful information

**🛑 To stop the server:**
1. **Double-click `stop-server.bat`**
   - Safely stops all voting system processes
   - Frees up port 5000
   - Cleans up the system

### Option 2: Manual Setup (Advanced Users)

1. **Create virtual environment**:
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```cmd
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```cmd
   python app.py
   ```

## 🚀 Batch Files Explained

### `quick-start.bat` 🏃‍♂️
- **One-click solution** for instant setup and launch
- Creates virtual environment automatically
- Installs all dependencies silently
- Starts server in background (minimized window)
- Opens web browser automatically to the application
- Perfect for end users who just want to use the app

### `run.bat` 🔧
- **Developer-friendly** setup and run script
- Shows detailed console output for debugging
- Creates virtual environment if needed
- Installs dependencies with full output
- Keeps console window open for monitoring
- Better for development and troubleshooting

### `setup-only.bat` ⚙️
- **Environment setup** without running the application
- Creates virtual environment
- Installs all required dependencies
- Perfect for initial setup or CI/CD environments
- Doesn't start the server

### `check-status.bat` 📊
- **System diagnostics** and status checking
- Shows virtual environment status
- Checks if dependencies are installed
- Displays server running status
- Shows process information
- Helpful for troubleshooting

### `stop-server.bat` 🛑
- **Safe shutdown** of the voting system
- Stops all Python processes running app.py
- Frees up port 5000 from any processes
- Cleans up background processes
- Use when you can't access the server window

## 🖥️ Usage

### For Voters:

1. **Register**: Create a new account with your details

   - First Name, Last Name
   - CNIC (format: 12345-1234567-1)
   - Email, Phone, Address
   - Password (minimum 6 characters)

2. **Login**: Use your CNIC and password to log in

3. **Vote**: Select your preferred party and cast your vote

   - Each user can vote only once
   - Vote confirmation is displayed

4. **View Results**: Check real-time voting results

### For Administrators:

- Access the **Admin Panel** at: `/admin`
- View detailed statistics and user voting records
- Monitor voter turnout and party-wise results

## 📁 File Structure

```
voting-system/
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── quick-start.bat          # One-click setup & launch
├── run.bat                  # Developer setup & run
├── setup-only.bat           # Environment setup only
├── check-status.bat         # System status checker
├── stop-server.bat          # Safe server shutdown
├── voting_system.db         # SQLite database (created automatically)
├── voting-portal.html       # Original HTML file (reference)
└── templates/               # Flask templates
    ├── index.html           # Login/Registration page
    ├── vote.html            # Voting page
    ├── results.html         # Results page
    └── admin.html           # Admin panel
```

## 🔐 Security Features

- **Password Hashing**: SHA-256 hashing for secure password storage
- **Session Management**: Secure Flask sessions
- **Input Validation**: CNIC format and email validation
- **One Vote Per User**: Database constraints prevent multiple votes
- **SQL Injection Protection**: Parameterized queries

## 📊 Database Schema

### Users Table

- `id` (Primary Key)
- `first_name`, `last_name`
- `cnic` (Unique)
- `email` (Unique)
- `phone`, `address`
- `password_hash`
- `has_voted` (Boolean)
- `created_at` (Timestamp)

### Votes Table

- `id` (Primary Key)
- `user_id` (Foreign Key)
- `party`
- `voted_at` (Timestamp)

### Party Stats Table

- `party` (Primary Key)
- `vote_count`

## 🎨 UI/UX Features

- **Modern Design**: Dark theme with gradient effects
- **Responsive Layout**: Works on all screen sizes
- **Smooth Animations**: CSS transitions and hover effects
- **Real-time Updates**: Auto-refresh for results
- **User Feedback**: Success/error messages
- **Progress Indicators**: Visual vote count representation

## 🔧 Configuration

### Environment Variables (Optional)

You can modify these in `app.py`:

- `SECRET_KEY`: Change for production use
- `DEBUG`: Set to `False` for production
- `HOST`: Default is `0.0.0.0`
- `PORT`: Default is `5000`

### Database Location

The SQLite database `voting_system.db` is created in the same directory as `app.py`.

## 🚨 Important Notes

1. **CNIC Format**: Must follow Pakistani CNIC format: `12345-1234567-1`
2. **One Vote Policy**: Each user can vote only once
3. **Data Persistence**: All data is stored in SQLite database
4. **Admin Access**: No special authentication for admin panel (add if needed)

## 📈 Monitoring & Analytics

The admin panel provides:

- Total registered users
- Vote count per party
- Voter turnout percentage
- Individual user voting status
- Real-time vote tracking
