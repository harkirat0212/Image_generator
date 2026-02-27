

# import streamlit as st
# import io
# import requests
# import base64
# import time
# from PIL import Image, ImageOps
# # from dotenv import load_dotenv
# import os

# # load_dotenv()

# st.set_page_config(page_title="Cinematic Persona Machine", layout="centered")

# st.title("🎬 The Cinematic Persona Test")
# st.markdown("Answer 10 questions to reveal your movie character and generate your poster.")

# # ---------- SIDEBAR ----------
# with st.sidebar:
#     st.header("🔑 API Configuration")
#     api_key = st.text_input("Freepik API Key", type="password", value=os.getenv("FREEPIK_API_KEY", ""))
#     st.page_link(label="Get your API key",page= "https://www.freepik.com/developers/dashboard/api-key")
#     # debug_mode = st.checkbox("🔍 Debug Mode", value=False)

#     if not api_key:
#         # st.warning("Please enter your Freepik API key")
#         # st.stop()
#         api_key="FPSX8acb3702de3611c4fc02a2e525b564f1"

#     st.markdown("---")
#     st.markdown("### ⚙️ Settings")
#     model_option = st.selectbox("AI Model", ["realism", "super_real", "fluid", "flexible", "zen"], index=0)
    
#     # Only realism and super_real support face/structure reference images
#     FACE_REF_MODELS = ["realism", "super_real"]
#     if model_option not in FACE_REF_MODELS:
#         st.info(f"ℹ️ **{model_option}** doesn't support face reference. Your photo will be used for prompt inspiration only.")
    
#     resolution = st.selectbox("Resolution", ["1k", "2k", "4k"], index=1)
#     aspect_ratio = st.selectbox("Aspect Ratio", ["square_1_1", "portrait_2_3", "widescreen_16_9"], index=0)
#     creative_detailing = st.slider("Creative Detailing", 0, 100, 33)
#     structure_strength = st.slider("Face Structure Strength", 0, 100, 70, 
#                                    help="Only applies to realism and super_real models")

# # ---------- UPLOAD ----------
# uploaded_file = st.file_uploader("📸 Upload your photo", type=["jpg", "png", "jpeg"])

# if not uploaded_file:
#     st.info("👆 Upload a photo to begin your cinematic journey.")
#     st.stop()

# col1, col2 = st.columns([1, 3])
# with col1:
#     uploaded_file.seek(0)
#     st.image(uploaded_file, caption="Your Hero", width=150)
# with col2:
#     st.markdown("### Now answer the questions below...")

# st.divider()

# # ---------- QUESTIONS ----------
# col1, col2 = st.columns(2)
# with col1:
#     q1 = st.radio("1. In a crisis, what is your instinct?", ["Charge forward", "Protect the weak", "Analyze", "Disappear"])
#     q2 = st.radio("2. Weapon of choice:", ["Heavy Broadsword", "Twin Daggers", "Strategy", "Compassion"])
#     q3 = st.radio("3. Favorite time of day?", ["High Noon", "Twilight", "Midnight", "Dawn"])
#     q4 = st.radio("4. Food palette:", ["Spicy", "Sweet", "Exotic", "Hearty"])
#     q5 = st.radio("5. Environment:", ["Battlefield", "Cyberpunk City", "Mystical Forest", "Throne Room"])

# with col2:
#     q6 = st.radio("6. Greatest fear?", ["Failure", "Loneliness", "Control", "Forgotten"])
#     q7 = st.radio("7. Color palette:", ["Grey & Red", "Pink & Gold", "Neon Blue", "Green & Brown"])
#     q8 = st.radio("8. Enemy treatment:", ["Crush them", "Mercy", "Outsmart", "Ignore"])
#     q9 = st.radio("9. Inner Animal:", ["Wolf", "Lion", "Owl", "Swan"])
#     q10 = st.radio("10. Tagline style:", ["Vengeance", "Love", "Mystery", "Leadership"])

# # ---------- PERSONALITY ----------
# def calculate_personality():
#     scores = {"WARRIOR": 0, "ROMANTIC": 0, "MYSTIC": 0, "LEADER": 0, "REBEL": 0}
#     mapping = {
#         q1: {"Charge forward": "WARRIOR", "Protect the weak": "ROMANTIC", "Analyze": "MYSTIC", "Disappear": "REBEL"},
#         q2: {"Heavy Broadsword": "WARRIOR", "Twin Daggers": "REBEL", "Strategy": "LEADER", "Compassion": "ROMANTIC"},
#         q3: {"High Noon": "WARRIOR", "Twilight": "ROMANTIC", "Midnight": "MYSTIC", "Dawn": "LEADER"},
#         q4: {"Spicy": "REBEL", "Sweet": "ROMANTIC", "Exotic": "MYSTIC", "Hearty": "WARRIOR"},
#         q5: {"Battlefield": "WARRIOR", "Cyberpunk City": "REBEL", "Mystical Forest": "MYSTIC", "Throne Room": "LEADER"},
#         q6: {"Failure": "WARRIOR", "Loneliness": "ROMANTIC", "Control": "LEADER", "Forgotten": "MYSTIC"},
#         q7: {"Grey & Red": "WARRIOR", "Pink & Gold": "ROMANTIC", "Neon Blue": "REBEL", "Green & Brown": "MYSTIC"},
#         q8: {"Crush them": "WARRIOR", "Mercy": "ROMANTIC", "Outsmart": "LEADER", "Ignore": "REBEL"},
#         q9: {"Wolf": "WARRIOR", "Lion": "LEADER", "Owl": "MYSTIC", "Swan": "ROMANTIC"},
#         q10: {"Vengeance": "WARRIOR", "Love": "ROMANTIC", "Mystery": "MYSTIC", "Leadership": "LEADER"},
#     }
#     for answer, m in mapping.items():
#         if answer in m:
#             scores[m[answer]] += 2
#     return max(scores, key=scores.get)

