import download_moneystuff
import moneystuff_rss
import article_to_text
import tts
import json
from pydub import AudioSegment
from feedgen.feed import FeedGenerator
import os
import sys
import unicodedata

if len(sys.argv) == 1:
    outdir = "./publish"
else:
    outdir = sys.argv[1]

base_url = "https://63efd2f9d13069226104c17e--heartfelt-kleicha-e5d7f4.netlify.app"

if not os.path.exists(outdir):
    os.mkdir(outdir)

tmpdir = "./tmp"
if not os.path.exists(tmpdir):
    os.mkdir(tmpdir)

filesdir = f"{outdir}/files"
if not os.path.exists(filesdir):
    os.mkdir(filesdir)

articlesdir = f"{outdir}/articles"
if not os.path.exists(articlesdir):
    os.mkdir(articlesdir)

articles = moneystuff_rss.get_articles()

for article in articles:
    file_path = f"{filesdir}/{article.title}.json"
    with open(file_path, "w") as f:
        json.dump(article, f, indent=4)


articles = download_moneystuff.get_articles()

for article in articles:
    file_path = f"{articlesdir}/{article.title}.html"

    if not os.path.exists(file_path):
        print("Creating", file_path)
        html = download_moneystuff.get_article_html(article.href)
        with open(file_path, "w") as f:
            f.write(html)


articles = [ f for f in os.listdir(articlesdir) if f.endswith(".html") ]

for article in articles:
    title = article.removesuffix(".html")
    mp3_file_path = f"{filesdir}/{title}.mp3"

    if not os.path.exists(mp3_file_path):
        file_path = f"{tmpdir}/{title}.txt"

        print("Creating", file_path)
        with open(f"{articlesdir}/{article}", "r") as f:
            html = f.read()
        text = article_to_text.convert(html)
        with open(file_path, "w") as f:
            f.write(text)

        wav_file_path = f"{tmpdir}/{title}.wav"
        print("Creating", wav_file_path)
        with open(file_path, "r") as f:
            text = f.read()
        tts.synthesise(text, wav_file_path)

        print("Creating", mp3_file_path)
        sound = AudioSegment.from_wav(wav_file_path)
        sound.export(mp3_file_path, format="mp3")

fg = FeedGenerator()
fg.load_extension('podcast', rss=True)

fg.podcast.itunes_category('News', 'Business News')
fg.title("Robo-Matt Levine")
fg.link({"href": "https://www.bloomberg.com/opinion/authors/ARbTQlRLRjE/matthew-s-levine"})
fg.description("Robo-Matt Levine")

episodes = [ f for f in os.listdir(filesdir) if f.endswith(".mp3") ]

for episode in episodes:
    title = episode[:-4]
    metadata_path = unicodedata.normalize("NFKC", f"{filesdir}/{title}.json")
    with open(metadata_path, "r") as f:
        metadata = json.load(f)
    
    fe = fg.add_entry()
    fe.id(f"{base_url}/files/{episode}")
    fe.title(metadata['title'])
    fe.description(metadata['summary'])
    fe.enclosure(f"{base_url}/files/{episode}", str(os.stat(f"{filesdir}/{episode}").st_size), "audio/mpeg")

fg.rss_file(f"{outdir}/podcast.rss")