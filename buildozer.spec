[app]

# Application name
title = D X D Calculations

# Package name
package.name = dxdcalculations

# Android package domain
package.domain = org.dxdcalculations

# Source directory
source.dir = .

# Files included in the APK
source.include_exts = py,png,jpg,jpeg,kv,atlas

# Application version
version = 1.0.0

# Python dependencies
requirements = python3,kivy,sympy

# Portrait mode
orientation = portrait

# Do not use fullscreen
fullscreen = 0

# Application icon
icon.filename = %(source.dir)s/assets/icon.png

# Android splash screen
presplash.filename = %(source.dir)s/assets/presplash.png


[buildozer]

# Buildozer logging level
log_level = 2

# Show warning when running Buildozer as root
warn_on_root = 1
