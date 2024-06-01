# Starry Ai Discord Bot
A Discord bot that generates images based on user prompts using the StarryAI API. The bot supports various art styles and image sizes, and can generate multiple images per request.

## Features
- Generate images using various art styles.
- Choose image sizes and the number of images to generate.
- Automatically completes options for art styles, sizes, and the number of images.
- Provides helpful commands.

#Setup
Clone the repository:

```bash
git clone https://github.com/itachi1621/Starry-Ai-Discord-Bot.git
cd Starry-Ai-Discord-Bot
```
## Install dependencies:
```bash
pip install discord aiohttp python-dotenv
```
or

```bash
pip install -r requirements.txt
```

## Create a .env file:
```plaintext
DISCORD_BOT_TOKEN=your_discord_bot_token
STARRY_AI_KEY=your_starry_ai_api_key
EMBED_COLOR=your_embed_color_in_hex
BOT_NAME=your_bot_name
GENERATION_STEPS=40
MAX_IMAGES=5
```
## Run the bot:

```bash
python Starry_Bot.py
```

## Usage
The bot supports the following commands:

- `/create_pic`

Generates an image based on the provided prompt.

- Prompt: The text prompt for image generation.
- Style:  The art style for the image.
- Size: (Optional) The size of the image (square, landscape, portrait, wide).
- Number of Images: (Optional) The number of images to generate.

- `/help`
Displays the help message with a list of available commands.

### Example Command
```arduino
/create_pic prompt="A sunset over a mountain" style="fantasy" size="landscape" number_of_images="2"
```
### Response
The bot will generate and send images based on the provided prompt and options.

## Contributing
Feel free to open issues or submit pull requests if you have suggestions or improvements.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements
Special thanks to the creators of the StarryAI API for providing an excellent image generation service.