# profiles = {
#     "WARRIOR": {
#         "title": "THE LAST RAJA",
#         "tagline": "Steel is the only language.",
#         "variants": [
#             {
#                 "name": "🔥 Battlefield Inferno",
#                 "prompt": "Epic war movie poster. A lone armored warrior stands on a burning battlefield at dusk, silhouetted against a sky of fire and smoke. Massive armies clash in the background. The hero wears ornate battle armor with golden engravings, holding a massive sword. Dramatic volumetric lighting, embers floating in air, dust and ash. Title \'THE LAST RAJA\' blazes across the top in ancient carved gold lettering. Tagline \'Steel is the only language.\' etched below in worn bronze. Professional movie poster composition, photorealistic, 4K."
#             },
#             {
#                 "name": "⚔️ Throne of Ashes",
#                 "prompt": "Cinematic war epic movie poster. A fierce warrior king sits on a throne built from broken swords and shields, ruins of a destroyed palace around him. Battle-scarred armor, gaze cold and commanding. Blood-red sky through crumbling columns. Dramatic chiaroscuro lighting. Title \'THE LAST RAJA\' in cracked stone lettering at top. Tagline \'Steel is the only language.\' in ember-glow font. Photorealistic, 4K."
#             },
#             {
#                 "name": "🌑 Shadow General",
#                 "prompt": "Dark fantasy war movie poster. A powerful warrior general emerges from swirling shadows and battle smoke, half his face lit by torchlight. Black ornate armor with red war markings. Lightning strikes on the stormy battlefield behind. His army barely visible in the fog. Title \'THE LAST RAJA\' in jagged silver letters at top. Tagline \'Steel is the only language.\' in blood-red drip style. Cinematic, photorealistic, blockbuster quality, 4K."
#             },
#         ]
#     },
#     "ROMANTIC": {
#         "title": "ETERNAL EMBRACE",
#         "tagline": "A love that defies time.",
#         "variants": [
#             {
#                 "name": "🌅 Golden Hour",
#                 "prompt": "Romantic drama movie poster. A figure stands on a hilltop at golden hour, silhouetted against a breathtaking sunset sky of deep orange and rose pink. Soft wind blows through hair and fabric. The scene feels timeless, like a classic Hollywood romance. Soft bokeh foreground with wildflowers. Title \'ETERNAL EMBRACE\' in elegant golden serif font at top. Tagline \'A love that defies time.\' in delicate cursive below. Photorealistic, warm tones, 4K."
#             },
#             {
#                 "name": "🌊 Ocean Edge",
#                 "prompt": "Epic romance movie poster. A figure stands at the edge of dramatic ocean cliffs at sunset, waves crashing below in mist. Dress and coat billow dramatically in the wind. Sky painted in violet, amber and deep blue. Cinematic wide shot. Title \'ETERNAL EMBRACE\' in large elegant white letters at top. Tagline \'A love that defies time.\' in italic gold below. Hollywood movie poster quality, photorealistic, 4K."
#             },
#             {
#                 "name": "🕯️ Candlelit Drama",
#                 "prompt": "Intimate romantic drama movie poster. Close portrait surrounded by dozens of candlelights melting into soft bokeh. Deep shadows and warm amber glow create intense intimacy. Tears on a cheek catch the light. Title \'ETERNAL EMBRACE\' in dark romantic serif font across the top. Tagline \'A love that defies time.\' in whisper-thin letters below. Cinematic portrait, photorealistic, award-worthy composition, 4K."
#             },
#         ]
#     },
#     "MYSTIC": {
#         "title": "THE SILENT SAGE",
#         "tagline": "Knowledge is deadly.",
#         "variants": [
#             {
#                 "name": "🌿 Forest Oracle",
#                 "prompt": "Dark fantasy mystery movie poster. A lone hooded sage stands in an ancient mystical forest at midnight. Glowing runes carved into massive trees pulse with blue-green light. Thick fog swirls at ground level. The sage holds an ancient glowing book. Moonlight filters through the canopy. Title \'THE SILENT SAGE\' in glowing rune-carved letters at top. Tagline \'Knowledge is deadly.\' fading into mist below. Photorealistic, cinematic, 4K."
#             },
#             {
#                 "name": "✨ Cosmic Seer",
#                 "prompt": "Sci-fi mystical movie poster. A cloaked figure floats in a cosmic void, surrounded by swirling galaxies, ancient star maps and floating celestial orbs. Robes made of living starlight. One hand raised, pulling constellations into a vortex. Deep space background of nebula purples and blues. Title \'THE SILENT SAGE\' in constellation-dot lettering across the top. Tagline \'Knowledge is deadly.\' in glowing gold below. Epic cinematic, photorealistic, 4K."
#             },
#             {
#                 "name": "🔮 Temple of Shadows",
#                 "prompt": "Dark thriller movie poster. A shadowed figure in ancient robes stands at the entrance of a massive underground temple. Torchlight reveals intricate serpent carvings. The floor floods with shallow water reflecting eerie light. Smoke and incense fill the air. Only intense eyes visible under the hood. Title \'THE SILENT SAGE\' carved in stone letters at top. Tagline \'Knowledge is deadly.\' in blood-red ink below. Cinematic, photorealistic, 4K."
#             },
#         ]
#     },
#     "LEADER": {
#         "title": "THE CROWN'S BURDEN",
#         "tagline": "To lead is to sacrifice.",
#         "variants": [
#             {
#                 "name": "👑 The Throne",
#                 "prompt": "Royal political drama movie poster. A solitary ruler sits on an enormous ornate throne in a grand palace hall. Towering marble columns, stained glass casting colored light. Heavy crown and elaborate royal garments, expression weary but resolute. Empty throne room. Title \'THE CROWN\'S BURDEN\' in regal gold embossed font at top. Tagline \'To lead is to sacrifice.\' in silver below. Dramatic cinematic lighting, photorealistic, 4K."
#             },
#             {
#                 "name": "🌆 Modern Power",
#                 "prompt": "Political thriller movie poster. A powerful modern leader stands at floor-to-ceiling glass windows overlooking a massive city skyline at night. Back turned to camera, sharp tailored suit. The city lights blur below like a sea of responsibility. Reflection in the glass shows a determined face. Title \'THE CROWN\'S BURDEN\' in bold clean white font at top. Tagline \'To lead is to sacrifice.\' in muted gold below. Cinematic, photorealistic, 4K."
#             },
#             {
#                 "name": "⚡ The Rally",
#                 "prompt": "Epic leadership drama movie poster. A charismatic leader stands on a podium before a crowd of thousands, arms raised, dramatic storm clouds gathering above with lightning. Searchlights sweep the sky. The crowd looks up with hope. Dramatic upward angle makes the leader appear monumental. Title \'THE CROWN\'S BURDEN\' in powerful bold typography at top. Tagline \'To lead is to sacrifice.\' below. Photorealistic, cinematic blockbuster quality, 4K."
#             },
#         ]
#     },
#     "REBEL": {
#         "title": "NEON OUTCAST",
#         "tagline": "Break the system.",
#         "variants": [
#             {
#                 "name": "🌧️ Neon Rain",
#                 "prompt": "Cyberpunk action movie poster. A lone rebel stands in a rain-soaked alley at night, neon signs reflecting in puddles. Leather jacket, cybernetic eye implant. Massive holographic advertisements flicker on towering buildings above. Rain streaks caught in neon light. Expression defiant and dangerous. Title \'NEON OUTCAST\' in glitching neon pink and blue letters at top. Tagline \'Break the system.\' in electric green below. Cinematic, photorealistic, blade runner aesthetic, 4K."
#             },
#             {
#                 "name": "💥 System Crash",
#                 "prompt": "Sci-fi rebellion movie poster. A hacker sits in a dark server room surrounded by glowing monitors showing crashing systems and code waterfalls. Hoodie up, face half-lit by screen glow. Warning alarms flash red. Title \'NEON OUTCAST\' in corrupted digital font at top. Tagline \'Break the system.\' in terminal green code below. Cinematic, photorealistic, 4K."
#             },
#             {
#                 "name": "🏍️ Midnight Rider",
#                 "prompt": "Action thriller movie poster. A rebel rides a futuristic neon-lit motorcycle at full speed through a cyberpunk highway at midnight, police drones in pursuit with searchlights. Motion blur, sparks flying. The rider looks back — fearless. Title \'NEON OUTCAST\' in slanted speed-blur neon font at top. Tagline \'Break the system.\' in exhaust-smoke lettering below. Epic cinematic, photorealistic, 4K."
#             },
#         ]
#     },
# }

