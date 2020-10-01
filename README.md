# Custom Materials for Materials Live Wallpaper

Materials that can be imported to [Materials Live Wallpaper](https://github.com/Reminimalism/MaterialsLiveWallpaper)

# Samples

Go to the [releases page](https://github.com/Reminimalism/MaterialsLiveWallpaperMaterialSamples/releases/) to download.

## Colorful Circular Brush

4 circles with red, green, blue and silver colors with a natural looking brush texture and visible edges.

Generated using `generate_circular_brush.py`, `generate_circular_colorful_base_ref.py` and `generate_circular_colorful_others.py` scripts.

## Glitter

TODO

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
File name: `normal.<image-format>`, for `example normal.png`

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
It is recommended to use 128 - 127 = 1 as -1, and 128 + 127 = 255 as 1.

Default behavior when brush texture is not included: A texture filled with (128, 128, 128) or #808080 (0 vector).

## Brush Intensity texture
File name: `brush_intensity.<image-format>`, for example `brush_intensity.png`

An image file representing a number at each point to multiply the brush vector by it.
This is used to have more precise brushes, by using more ranges in the brush texture, representing brush directions, and then reducing the brush vector sizes using this texture.

Default behavior when brush intensity texture is not included: A texture filled with (255, 255, 255) or #FFFFFF, or 255 or #FF grayscale value (1 coefficient).

As an example, see `CircularBrush.zip` located in `DefaultMaterials.zip` or one of `ColorfulCircularBrush_<resolution>.zip`,
available in [releases](https://github.com/Reminimalism/MaterialsLiveWallpaperMaterialSamples/releases/).

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

See [sample_config.json](https://github.com/Reminimalism/MaterialsLiveWallpaperMaterialSamples/blob/master/sample_config.json) as an example.
Note that the name of this file in the zip should exactly be `config.json`.

# Layers

Additional layers of each texture can be added to create global illumination or other effects.
Maximum allowed number of additional layers is 4.
Each layer's file is named like this (1 ≤ number ≤ 4): `<texture-name><layer-number>.<image-format>`

For example: `base1.png`, `reflections1.png`, `normal1.png`, `shininess1.png`, `reflections2.png`, `brush2.png`, `brush_intensity2.png`

Avoid bright base and reflections for the additional layers to prevent an overexposed look.

# Changelog

- 0.2:
  - Added layers support
  - Not including the base or reflections textures results in a behavior like the missing ones are black (don't exist).

- 0.1:
  - Default base and reflections textures are gray.
