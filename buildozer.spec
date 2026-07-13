[app]
# (str) Title of your application
title = UniChat

# (str) Package name
package.name = unichat

# (str) Package domain (needed for android/ios packaging)
package.domain = org.university

# (str) Source code where the main.py live
source.include_exts = py,png,jpg,kv,atlas,mp4,avi,mov,mkv,3gp

# (list) Application requirements
# (comma separated strings)
requirements = python3,kivy,kivymd,requests,plyer,certifi,urllib3,idna,charset-normalizer

# (str) Application versioning
version = 1.0

# (list) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (int) Target Android API
android.api = 33

# (int) Minimum Android API
android.minapi = 21

# (int) Android SDK build tools version
# මෙය හිස්ව තැබීමෙන් පවතින උසස්ම අනුවාදය ස්වයංක්‍රීයව තෝරාගනී
android.build_tools_version = 

# (bool) Android SDK license automatically accepted
# මෙය අනිවාර්යයෙන්ම True විය යුතුය (ඔබේ ගැටලුව සඳහා)
android.accept_sdk_license = True

# (str) Presplash of the application
# presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
# icon.filename = %(source.dir)s/data/icon.png

# (bool) Indicate if the application should be fullscreen
fullscreen = 0

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2
