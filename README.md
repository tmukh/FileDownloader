# Image Downloader

This repository contains a Python script that downloads images from a plaintext file containing URLs and saves them to the hard disk..

## Installation & Usage

Clone this repo to your local machine

1. Clone this repository to your local machine using the following command:

   ```bash
   git clone https://github.com/tmukh/FileDownloader.git
   ```

2. Cd into the main directory:

   ```bash
   cd FileDownloader
   ```
3. The script expect a URL file, please make sure your *urls.txt* file is in the same directory as the script

    ```bash
    python main.py <url_text_file_name.txt>
    ```

Replace `<input_file>` with your txt file.

### Example usage:

```bash
python main.py urls.txt
```
After launching the script it will download all images to the new *images/* folder

## Testing

We also includes a test file, `tests.py`, in order to check for image integrity and availability.

```bash
python -m unittest main.py
```
