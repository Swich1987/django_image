import os


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = CURRENT_DIR.replace("/tests", "")

TEST_IMAGE_PATH = os.path.join(CURRENT_DIR, "media/images/dental-x-ray.jpeg")

TEST_IMAGE_2_FILENAME = "dental-x-ray_2"
TEST_IMAGE_2_PATH = os.path.join(CURRENT_DIR, "media/images/dental-x-ray_2.jpeg")

TEST_INVALID_IMAGE_PATH = os.path.join(CURRENT_DIR, "media/images/invalid_file.txt")
