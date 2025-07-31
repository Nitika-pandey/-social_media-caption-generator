Instagram Caption & Hashtag Generator - README (Plain Text)
============================================================

Overview:
---------
This Python command-line tool generates Instagram-ready captions, emojis, and hashtags using AI. You provide a short theme or keyword (like "sunset" or "morning coffee"), and the program produces a creative caption, analyzes its sentiment to suggest matching emojis, and adds relevant hashtags.

It uses pre-trained models from Hugging Face, so no API token or login is needed. Everything runs locally (once models are downloaded).

Features:
---------
✅ Uses GPT-2 to generate human-like captions  
✅ Adds emojis based on the sentiment of the generated text  
✅ Suggests relevant Instagram hashtags (custom + popular)  
✅ Saves each result to a timestamped `.txt` file  
✅ Requires no Hugging Face account or token  

How It Works:
-------------
1. The user enters a prompt (e.g., "new puppy", "beach vacation").
2. The GPT-2 model generates a creative caption.
3. The sentiment analysis model evaluates whether the caption is positive, negative, or neutral.
4. The program selects a few random emojis based on that sentiment.
5. Hashtags are formed by combining keywords from the prompt and popular Instagram tags.
6. All content is printed to the terminal and saved in the `GeneratedInstagramPosts/` folder.

Technologies Used:
------------------
- **Python 3**
- **Hugging Face Transformers Library**
  - `gpt2` (text-generation model)
  - `distilbert-base-uncased-finetuned-sst-2-english` or similar (sentiment model)
- **Built-in Libraries**: `os`, `datetime`, `random`

Example Output:
---------------
Prompt: new puppy  
Caption: Welcome home, little buddy! You're already part of the family.  
Emojis: ❤️🐶🎉  
Hashtags: #newpuppy #love #picoftheday #instadaily #happy #puppygram #petlovers #cute #dogsofinstagram #photooftheday  

File Saved:
-----------
`GeneratedInstagramPosts/instagram_post_20250731_142623.txt`

Usage:
------
1. Ensure Python and `transformers` are installed:
2. pip install transformers

2. Run the script:
3. python instagram_generator.py
4. Follow the prompt and enter a caption theme. Example:
5. The output will be displayed and saved in a `.txt` file.

Folder Structure:
-----------------
- instagram_generator.py
- README.txt
- GeneratedInstagramPosts/
 - instagram_post_YYYYMMDD_HHMMSS.txt

License:
--------
MIT License – free to use, modify, and distribute.

Credits:
--------
Built using OpenAI's GPT-2 model and Hugging Face Transformers library.
Created to automate and simplify social media content creation using AI.
