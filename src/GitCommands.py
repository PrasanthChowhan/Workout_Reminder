import subprocess,requests

class GitCommands:
    repo_url = 'PrasanthChowhan/Workout_Reminder'

    @classmethod
    def get_local_repository_version(cls,repo_dir=''):
        """
        Retrieve the version tag of a local Git repository.

        This function runs the 'git describe' command to get the latest version tag in
        the specified local Git repository. If a version tag is found, it will be returned.

        Args:
            repo_dir (str, optional): The path to the local Git repository directory.
                If not provided, the current working directory will be used.

        Returns:
            str or None: The latest version tag of the repository if found, or None if no tag is available.

        Note:
            - The 'git describe' command is used to retrieve the latest version tag.
            - If the repository doesn't have any tags, or if there is an error executing the
            Git command, None will be returned.

        Example:
            version = get_local_repository_version('/path/to/your/repository')
            if version:
                print(f"Local repository version: {version}")
            else:
                print("No version tag found or an error occurred.")
        """
        try:
            # Use the git describe command to get the latest commit hash and version tag
            git_command = ['git', '-C', repo_dir, 'describe', '--tags', '--abbrev=0']
            result = subprocess.check_output(git_command, stderr=subprocess.STDOUT, text=True)
            return result.strip()  # Strip any leading/trailing whitespace
        except subprocess.CalledProcessError as e:
            # Handle any errors or exceptions here
            print(f"Error: {e}")
            return None

    @classmethod
    def get_latest_release(cls,repo_url):
        """
        Get the latest release tag of a GitHub repository.

        This function sends a GET request to the GitHub API to fetch information about the
        latest release of a specified GitHub repository. If successful, it returns the
        latest release tag name.

        Args:
            repo_url (str): The URL of the GitHub repository in the format 'user/repo'.
                            Your GitHub repository (without 'https://github.com/').

        Returns:
            str or None: The latest release tag name if found, or None if there was an error.

        Example:
            latest_tag = get_latest_release('username/repository')
            if latest_tag:
                print(f"Latest release tag: {latest_tag}")
            else:
                print("Error retrieving release information.")
        """
        try:
            # Send a GET request to the GitHub API to fetch release information
            response = requests.get(f'https://api.github.com/repos/{repo_url}/releases/latest')
            if response.status_code == 200:
                release_info = response.json()
                # print('yo')
                
                return release_info['tag_name']
        except Exception as e:
            print(f'Error getting release information: {e}')
        return None

    @classmethod
    def git_pull(cls,repo_url):
        """
        Pull the latest changes from a GitHub repository using Git.

        This function performs a Git pull operation to fetch the latest changes from a
        specified GitHub repository.

        Args:
            repo_url (str): The GitHub repository URL (e.g., 'username/repository').

        Returns:
            None

        Raises:
            subprocess.CalledProcessError: If an error occurs during the Git pull.

        Example:
            git_pull('PrasanthChowhan/Workout_Reminder')

        Note:
            Ensure that you have Git installed and configured.

        """
        try:
            subprocess.run(['git', 'pull', f'https://github.com/{repo_url}.git'], check=True)
            print('Git pull completed successfully.')
        except subprocess.CalledProcessError as e:
            print(f'Error during Git pull: {e}')

    @classmethod
    def check_for_update(cls):
        local_version = cls.get_local_repository_version()
        latest_release = cls.get_latest_release(cls.repo_url)
        
        if latest_release is not None:
            if local_version == latest_release:
                return "Up to date"
            elif local_version < latest_release:
                return "Update available"
            else: # Ignore this 
                return "Local version is ahead"
        else:
            return "No Release available"
        
    @classmethod
    def update_app(cls):
        cls.git_pull(cls.repo_url)
        
        command = "pip install -e ."
        # Run the command in the shell
        try:
            subprocess.run(command, shell=True, check=True)
            print("Package installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error installing package: {e}")

# def update_app():
#     current_version = GitCommands.get_local_repository_version()
#     print(current_version)

if __name__ == '__main__':
    # update_app()
    GitCommands.check_for_update()