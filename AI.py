

import streamlit as st
import io
import requests
import base64
import time
from PIL import Image, ImageOps
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(page_title="Cinematic Persona Machine", layout="centered")

st.title("🎬 The Cinematic Persona Test")
st.markdown("Answer 10 questions to reveal your movie character and generate your poster.")

# ---------- SIDEBAR ----------
with st.sidebar:
    st.header("🔑 API Configuration")
    api_key = st.text_input("Freepik API Key", type="password", value=os.getenv("FREEPIK_API_KEY", ""))
    st.page_link(label="Get your API key",page= "https://www.freepik.com/developers/dashboard/api-key")
    # debug_mode = st.checkbox("🔍 Debug Mode", value=False)

    if not api_key:
        # st.warning("Please enter your Freepik API key")
        # st.stop()
        api_key="FPSX8acb3702de3611c4fc02a2e525b564f1"

    st.markdown("---")
    st.markdown("### ⚙️ Settings")
    model_option = st.selectbox("AI Model", ["realism", "super_real", "fluid", "flexible", "zen"], index=0)
    
    # Only realism and super_real support face/structure reference images
    FACE_REF_MODELS = ["realism", "super_real"]
    if model_option not in FACE_REF_MODELS:
        st.info(f"ℹ️ **{model_option}** doesn't support face reference. Your photo will be used for prompt inspiration only.")
    
    resolution = st.selectbox("Resolution", ["1k", "2k", "4k"], index=1)
    aspect_ratio = st.selectbox("Aspect Ratio", ["square_1_1", "portrait_2_3", "widescreen_16_9"], index=0)
    creative_detailing = st.slider("Creative Detailing", 0, 100, 33)
    structure_strength = st.slider("Face Structure Strength", 0, 100, 70, 
                                   help="Only applies to realism and super_real models")

# ---------- UPLOAD ----------
uploaded_file = st.file_uploader("📸 Upload your photo", type=["jpg", "png", "jpeg"])

if not uploaded_file:
    st.info("👆 Upload a photo to begin your cinematic journey.")
    st.stop()

col1, col2 = st.columns([1, 3])
with col1:
    uploaded_file.seek(0)
    st.image(uploaded_file, caption="Your Hero", width=150)
with col2:
    st.markdown("### Now answer the questions below...")

st.divider()

# ---------- QUESTIONS ----------
col1, col2 = st.columns(2)
with col1:
    q1 = st.radio("1. In a crisis, what is your instinct?", ["Charge forward", "Protect the weak", "Analyze", "Disappear"])
    q2 = st.radio("2. Weapon of choice:", ["Heavy Broadsword", "Twin Daggers", "Strategy", "Compassion"])
    q3 = st.radio("3. Favorite time of day?", ["High Noon", "Twilight", "Midnight", "Dawn"])
    q4 = st.radio("4. Food palette:", ["Spicy", "Sweet", "Exotic", "Hearty"])
    q5 = st.radio("5. Environment:", ["Battlefield", "Cyberpunk City", "Mystical Forest", "Throne Room"])

with col2:
    q6 = st.radio("6. Greatest fear?", ["Failure", "Loneliness", "Control", "Forgotten"])
    q7 = st.radio("7. Color palette:", ["Grey & Red", "Pink & Gold", "Neon Blue", "Green & Brown"])
    q8 = st.radio("8. Enemy treatment:", ["Crush them", "Mercy", "Outsmart", "Ignore"])
    q9 = st.radio("9. Inner Animal:", ["Wolf", "Lion", "Owl", "Swan"])
    q10 = st.radio("10. Tagline style:", ["Vengeance", "Love", "Mystery", "Leadership"])

