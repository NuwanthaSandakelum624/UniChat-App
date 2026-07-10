[app]
# (str) Title of your application
title = UniChat

# (str) Package name
package.name = unichat

# (str) Package domain
package.domain = org.unichat

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas,mp4

# (str) Application version
version = 0.1

# (list) Application requirements
requirements = python3,kivy,kivymd,requests,plyer,pillow

# (list) Permissions
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

# (str) Orientation
orientation = portrait

# (bool) Fullscreen
fullscreen = 0

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

[android]
# (list) Android archs to build
android.archs = arm64-v8a

# (str) Android NDK version to use (මේක අනිවාර්යයි)
android.ndk = 25b

# (bool) Accept SDK license
android.accept_sdk_license = True

# (int) Android API version
android.api = 33

# (int) Android min API version
android.minapi = 21
