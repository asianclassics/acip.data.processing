from apiclient import errors


# in drive both files and folders are seen as 'files'
# with names and id's
# each has a parent, for each it's the enclosing folder
def get_drive_items(service, query, driveId, flag_type='folder'):
    # Call the Drive v3 API
    page_token = None
    drive_list = []
    kwargs = {
        "q": query,
        "spaces": "drive",
        "fields": "nextPageToken, incompleteSearch, files(id,parents,name)",
        "driveId": driveId,
        "corpora": "drive",
        "supportsAllDrives": True,
        "includeItemsFromAllDrives": True
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
                # if flag_type != 'folder':
                print(f"Found file: {file.get('name')} ({file.get('parents')})")
                drive_list.append(file.get('id'))
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break

        except errors.httpError as error:
            print('An error occurred: %s' % error)
            break

    if flag_type == 'folder':
        if len(drive_list) < 1:
            print('folder not found, check folder name variable...')
            return None
        elif len(drive_list) > 1:
            print('folder name is not unique, check google drive...')
            return None

    # print(f'Found {flag_type} {drive_list[0]}')
    return drive_list
