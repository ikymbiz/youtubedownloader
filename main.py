import streamlit as st
import yt_dlp
import os
from pathlib import Path

def download_video(url: str) -> Path | None:
    """
    動画を一時的に保存し、ダウンロードリンク用のパスを返す
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
            with st.spinner("ダウンロード中..."):
                info_dict = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info_dict)

        st.success("ダウンロード完了！")
        return Path(filename)

    except Exception as e:
        st.error(f'エラー: {e}')
        return None

def main():
    st.title('YouTube動画ダウンローダー（Streamlit Cloud用）')
    st.write('YouTubeの動画URLを入力してください')

    url = st.text_input('動画URL')

    if st.button('ダウンロード開始'):
        if url:
            file_path = download_video(url)
            if file_path and file_path.exists():
                with open(file_path, 'rb') as f:
                    st.download_button(
                        label="動画をダウンロード",
                        data=f,
                        file_name=file_path.name,
                        mime='video/mp4'
                    )
        else:
            st.warning('URLを入力してください')

if __name__ == '__main__':
    main()
