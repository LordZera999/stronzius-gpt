[app]
title = Stronzius GPT
package.name = stronziusgpt
package.domain = org.stronzius

# (str) Source files to include (let it empty to include all files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Directory where the source files are located
source.dir = .

version = 1.0
requirements = python3,kivy,google-genai,pydantic,certifi,urllib3,idna,charset-normalizer,requests
orientation = portrait
fullscreen = 0
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33