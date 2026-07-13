[app]
title = UniChat
package.name = unichat
package.domain = org.unichat

source.dir =.
source.include_exts = py,png,jpg,kv,atlas,ttf
source.exclude_dirs = tests, bin,.git

version = 1.0.0
requirements = python3,kivy==2.3.0,kivymd==1.2.0,requests,plyer,urllib3,chardet,idna,certifi
presplash.filename = %(source.dir)s/data/presplash.png
icon.filename = %(source.dir)s/data/icon.png

orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2

android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk_path = ~/.buildozer/android/platform/android-sdk
android.accept_sdk_license = True
android.archs = arm64-v8a
p4a.branch = develop

[app:android]
android.allow_backup = true