# ---------- PERSONALITY ----------
def calculate_personality():
    scores = {"WARRIOR": 0, "ROMANTIC": 0, "MYSTIC": 0, "LEADER": 0, "REBEL": 0}
    mapping = {
        q1: {"Charge forward": "WARRIOR", "Protect the weak": "ROMANTIC", "Analyze": "MYSTIC", "Disappear": "REBEL"},
        q2: {"Heavy Broadsword": "WARRIOR", "Twin Daggers": "REBEL", "Strategy": "LEADER", "Compassion": "ROMANTIC"},
        q3: {"High Noon": "WARRIOR", "Twilight": "ROMANTIC", "Midnight": "MYSTIC", "Dawn": "LEADER"},
        q4: {"Spicy": "REBEL", "Sweet": "ROMANTIC", "Exotic": "MYSTIC", "Hearty": "WARRIOR"},
        q5: {"Battlefield": "WARRIOR", "Cyberpunk City": "REBEL", "Mystical Forest": "MYSTIC", "Throne Room": "LEADER"},
        q6: {"Failure": "WARRIOR", "Loneliness": "ROMANTIC", "Control": "LEADER", "Forgotten": "MYSTIC"},
        q7: {"Grey & Red": "WARRIOR", "Pink & Gold": "ROMANTIC", "Neon Blue": "REBEL", "Green & Brown": "MYSTIC"},
        q8: {"Crush them": "WARRIOR", "Mercy": "ROMANTIC", "Outsmart": "LEADER", "Ignore": "REBEL"},
        q9: {"Wolf": "WARRIOR", "Lion": "LEADER", "Owl": "MYSTIC", "Swan": "ROMANTIC"},
        q10: {"Vengeance": "WARRIOR", "Love": "ROMANTIC", "Mystery": "MYSTIC", "Leadership": "LEADER"},
    }
    for answer, m in mapping.items():
        if answer in m:
            scores[m[answer]] += 2
    return max(scores, key=scores.get)

