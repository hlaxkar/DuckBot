
## DuckBot

DuckBot is a Telegram bot that can perform several tasks, including sending wallpapers, duck, cat and dog images, downloading and sending YouTube videos as audio to the user, and resizing images to fit a specific ratio without lowering the quality or cropping the image. DuckBot keeps track of all the videos it has sent by storing their IDs in a SQLite database.

### Installation

1. Clone the repository to your local machine
2. Install the required packages by running `pip install -r requirements.txt`
3. Create a Telegram bot by following the instructions [here](https://core.telegram.org/bots#6-botfather)
4. Copy the bot token and paste it in the `config.py` file

### Features
- /start and /help commands to greet and guide users on how to use the bot.
- /image command to return a random wallpaper using the Unsplash API.
- /cat command to get a random cat image using the Cat API.
- /duck command to get a random duck image using the Random-d.uk API.
- Send any image to convert it into desired ratios with black borders.
- /yt command to download YouTube videos as audio.

### Image Resizing

DuckBot also includes an image resizing feature that allows users to resize their images to a specific ratio without lowering the quality or cropping the image. To use this feature, follow these steps:

1. Send an image to the bot
2. The bot will ask you to provide the desired ratio in the format `width:height`. For example, if you want the image to be in a 4:3 ratio, you would enter `4:3`.
3. The bot will add white borders to the image so that it fits the desired ratio.

### SQLite Database

DuckBot uses an SQLite database to keep track of all the videos it has sent to users. This database is automatically created when the bot is first run and is used to store the video IDs. If you need to access this database for any reason, you can find it in the `database.db` file.

### Contributing

If you want to contribute to DuckBot, feel free to submit a pull request with your changes. Before submitting, please make sure to run the tests to ensure that everything is working as expected. To run the tests, simply run `pytest` in the root directory of the project.

### License

DuckBot is released under the MIT License. See the `LICENSE` file for more information.