# # ---------- API FUNCTIONS ----------
# def poll_task(api_key, task_id, debug=False):
#     url = f"https://api.freepik.com/v1/ai/mystic/{task_id}"
#     headers = {"x-freepik-api-key": api_key}
#     progress = st.progress(0)
#     status_text = st.empty()

#     for attempt in range(40):
#         status_text.text(f"🎨 Generating... ({attempt + 1}/40)")
#         progress.progress((attempt + 1) / 40)
#         try:
#             r = requests.get(url, headers=headers, timeout=15)
#             if debug:
#                 st.write(f"Poll {attempt+1}: status={r.status_code}, body={r.text[:300]}")
#             if r.status_code == 200:
#                 data = r.json().get("data", {})
#                 status = data.get("status", "")
#                 if status in ("SUCCEEDED", "COMPLETED"):
#                     progress.empty()
#                     status_text.empty()
#                     return data.get("generated", [])
#                 elif status == "FAILED":
#                     progress.empty()
#                     status_text.empty()
#                     st.error(f"Generation failed: {data.get('error', 'Unknown error')}")
#                     return None
#         except Exception as e:
#             if debug:
#                 st.warning(f"Poll error: {e}")
#         time.sleep(3)

#     progress.empty()
#     status_text.empty()
#     st.warning("Timed out waiting for image. Try again.")
#     return None


# def generate_image(api_key, prompt, image_base64, model, resolution, aspect_ratio, creative_detailing, structure_strength, debug=False):
#     url = "https://api.freepik.com/v1/ai/mystic"
#     headers = {"Content-Type": "application/json", "x-freepik-api-key": api_key, "Accept": "application/json"}
#     FACE_REF_MODELS = ["realism", "super_real"]
#     payload = {
#         "prompt": prompt,
#         "model": model,
#         "resolution": resolution,
#         "aspect_ratio": aspect_ratio,
#         "creative_detailing": creative_detailing,
#         "filter_nsfw": True,
#     }
#     if model in FACE_REF_MODELS and image_base64:
#         payload["structure_reference"] = image_base64
#         payload["structure_strength"] = structure_strength
#     if debug:
#         st.write("Sending request to Freepik API...")
#     try:
#         r = requests.post(url, json=payload, headers=headers, timeout=30)
#         if debug:
#             st.write(f"Response status: {r.status_code}")
#             st.write(f"Response body: {r.text[:500]}")
#         if r.status_code == 200:
#             result = r.json()
#             data = result.get("data", {})
#             # Direct result
#             if "generated" in data and data["generated"]:
#                 return data["generated"]
#             # Async task
#             if "task_id" in data:
#                 return poll_task(api_key, data["task_id"], debug)
#             st.error(f"Unexpected response structure: {data}")
#         elif r.status_code == 401:
#             st.error("❌ Invalid API key (401). Check your Freepik API key.")
#         elif r.status_code == 429:
#             st.error("⚠️ Rate limit exceeded. Please wait and try again.")
#         else:
#             st.error(f"❌ API error {r.status_code}: {r.text[:300]}")
#     except requests.exceptions.Timeout:
#         st.error("⏱️ Request timed out.")
#     except Exception as e:
#         st.error(f"Error: {e}")
#         if debug:
#             st.exception(e)
#     return None


