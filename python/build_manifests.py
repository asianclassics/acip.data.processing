import os
import json
from pathlib import Path
from python.templates.placeholder_values import p as placeholder_values
from python.functions import get_spaces_directory_files, \
    load_templates, update_json_placeholders, update_canvas_items, configure_logger

# https://acip.sfo2.digitaloceanspaces.com/scans/published/V8LS16868_I8LS16897_3-738/
# https://acip.sfo2.digitaloceanspaces.com/scans/published/V8LS16868_I8LS16897_3-738/I8LS168970005.jpg

configure_logger()

start_page = 193
end_page = 280

data_dir = '../data/manifests'
# get s3 images for manifest
spaces_dir = 'V8LS16868_I8LS16897_3-738'
spaces_pages = get_spaces_directory_files(spaces_dir)
# load json templates
python_dir = os.path.dirname(os.path.abspath(__file__))
manifest, canvas = load_templates(python_dir)

# update the manifest placeholders
manifest = update_json_placeholders(manifest, placeholder_values)
print(manifest)
quit()


# TO_DO: set up so it can traverse entire directory on spaces
def build_manifests():
    c = []
    if 'sequences' in manifest:
        for seq in manifest['sequences']:
            if 'canvases' in seq:
                # delete the canvases list
                seq.pop('canvases')
                # replace with loop over all images in
                for _, image_listing in spaces_pages.items():
                    for image_seq, image_url in enumerate(image_listing, start=1):
                        image_name = Path(image_url).stem
                        image_num = int(image_name[-3:])
                        # create canvas for image
                        if start_page <= image_num <= end_page:
                            replacement_items = {
                                "image_url": image_url,
                                "image_name": image_name,
                                "image_seq": image_seq,
                                "image_num": image_num,
                                "group_name": spaces_dir
                            }
                            update_items = update_canvas_items(placeholder_values, **replacement_items)
                            current_canvas = update_json_placeholders(canvas, update_items)
                            c.append(current_canvas)

                seq.update({"canvases": c})

    print(json.dumps(manifest, indent=4))

    new_manifest = os.path.join(python_dir, data_dir, f'{spaces_dir}_p{start_page}_p{end_page}.json')
    with open(new_manifest, 'w') as m:
        json.dump(manifest, m)


if __name__ == "__main__":
    build_manifests()

# CommonPrefixes to get 1st level directories
# for response in paginator.paginate(**operation_parameters):
#     for x in response.get('CommonPrefixes', []):
#         if x['Prefix'] == 'scans/published/V8LS16868_I8LS16897_3-738/':
#             print(x)
