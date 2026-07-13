[app]
title = UniChat
package.name = unichat
package.domain = org.unichat
source.dir =.
source.include_exts = py,png,jpg,kv,atlas,ttf
version = 1.0.0
requirements = python3,kivy==2.3.0,kivymd==1.2.0,requests,plyer,urllib3,chardet,idna,certifi
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2

android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a
