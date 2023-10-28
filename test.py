import tkinter as tk
import subprocess
import requests

def get_latest_release(repo_url):
    try:
        # Send a GET request to the GitHub API to fetch release information
        response = requests.get(f'https://api.github.com/repos/{repo_url}/releases/latest')
        if response.status_code == 200:
            release_info = response.json()
            return release_info['tag_name']
    except Exception as e:
        print(f'Error getting release information: {e}')
    return None

def git_pull():
    try:
        repo_url = 'PrasanthChowhan/Workout_Reminder'  # Your GitHub repository (without 'https://github.com/')
        latest_release = get_latest_release(repo_url)

        if latest_release is not None:
            print(f'Latest release: {latest_release}')
            # You can compare the latest release with your current version if needed.

            subprocess.run(['git', 'pull', f'https://github.com/{repo_url}.git'], check=True)
            print('Git pull completed successfully.')
        else:
            print('No releases found.')
    except subprocess.CalledProcessError as e:
        print(f'Error during Git pull: {e}')

app = tk.Tk()
app.title('GitHub Release Check and Update')

update_button = tk.Button(app, text='Check for Updates', command=git_pull)
update_button.pack()

app.mainloop()
