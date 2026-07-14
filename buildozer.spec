[app]
# (str) Title of your application
title = UniChat

# (str) Package name
package.name = unichat

# (str) Package domain
package.domain = org.university

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (whitelist)
source.include_exts = py,png,jpg,kv,atlas,mp4,avi,mov,mkv,3gp

# (list) Application requirements
requirements = python3,kivy,kivymd,requests,plyer,certifi,urllib3,idna,charset-normalizer

# (str) Application versioning
version = 1.0

# (list) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (int) Target Android API
android.api = 33

# (int) Minimum Android API
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (list) The Android archs to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) Android SDK license automatically accepted
android.accept_sdk_license = True

# (bool) Indicate if the application should be fullscreen
fullscreen = 0

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2
