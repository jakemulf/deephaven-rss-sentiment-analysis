"""
read_rss_podcasts.py

An RSS reader that reads from multiple podcast URLs.

This file is meant to run through Deephaven's Application Mode as part of several Python scripts. Because of this, some
variables may not be defined in here, but instead in helper_functions.py or read_rss.py.
"""
import json

def rss_attributes_method_podcasts(entry):
    return (entry["title"], rss_datetime_converter_podcasts(entry), entry["title_detail"]["base"],
            json.dumps(entry))

def rss_datetime_converter_podcasts(entry):
    try:
        dt = parser.parse(entry["published"])
        dts = dt.strftime("%Y-%m-%dT%H:%M:%S") + " UTC"
        return convertDateTime(dts)
    except:
        return currentTime()

podcast_feed_urls = [
    "https://markalanwilliams.libsyn.com/rss",
    "https://anchor.fm/s/19ccb320/podcast/rss",
    "http://www.snec.org.uk/site/itunes",
    "http://feeds.soundcloud.com/users/soundcloud:users:150466516/sounds.rss",
    "https://audioboom.com/channels/4597972.rss",
    "https://anchor.fm/s/212c47d4/podcast/rss",
    "http://feeds.feedburner.com/DirtBikePodcast",
    "https://anchor.fm/s/28f184c/podcast/rss",
    "https://galaktacus.libsyn.com/rss",
    "https://sportsfromherperspective.podomatic.com/rss2.xml",
    "http://feeds.soundcloud.com/users/soundcloud:users:37022259/sounds.rss",
    "http://feeds.soundcloud.com/users/soundcloud:users:151205561/sounds.rss",
    "https://nocturniarecords.podomatic.com/rss2.xml",
    "http://feeds.soundcloud.com/users/soundcloud:users:142613909/sounds.rss",
    "https://noextrawords.libsyn.com/rss",
    "http://feeds.feedburner.com/TheSpysonHour",
    "http://rss.lizhi.fm/rss/1312446.xml",
    "http://feeds.soundcloud.com/users/soundcloud:users:155565658/sounds.rss",
    "https://talkingpicturespodcast.podbean.com/feed.xml",
    "https://hillaryandjason.podomatic.com/rss2.xml",
    "http://feeds.soundcloud.com/users/soundcloud:users:154694102/sounds.rss",
    "https://anchor.fm/s/2e03f13c/podcast/rss",
    "https://www.corechurchtampa.com/messages?format=rss",
    "https://CBCHSV.podbean.com/feed.xml",
    "http://feeds.soundcloud.com/users/soundcloud:users:135870190/sounds.rss",
    "https://lutheryoung.podomatic.com/rss2.xml",
    "https://kevin-zade.squarespace.com/episodes?format=rss",
    "https://mtviewumc.org/sermons/feed/",
    "http://feeds.soundcloud.com/users/soundcloud:users:154617860/sounds.rss",
    "http://feeds.soundcloud.com/users/soundcloud:users:21640516/sounds.rss",
    "https://itunesu.itunes.apple.com/feed/id1000264965",
    "https://rss.art19.com/results-may-vary",
    "http://thebigsbie.podfm.ru/Gamecast/rss/rss.xml",
    "https://itunesu.itunes.apple.com/feed/id1000272661",
    "https://anchor.fm/s/2118ce48/podcast/rss",
    "https://itunesu.itunes.apple.com/feed/id1000278930",
    "https://itunesu.itunes.apple.com/feed/id1000282323",
    "http://feeds.soundcloud.com/users/soundcloud:users:15937/sounds.rss",
    "https://crmaudio.libsyn.com/crm",
    "http://harbourcitystories.com/?feed=podcast",
    "https://rss.whooshkaa.com/rss/podcast/id/7252",
    "http://occasionallythinking.org/podcast/feed.xml",
    "http://feeds.soundcloud.com/users/soundcloud:users:155730467/sounds.rss",
    "https://www.bennytime.com/feed/podcast/",
    "https://starbug42.podbean.com/feed.xml",
    "http://feeds.feedburner.com/TristanGreth-Sermons",
    "http://feeds.soundcloud.com/users/soundcloud:users:151393324/sounds.rss",
    "https://itunesu.itunes.apple.com/feed/id1000319186",
    "https://itunesu.itunes.apple.com/feed/id1000320254",
    "https://itunesu.itunes.apple.com/feed/id1000320648",
    "https://itunesu.itunes.apple.com/feed/id1000320852",
    "https://djodawa.com/feed/podcast/",
    "https://feeds.soundcloud.com/users/soundcloud:users:155741544/sounds.rss",
    "https://gloryrevolution.podomatic.com/rss2.xml",
    "https://sreeyahpathe-srinivasa.podomatic.com/rss2.xml",
    "http://pod.ssenhosting.com/rss/wpffhtm/yamete.xml",
    "http://www.fahlstaff.com/podcast?format=rss",
    "http://feeds.soundcloud.com/users/soundcloud:users:155830450/sounds.rss",
    "https://rss.simplecast.com/podcasts/4737/rss",
    "http://feeds.soundcloud.com/users/soundcloud:users:154573494/sounds.rss",
    "http://feeds.soundcloud.com/users/soundcloud:users:140188249/sounds.rss",
    "http://feeds.soundcloud.com/users/soundcloud:users:153400625/sounds.rss",
    "https://itunesu.itunes.apple.com/feed/id1000421916",
    "https://podmaxpodcast.libsyn.com/rss",
    "https://whatsyourdealpodcast75480.podomatic.com/rss2.xml",
    "http://wtovpicpod.audiopress.co.uk/feed/podcast/",
    "https://greenspirit.org.uk/podcast/feed.xml",
    "https://itunesu.itunes.apple.com/feed/id1000425578",
    "http://bloodsuckingfeminists.com/feed/podcast/",
    "https://itunesu.itunes.apple.com/feed/id1000428288",
    "https://itunesu.itunes.apple.com/feed/id1000433285",
    "https://feeds.buzzsprout.com/165777.rss",
    "http://www.dragonliterature.com/once-upon-a-die/?format=rss",
    "https://itunesu.itunes.apple.com/feed/id1000436282",
    "https://enotrasnoticias.podomatic.com/rss2.xml",
    "http://feeds.soundcloud.com/users/soundcloud:users:155047175/sounds.rss",
    "http://whitehorsebaptistchurch.cloversites.com/podcast/7b079ab6-5db3-4935-bd15-f0867590fbd6.xml",
    "https://itunesu.itunes.apple.com/feed/id1000441627",
    "https://feeds.podcastmirror.com/ptpintcast",
    "http://feeds.soundcloud.com/users/soundcloud:users:3606375/sounds.rss",
    "https://itunesu.itunes.apple.com/feed/id1000443999",
    "http://feeds.soundcloud.com/users/soundcloud:users:155387351/sounds.rss",
    "http://feeds.soundcloud.com/users/soundcloud:users:11097920/sounds.rss",
    "https://theGroveZone.podbean.com/feed.xml",
    "http://fiveminutemd.com/feed/five-minute-kidkast/",
    "https://living-the-dream.libsyn.com/rss",
]

column_names = [
    "RssEntryTitle",
    "PublishDatetime",
    "RssFeedUrl",
    "JsonObject",
]
column_types = [
    dht.string,
    dht.datetime,
    dht.string,
    dht.string,
]

podcast_feeds = read_rss_continual(podcast_feed_urls, sleep_time=300, rss_attributes_method=rss_attributes_method_podcasts,
                                   rss_datetime_converter=rss_datetime_converter_podcasts, column_names=column_names,
                                   column_types=column_types)