profiles = {
    "WARRIOR": {
        "title": "THE LAST RAJA",
        "tagline": "Steel is the only language.",
        "variants": [
            {
                "name": "🔥 Battlefield Inferno",
                "prompt": "Epic war movie poster. A lone armored warrior stands on a burning battlefield at dusk, silhouetted against a sky of fire and smoke. Massive armies clash in the background. The hero wears ornate battle armor with golden engravings, holding a massive sword. Dramatic volumetric lighting, embers floating in air, dust and ash. Title \'THE LAST RAJA\' blazes across the top in ancient carved gold lettering. Tagline \'Steel is the only language.\' etched below in worn bronze. Professional movie poster composition, photorealistic, 4K."
            },
            {
                "name": "⚔️ Throne of Ashes",
                "prompt": "Cinematic war epic movie poster. A fierce warrior king sits on a throne built from broken swords and shields, ruins of a destroyed palace around him. Battle-scarred armor, gaze cold and commanding. Blood-red sky through crumbling columns. Dramatic chiaroscuro lighting. Title \'THE LAST RAJA\' in cracked stone lettering at top. Tagline \'Steel is the only language.\' in ember-glow font. Photorealistic, 4K."
            },
            {
                "name": "🌑 Shadow General",
                "prompt": "Dark fantasy war movie poster. A powerful warrior general emerges from swirling shadows and battle smoke, half his face lit by torchlight. Black ornate armor with red war markings. Lightning strikes on the stormy battlefield behind. His army barely visible in the fog. Title \'THE LAST RAJA\' in jagged silver letters at top. Tagline \'Steel is the only language.\' in blood-red drip style. Cinematic, photorealistic, blockbuster quality, 4K."
            },
        ]
    },
    "ROMANTIC": {
        "title": "ETERNAL EMBRACE",
        "tagline": "A love that defies time.",
        "variants": [
            {
                "name": "🌅 Golden Hour",
                "prompt": "Romantic drama movie poster. A figure stands on a hilltop at golden hour, silhouetted against a breathtaking sunset sky of deep orange and rose pink. Soft wind blows through hair and fabric. The scene feels timeless, like a classic Hollywood romance. Soft bokeh foreground with wildflowers. Title \'ETERNAL EMBRACE\' in elegant golden serif font at top. Tagline \'A love that defies time.\' in delicate cursive below. Photorealistic, warm tones, 4K."
            },
            {
                "name": "🌊 Ocean Edge",
                "prompt": "Epic romance movie poster. A figure stands at the edge of dramatic ocean cliffs at sunset, waves crashing below in mist. Dress and coat billow dramatically in the wind. Sky painted in violet, amber and deep blue. Cinematic wide shot. Title \'ETERNAL EMBRACE\' in large elegant white letters at top. Tagline \'A love that defies time.\' in italic gold below. Hollywood movie poster quality, photorealistic, 4K."
            },
            {
                "name": "🕯️ Candlelit Drama",
                "prompt": "Intimate romantic drama movie poster. Close portrait surrounded by dozens of candlelights melting into soft bokeh. Deep shadows and warm amber glow create intense intimacy. Tears on a cheek catch the light. Title \'ETERNAL EMBRACE\' in dark romantic serif font across the top. Tagline \'A love that defies time.\' in whisper-thin letters below. Cinematic portrait, photorealistic, award-worthy composition, 4K."
            },
        ]
    },
    "MYSTIC": {
        "title": "THE SILENT SAGE",
        "tagline": "Knowledge is deadly.",
        "variants": [
            {
                "name": "🌿 Forest Oracle",
                "prompt": "Dark fantasy mystery movie poster. A lone hooded sage stands in an ancient mystical forest at midnight. Glowing runes carved into massive trees pulse with blue-green light. Thick fog swirls at ground level. The sage holds an ancient glowing book. Moonlight filters through the canopy. Title \'THE SILENT SAGE\' in glowing rune-carved letters at top. Tagline \'Knowledge is deadly.\' fading into mist below. Photorealistic, cinematic, 4K."
            },
            {
                "name": "✨ Cosmic Seer",
                "prompt": "Sci-fi mystical movie poster. A cloaked figure floats in a cosmic void, surrounded by swirling galaxies, ancient star maps and floating celestial orbs. Robes made of living starlight. One hand raised, pulling constellations into a vortex. Deep space background of nebula purples and blues. Title \'THE SILENT SAGE\' in constellation-dot lettering across the top. Tagline \'Knowledge is deadly.\' in glowing gold below. Epic cinematic, photorealistic, 4K."
            },
            {
                "name": "🔮 Temple of Shadows",
                "prompt": "Dark thriller movie poster. A shadowed figure in ancient robes stands at the entrance of a massive underground temple. Torchlight reveals intricate serpent carvings. The floor floods with shallow water reflecting eerie light. Smoke and incense fill the air. Only intense eyes visible under the hood. Title \'THE SILENT SAGE\' carved in stone letters at top. Tagline \'Knowledge is deadly.\' in blood-red ink below. Cinematic, photorealistic, 4K."
            },
        ]
    },
    "LEADER": {
        "title": "THE CROWN'S BURDEN",
        "tagline": "To lead is to sacrifice.",
        "variants": [
            {
                "name": "👑 The Throne",
                "prompt": "Royal political drama movie poster. A solitary ruler sits on an enormous ornate throne in a grand palace hall. Towering marble columns, stained glass casting colored light. Heavy crown and elaborate royal garments, expression weary but resolute. Empty throne room. Title \'THE CROWN\'S BURDEN\' in regal gold embossed font at top. Tagline \'To lead is to sacrifice.\' in silver below. Dramatic cinematic lighting, photorealistic, 4K."
            },
            {
                "name": "🌆 Modern Power",
                "prompt": "Political thriller movie poster. A powerful modern leader stands at floor-to-ceiling glass windows overlooking a massive city skyline at night. Back turned to camera, sharp tailored suit. The city lights blur below like a sea of responsibility. Reflection in the glass shows a determined face. Title \'THE CROWN\'S BURDEN\' in bold clean white font at top. Tagline \'To lead is to sacrifice.\' in muted gold below. Cinematic, photorealistic, 4K."
            },
            {
                "name": "⚡ The Rally",
                "prompt": "Epic leadership drama movie poster. A charismatic leader stands on a podium before a crowd of thousands, arms raised, dramatic storm clouds gathering above with lightning. Searchlights sweep the sky. The crowd looks up with hope. Dramatic upward angle makes the leader appear monumental. Title \'THE CROWN\'S BURDEN\' in powerful bold typography at top. Tagline \'To lead is to sacrifice.\' below. Photorealistic, cinematic blockbuster quality, 4K."
            },
        ]
    },
    "REBEL": {
        "title": "NEON OUTCAST",
        "tagline": "Break the system.",
        "variants": [
            {
                "name": "🌧️ Neon Rain",
                "prompt": "Cyberpunk action movie poster. A lone rebel stands in a rain-soaked alley at night, neon signs reflecting in puddles. Leather jacket, cybernetic eye implant. Massive holographic advertisements flicker on towering buildings above. Rain streaks caught in neon light. Expression defiant and dangerous. Title \'NEON OUTCAST\' in glitching neon pink and blue letters at top. Tagline \'Break the system.\' in electric green below. Cinematic, photorealistic, blade runner aesthetic, 4K."
            },
            {
                "name": "💥 System Crash",
                "prompt": "Sci-fi rebellion movie poster. A hacker sits in a dark server room surrounded by glowing monitors showing crashing systems and code waterfalls. Hoodie up, face half-lit by screen glow. Warning alarms flash red. Title \'NEON OUTCAST\' in corrupted digital font at top. Tagline \'Break the system.\' in terminal green code below. Cinematic, photorealistic, 4K."
            },
            {
                "name": "🏍️ Midnight Rider",
                "prompt": "Action thriller movie poster. A rebel rides a futuristic neon-lit motorcycle at full speed through a cyberpunk highway at midnight, police drones in pursuit with searchlights. Motion blur, sparks flying. The rider looks back — fearless. Title \'NEON OUTCAST\' in slanted speed-blur neon font at top. Tagline \'Break the system.\' in exhaust-smoke lettering below. Epic cinematic, photorealistic, 4K."
            },
        ]
    },
}

