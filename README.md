# Custom Materials for Materials Live Wallpaper

Materials that can be imported to [Materials Live Wallpaper](https://github.com/Reminimalism/MaterialsLiveWallpaper)

# Samples

Go to the [releases page](https://github.com/Reminimalism/MaterialsLiveWallpaperCustomMaterials/releases/) to download.

-  Colorful Circular Brush

    4 circles with red, green, blue and silver colors with a natural looking brush texture and visible edges.

    Generated using `generate_circular_brush.py`, `generate_circular_colorful_base_ref.py` and `generate_circular_colorful_others.py` scripts.

    [Download 1024x1024](https://github.com/Reminimalism/MaterialsLiveWallpaperCustomMaterials/releases/download/v2020.08.30/ColorfulCircularBrush_1024x1024.zip),
    [Download 2048x2048](https://github.com/Reminimalism/MaterialsLiveWallpaperCustomMaterials/releases/download/v2020.08.30/ColorfulCircularBrush_2048x2048.zip),
    [Download 4096x4096](https://github.com/Reminimalism/MaterialsLiveWallpaperCustomMaterials/releases/download/v2020.08.30/ColorfulCircularBrush_4096x4096.zip)

- Glitter

    Generated using `generate_glitter.py` script.

    512x512 is recommended for most screen resolutions.
    All glitter variations have 5 layers (4 additional layers),
    you can reduce them by setting the Max Allowed Additional Layers in the app settings if it runs slow or drains battery.
    Only glitter materials with black backgrounds are (almost) compatible with v0.1.

    Dark gray background and RGB & white glitters:
    [Download 512x512](https://github.com/Reminimalism/MaterialsLiveWallpaperCustomMaterials/releases/download/v2020.08.30/Glitter_512x512_DarkGray_RGB.zip),
    [Download 1024x1024](https://github.com/Reminimalism/MaterialsLiveWallpaperCustomMaterials/releases/download/v2020.08.30/Glitter_1024x1024_DarkGray_RGB.zip)

    Gray background and RGB & white glitters:
    [Download 512x512](https://github.com/Reminimalism/MaterialsLiveWallpaperCustomMaterials/releases/download/v2020.08.30/Glitter_512x512_Gray_RGB.zip),
    [Download 1024x1024](https://github.com/Reminimalism/MaterialsLiveWallpaperCustomMaterials/releases/download/v2020.08.30/Glitter_1024x1024_Gray_RGB.zip)

    Black background and RGB & white glitters:
    [Download 512x512](https://github.com/Reminimalism/MaterialsLiveWallpaperCustomMaterials/releases/download/v2020.08.30/Glitter_512x512_Black_RGB.zip),
    [Download 1024x1024](https://github.com/Reminimalism/MaterialsLiveWallpaperCustomMaterials/releases/download/v2020.08.30/Glitter_1024x1024_Black_RGB.zip)

    Dark gray background and Reminimalism colors & white glitters:
    [Download 512x512](https://github.com/Reminimalism/MaterialsLiveWallpaperCustomMaterials/releases/download/v2020.08.30/Glitter_512x512_DarkGray_ReminimalismColors.zip),
    [Download 1024x1024](https://github.com/Reminimalism/MaterialsLiveWallpaperCustomMaterials/releases/download/v2020.08.30/Glitter_1024x1024_DarkGray_ReminimalismColors.zip)

- Default Materials

    The samples offered in the app.

    [Download zip (4096x4096)](https://github.com/Reminimalism/MaterialsLiveWallpaperCustomMaterials/releases/download/v2020.08.30/DefaultMaterials.zip)

# How to create a Custom Material

Create a zip file containing these optional files:

## Base color texture a.k.a. Diffuse map
File name: `base.<image-format>`, for example `base.png`

An image file representing the colors of the materials. Aka diffuse map.

Default behavior when base texture is not included: Black texture.

## Reflections color texture
File name: `reflections.<image-format>`, for example `reflections.png`

An image file representing the color (filter) of reflections in different points.
Black color reflects no light, white reflects any light with max brightness, red reflects only red lights.
Make sure that the sum of base and reflections color at each point is less than or equal to white color.

Default behavior when reflections texture is not included: Black texture.

## Normal texture
File name: `normal.<image-format>`, for example `normal.png`

An image file that represents the normal vector at each point.
Red represents x, Green represents y, Blue represents z. 0 is -1, 128 or 127 is 0, and 255 is 1.

Default behavior when normal texture is not included: A texture filled with (128, 128, 255) or #8080FF (forward direction).

## Shininess texture
File name: `shininess.<image-format>`, for example `shininess.png`

An image file that represents shininess, the more the shininess, the smaller the reflection radius/size is.

Default behavior when shininess texture is not included: Black texture (0 value).

## Brush texture
File name: `brush.<image-format>`, for example `brush.png`

An image file representing brush direction and magnitude at different points.
The brush effect doesn't expand the reflection radius, it shrinks it in a specific direction, so try to use less shininess values in the brushed areas.
Red represents x, Green represents y, Blue represents z.
0 is almost -1 (-1.003921569), 128 is exactly 0, and 255 is almost 1 (0.996078431).
It is recommended to use 1 (= 128 - 127) as -1, and 255 (= 128 + 127) as 1.

Default behavior when brush texture is not included: A texture filled with (128, 128, 128) or #808080 (0 vector).

## Brush Intensity texture
File name: `brush_intensity.<image-format>`, for example `brush_intensity.png`

An image file representing a number at each point to multiply the brush vector by it.
This is used to have more precise brushes, by using more ranges in the brush texture, representing brush directions, and then reducing the brush vector sizes using this texture.

Default behavior when brush intensity texture is not included: A texture filled with (255, 255, 255) or #FFFFFF, or 255 or #FF grayscale value (1 coefficient).

As an example, see `CircularBrush.zip` located in `DefaultMaterials.zip` or one of `ColorfulCircularBrush_<resolution>.zip`,
available in [releases](https://github.com/Reminimalism/MaterialsLiveWallpaperCustomMaterials/releases/).

## Config
File name: `config.json`

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

See [sample_config.json](https://github.com/Reminimalism/MaterialsLiveWallpaperCustomMaterials/blob/master/sample_config.json) as an example.
Note that the name of this file in the zip should exactly be `config.json`.

# Resolutions and aspect ratios

Please use 1:1 aspect ratio (width=height) in all of the images, this is to support both portrait and landscape view without rotating the textures 90 degrees.
Images can have different resolutions, they will be stretched to match the square, it is recommended to use resolutions that are powers of 2, for example 2048x2048.
If the result is not intended to look pixelated, 2048x2048 is enough for 1080p displays, and almost fine for 1440p, 4096x4096 is enough for 4K and 1440p, 1024x1024 is almost fine for 720p.

# Layers

Additional layers of each texture can be added to create global illumination or other effects.
Maximum allowed number of additional layers is 4, and the default is 2 from v0.4.
Each additional layer's file is named like this (1 ≤ number ≤ 4): `<texture-name><layer-number>.<image-format>`

For example: `base.png`, `reflections.png`, `base1.png`, `reflections1.png`, `normal1.png`, `shininess1.png`, `reflections2.png`, `brush2.png`, `brush_intensity2.png`

Avoid bright base and reflections for the additional layers to prevent an overexposed look.
The blending mode used is additive, that means the resulting color in a pixel is the sum of all the colors in all layers in that pixel.

Users might allow a limited number of additional layers or turn them off, so prioritize on what to put in the main layer and the additional layers.
The main layer (rendered from the files without numbers) is always shown.
For additional layers, the less the layer's number, the more likely it's going to be shown.

# Changelog

- 0.2:
  - Added layers support
  - Not including the base or reflections textures results in a behavior like the missing ones are black (don't exist).

- 0.1:
  - Default base and reflections textures are gray.
