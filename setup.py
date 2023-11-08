from setuptools import setup, find_packages

# Application details
app_name = "Workout Reminder"
app_version = "0.1.2"
app_author = "Prasanth Chowhan"
app_email = "your.email@example.com"  # Replace with your email
app_description = "A reminder app for exercise breaks."
app_license = "Free for personal use"

# Required packages
install_requires = [
    "Pillow",
    "pyyaml",
    "requests",
    "schedule",
    "pystray",
    "pywin32",
]

setup(
    name=app_name,
    version=app_version,
    author=app_author,
    author_email=app_email,
    description=app_description,
    license=app_license,
    packages=find_packages(),
    install_requires=install_requires,
    
)
