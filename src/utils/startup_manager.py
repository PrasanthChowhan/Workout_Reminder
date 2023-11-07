import os
import getpass
import shutil

class StartupFileManager:
    def __init__(self, filename):
        """
        Initializes the StartupFileManager with the given filename.

        Args:
            filename (str): The name of the file to manage in the startup folder.
        """
        self.filename = filename

    def get_startup_folder_path(self):
        """
        Get the full path to the user's startup folder where the file will be managed.

        Returns:
            str: The full path to the startup folder.
        """
        # Get the current user's username
        username = getpass.getuser()

        # Determine the path to the user's startup folder
        startup_folder = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Roaming', 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')

        return os.path.join(startup_folder, self.filename)

    def add_to_startup(self):
        """
        Add the specified file to the user's startup folder.
        """
        file_path = self.get_startup_folder_path()

        if os.path.exists(file_path):
            print(f"The file '{self.filename}' already exists in the startup folder.")
        else:
            try:
                # Copy the file to the startup folder
                shutil.copy(self.filename, file_path)
                print(f"Successfully copied '{self.filename}' to the startup folder.")
            except Exception as e:
                print(f"An error occurred: {e}")

    def remove_from_startup(self):
        """
        Remove the specified file from the user's startup folder.
        """
        file_path = self.get_startup_folder_path()

        if os.path.exists(file_path):
            try:
                # Remove the file from the startup folder
                os.remove(file_path)
                print(f"Successfully removed '{self.filename}' from the startup folder.")
            except Exception as e:
                print(f"An error occurred: {e}")
        else:
            print(f"The file '{self.filename}' does not exist in the startup folder.")

# Example usage:
# startup_manager = StartupFileManager('run_at_startup.bat')
# Comment out the following line and uncomment the next line to remove the file
# startup_manager.add_to_startup()
# startup_manager.remove_from_startup()
