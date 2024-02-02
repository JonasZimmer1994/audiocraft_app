import validators
import streamlit as st
import langchain as lc
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import UnstructuredURLLoader
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
from transformers import AutoProcessor, MusicgenForConditionalGeneration
import scipy

# Streamlit app
st.subheader('Text for Song:')
st.caption(
    "Audiocraft will create a song out of the given text and save it as musicgen_out.wav in your project's folder. This might take a while the first time your run it because Audiocraft needs to download the models.")

song_description = st.text_input("Text aus dem ein Track erzeugt werden soll", label_visibility="collapsed")

# If 'Create song' button is clicked
if st.button("Create song"):
    try:
        with st.spinner("Please wait..."):
            # Load the MusicGen model
            processor = AutoProcessor.from_pretrained(
                "facebook/musicgen-small")
            model = MusicgenForConditionalGeneration.from_pretrained(
                "facebook/musicgen-small")

            # Format the input based on the song description
            inputs = processor(
                text=[song_description],
                padding=True,
                return_tensors="pt",
            )

            # Generate the audio
            audio_values = model.generate(**inputs, max_new_tokens=256)

            sampling_rate = model.config.audio_encoder.sampling_rate
            # Save the wav file into your system
            scipy.io.wavfile.write(
                "musicgen_out.wav", rate=sampling_rate, data=audio_values[0, 0].numpy())

            # Render a success message with the song description generated by ChatGPT
            st.success("Your song has been succesfully created with the following prompt: "+song_description)
    except Exception as e:
        st.exception(f"Exception: {e}")