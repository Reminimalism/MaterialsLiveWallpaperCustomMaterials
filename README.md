# Material Samples for Materials Live Wallpaper

Some material samples that can be imported to [Materials Live Wallpaper](https://github.com/Reminimalism/MaterialsLiveWallpaper)

# More Materials

  - **ColorfulCircularBrush:** generated using `generate_circular_brush.py`, `generate_circular_colorful_base_ref.py` and `generate_circular_colorful_others.py` scripts.
    - [Download 1024x1024](https://github.com/Reminimalism/MaterialsLiveWallpaperMaterialSamples/raw/master/More%20Materials/ColorfulCircularBrush_1024x1024.zip)
    - [Download 2048x2048](https://github.com/Reminimalism/MaterialsLiveWallpaperMaterialSamples/raw/master/More%20Materials/ColorfulCircularBrush_2048x2048.zip)
    - [Download 4096x4096](https://github.com/Reminimalism/MaterialsLiveWallpaperMaterialSamples/raw/master/More%20Materials/ColorfulCircularBrush_2048x2048.zip)

# How to create a Custom Material

Create a zip file containing these optional files:

## Base color texture a.k.a. Diffuse map (base.\<image-format\>, for example base.png)

An image file representing the colors of the materials. Aka diffuse map.

The default texture is filled with (128, 128, 128) or #808080 (gray).

## Reflections color texture (reflections.\<image-format\>, for example reflections.png)

An image file representing the color (filter) of reflections in different points.
Black color reflects no light, white reflects any light with max brightness, red reflects only red lights.
Make sure that the sum of base and reflections color at each point is less than or equal to white color.

The default texture is filled with (128, 128, 128) or #808080 (gray).

## Normal texture (normal.\<image-format\>, for example normal.png)

An image file that represents the normal vector at each point.
Red represents x, Green represents y, Blue represents z. 0 is -1, 128 is 0, and 255 is 1.

The default texture is filled with (128, 128, 255) or #8080FF (forward direction).

## Shininess texture (shininess.\<image-format\>, for example shininess.png)

An image file that represents shininess, the more the shininess, the smaller the reflection radius/size is.

The default texture is filled with (0, 0, 0) or #000000 (black).

## Brush texture (brush.\<image-format\>, for example brush.png)

An image file representing brush direction and magnitude at different points.
The brush effect doesn't expand the reflection radius, it shrinks it in a specific direction, so try to use less shininess values in the brushed areas.
Red represents x, Green represents y, Blue represents z.
0 is almost -1 (-1.003921569), 128 is exactly 0, and 255 is almost 1 (0.996078431).

The default texture is filled with (128, 128, 128) or #808080 (0 vector).

## Brush Intensity texture (brush_intensity.\<image-format\>, for example brush_intensity.png)

An image file representing a number at each point to multiply the brush vector by it.
This is used to have more precise brushes, by using more ranges in the brush texture and then reducing the brush vector sizes using this texture.

As an example, see [CircularBrush.zip](https://github.com/Reminimalism/MaterialsLiveWallpaperMaterialSamples/raw/master/Materials/CircularBrush.zip).

## Config (config.json)

There are these optional fields to set:

  - TargetVersion: The version name of the target version.
  - Pixelated<texture-name>: Whether the pixels of a low res texture should be rendered as squares. This is the full list:
    - PixelatedBase
    - PixelatedReflections
    - PixelatedNormal
    - PixelatedShininess
    - PixelatedBrush
    - PixelatedBrushIntensity
  - NormalizeNormal: Whether to normalize the normal map in the shader.

See sample_config.json as an example. Note that the name of this file in the zip should exactly be "config.json".
