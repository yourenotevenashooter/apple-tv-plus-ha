"""Apple TV app identifiers and deep-link targets.

Apple's own apps (marked below) are sourced from Apple's official tvOS
bundle-ID documentation and can be trusted as-is:
https://support.apple.com/guide/deployment/bundle-ids-for-apple-tv-apple-apps-depcdd66fe58/web

Everything else is community/testing-verified rather than officially
documented — third-party developers don't publish their tvOS bundle IDs,
so those entries are only as good as real-device confirmation. If one
doesn't launch for you, that's the most likely reason; see the README's
Known Limitations.
"""

APP_IDS = {
    # --- Apple apps (official, per Apple's documentation) ---
    "Apple TV": "com.apple.TV",
    "Apple Music": "com.apple.TVMusic",
    "Apple Podcasts": "com.apple.podcasts",
    "Apple Photos": "com.apple.TVPhotos",
    "Apple Settings": "com.apple.TVSettings",
    "Apple App Store": "com.apple.TVAppStore",
    "Apple Arcade": "com.apple.Arcade",
    "Apple Fitness+": "com.apple.Fitness",
    "FaceTime": "com.apple.facetime",
    # --- Third-party apps (community/testing-verified, not officially documented) ---
    "Netflix": "com.netflix.Netflix",
    "YouTube": "com.google.ios.youtube",
    "Hulu": "com.hulu.plus",
    "Disney+": "com.disney.disneyplus",
    "Max": "com.hbo.hbonow",
    "Amazon Prime Video": "com.amazon.aiv.AIVApp",
    "Peacock": "com.peacocktv.peacock",
    "Twitch": "tv.twitch",
    "Crunchyroll": "com.crunchyroll.Crunchyroll",
    "Calendar by Dashbd": "com.benoitzohar.Calendar",
}