# def display_image_from_result(image_item):
#     """Handle all possible image formats from Freepik API response."""
#     if isinstance(image_item, str):
#         # Could be a URL or base64
#         if image_item.startswith("http"):
#             # It's a URL - fetch and display
#             try:
#                 img_response = requests.get(image_item, timeout=30)
#                 img = Image.open(io.BytesIO(img_response.content))
#                 st.image(img, use_container_width=True)
#                 return image_item  # return URL for download
#             except Exception as e:
#                 st.error(f"Failed to load image from URL: {e}")
#                 st.markdown(f"[🔗 Open image directly]({image_item})")
#                 return image_item
#         else:
#             # Assume base64
#             try:
#                 img_bytes = base64.b64decode(image_item)
#                 img = Image.open(io.BytesIO(img_bytes))
#                 st.image(img, use_container_width=True)
#                 return image_item
#             except Exception as e:
#                 st.error(f"Failed to decode base64 image: {e}")
#                 return None

#     elif isinstance(image_item, dict):
#         # Could be {"url": "..."} or {"base64": "..."}
#         if "url" in image_item:
#             return display_image_from_result(image_item["url"])
#         elif "base64" in image_item:
#             return display_image_from_result(image_item["base64"])
#         else:
#             st.error(f"Unknown image dict format: {list(image_item.keys())}")
#             # if debug_mode:
#             #     st.write(image_item)
#             return None
#     else:
#         st.error(f"Unknown image format: {type(image_item)}")
#         return None


# # ---------- GENERATE BUTTON ----------
# import random

# if st.button("🎬 Reveal My Persona", type="primary"):
#     personality = calculate_personality()
#     profile = profiles[personality]
#     st.session_state["personality"] = personality
#     st.session_state["profile"] = profile
#     st.session_state["show_variants"] = True

# if st.session_state.get("show_variants"):
#     personality = st.session_state["personality"]
#     profile = st.session_state["profile"]

#     st.divider()
#     st.markdown(f"## 🎭 You are: **{personality}**")
#     st.markdown(f"### {profile['title']}")
#     st.markdown(f'*"{profile["tagline"]}"*')
#     st.markdown("---")
#     st.markdown("### 🎬 Choose your poster style:")

#     variant_names = [v["name"] for v in profile["variants"]]
#     variant_names_with_random = ["🎲 Random — Surprise me!"] + variant_names

#     chosen = st.radio("Pick a cinematic style:", variant_names_with_random, key="variant_choice")

#     if st.button("✨ Generate My Poster", type="primary"):
#         if chosen == "🎲 Random — Surprise me!":
#             selected_variant = random.choice(profile["variants"])
#             st.info(f"🎲 Randomly selected: **{selected_variant['name']}**")
#         else:
#             selected_variant = next(v for v in profile["variants"] if v["name"] == chosen)

#         base_prompt = selected_variant["prompt"]
#         FACE_REF_MODELS = ["realism", "super_real"]
#         if model_option in FACE_REF_MODELS:
#             prompt = base_prompt + " The person\'s face from the reference photo is used as the main character\'s face, integrated naturally and seamlessly into the scene."
#         else:
#             prompt = base_prompt

#         # if debug_mode:
#         #     st.markdown("**Prompt:**")
#         #     st.info(prompt)

#         # Process image
#         with st.spinner("Processing your photo..."):
#             uploaded_file.seek(0)
#             raw_img = Image.open(uploaded_file).convert("RGB")
#             square_img = ImageOps.fit(raw_img, (1024, 1024), centering=(0.5, 0.5))
#             buf = io.BytesIO()
#             square_img.save(buf, format="JPEG", quality=90)
#             img_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")

#         # Generate
#         generated = generate_image(
#             api_key=api_key,
#             prompt=prompt,
#             image_base64=img_base64,
#             model=model_option,
#             resolution=resolution,
#             aspect_ratio=aspect_ratio,
#             creative_detailing=creative_detailing,
#             structure_strength=structure_strength,
#             # debug=debug_mode,
#         )

#         # Display result
#         if generated:
#             st.divider()
#             st.balloons()
#             st.markdown(f"## 🎬 {profile['title']}")
#             st.markdown(f"*\"{profile['tagline']}\"*")
#             st.caption(f"Style: {selected_variant['name']}")

#             # if debug_mode:
#             #     st.write("Raw generated response:", generated)

#             image_item = generated[0] if isinstance(generated, list) else generated
#             image_url = display_image_from_result(image_item)

#             if image_url and isinstance(image_url, str) and image_url.startswith("http"):
#                 st.markdown(f"[⬇️ Download / Open Full Image]({image_url})")

#             with st.expander("Details"):
#                 st.write(f"**Personality:** {personality} | **Style:** {selected_variant['name']} | **Model:** {model_option} | **Resolution:** {resolution}")
#         else:
#             st.error("No image was generated. Please check your API key and try again.")

# st.divider()

# st.markdown("<center>Made with 🎬 Streamlit & Freepik Mystic AI</center>", unsafe_allow_html=True)

