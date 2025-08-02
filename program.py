import random
import datetime
import os
import gradio as gr
from transformers import pipeline

# Load models
print("Loading models...")
caption_generator = pipeline("text-generation", model="gpt2")
sentiment_pipeline = pipeline("sentiment-analysis")
print("Models loaded.")

# Define emojis
emoji_dict = {
    "positive": ["😊", "🌟", "🔥", "💪", "🚀", "✨", "❤️", "👍", "😁", "🎉"],
    "negative": ["😢", "😞", "💔", "😠", "😓", "👎", "😟", "😭", "🤦‍♀️"],
    "neutral": ["🙂", "😐", "🧐", "🤔", "😶", "👀", "🤷‍♀️", "👌"]
}

# Clean hashtags (shorter and broader)
common_hashtags = [
    "#instadaily", "#picoftheday", "#photooftheday", "#love", "#instagood",
    "#travelgram", "#foodie", "#fashion", "#lifestyle", "#beautiful", "#happy",
    "#art", "#nature", "#motivation", "#explore"
]

# Banned or inappropriate words
banned_words = {"kill", "hate", "nude", "violence", "drugs", "weapon", "die", "blood"}

def clean_caption(text):
    """Limit to 8 words, remove banned words."""
    words = text.split()
    clean_words = [w for w in words if w.lower() not in banned_words]
    return ' '.join(clean_words[:8]).strip()

def get_emojis(text):
    """Get sentiment-based emojis."""
    sentiment = sentiment_pipeline(text)[0]['label'].lower()
    if "pos" in sentiment:
        category = "positive"
    elif "neg" in sentiment:
        category = "negative"
    else:
        category = "neutral"
    return ''.join(random.sample(emoji_dict[category], 3))

def get_hashtags(prompt):
    words = [w.strip("#").lower() for w in prompt.split() if w.isalpha()]
    tags = ["#" + w for w in words if len(w) > 3]
    all_tags = list(set(tags + common_hashtags))
    return ' '.join(random.sample(all_tags, min(10, len(all_tags))))

def generate_instagram_post(prompt_text):
    if not prompt_text.strip():
        return "❌ Please enter a prompt to generate content."

    try:
        raw = caption_generator(prompt_text, max_length=50, num_return_sequences=1)[0]['generated_text']
        caption = raw.strip()

        # Remove prompt if repeated
        if caption.lower().startswith(prompt_text.lower()):
            caption = caption[len(prompt_text):].lstrip(".,;!?- ").strip()

        # Filter caption
        caption = clean_caption(caption)
        if not caption:
            caption = "Captured a special moment"

        emojis = get_emojis(caption)
        hashtags = get_hashtags(prompt_text)

        # Save output
        save_dir = "GeneratedInstagramPosts"
        os.makedirs(save_dir, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(save_dir, f"post_{timestamp}.txt")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Prompt: {prompt_text}\n")
            f.write(f"Caption: {caption}\n")
            f.write(f"Emojis: {emojis}\n")
            f.write(f"Hashtags: {hashtags}\n")

        return f"📝 **Caption:** {caption}\n😀 **Emojis:** {emojis}\n#️⃣ **Hashtags:** {hashtags}"

    except Exception as e:
        return f"❌ Error occurred: {str(e)}"

# Gradio Interface
demo = gr.Interface(
    fn=generate_instagram_post,
    inputs=gr.Textbox(
        lines=2,
        placeholder="Enter a theme or phrase (e.g., 'sunset by the ocean')",
        label="Enter your Instagram prompt"
    ),
    outputs=gr.Textbox(label="Generated Caption + Emojis + Hashtags"),
    title="📸 Instagram Caption & Hashtag Generator",
    description="Creates short, safe, stylish captions powered by GPT-2 & sentiment analysis. No downloads required."
)

if __name__ == "__main__":
    demo.launch()
