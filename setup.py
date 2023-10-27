from setuptools import setup, find_packages

setup(
    name='Workout_Reminder',
    version='1.0.0',
    packages=find_packages(),
    install_requires=['pillow','pyyaml','requests','schedule'])