import streamlit as st
import io
import requests
import base64
import time
import random
from PIL import Image, ImageOps
import os

st.set_page_config(page_title="Cinematic Persona Machine", layout="centered")

st.title("🎬 The Cinematic Persona Test")
st.markdown("Answer 10 questions to reveal your movie character and generate your poster.")

# ---------- SIDEBAR ----------
with st.sidebar:
    st.header("🔑 API Configuration")
    api_key = st.text_input("Freepik API Key", type="password", value=os.getenv("FREEPIK_API_KEY", ""))
    st.page_link(label="Get your API key", page="https://www.freepik.com/developers/dashboard/api-key")

    if not api_key:
        # st.warning("Please enter your Freepik API key")
        # st.stop()
        api_key="FPSX8acb3702de3611c4fc02a2e525b564f1"

    st.markdown("---")
    st.markdown("### ⚙️ Generation Settings")

    model_option = st.selectbox(
        "AI Model",
        ["realism", "super_real", "editorial_portraits", "flexible", "fluid", "zen"],
        index=0,
        help="realism / super_real / editorial_portraits support face preservation"
    )

    FACE_REF_MODELS = ["realism", "super_real", "editorial_portraits"]
    if model_option not in FACE_REF_MODELS:
        st.info(f"**{model_option}** doesn't support face reference.")

    resolution = st.selectbox("Resolution", ["1k", "2k", "4k"], index=1)
    aspect_ratio = st.selectbox(
        "Aspect Ratio",
        ["portrait_2_3", "square_1_1", "widescreen_16_9", "social_story_9_16"],
        index=0,
        help="portrait_2_3 looks best for movie posters"
    )
    creative_detailing = st.slider("Creative Detailing", 0, 100, 33)

    st.markdown("---")
    st.markdown("### 👤 Face Preservation")
    face_strength = st.slider(
        "Face Strength", 0, 100, 35,
        help="How strongly to lock in the face.\n\n30-45 = best balance (face kept, costume transformed)\n60+ = rigid face lock"
    )
    st.caption("💡 **35–45** gives the best movie poster look: face recognized but fully transformed into costume/scene.")

# ---------- UPLOAD ----------
uploaded_file = st.file_uploader("📸 Upload your photo (clear face photo works best)", type=["jpg", "png", "jpeg"])

if not uploaded_file:
    st.info("👆 Upload a clear face photo to begin your cinematic journey.")
    with st.expander("💡 Tips for best results"):
        st.markdown("""
        - Use a **clear, well-lit face photo**
        - **Front-facing** photos work best
        - Avoid heavy shadows or obstructions on the face
        - **Face Strength 35–45** gives the best balance of face preservation + cinematic transformation
        """)
    st.stop()

col1, col2 = st.columns([1, 3])
with col1:
    uploaded_file.seek(0)
    st.image(uploaded_file, caption="Your Hero", width=150)
with col2:
    st.markdown("### Now answer the questions below...")
    st.caption("Your answers determine your cinematic persona type.")

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

