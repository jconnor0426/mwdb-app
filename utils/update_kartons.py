# Simple python script to get submodule commits and update them in the config repo
from importlib.resources import path
from shutil import ExecError
import subprocess
import argparse
import pathlib
from unicodedata import name
import ruamel.yaml



def get_karton_name_to_image_tags():
    lines = [
        x.strip().decode('utf8')
        for x in subprocess.check_output(
            "git submodule status --cached", shell=True
        ).splitlines()
    ]
    name_to_image_tag = {}
    for line in lines:
        hash = line.split(" ")[0]
        if not str.isalnum(hash[0]):
            hash = hash[1:]
        submodule = line.split(" ")[1]
        if "kartons" not in submodule:
            continue
        karton = submodule.split("/")[1]
        name_to_image_tag[karton] = hash[:7]
    
    return name_to_image_tag

def update_values_file(name_to_image_tag: dict, path: pathlib.Path):
    """Update the values file from the karton-analyzer helm chart

    Args:
        name_to_image_tag (dict): name of images with tags to update
        path (pathlib.Path): path to images file
    """
    yaml = ruamel.yaml.YAML()
    # Load the file
    with open(path) as f:
        values_dict = yaml.load(f.read())
    
    # Iterate the kartons list
    kartons = values_dict["kartons"]
    for karton in kartons:
        # Don't try to update karton's that are from certpl
        if "certpl" in karton['image']:
            continue
        if karton["name"] not in name_to_image_tag:
            raise Exception(f"{karton['name']} not in {name_to_image_tag.keys()}")
        karton['imageTag'] = name_to_image_tag[karton['name']]

        name_to_image_tag.pop(karton['name'])
    if len(name_to_image_tag.keys()) > 0:
        raise Exception(f"Kartons unaccounted for: {name_to_image_tag.keys()}")
    
    # Dump the updated dict
    with open(path, 'w') as f:
        yaml.dump(values_dict, f)
        





def main():
    parser = argparse.ArgumentParser(description='Update karton-analyzer values file with current karton images')
    parser.add_argument('path', help='path of karton-analyzer helm chart values files', type=pathlib.Path)
    args = parser.parse_args()
    name_to_image_tag = get_karton_name_to_image_tags()
    update_values_file(name_to_image_tag, args.path)


if __name__ == "__main__":
    main()