
from pathlib import Path
from io import BytesIO
import tempfile

from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageClip, concatenate_videoclips, vfx

WIDTH, HEIGHT = 1280, 720
SCENE_SECONDS = 3.5
TRANSITION_SECONDS = 0.5

GOLD = (213, 177, 105)
WHITE = (250, 247, 240)
DARK = (16, 18, 21)


def get_font(size, bold=False):
    candidates = (
        ["C:/Windows/Fonts/arialbd.ttf",
         "C:/Windows/Fonts/arial.ttf"]
        if bold else
        ["C:/Windows/Fonts/arial.ttf",
         "C:/Windows/Fonts/arialbd.ttf"]
    )

    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)

    return ImageFont.load_default()


def fit_image(image, size=(WIDTH, HEIGHT)):
    """Crop an image to fill the video frame."""
    target_w, target_h = size
    image = image.convert("RGB")

    scale = max(target_w / image.width, target_h / image.height)
    new_size = (
        int(image.width * scale),
        int(image.height * scale),
    )
    image = image.resize(new_size, Image.Resampling.LANCZOS)

    left = (image.width - target_w) // 2
    top = (image.height - target_h) // 2

    return image.crop((
        left, top, left + target_w, top + target_h
    ))


def add_gradient(image):
    """Add a cinematic dark gradient for readable text."""
    image = image.convert("RGBA")
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    pixels = overlay.load()

    for y in range(HEIGHT):
        strength = int(180 * (y / HEIGHT) ** 2)
        for x in range(WIDTH):
            pixels[x, y] = (5, 7, 10, strength)

    return Image.alpha_composite(image, overlay)


def draw_centered(draw, text, y, font, fill, anchor="mt"):
    draw.text(
        (WIDTH // 2, y),
        text,
        font=font,
        fill=fill,
        anchor=anchor,
    )


def save_card(image, path):
    image.convert("RGB").save(path, quality=94)


def create_opening(property_name, location, price, path):
    image = Image.new("RGB", (WIDTH, HEIGHT), DARK)
    draw = ImageDraw.Draw(image)

    # Refined architectural-style frame
    draw.rectangle(
        (35, 35, WIDTH - 35, HEIGHT - 35),
        outline=GOLD,
        width=2,
    )

    draw_centered(
        draw, "EXCLUSIVE PROPERTY COLLECTION",
        205, get_font(22), GOLD
    )

    draw_centered(
        draw, property_name[:45],
        290, get_font(54, True), WHITE
    )

    draw.line(
        (WIDTH // 2 - 100, 375, WIDTH // 2 + 100, 375),
        fill=GOLD, width=3,
    )

    draw_centered(
        draw, location,
        405, get_font(27), WHITE
    )

    draw_centered(
        draw, price,
        465, get_font(32, True), GOLD
    )

    save_card(image, path)


def create_property_scene(image_bytes, caption, index, path):
    with Image.open(BytesIO(image_bytes)) as source:
        image = fit_image(source)

    image = add_gradient(image)
    draw = ImageDraw.Draw(image)

    # Scene number and restrained gold detailing
    draw.text(
        (65, 45),
        f"PROPERTY HIGHLIGHTS  /  {index:02d}",
        font=get_font(18),
        fill=GOLD,
    )

    draw.line(
        (65, HEIGHT - 150, 160, HEIGHT - 150),
        fill=GOLD,
        width=4,
    )

    draw.text(
        (65, HEIGHT - 125),
        caption[:55],
        font=get_font(38, True),
        fill=WHITE,
    )

    draw.text(
        (65, HEIGHT - 65),
        "DESIGNED FOR BETTER LIVING",
        font=get_font(17),
        fill=GOLD,
    )

    save_card(image, path)


def create_closing(property_name, location, price, contact, path):
    image = Image.new("RGB", (WIDTH, HEIGHT), DARK)
    draw = ImageDraw.Draw(image)

    draw.rectangle(
        (35, 35, WIDTH - 35, HEIGHT - 35),
        outline=GOLD,
        width=2,
    )

    draw_centered(
        draw, "YOUR NEXT CHAPTER STARTS HERE",
        175, get_font(23), GOLD
    )

    draw_centered(
        draw, property_name[:45],
        245, get_font(45, True), WHITE
    )

    draw_centered(
        draw, location,
        325, get_font(25), WHITE
    )

    draw_centered(
        draw, price,
        390, get_font(39, True), GOLD
    )

    draw.line(
        (WIDTH // 2 - 90, 455, WIDTH // 2 + 90, 455),
        fill=GOLD, width=2,
    )

    draw_centered(
        draw, contact[:55],
        490, get_font(24, True), WHITE
    )

    draw_centered(
        draw, "ENQUIRE TODAY",
        550, get_font(18), GOLD
    )

    save_card(image, path)


def generate_video(
    property_name,
    location,
    price,
    property_type,
    features,
    contact,
    images,
    output_path="output/property_video.mp4",
):
    """Create a luxury-styled property marketing video."""

    if not 4 <= len(images) <= 8:
        raise ValueError("Upload between 4 and 8 property images.")

    fields = {
        "Property name": property_name,
        "Location": location,
        "Price": price,
        "Property type": property_type,
        "Features": features,
        "Contact text": contact,
    }

    for name, value in fields.items():
        if not value or not value.strip():
            raise ValueError(f"{name} is required.")

    feature_list = [
        item.strip()
        for item in features.replace("\n", ",").split(",")
        if item.strip()
    ]

    # Captions contain only user-provided property facts.
    captions = [
        f"{property_type} Living",
        f"Located in {location}",
        f"Price: {price}",
    ]

    captions.extend(feature_list)
    captions = captions[:len(images)]

    output = Path(output_path).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    clips = []
    final_clip = None

    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)

            opening = temp / "opening.jpg"
            create_opening(
                property_name, location, price, opening
            )

            paths = [opening]

            for index, (image_bytes, caption) in enumerate(
                zip(images, captions), start=1
            ):
                scene_path = temp / f"scene_{index}.jpg"

                create_property_scene(
                    image_bytes,
                    caption,
                    index,
                    scene_path,
                )
                paths.append(scene_path)

            closing = temp / "closing.jpg"
            create_closing(
                property_name, location, price, contact, closing
            )
            paths.append(closing)

            for index, path in enumerate(paths):
                clip = ImageClip(str(path)).with_duration(
                    SCENE_SECONDS
                )

                if index > 0:
                    clip = clip.with_effects([
                        vfx.CrossFadeIn(TRANSITION_SECONDS)
                    ])

                clips.append(clip)

            final_clip = concatenate_videoclips(
                clips,
                method="compose",
                padding=-TRANSITION_SECONDS,
            )

            final_clip.write_videofile(
                str(output),
                fps=24,
                codec="libx264",
                audio=False,
                logger=None,
            )

    finally:
        if final_clip is not None:
            final_clip.close()

        for clip in clips:
            clip.close()

    if not output.exists() or output.stat().st_size == 0:
        raise RuntimeError("Video export failed.")

    return str(output)


if __name__ == "__main__":
    print("Luxury video generator is ready.")