# ---------- API FUNCTIONS ----------
def poll_task(api_key, task_id, debug=False):
    url = f"https://api.freepik.com/v1/ai/mystic/{task_id}"
    headers = {"x-freepik-api-key": api_key}
    progress = st.progress(0)
    status_text = st.empty()

    for attempt in range(40):
        status_text.text(f"🎨 Generating... ({attempt + 1}/40)")
        progress.progress((attempt + 1) / 40)
        try:
            r = requests.get(url, headers=headers, timeout=15)
            if debug:
                st.write(f"Poll {attempt+1}: status={r.status_code}, body={r.text[:300]}")
            if r.status_code == 200:
                data = r.json().get("data", {})
                status = data.get("status", "")
                if status in ("SUCCEEDED", "COMPLETED"):
                    progress.empty()
                    status_text.empty()
                    return data.get("generated", [])
                elif status == "FAILED":
                    progress.empty()
                    status_text.empty()
                    st.error(f"Generation failed: {data.get('error', 'Unknown error')}")
                    return None
        except Exception as e:
            if debug:
                st.warning(f"Poll error: {e}")
        time.sleep(3)

    progress.empty()
    status_text.empty()
    st.warning("Timed out waiting for image. Try again.")
    return None


def generate_image(api_key, prompt, image_base64, model, resolution, aspect_ratio, creative_detailing, structure_strength, debug=False):
    url = "https://api.freepik.com/v1/ai/mystic"
    headers = {"Content-Type": "application/json", "x-freepik-api-key": api_key, "Accept": "application/json"}
    FACE_REF_MODELS = ["realism", "super_real"]
    payload = {
        "prompt": prompt,
        "model": model,
        "resolution": resolution,
        "aspect_ratio": aspect_ratio,
        "creative_detailing": creative_detailing,
        "filter_nsfw": True,
    }
    if model in FACE_REF_MODELS and image_base64:
        payload["structure_reference"] = image_base64
        payload["structure_strength"] = structure_strength
    if debug:
        st.write("Sending request to Freepik API...")
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=30)
        if debug:
            st.write(f"Response status: {r.status_code}")
            st.write(f"Response body: {r.text[:500]}")
        if r.status_code == 200:
            result = r.json()
            data = result.get("data", {})
            # Direct result
            if "generated" in data and data["generated"]:
                return data["generated"]
            # Async task
            if "task_id" in data:
                return poll_task(api_key, data["task_id"], debug)
            st.error(f"Unexpected response structure: {data}")
        elif r.status_code == 401:
            st.error("❌ Invalid API key (401). Check your Freepik API key.")
        elif r.status_code == 429:
            st.error("⚠️ Rate limit exceeded. Please wait and try again.")
        else:
            st.error(f"❌ API error {r.status_code}: {r.text[:300]}")
    except requests.exceptions.Timeout:
        st.error("⏱️ Request timed out.")
    except Exception as e:
        st.error(f"Error: {e}")
        if debug:
            st.exception(e)
    return None


