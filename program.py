import os
import datetime
import random
from transformers import pipeline

# --- Hugging Face Models ---
# These models will be downloaded by the 'transformers' library on first run.
# They are public models and generally do not require a Hugging Face token for basic usage.
print("Loading GPT-2 text generation model (this happens once)...")
caption_generator_text_to_text = pipeline("text-generation", model="gpt2")
print("Loading sentiment analysis model (this happens once)...")
sentiment_pipeline = pipeline("sentiment-analysis")
print("AI models loaded successfully!")

emoji_dict = {
    "positive": ["😊", "🌟", "🔥", "💪", "🚀", "✨", "❤️", "👍", "😁", "🎉"],
    "negative": ["😢", "😞", "💔", "😠", "😓", "👎", "😟", "😭", "🤦‍♀️"],
    "neutral": ["🙂", "😐", "🧐", "🤔", "😶", "👀", "🤷‍♀️", "👌"]
}

# Instagram-specific hashtags
instagram_hashtags_data = [
    "#instadaily", "#igers", "#picoftheday", "#photooftheday", "#love", "#instagood",
    "#travelgram", "#foodie", "#fashion", "#lifestyle", "#beautiful", "#happy",
    "#art", "#nature", "#inspiration", "#motivation", "#explore", "#discover"
]

# --- Helper Functions ---

def get_emojis(text):
    """Determines sentiment of text and returns a few relevant emojis."""
    sentiment_result = sentiment_pipeline(text)
    label = sentiment_result[0]['label'].lower() # e.g., 'positive', 'negative', 'neutral'

    emojis_for_sentiment = emoji_dict.get(label, ["🙂"]) # Default to neutral if sentiment not found

    # Ensure we don't try to pick more emojis than available
    num_emojis_to_pick = min(3, len(emojis_for_sentiment))
    
    selected_emojis = random.sample(emojis_for_sentiment, num_emojis_to_pick)
    
    return ''.join(selected_emojis)

def get_instagram_hashtags(prompt_text):
    """Generates Instagram-specific hashtags based on a prompt."""
    words = prompt_text.lower().split()
    # Create tags from words longer than 3 characters
    tags = ["#" + word.replace(" ", "") for word in words if len(word) > 3]

    all_possible_tags = tags + instagram_hashtags_data
    unique_tags = list(set(all_possible_tags))
    num_tags_to_select = min(10, len(unique_tags)) # Aim for up to 10 unique hashtags for Instagram
    
    selected_hashtags = random.sample(unique_tags, num_tags_to_select)
    return " ".join(selected_hashtags)

# --- Main Program Logic ---
def main():
    print("📸 Instagram Caption & Hashtag Generator (Command Line) 📸")
    print("---------------------------------------------------------")
    print("This tool generates captions, emojis, and hashtags for Instagram based on your text input.")
    print("It uses publicly available AI models and does NOT require a Hugging Face token.")
    print("Ensure you have an active internet connection for initial model download.")
    print("---------------------------------------------------------")

    # Removed token handling: The program no longer explicitly asks for a token.
    # Public models in transformers.pipeline generally work without one.

    prompt_text = input("Enter a keyword or theme for your Instagram post (e.g., 'beautiful sunset', 'morning coffee', 'new pet'): ").strip()

    if not prompt_text:
        print("🔴 No prompt entered. Exiting.")
        return

    print(f"\n🧠 Generating Instagram content based on: '{prompt_text}'...")

    try:
        # Generate raw text from GPT-2
        generated_raw_text = caption_generator_text_to_text(
            prompt_text,
            max_length=80, # Limit length of generated text
            num_return_sequences=1,
            no_repeat_ngram_size=2, # Helps reduce repetitive phrases
            early_stopping=True # Stops generation early if a natural end is found
        )[0]['generated_text']

        # Post-process the generated text to clean up GPT-2's conversational style
        caption = generated_raw_text.strip()
        # Remove the input prompt if GPT-2 repeated it at the beginning
        if caption.lower().startswith(prompt_text.lower()):
            caption = caption[len(prompt_text):].strip()
            # Remove any leading punctuation or spaces that might remain after prompt removal
            caption = caption.lstrip(".,;!?- ").strip()

        # Fallback if the cleaned caption is empty
        if not caption:
            caption = "A beautiful moment captured." # Generic fallback
            
        # Ensure caption is not too long for Instagram (approx 2200, but shorter is better)
        if len(caption) > 500: # A more generous but still reasonable limit for Instagram
            caption = caption[:497] + "..."

        # Generate emojis based on the *final generated caption* for sentiment
        emojis = get_emojis(caption)
        
        # Generate hashtags based on the *original prompt text* for broader relevance
        hashtags = get_instagram_hashtags(prompt_text)

        print("\n--- ✨ Generated Instagram Post ✨ ---")
        print(f"Caption: {caption}")
        print(f"Emojis: {emojis}")
        print(f"Hashtags: {hashtags}")
        print("------------------------------------------")

        # Save the generated post to a file
        save_dir = "GeneratedInstagramPosts"
        os.makedirs(save_dir, exist_ok=True) # Create directory if it doesn't exist
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = os.path.join(save_dir, f"instagram_post_{timestamp}.txt")

        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(f"--- Instagram Post ---\n")
            f.write(f"Prompt: {prompt_text}\n")
            f.write("-" * 30 + "\n")
            f.write(f"Caption: {caption}\n")
            f.write(f"Emojis: {emojis}\n")
            f.write(f"Hashtags: {hashtags}\n")
            f.write(f"Generated at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        print(f"\n✅ Generated post successfully saved to: {output_filename}")

    except Exception as e:
        print(f"❌ A critical error occurred during Instagram content generation: {e}")
        print("Please review the error message and ensure all steps (installation, internet) are correct.")

if __name__ == "__main__":
    main()
