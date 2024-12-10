import xml.etree.ElementTree as ET
import re

def convert_xml_to_markdown(xml_file, output_folder):
    # XMLをパースする
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # WordPressのエントリーを探す
    for item in root.findall(".//item"):
        title = item.find("title").text or "untitled"
        content = item.find("{http://purl.org/rss/1.0/modules/content/}encoded").text or ""

        # 不要なタグを削除
        content = re.sub(r"<[^>]+>", "", content)

        # 画像タグを変換
        content = re.sub(
            r"https?://[^\"\'\s]+/([^\"\'\s]+(\.png|\.jpg|\.jpeg|\.gif))",
            r"イメージ：\1",
            content,
        )

        # インライン数式を変換
        content = re.sub(r"\$(.+?)\$", r"$$\1$$", content)

        # リンクを変換
        content = re.sub(r"\[(.+?)\]\((.+?)\)", r"\1：\2", content)

        # リストを変換
        content = re.sub(r"<li>(.*?)</li>", r"- \1", content)

        # 見出しを変換 
        content = re.sub(r"<h1>(.*?)</h1>", r"## \1", content)


        # ファイル名を決定
        safe_title = re.sub(r"[\\/*?\"<>|]", "_", title)  # 禁止文字を置換
        output_file = f"{output_folder}/{safe_title}.md"

        # Markdown形式で保存
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"# {title}\n\n")
            f.write(content)

        print(f"Converted: {title}")

# 実行例
if __name__ == "__main__":
    input_file = "wordpress.xml"  # 入力XMLファイル
    output_dir = "output_markdown"  # 出力フォルダ
    import os
    os.makedirs(output_dir, exist_ok=True)
    convert_xml_to_markdown(input_file, output_dir)
