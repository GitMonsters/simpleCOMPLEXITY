# COMPLEXITY

A project for managing complexity in software systems.

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Installation

### Prerequisites

Before installing COMPLEXITY, ensure you have the following:

- Git
- Bash shell (Linux/macOS) or Git Bash (Windows)
- Optional: Python 3.x, Node.js, or Docker (depending on your use case)

### Method 1: Quick Installation (Recommended)

1. **Clone the repository:**
   ```bash
   git clone <repository-url> ~/COMPLEXITY
   cd ~/COMPLEXITY
   ```

2. **Run the quick install script:**
   ```bash
   bash QUICK_INSTALL.sh
   ```

   The script will:
   - Check for required dependencies
   - Pull the latest changes
   - Set up the project structure
   - Configure permissions

### Method 2: Manual Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url> ~/COMPLEXITY
   cd ~/COMPLEXITY
   ```

2. **Pull latest changes:**
   ```bash
   git pull
   ```

3. **Create necessary directories:**
   ```bash
   mkdir -p data logs config
   ```

4. **Make scripts executable:**
   ```bash
   chmod +x *.sh
   ```

## Quick Start

After installation, you can start using COMPLEXITY:

```bash
cd ~/COMPLEXITY
# Add your usage commands here
```

## Usage

### Basic Commands

```bash
# Navigate to the project directory
cd ~/COMPLEXITY

# Pull latest updates
git pull

# Run the quick install script
bash QUICK_INSTALL.sh
```

### Common Issues

#### "No such file or directory" error

If you get an error like `bash: cd: /home/user/COMPLEXITY: No such file or directory`, it means:

1. The directory doesn't exist yet - you need to **clone** the repository first
2. You're in the wrong location - check your path with `pwd`

**Solution:**
```bash
# Clone the repository first
git clone <repository-url> ~/COMPLEXITY

# Then navigate to it
cd ~/COMPLEXITY
```

#### Multiple commands on one line

Don't try to run multiple commands without proper separators:
```bash
# WRONG - "too many arguments" error
cd ~/COMPLEXITY git pull bash QUICK_INSTALL.sh

# CORRECT - use && to chain commands
cd ~/COMPLEXITY && git pull && bash QUICK_INSTALL.sh
```

## Project Structure

```
COMPLEXITY/
├── LICENSE              # Project license
├── README.md           # This file
├── QUICK_INSTALL.sh    # Quick installation script
├── config/             # Configuration files
├── data/               # Data directory
└── logs/               # Log files
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the terms specified in the LICENSE file.

## Support

If you encounter any issues or have questions:

1. Check the [Common Issues](#common-issues) section
2. Review the installation steps carefully
3. Ensure all prerequisites are installed
4. Open an issue in the repository

---

**Note:** Make sure to replace `<repository-url>` with the actual URL of your repository when sharing these instructions.