# ---------- PROFILES ----------
profiles = {
    "WARRIOR": {
        "title": "THE LAST RAJA",
        "tagline": "Steel is the only language.",
        "variants": [
            {
                "name": "🔥 Battlefield Inferno",
                "prompt": (
                    "Epic Bollywood war movie poster. A lone warrior hero standing tall on a burning battlefield at dusk. "
                    "The hero's face is clearly visible, front-facing, strong and fierce expression. "
                    "Wearing ornate Indian battle armor with gold engravings and a royal blue flowing cape. "
                    "Holding a massive engraved sword pointed downward. "
                    "Background: massive armies clashing in fire and smoke, embers floating, dust and ash in the air. "
                    "Dramatic volumetric lighting from the fires below illuminating the face heroically. "
                    "Title text 'THE LAST RAJA' blazes across the top in ancient carved gold lettering. "
                    "Tagline 'Steel is the only language.' etched below in worn bronze. "
                    "Professional movie poster composition, photorealistic, cinematic, IMAX quality, 4K."
                )
            },
            {
                "name": "⚔️ Throne of Ashes",
                "prompt": (
                    "Cinematic war epic movie poster. A fierce warrior king seated on a throne built entirely from broken swords and war shields. "
                    "The hero's face clearly visible, cold commanding gaze, battle scar on cheek. "
                    "Wearing heavy ornate battle-scarred black and gold armor. "
                    "Background: ruins of a grand stone palace, crumbling columns, blood-red stormy sky. "
                    "Dramatic chiaroscuro lighting, one side of the face in golden light, other in shadow. "
                    "Title 'THE LAST RAJA' in cracked stone lettering at top of the poster. "
                    "Tagline 'Steel is the only language.' in ember-orange glowing font below. "
                    "Photorealistic, cinematic blockbuster poster quality, 4K."
                )
            },
            {
                "name": "🌑 Shadow General",
                "prompt": (
                    "Dark fantasy war movie poster. A powerful warrior general emerging dramatically from swirling battle smoke. "
                    "Hero's face half-illuminated by flickering torchlight, intense and fearless expression. "
                    "Wearing black ornate armor with red war clan markings and a dark cape. "
                    "Background: stormy battlefield with lightning strikes, ghostly army barely visible in the fog. "
                    "Upward camera angle making the hero look monumental and imposing. "
                    "Title 'THE LAST RAJA' in jagged silver lightning-bolt letters at top. "
                    "Tagline 'Steel is the only language.' in blood-red drip style font below title. "
                    "Cinematic, photorealistic, blockbuster movie poster quality, 4K."
                )
            },
        ]
    },
    "ROMANTIC": {
        "title": "ETERNAL EMBRACE",
        "tagline": "A love that defies time.",
        "variants": [
            {
                "name": "🌅 Golden Hour",
                "prompt": (
                    "Romantic Hollywood drama movie poster. Hero standing on a hilltop at golden hour. "
                    "Hero's face clearly visible, soft warm light falling on features, expression tender and longing. "
                    "Wearing an elegant flowing period-drama outfit, soft wind moving through hair and fabric. "
                    "Background: breathtaking sunset sky of deep orange, rose pink, and amber. Wildflowers in soft bokeh foreground. "
                    "Cinematic and painterly lighting like a classic Hollywood romance. "
                    "Title 'ETERNAL EMBRACE' in elegant golden serif font at the top of poster. "
                    "Tagline 'A love that defies time.' in delicate italic cursive below. "
                    "Photorealistic, warm romantic tones, movie poster composition, 4K."
                )
            },
            {
                "name": "🌊 Ocean Edge",
                "prompt": (
                    "Epic romance movie poster. Hero standing at the edge of dramatic ocean cliffs at sunset. "
                    "Hero's face clearly visible, wind-swept hair, emotional expression, looking slightly off-camera. "
                    "Wearing an elegant coat or dress billowing dramatically in the ocean wind. "
                    "Background: giant waves crashing into cliffs below, misty spray. Sky in violet, amber, and deep blue. "
                    "Wide cinematic composition, small heroic figure against vast dramatic seascape. "
                    "Title 'ETERNAL EMBRACE' in large elegant white letters at top. "
                    "Tagline 'A love that defies time.' in italic gold below title. "
                    "Hollywood movie poster quality, photorealistic, 4K."
                )
            },
            {
                "name": "🕯️ Candlelit Drama",
                "prompt": (
                    "Intimate romantic drama movie poster. Close-up portrait of the hero surrounded by dozens of candles. "
                    "Hero's face is the centerpiece, warm amber candlelight highlighting features, one tear on cheek catching the light. "
                    "Soft luxurious clothing, candles melting into soft bokeh background of golden light and deep shadow. "
                    "Extremely intimate and emotional atmosphere. "
                    "Title 'ETERNAL EMBRACE' in dark romantic serif font at the very top of poster. "
                    "Tagline 'A love that defies time.' in whisper-thin italic letters below. "
                    "Cinematic portrait, photorealistic, award-worthy movie poster composition, 4K."
                )
            },
        ]
    },
    "MYSTIC": {
        "title": "THE SILENT SAGE",
        "tagline": "Knowledge is deadly.",
        "variants": [
            {
                "name": "🌿 Forest Oracle",
                "prompt": (
                    "Dark fantasy mystery movie poster. A lone hooded sage standing in an ancient mystical forest at midnight. "
                    "Hero's face partially visible under a hood, intense glowing eyes catching the moonlight. "
                    "Wearing ancient mystical robes with glowing runic patterns. Holding an open ancient glowing tome. "
                    "Background: massive ancient trees with blue-green glowing runes carved into bark, thick ground fog, moonbeams filtering through canopy. "
                    "Ethereal otherworldly atmosphere with magical particle effects floating in the air. "
                    "Title 'THE SILENT SAGE' in glowing rune-carved letters at top of poster. "
                    "Tagline 'Knowledge is deadly.' fading into mist below title. "
                    "Photorealistic, cinematic, dark fantasy movie poster, 4K."
                )
            },
            {
                "name": "✨ Cosmic Seer",
                "prompt": (
                    "Sci-fi mystical epic movie poster. A cloaked cosmic figure floating in deep space. "
                    "Hero's face clearly visible, otherworldly expression, eyes reflecting galaxies. "
                    "Wearing magnificent robes made of living starlight and flowing cosmic energy. "
                    "One hand raised, pulling constellations and nebula clouds into a swirling vortex. "
                    "Background: stunning deep space, purples, blues, gold nebula clouds, star fields. "
                    "Title 'THE SILENT SAGE' in constellation dot lettering across the top. "
                    "Tagline 'Knowledge is deadly.' in glowing gold below title. "
                    "Epic cinematic composition, photorealistic, 4K."
                )
            },
            {
                "name": "🔮 Temple of Shadows",
                "prompt": (
                    "Dark thriller mystery movie poster. A figure in ancient ceremonial robes at the towering entrance of an underground temple. "
                    "Hero's face in partial shadow, only intense piercing eyes fully visible, expression dangerous and knowing. "
                    "Wearing ancient ceremonial robes with serpent and eye motifs. "
                    "Background: massive stone temple walls with carved serpent reliefs, torchlight casting eerie shadows, floor flooded with shallow reflecting water, incense smoke. "
                    "Title 'THE SILENT SAGE' carved in stone relief lettering at the top. "
                    "Tagline 'Knowledge is deadly.' in blood-red ink drip style below title. "
                    "Cinematic, photorealistic, dark thriller movie poster, 4K."
                )
            },
        ]
    },
    "LEADER": {
        "title": "THE CROWN'S BURDEN",
        "tagline": "To lead is to sacrifice.",
        "variants": [
            {
                "name": "👑 The Throne",
                "prompt": (
                    "Royal political drama movie poster. A solitary ruler seated on an enormous ornate golden throne. "
                    "Hero's face clearly visible, expression weary but resolute, the weight of the world visible in the eyes. "
                    "Wearing elaborate royal garments and a heavy jeweled crown. "
                    "Background: grand palace hall, towering marble columns, stained glass casting cathedral light, completely empty throne room. "
                    "Dramatic side-lighting making the face look powerful and melancholy simultaneously. "
                    "Title THE CROWN'S BURDEN in regal gold embossed serif font at the top. "
                    "Tagline 'To lead is to sacrifice.' in silver italic below title. "
                    "Dramatic cinematic lighting, photorealistic, prestige drama movie poster, 4K."
                )
            },
            {
                "name": "🌆 Modern Power",
                "prompt": (
                    "Political thriller movie poster. A powerful modern leader standing at towering floor-to-ceiling glass windows. "
                    "Hero's face reflected in the glass, determined haunted expression visible in reflection. Back to camera but face visible via reflection. "
                    "Wearing a sharp tailored charcoal suit, hands clasped behind back. "
                    "Background: massive city skyline at night, a sea of blurred lights stretching to the horizon below. "
                    "Cinematic blue-grey color palette, cool and commanding. "
                    "Title THE CROWN'S BURDEN in bold clean white font at the very top. "
                    "Tagline 'To lead is to sacrifice.' in muted gold below title. "
                    "Cinematic, photorealistic, political thriller movie poster, 4K."
                )
            },
            {
                "name": "⚡ The Rally",
                "prompt": (
                    "Epic leadership drama movie poster. A charismatic leader on a massive podium, arms raised triumphantly. "
                    "Hero's face clearly visible from below, dynamic upward angle, powerful and inspiring expression. "
                    "Wearing a dramatic coat or military-inspired outfit billowing in the wind. "
                    "Background: crowd of thousands with upturned faces, searchlights sweeping a stormy sky, lightning striking in storm clouds above. "
                    "Low upward camera angle makes the hero appear monumental against the sky. "
                    "Title THE CROWN'S BURDEN in massive bold dramatic typography at top. "
                    "Tagline 'To lead is to sacrifice.' below title. "
                    "Photorealistic, cinematic blockbuster movie poster quality, 4K."
                )
            },
        ]
    },
    "REBEL": {
        "title": "NEON OUTCAST",
        "tagline": "Break the system.",
        "variants": [
            {
                "name": "🌧️ Neon Rain",
                "prompt": (
                    "Cyberpunk action movie poster. A lone rebel standing in a rain-soaked neon alley at night. "
                    "Hero's face clearly visible, rain-soaked, lit by multicolored neon signs, expression defiant and dangerous. "
                    "Wearing a worn leather jacket with circuit-pattern patches, cybernetic eye implant glowing blue. "
                    "Background: cyberpunk alley with neon signs reflecting in rain puddles, massive holographic advertisements on skyscrapers, rain streaks in neon light. "
                    "Title 'NEON OUTCAST' in glitching neon pink and electric blue letters at the top. "
                    "Tagline 'Break the system.' in electric green terminal font below title. "
                    "Cinematic, photorealistic, Blade Runner aesthetic movie poster, 4K."
                )
            },
            {
                "name": "💥 System Crash",
                "prompt": (
                    "Sci-fi rebellion thriller movie poster. A hacker in a dark server room. "
                    "Hero's face half-lit by blue-white glow of dozens of monitors, intense focused expression. "
                    "Wearing a dark hoodie, face partially shadowed, fingers poised over a holographic keyboard. "
                    "Background: wall-to-wall server racks, monitors showing cascading code, system crash alerts in red, warning lights flashing. "
                    "Claustrophobic tense atmosphere with cool blue and red lighting. "
                    "Title 'NEON OUTCAST' in corrupted glitch-effect digital font at the top. "
                    "Tagline 'Break the system.' in terminal green code style below title. "
                    "Cinematic, photorealistic, cyberpunk thriller movie poster, 4K."
                )
            },
            {
                "name": "🏍️ Midnight Rider",
                "prompt": (
                    "Action thriller movie poster. A rebel on a futuristic neon-lit motorcycle at full speed on a cyberpunk highway at midnight. "
                    "Hero's face visible looking back over shoulder, fearless wild expression, wind-blown, determined. "
                    "Wearing a biker jacket with neon stripe details, visor lifted. "
                    "Background: streaking city lights creating motion blur tunnels, police drones with searchlights in pursuit behind, sparks flying from the road. "
                    "Extreme motion and speed conveyed through blur and angle. "
                    "Title 'NEON OUTCAST' in slanted high-speed motion-blur neon font at the top. "
                    "Tagline 'Break the system.' in exhaust-smoke style lettering below title. "
                    "Epic cinematic, photorealistic, action movie poster, 4K."
                )
            },
        ]
    },
}


