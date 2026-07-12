[app]
title = UniChat
package.name = unichat
package.domain = org.unichat

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,mp4

version = 1.0
requirements = python3,kivy==2.3.0,kivymd==1.2.0,requests,plyer,pillow,certifi,urllib3,idna,charset-normalizer

# Screen orientation
orientation = portrait
fullscreen = 0

# Android permissions needed for: network calls, picking photos/videos from storage
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,READ_MEDIA_IMAGES,READ_MEDIA_VIDEO

# API / SDK targets
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

# Needed by plyer.filechooser on modern Android
android.allow_backup = True

# Auto-accept SDK licenses so CI builds don't hang waiting for input
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
