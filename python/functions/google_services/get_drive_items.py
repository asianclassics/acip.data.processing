from apiclient import errors


def get_drive_items(service, query):
    # Call the Drive v3 API
    page_token = None
    drive_list = []
    kwargs = {
        "q": query,
        "spaces": "drive",
        "fields": "nextPageToken, incompleteSearch, files(id,parents,name)",
        # Specify what you want in the response as a best practice. This string
        # will only get the files' ids, names, and the ids of any folders that they are in
        # Add any other arguments to pass to list()
    }

    while True:

        try:
            response = service.files().list(**kwargs, pageToken=page_token).execute()
            # note that you can chain everything together and loop through actual files
            # files = DRIVE.files().list().execute().get('files', [])
            # for file in files
            for file in response.get('files', []):
                # Process change
                print('Found file: %s (%s)' % (file.get('name'), file.get('id')))
                drive_list.append(file.get('id'))
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break

        except errors.httpError as error:
            print('An error occurred: %s' % error)
            break

    return drive_list
