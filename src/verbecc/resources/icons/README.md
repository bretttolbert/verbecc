# Verbecc Icons

> ⚠️
> **Developer Only:** This section is intended exclusively for package maintainers and developers. Regular users can safely skip these instructions.

### (Linux) commands used to convert SVG to PNG

Best option is to install the TTF font, since inkscape and imagemagick don't support relative imports

```bash
# Install Spectral TTF font
mkdir -p ~/.local/share/fonts
cp ../fonts/Spectral-Bold.ttf ~/.local/share/fonts/
fc-cache -f -v

# Convert logo SVG to PNG (32-bit, with transparent background)
# 32-bit PNG (preserves the 24-bit RGB true color channels plus an 8-bit alpha transparency channel)
magick -background none -size 512x512 -depth 8 -define png:color-type=6 logo.svg logo.png

# Convert feature graphic SVG to PNG (24-bit, with white background)
# 24-bit PNG (no-alpha)
# -flatten: Tells ImageMagick to merge the transparent layers of the SVG onto that background color, completely removing the alpha channel.
magick -background white -size 1024x500 -depth 8 -define png:color-type=2 feature_graphic.svg -flatten feature_graphic.png

```

### About the Spectral Font

> Spectral is an open-source, contemporary serif typeface commissioned by Google Fonts and designed by Production Type, a digital type foundry based in Paris led by Jean-Baptiste Levée.

> Spectral (designed by Production Type) was designated as the official secondary typeface in the French government design system (Système de Design de l'État).
