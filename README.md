# Keywwy

Keywyy is an application that allows you to control your mouse cursor using keyboard shortcuts. It's inspired by a similar tool called Keytty.

The core functionality is implemented using:

1. The keyboard library for keyboard event handling
2. Custom mouse control logic in mouse.py
3. Application configuration in config.py
4. The main application loop in app.py

The application provides a keyboard-driven interface where you can:

* Move the mouse cursor using keyboard shortcuts
* Click, double-click and scroll using keyboard commands
* Toggle the control mode by pressing CTRL twice

This is particularly useful for users who prefer keyboard-based navigation or want to minimize mouse usage.

## Installation

```shell
# Create virtual environment
python -m venv keywwy

# Activate virtual environment (Windows)
.\keywwy\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Running

```shell
# Activate virtual environment (if not already activated)
.\keywwy\Scripts\activate

# Run the application
python app.py
```

## Troubleshooting

### Error during installation

> O arquivo ...\keywwy\Scripts\Activate.ps1 não pode ser carregado porque a execução de scripts foi desabilitada neste sistema. Para obter mais informações, consulte about_Execution_Policies

This error occurs because PowerShell's execution policy is preventing scripts from running. Here are the different ways to activate a virtual environment in Windows:

#### Using Command Prompt (cmd.exe)

```cmd
.\keywwy\Scripts\activate.bat
```

#### Using PowerShell

First, you need to allow script execution. Run PowerShell as Administrator and execute:

```shell
Set-ExecutionPolicy RemoteSigned
```

Then you can activate using

```shell
.\keywwy\Scripts\Activate.ps1
```