# ---------- API FUNCTIONS ----------
def poll_task(api_key, task_id):
    url = f"https://api.freepik.com/v1/ai/mystic/{task_id}"
    headers = {"x-freepik-api-key": api_key}
    progress = st.progress(0)
    status_text = st.empty()

    for attempt in range(40):
        status_text.text(f"🎨 Generating your cinematic poster... ({attempt + 1}/40)")
        progress.progress((attempt + 1) / 40)
        try:
            r = requests.get(url, headers=headers, timeout=15)
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
        except Exception:
            pass
        time.sleep(3)

    progress.empty()
    status_text.empty()
    st.warning("Timed out. Try generating again.")
    return None


def generate_image(api_key, prompt, image_base64, model, resolution, aspect_ratio, creative_detailing, face_strength):
    url = "https://api.freepik.com/v1/ai/mystic"
    headers = {"Content-Type": "application/json", "x-freepik-api-key": api_key, "Accept": "application/json"}
    FACE_REF_MODELS = ["realism", "super_real", "editorial_portraits"]

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
        payload["structure_strength"] = face_strength

    try:
        r = requests.post(url, json=payload, headers=headers, timeout=30)
        if r.status_code == 200:
            result = r.json()
            data = result.get("data", {})
            if "generated" in data and data["generated"]:
                return data["generated"]
            if "task_id" in data:
                return poll_task(api_key, data["task_id"])
            st.error(f"Unexpected response: {data}")
        elif r.status_code == 401:
            st.error("Invalid API key (401). Check your Freepik API key.")
        elif r.status_code == 429:
            st.error("Rate limit exceeded. Please wait and try again.")
        elif r.status_code == 400:
            err = r.json() if r.headers.get("content-type", "").startswith("application/json") else {}
            st.error(f"Bad request: {err.get('message', r.text[:200])}")
        else:
            st.error(f"API error {r.status_code}: {r.text[:300]}")
    except requests.exceptions.Timeout:
        st.error("Request timed out.")
    except Exception as e:
        st.error(f"Error: {e}")
    return None


