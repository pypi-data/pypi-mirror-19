import hug
from requests import exceptions
from lyricfool import AZLyricAdapter, GeniusAdapter, LyricsWikiaAdapter, MetroLyricsAdapter

adapters = {
    # 'azlyrics': AZLyricAdapter, # they aren't a fan of this
    'genius': GeniusAdapter(), #default
    'metro': MetroLyricsAdapter(),
    'wikia': LyricsWikiaAdapter()
}

@hug.cli()
def get_lyric(artist: hug.types.text, title: hug.types.text, adapter: hug.types.text='genius'):
    """
    Gets lyrics from Genius, MetroLyrics, or LyricsWikia. Default: Genius.
    Add 'metro' or 'wikia' to your command to change adapters.
    """
    if adapter not in adapters.keys():
        return "{} is not a valid adapter. Please choose from: {}".format(adapter, ' '.join(adapters))
    try:
        return adapters[adapter].get_lyrics(artist, title)
    except exceptions.HTTPError as e:
        if '404' in str(e):
            return "I'm sorry I couldn't find: {} by {}".format(artist, title)
        return str(e)

def main():
    get_lyric.interface.cli()

if __name__ == "__main__":
    main()
