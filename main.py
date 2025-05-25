import streamlit as st
import yt_dlp
from pathlib import Path

def download_video(url: str) -> Path | None:
    """
    Downloads a YouTube video from the given URL and saves it to a specified directory.
    """
    try:
        output_dir = Path("downloads")
        output_dir.mkdir(exist_ok=True)

        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
            'outtmpl': str(output_dir / '%(title)s.%(ext)s'),
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            with st.spinner("Downloading..."):
                info_dict = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info_dict)

        st.success("Download complete!")
        return Path(filename)

    except Exception as e:
        st.error(f'Error: {e}')
        return None

def main():
    st.title('YouTube Downloader')
    st.write('Input YouTube video URL to download the video.')

    url = st.text_input('YouTube Video URL', placeholder='https://www.youtube.com/watch?v=example')

    if st.button('Download Video'):
        if url:
            file_path = download_video(url)
            if file_path and file_path.exists():
                with open(file_path, 'rb') as f:
                    st.download_button(
                        label="Download Video",
                        data=f,
                        file_name=file_path.name,
                        mime='video/mp4'
                    )
        else:
            st.warning('Input a valid YouTube video URL.')

if __name__ == '__main__':
    main()
