from googleapiclient.discovery import build
from google.oauth2 import service_account


# Function to find a file by name and copy it in the same folder
def new_form(new_file_name: str):
    # Function to authenticate and create the Google Drive service
    SCOPES = ['https://www.googleapis.com/auth/drive']
    SERVICE_ACCOUNT_FILE = 'drive_credentials.json'

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=credentials)
    # Search for the file
    results = service.files().list(q=f"name='sample form'", fields="files(id, name, parents)").execute()
    items = results.get('files', [])

    if not items:
        print(f"No files found with the name: sample form")
        return

    # Assuming the first search result is the file you want to copy
    file_id = items[0]['id']
    parent_id = items[0]['parents'][0]  # Assuming the file has at least one parent folder

    # Copy the file
    file_metadata = {
        'name': new_file_name,
        'parents': [parent_id]  # Place the copy in the same folder
    }
    copied_file = service.files().copy(fileId=file_id, body=file_metadata).execute()

    print(f"Copied 'sample form' to '{new_file_name}' with ID: {copied_file['id']}")
    return str(copied_file['id'])


def update_google_form(form_id, title, description, max_attendees):
    """Update a Google Form's title, description, and add a max attendees note.

    Args:
        form_id (str): The ID of the Google Form to update.
        title (str): The new title for the form.
        description (str): The new description for the form.
        max_attendees (int): The maximum number of attendees to note in the form.
    """
    # Authenticate with the Google Forms API
    credentials = service_account.Credentials.from_service_account_file(
        'drive_credentials.json',
        scopes=['https://www.googleapis.com/auth/forms.body',
                'https://www.googleapis.com/auth/forms.responses.readonly'])
    service = build('forms', 'v1', credentials=credentials)

    # Fetch the current form configuration
    form = service.forms().get(formId=form_id).execute()

    updated_description = f"{description}\n\nMaximum Attendees: {max_attendees}"

    # Prepare the request body for updating the form's title and description
    requests = [
        {
            "updateFormInfo": {
                "info": {
                    "title": title,
                    "description": updated_description
                },
                "updateMask": "title,description"
            }
        }
    ]
    service.forms().batchUpdate(formId=form_id, body={'requests': requests}).execute()

    print(f"Form with ID {form_id} has been updated.")

