import streamlit as st
import os
import yt_dlp
from pathlib import Path

def download_video(url: str, output_dir: str) -> None:
    """
    ダウンロード関数

    Args:
        url: YouTube 動画の URL
        output_dir: 保存先ディレクトリ
    """
    try:
        # 出力ディレクトリが存在しない場合は作成
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # yt-dlpのオプション設定
        ydl_opts = {
            'format': 'best',  # 最高画質
            'quiet': True,     # 進捗表示を抑制
            'no_warnings': True,
            'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        }

        # ダウンロード実行
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            with st.spinner('ダウンロード中...'):
                ydl.download([url])
            st.success('ダウンロード完了！')

    except Exception as e:
        st.error(f'エラー: {e}')
        st.info('ヒント: 動画が非公開または地域制限されている可能性があります。')

def main():
    st.title('YouTube動画ダウンローダー')
    
    # サイドバーで保存先を設定
    # 現在のルートフォルダをデフォルトに設定
    with st.sidebar:
        st.header('設定')
        output_dir = st.text_input(
            '保存先ディレクトリ',
            value=str(Path.home() / 'Downloads'),
            # value=str(Path.cwd() / 'downloads'),
            help='ダウンロードした動画の保存先を指定してください'
        )
    
    # メイン画面
    st.write('YouTubeの動画URLを入力してください')
    
    # URL入力フォーム
    url = st.text_input('動画URL', '')
    
    # ダウンロードボタン
    if st.button('ダウンロード開始'):
        if url:
            download_video(url, output_dir)
        else:
            st.warning('URLを入力してください')

if __name__ == '__main__':
    main() 