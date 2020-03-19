# Facebook Post Search

Facebook Post Search is a simple Python program that filters Facebook's download file for a user's posts and outputs them to a text file.

## Notice

This application is in alpha testing, and I'm looking for additional testers.

## Requirements

Python 3.7 or later.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the required package jsonschema.

```bash
pip install jsonschema
```

## Installation

Simply copy the files to a directory that can run Python.

## Usage

Log into Facebook and go to Settings > Your Facebook Information > Download Your Information. Request your post file in the JSON format. Facebook takes a little while to put together the file and will notify you when it's ready for download.

Download the zip file, unzip it, and put your_posts.json somewhere that can access Python. (You can change the filename if you want, the application doesn't care.)

From the command line:

```bash
fbpostsearch.py "FILEPATH"  # example "D:\Data\your_posts.json"
```

## Support

[Report an issue](https://github.com/glosborne/fbpostsearch/issues) if you have problems.

## Notes

This is my first open-source project.  Be gentle.

Facebook changes things often and with no notice.  I'm checking twice a month to see if their JSON schema or encoding has changed, and will update the application accordingly.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)