def display_image_from_result(image_item):
    """Handle all possible image formats from Freepik API response."""
    if isinstance(image_item, str):
        # Could be a URL or base64
        if image_item.startswith("http"):
            # It's a URL - fetch and display
            try:
                img_response = requests.get(image_item, timeout=30)
                img = Image.open(io.BytesIO(img_response.content))
                st.image(img, use_container_width=True)
                return image_item  # return URL for download
            except Exception as e:
                st.error(f"Failed to load image from URL: {e}")
                st.markdown(f"[🔗 Open image directly]({image_item})")
                return image_item
        else:
            # Assume base64
            try:
                img_bytes = base64.b64decode(image_item)
                img = Image.open(io.BytesIO(img_bytes))
                st.image(img, use_container_width=True)
                return image_item
            except Exception as e:
                st.error(f"Failed to decode base64 image: {e}")
                return None

    elif isinstance(image_item, dict):
        # Could be {"url": "..."} or {"base64": "..."}
        if "url" in image_item:
            return display_image_from_result(image_item["url"])
        elif "base64" in image_item:
            return display_image_from_result(image_item["base64"])
        else:
            st.error(f"Unknown image dict format: {list(image_item.keys())}")
            # if debug_mode:
            #     st.write(image_item)
            return None
    else:
        st.error(f"Unknown image format: {type(image_item)}")
        return None


# ---------- GENERATE BUTTON ----------
import random

if st.button("🎬 Reveal My Persona", type="primary"):
    personality = calculate_personality()
    profile = profiles[personality]
    st.session_state["personality"] = personality
    st.session_state["profile"] = profile
    st.session_state["show_variants"] = True

if st.session_state.get("show_variants"):
    personality = st.session_state["personality"]
    profile = st.session_state["profile"]

    st.divider()
    st.markdown(f"## 🎭 You are: **{personality}**")
    st.markdown(f"### {profile['title']}")
    st.markdown(f'*"{profile["tagline"]}"*')
    st.markdown("---")
    st.markdown("### 🎬 Choose your poster style:")

    variant_names = [v["name"] for v in profile["variants"]]
    variant_names_with_random = ["🎲 Random — Surprise me!"] + variant_names

    chosen = st.radio("Pick a cinematic style:", variant_names_with_random, key="variant_choice")

    if st.button("✨ Generate My Poster", type="primary"):
        if chosen == "🎲 Random — Surprise me!":
            selected_variant = random.choice(profile["variants"])
            st.info(f"🎲 Randomly selected: **{selected_variant['name']}**")
        else:
            selected_variant = next(v for v in profile["variants"] if v["name"] == chosen)

        base_prompt = selected_variant["prompt"]
        FACE_REF_MODELS = ["realism", "super_real"]
        if model_option in FACE_REF_MODELS:
            prompt = base_prompt + " The person\'s face from the reference photo is used as the main character\'s face, integrated naturally and seamlessly into the scene."
        else:
            prompt = base_prompt

        # if debug_mode:
        #     st.markdown("**Prompt:**")
        #     st.info(prompt)

        # Process image
        with st.spinner("Processing your photo..."):
            uploaded_file.seek(0)
            raw_img = Image.open(uploaded_file).convert("RGB")
            square_img = ImageOps.fit(raw_img, (1024, 1024), centering=(0.5, 0.5))
            buf = io.BytesIO()
            square_img.save(buf, format="JPEG", quality=90)
            img_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")

        # Generate
        generated = generate_image(
            api_key=api_key,
            prompt=prompt,
            image_base64=img_base64,
            model=model_option,
            resolution=resolution,
            aspect_ratio=aspect_ratio,
            creative_detailing=creative_detailing,
            structure_strength=structure_strength,
            # debug=debug_mode,
        )

        # Display result
        if generated:
            st.divider()
            st.balloons()
            st.markdown(f"## 🎬 {profile['title']}")
            st.markdown(f"*\"{profile['tagline']}\"*")
            st.caption(f"Style: {selected_variant['name']}")

            # if debug_mode:
            #     st.write("Raw generated response:", generated)

            image_item = generated[0] if isinstance(generated, list) else generated
            image_url = display_image_from_result(image_item)

            if image_url and isinstance(image_url, str) and image_url.startswith("http"):
                st.markdown(f"[⬇️ Download / Open Full Image]({image_url})")

            with st.expander("Details"):
                st.write(f"**Personality:** {personality} | **Style:** {selected_variant['name']} | **Model:** {model_option} | **Resolution:** {resolution}")
        else:
            st.error("No image was generated. Please check your API key and try again.")

st.divider()
st.markdown("<center>Made with 🎬 Streamlit & Freepik Mystic AI</center>", unsafe_allow_html=True)