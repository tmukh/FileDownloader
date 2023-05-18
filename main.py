import os, sys
import mimetypes
import wget

class FileDownloader:
    # Initialize the object with the file name
    def __init__(self, file):
        self.file = file

    # Download the images from all the urls
    def download_images(self):

        # Start of by reading in the file and making a folder, so not all images are int he . directory.
        urls = self.parse_urls()
        self.make_folder()

        # Try catch in case we get non-images (Unit tests on this later)
        for url in urls:
            try:
                name = self.name_file(url)
                path = os.path.join("images", name)
                wget.download(url, out=path)

                # Verify that download is of image type (jpeg, png, etc.)
                if self.is_image(path):
                    print(f" | Image successfully downloaded: {name}")
                # Otherwise skip file
                else:
                
                    os.remove(path)
                    print(f"Skipping file: {name}, Invalid extension")
            # Only really thrown with 404 or 403
            except Exception as e:
                print(f"Error downloading {url}: {str(e)}")

    # Use python's annoying parsing library  
    def parse_urls(self):
        
        with open(self.file, 'r') as file:
            urls_list = file.read().splitlines()
        return urls_list

    # Create the 'images' folder, if it already exists, do nothing
    def make_folder(self):
        os.makedirs("images", exist_ok=True)

    # Turn url into an array, split at '/' and take the last element
    def name_file(self, url):
        return url.split("/")[-1]

    # Okay, to be honest, I have no idea. This is from StackOverflow
    # https://docs.python.org/3/library/mimetypes.html
    # https://stackoverflow.com/questions/43580/how-to-find-the-mime-type-of-a-file-in-python
    def is_image(self, filepath):
        mime_type, _ = mimetypes.guess_type(filepath)
        return mime_type and mime_type.startswith("image")
    
if __name__ == '__main__':
    # Make sure that the right command in the terminal was used.
    # I got this from a youtube video, it was something about user safety python modules? I can't remember.
    if len(sys.argv) != 2: # 2 is arbitrary, this is the number of args.
        print("Please use the following command: python main.py <File containing urls>")
        sys.exit(1)

    # Make sure the file exists in the first place (Human error proofing)
    url_file = sys.argv[1]
    if not os.path.isfile(url_file):
        print(f"File not found: {url_file}")
        sys.exit(1)
    
    objd = FileDownloader(url_file)
    objd.download_images()