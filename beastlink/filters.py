FILTERS = {
    "bassboost": "bass=g=8,dynaudnorm",
    "treble": "treble=g=5",
    "nightcore": "asetrate=48000*1.25,aresample=48000",
    "vaporwave": "asetrate=48000*0.8,aresample=48000",
    "8d": "apulsator=hz=0.09",
    "karaoke": "stereotools=mlev=0.03",
    "vocal": "equalizer=f=2500:t=q:w=1:g=5",
    "lofi": "lowpass=f=3000,highpass=f=200",
    "pop": "equalizer=f=1000:t=q:w=1:g=2",
    "rock": "equalizer=f=100:t=q:w=1:g=3",
    "electronic": "equalizer=f=60:t=q:w=1:g=4",
    "soft": "lowpass=f=8000,equalizer=f=250:t=q:w=1:g=2",
    "concert": "aecho=0.8:0.9:1000:0.3",
    "stadium": "aecho=0.8:0.9:1500:0.4",
}


def apply_filter(name):
    if not name:
        return None
    return FILTERS.get(name.lower())