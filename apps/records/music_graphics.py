from functools import lru_cache
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
    image = image.convert("RGBA")

    # Flatten onto white so transparent pixels count as background
    background = Image.new("RGBA", image.size, (255, 255, 255, 255))
    flattened = Image.alpha_composite(background, image).convert("L")

    # Anything darker than 245 is notation
    mask = flattened.point(lambda p: 255 if p < 245 else 0)
    bbox = mask.getbbox()

    if bbox is None:
        raise RuntimeError("MuseScore produced an empty graphic.")

    return image.crop(bbox)


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

@lru_cache(maxsize=2048)
def _render_chord(clef_name, note_names):
    measure = _make_measure(clef_name)
    chord = m21.chord.Chord([m21.pitch.Pitch(n) for n in note_names])
    chord.quarterLength = 4.0
    measure.append(chord)
    return _render_with_musescore(measure)

def _make_chord_graphic(record, pitches):
    names = tuple(
        _frequency_to_note(f).nameWithOctave for f in pitches
    )
    return _render_chord(record.clef_range, names)


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