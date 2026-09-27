import tempfile
from io import BytesIO

import music21 as m21
from PIL import Image
from src.utils import freq_to_note


# CSS/display size is roughly 180px wide.
# We render at 2x resolution for better sharpness.
GRAPHIC_WIDTH = 180
RENDER_SCALE = 2


def _make_measure(clef_name):
    measure = m21.stream.Measure()

    if clef_name == "Bass":
        measure.append(m21.clef.BassClef())
    else:
        measure.append(m21.clef.TrebleClef())

    time_signature = m21.meter.TimeSignature("4/4")
    time_signature.style.hideObjectOnPrint = True
    measure.insert(0, time_signature)

    measure.rightBarLine = None

    return measure


def _frequency_to_note(frequency):
    note, octave = freq_to_note(frequency)
    note = note.replace("♯", "#")
    return m21.pitch.Pitch(f"{note}{octave}")


def _crop_to_notation(image):
    """
    Remove the whitespace surrounding the actual MuseScore notation.
    """

    image = image.convert("RGBA")
    pixels = image.load()

    bbox = None

    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = pixels[x, y]

            # MuseScore notation is dark against a white background.
            if a > 0 and min(r, g, b) < 245:
                if bbox is None:
                    bbox = [x, y, x, y]
                else:
                    bbox[0] = min(bbox[0], x)
                    bbox[1] = min(bbox[1], y)
                    bbox[2] = max(bbox[2], x)
                    bbox[3] = max(bbox[3], y)

    if bbox is None:
        raise RuntimeError("MuseScore produced an empty graphic.")

    left, top, right, bottom = bbox

    return image.crop(
        (left, top, right + 1, bottom + 1)
    )


def _render_with_musescore(measure):
    """
    Render a music21 measure with MuseScore.

    The resulting image is cropped to the actual notation and rendered
    at 2x display resolution. Height is allowed to grow for ledger lines.
    """

    with tempfile.TemporaryDirectory() as temp_dir:
        output_path = f"{temp_dir}/graphic"

        png_path = measure.write(
            "musicxml.png",
            fp=output_path,
        )

        with Image.open(png_path) as image:
            cropped = _crop_to_notation(image)

            # ---------------------------------------------------------
            # Render at 2x the intended display width.
            #
            # We intentionally DO NOT constrain height.
            # Ledger lines therefore increase the image height instead
            # of causing the notation to be vertically squashed.
            # ---------------------------------------------------------

            target_width = GRAPHIC_WIDTH * RENDER_SCALE

            if cropped.width > target_width:
                scale = target_width / cropped.width

                cropped = cropped.resize(
                    (
                        target_width,
                        round(cropped.height * scale),
                    ),
                    Image.Resampling.LANCZOS,
                )

            # Small amount of whitespace around the notation.
            padding_x = 8 * RENDER_SCALE
            padding_y = 4 * RENDER_SCALE

            canvas_width = max(
                target_width,
                cropped.width + (2 * padding_x),
            )

            canvas_height = (
                cropped.height + (2 * padding_y)
            )

            canvas = Image.new(
                "RGBA",
                (
                    canvas_width,
                    canvas_height,
                ),
                (255, 255, 255, 255),
            )

            x = (canvas_width - cropped.width) // 2
            y = padding_y

            canvas.alpha_composite(
                cropped,
                (x, y),
            )

            output = BytesIO()

            canvas.save(
                output,
                format="PNG",
                optimize=True,
            )

            return output.getvalue()


def _make_chord_graphic(record, pitches):
    measure = _make_measure(record.clef_range)

    notes = [
        _frequency_to_note(frequency)
        for frequency in pitches
    ]

    chord = m21.chord.Chord(notes)
    chord.quarterLength = 4.0

    measure.append(chord)

    return _render_with_musescore(measure)


def generate_compositional_range(record):
    return _make_chord_graphic(
        record,
        [
            record.min_freq,
            record.max_freq,
        ],
    )


def generate_tessitura(record):
    return _make_chord_graphic(
        record,
        [
            record.q1_freq,
            record.q3_freq,
        ],
    )


def generate_median_pitch(record):
    measure = _make_measure(record.clef_range)

    median_pitch = _frequency_to_note(record.median_freq)

    note = m21.note.Note(median_pitch)
    note.quarterLength = 4.0

    measure.append(note)

    return _render_with_musescore(measure)