def display_image(image_item):
    if isinstance(image_item, dict):
        image_item = image_item.get("url") or image_item.get("base64", "")
    if isinstance(image_item, str):
        if image_item.startswith("http"):
            try:
                img_bytes = requests.get(image_item, timeout=30).content
                img = Image.open(io.BytesIO(img_bytes))
                st.image(img, use_container_width=True)
                return image_item
            except Exception as e:
                st.error(f"Failed to load image: {e}")
                st.markdown(f"[Open image directly]({image_item})")
                return image_item
        else:
            try:
                img = Image.open(io.BytesIO(base64.b64decode(image_item)))
                st.image(img, use_container_width=True)
            except Exception as e:
                st.error(f"Failed to decode image: {e}")
    return None


# ---------- REVEAL PERSONA BUTTON ----------
if st.button("🎬 Reveal My Persona", type="primary", use_container_width=True):
    personality = calculate_personality()
    profile = profiles[personality]
    st.session_state["personality"] = personality
    st.session_state["profile"] = profile
    st.session_state["show_variants"] = True
    st.session_state.pop("generated_image", None)
    st.session_state.pop("selected_variant", None)

# ---------- VARIANT PICKER + GENERATE ----------
if st.session_state.get("show_variants"):
    personality = st.session_state["personality"]
    profile = st.session_state["profile"]

    st.divider()

    icons = {"WARRIOR": "⚔️", "ROMANTIC": "💕", "MYSTIC": "🔮", "LEADER": "👑", "REBEL": "⚡"}
    st.markdown(f"## {icons.get(personality, '')} You are: **{personality}**")
    st.markdown(f"### 🎬 *{profile['title']}*")
    st.markdown(f"> *\"{profile['tagline']}\"*")

    st.markdown("---")
    st.markdown("### 🎨 Choose your poster style:")

    all_choices = ["🎲 Random — Surprise me!"] + [v["name"] for v in profile["variants"]]
    chosen = st.radio("Pick a cinematic style:", all_choices, key="variant_choice")

    col1, col2 = st.columns([3, 1])
    with col1:
        generate_clicked = st.button("✨ Generate My Poster", type="primary", use_container_width=True)
    with col2:
        st.caption(f"Face: **{face_strength}**\n{model_option}")

    if generate_clicked:
        if chosen == "🎲 Random — Surprise me!":
            selected_variant = random.choice(profile["variants"])
            st.info(f"🎲 Selected: **{selected_variant['name']}**")
        else:
            selected_variant = next(v for v in profile["variants"] if v["name"] == chosen)

        st.session_state["selected_variant"] = selected_variant

        # Build prompt — append face instruction for supported models
        base_prompt = selected_variant["prompt"]
        FACE_REF_MODELS = ["realism", "super_real", "editorial_portraits"]
        if model_option in FACE_REF_MODELS:
            prompt = (
                base_prompt +
                " CRITICAL: The subject's exact face, facial structure, skin tone, eyes, beard and hair must be "
                "faithfully preserved as the main character's face. Only the costume, outfit, pose, background "
                "and setting should be transformed into the cinematic style. Do not change the face."
            )
        else:
            prompt = base_prompt

        # Process photo — smart crop biased toward face (upper portion)
        with st.spinner("Processing your photo..."):
            uploaded_file.seek(0)
            raw_img = Image.open(uploaded_file).convert("RGB")
            w, h = raw_img.size
            size = min(w, h)
            left = (w - size) // 2
            top = max(0, min((h - size) // 3, h - size))  # bias upper third for face
            cropped = raw_img.crop((left, top, left + size, top + size))
            resized = cropped.resize((1024, 1024), Image.LANCZOS)
            buf = io.BytesIO()
            resized.save(buf, format="JPEG", quality=95)
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
            face_strength=face_strength,
        )

        if generated:
            st.session_state["generated_image"] = generated[0] if isinstance(generated, list) else generated

    # ---------- DISPLAY RESULT ----------
    if "generated_image" in st.session_state:
        selected_variant = st.session_state.get("selected_variant", {})
        st.divider()
        st.balloons()

        st.markdown(f"## 🎬 {profile['title']}")
        st.markdown(f"*\"{profile['tagline']}\"*")
        if selected_variant:
            st.caption(f"Style: {selected_variant.get('name', '')}")

        image_url = display_image(st.session_state["generated_image"])

        if image_url and isinstance(image_url, str) and image_url.startswith("http"):
            st.markdown(f"[⬇️ Download / Open Full Image]({image_url})")

        with st.expander("📋 Details"):
            st.write(f"**Persona:** {personality} | **Style:** {selected_variant.get('name', 'N/A')}")
            st.write(f"**Model:** {model_option} | **Resolution:** {resolution} | **Face Strength:** {face_strength}")

        if st.button("🔄 Try Another Style", use_container_width=True):
            st.session_state.pop("generated_image", None)
            st.rerun()

st.divider()
st.markdown("<center>Made with 🎬 Streamlit & Freepik Mystic AI</center>", unsafe_allow_html=True)
