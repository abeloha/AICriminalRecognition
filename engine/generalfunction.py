import os

def check_path_exists(path):
    #dir = os.path.dirname(path)
    if not os.path.exists(path):
        return 0
    return 1

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

def get_images(path):
    imagePaths = []
    for root, dirs, files in os.walk(os.path.abspath(path)):
        for file in files:
            imagePaths.append(os.path.join(root, file))
            #print(os.path.join(root, file))

    return imagePaths

