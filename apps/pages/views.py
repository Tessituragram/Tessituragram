from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.views.generic import TemplateView
from .forms import ContactForm


def home(request):
    return render(request, "pages/home.html")


class PeopleView(TemplateView):
    template_name = "pages/static_page.html"
    extra_context = {
        "page_title": "People",
        "content": [
            """
                <b1>Troy O. Conklin</b1> <b2>(he/him/Mr.) is an associate developer at
                Thoughtworks and graduated summa cum laude from Brown University
                with degrees in computer science and philosophy. He previously worked as a systems
                engineer with General Dynamics Electric Boat
                and completed a competitive internship with the National Institute of Standards and Technology.
                Troy’s personal interests span from the fabric arts to astrophotography to wild foraging.
                Troy is the coder behind
                <a href="https://github.com/Tessituragram/Tessituragram" target="_blank" rel="noopener"><i>Tessituragram</i></a>
                and manages the backend of
                <a href="https://tessituragram.com" target="_blank" rel="noopener">tessituragram.com</a>.</b2>
            """,
            """
                <b1>Paul M. Patinka</span> </b1><b2>(they/them/Mx.) is a PhD student in Music Education at Northwestern University.
                Paul’s collaborative and independent publications appear in the <i>College Music Symposium</i>,
                <i>InterNos</i>, <i>Journal of Singing</i>, <i>Journal of Voice</i>, and
                <i>Studies in Musical Theatre</i>.
                They collaborated on the “Developmental Selection of Vocal Music” chapter in the forthcoming
                <i>Oxford Handbook of Voice Pedagogy</i>, and regularly present research at national and regional
                conferences. Paul is the musician and researcher behind
                <a href="https://github.com/Tessituragram/Tessituragram" target="_blank" rel="noopener"><i>Tessituragram</i></a>
                and manages the content and data of
                <a href="https://tessituragram.com" target="_blank" rel="noopener">tessituragram.com</a>.</b2>
            """,
        ],
    }


class MissionView(TemplateView):
    template_name = "pages/static_page.html"
    extra_context = {
        "page_title": "Our Mission",
        "content": [
            """
            <b1>
                Our mission in creating and perpetuating this database is to provide singers and teachers
                with resources that allow them to assess the musical difficulty of vocal pieces more
                objectively. We developed Tessituragram, a software, to analyze MIDI files and produce
                the metrics in this database. Through member contributions and access to information,
                we hope that this resource serves as another tool through which we can better understand
                our musical selections.
            </b1>
            """,
        ],
    }


class BackgroundView(TemplateView):
    template_name = "pages/static_page.html"
    extra_context = {
        "page_title": "Background",
        "content": [
            """
            <div class="content-card">
                <q1>
                    The practical application of the term tessitura has in the past been vague.
                    Teachers, singers, musical directors, and connoisseurs of vocal music all have
                    their own ideas—often subjective—of what the tessitura of a piece is. Often the
                    extreme notes of a composition, the highest and lowest notes to be sung, are
                    specified; but this information alone is insufficient to determine vocal difficulty.<sup>1</sup>
                </q1>
                <footer>
                </footer>
                <h2>Brief History</h2>
                    <div class="background-history">
                        <p><b1>1988</b1><b2> - Stefan Thürmer proposed an analysis procedure to generate a “tessiturogram” and provide singers with objective measurements of <i>tessitura</i> graphically represented as a histogram.<sup>2</sup></b2></p>
                        <p><b1>2008</b1><b2> - Ingo Titze renamed Thürmer’s process the “tessituragram,” (the current nomenclature), included musical accidentals in analysis, and defined time dose and cycle dose.<sup>3</sup></b2></p>
                        <p><b1>2014</b1><b2> - John Nix defined recovery/rest time.<sup>4</sup></b2></p>
                        <p><b1>2019</b1><b2> - Nicole Pizzorni et al. proposed a method of understanding musical difficulty based on assessing musical <i>passaggi</i> zones.<sup>5</sup></b2></p>
                        <p><b1>2022</b1><b2> - Paul M. Patinka, Jesus De Hoyos, and James D. Rodriguez used quartile analysis with equally weighted pitch subdivisions to calculate musical <i>tessitura</i> and compositional range.<sup>6</sup></b2></p>
                        <p><b1>2025</b1><b2> - Patinka expanded on the analysis proposed by Pizzorni et al. for assessing musical <i>passaggi</i>.<sup>7</sup></b></p>
                        <p><b1>2026</b1><b2> - Patinka manually analyzed 150 Western classical operatic arias to set up a ground truth dataset and worked with Troy O. Conklin to build <i>Tessituragram</i>.<sup>8</sup></b></p>
                    </div>
                <footer>
                    <ol start="1">
                        <li><span class="upright">Thürmer, Stefan. “The Tessiturogram.” <i>Journal of Voice</i> 2, no. 4 (1988): 327. <a href="https://doi.org/10.1016/S0892-1997(88)80025-0" target="_blank" rel="noopener">https://doi.org/10.1016/S0892-1997(88)80025-0</a>.</span></li>
                        <li><span class="upright">Thürmer, The Tessiturogram, 327–29.</span></li>
                        <li><span class="upright">Titze, Ingo R. “Quantifying Tessitura in a Song.” <i>Journal of Singing</i> 65, no. 1 (2008): 59–61.</span></li>
                        <li><span class="upright">Nix, John. “Measuring Mozart: A Pilot Study Testing the Accuracy of Objective Methods for Matching a Song to a Singer.” <i>Journal of Singing</i> 70, no. 5 (2014): 561–72.</span></li>
                        <li><span class="upright">Pizzorni, Nicole, Antonio Schindler, Matteo Sozzi, Massimo Corbo, and Marco Gilardone. “The Vocal Score Profile in Verdi’s Characters.” <i>Journal of Voice</i> 33, no. 5 (2019): 805.e13–e20. <a href="https://doi.org/10.1016/j.jvoice.2018.03.013" target="_blank" rel="noopener">https://doi.org/10.1016/j.jvoice.2018.03.013</a>.</span></li>
                        <li><span class="upright">Patinka, Paul M., Jesus De Hoyos Jr., and James Rodriguez. “Quantitative Analysis of the Texas Music Educators Association (TMEA) All-State Choral Audition Music.” <i>Journal of Voice</i> 36, no. 5 (2022): 732.e9–e19. <a href="https://doi.org/10.1016/j.jvoice.2020.08.038" target="_blank" rel="noopener">https://doi.org/10.1016/j.jvoice.2020.08.038</a>.</span></li>
                        <li><span class="upright">Patinka, Paul M. “Analyzing Musical <i>passaggi</i> in <i>Erlkönig</i> by Franz Schubert: A Pilot Study.” <i>Journal of Voice</i> (2025). <a href="https://doi.org/10.1016/j.jvoice.2025.05.030" target="_blank" rel="noopener">https://doi.org/10.1016/j.jvoice.2025.05.030</a>.</span></li>
                        <li><span class="upright">Patinka, Paul M. “Musical Tessituragram Analysis of Arias in the G. Schirmer Opera Anthology Series.” <i>Journal of Voice</i> (2026). <a href="https://doi.org/10.1016/j.jvoice.2026.01.004" target="_blank" rel="noopener">https://doi.org/10.1016/j.jvoice.2026.01.004</a>.; Conklin, Troy O., and Paul M. Patinka. “Automated Tessituragram Analysis Software of Musical Instrument Digital Interface (MIDI) Files to Quantitatively Assess Musical Demands.” <i>Journal of Voice</i> (2026).</span></li>
                    </ol>
                </footer>
            </div>
            """,
            """
            <div class="content-card">
                <h2>Selected Bibliography</h2>
                    <p><b2>
                        We intentionally include a mixture of practitioner and research sources in this selected bibliography to highlight the importance of <i>tessitura</i> when discussing the appropriateness of fit between a singer and their music. Additionally, we incorporated the sources we used to develop the metrics reported on each Musical Demand Profile that generates from uploaded MIDI files.
                    </b2></p>

                    <p><b2>
                        American Academy of Teachers of Singing. “Suggested Guidelines for the Composition of Vocal Music.”
                        <i>Journal of Singing</i> 63, no. 5 (2007): 513–21.
                    </b2></p>

                    <p><b2>
                        Blades-Zeller, Elizabeth.
                        <i>A Spectrum of Voices: Prominent American Voice Teachers Discuss the Teaching of Singing.</i>
                        Scarecrow Press, 2002.
                    </b2></p>

                    <p><b2>
                        Blyskal, Elena. “The Female <i>Primo Passaggio:</i> A Survey of Its Physiology, Psychology, and Pedagogy.”
                        <i>Journal of Singing</i> 69, no. 1 (2012): 11–9.
                    </b2></p>

                    <p><b2>
                        Conklin, Troy O., and Paul M. Patinka.
                        “Automated Tessituragram Analysis Software of Musical Instrument Digital Interface (MIDI) Files to Quantitatively Assess Musical Demands.”
                        <i>Journal of Voice</i> (forthcoming).
                    </b2></p>

                    <p><b2>
                        Cotton, Sandra. “<i>Fach</i> vs. Voice Type: A Call for Critical Discussion.”
                        <i>Journal of Singing</i> 69, no. 2 (2012): 153–66.
                    </b2></p>

                    <p><b2>
                        Davids, Julia, and Stephen LaTour.
                        <i>Vocal Technique: A Guide to Classical and Contemporary Styles for Conductors, Teachers, and Singers.</i>
                        Waveland Press, 2021.
                    </b2></p>

                    <p><b2>
                        Doscher, Barbara M.
                        <i>The Functional Unity of the Singing Voice.</i>
                        2nd ed. The Scarecrow Press, Inc., 1994.
                    </b2></p>

                    <p><b2>
                        Echternach, Matthias, Fabian Burk, Marie Köberlein, et al.
                        “Laryngeal Evidence for the First and Second <i>Passaggio</i> in Professionally Trained Sopranos.”
                        <i>PLOS ONE</i> 12, no. 5 (2017): 1–18.
                        <a href="https://doi.org/10.1371/journal.pone.0175865" target="_blank" rel="noopener">https://doi.org/10.1371/journal.pone.0175865</a>.
                    </b2></p>

                    <p><b2>
                        Elliott, JanClaire. “Frequency, Duration, and Pitch <i>or</i> What Makes a <i>Tessitura</i>?”
                        <i>Journal of Singing</i> 60, no. 3 (2004): 239–53.
                    </b2></p>

                    <p><b2>
                        Hansen, Sharon, Allen Henderson, Scott McCoy, Donald Simonson, and Brenda Smith.
                        “Choral Directors Are from Mars and Voice Teachers Are from Venus: “Sing from the Diaphragm” and Other Vocal Mistructions Part 2.”
                        <i>Choral Journal</i> 54, no. 11 (2014): 47–53.
                        <a href="https://www.jstor.org/stable/43052014" target="_blank" rel="noopener">https://www.jstor.org/stable/43052014</a>.
                    </b2></p>

                    <p><b2>
                        Herbst, Christian T. “Registers—The Snake Pit of Voice Pedagogy Part 1: Proprioception, Perception, and Laryngeal Mechanisms.”
                        <i>Journal of Singing</i> 77, no. 2 (2020): 175–90.
                    </b2></p>

                    <p><b2>
                        Herbst, Christian T. “Registers—The Snake Pit of Voice Pedagogy Part 2: Mixed Voice, Vocal Tract Influences, Individual Teaching Systems.”
                        <i>Journal of Singing</i> 77, no. 3 (2021): 345–58.
                    </b2></p>

                    <p><b2>
                        Herbst, Christian T., Elke Duus, Harald Jers, and Jan G. Švec.
                        “Quantitative Voice Class Assessment of Amateur Choir Singers: A Pilot Investigation.”
                        <i>International Journal of Research in Choral Singing</i> 4, no. 1 (2012): 47–59.
                    </b2></p>

                    <p><b2>
                        Lamarche, Anick, Sten Ternström, and Peter Pabon.
                        “The Singer’s Voice Range Profile: Female Professional Opera Soloists.”
                        <i>Journal of Voice</i> 24, no. 4 (2010): 410–26.
                        <a href="https://doi.org/10.1016/j.jvoice.2008.12.008" target="_blank" rel="noopener">https://doi.org/10.1016/j.jvoice.2008.12.008</a>.
                    </b2></p>

                    <p><b2>
                        McCoy, Scott. “Building the Foundation.”
                        <i>Journal of Singing</i> 67, no. 1 (2010): 43–6.
                    </b2></p>

                    <p><b2>
                        McCoy, Scott. “The Choir Issue, Part 1.”
                        <i>Journal of Singing</i> 67, no. 3 (2011): 297–301.
                    </b2></p>

                    <p><b2>
                        McCoy, Scott.
                        <i>Your Voice: An Inside View.</i>
                        2nd ed. Inside View Press, 2012.
                    </b2></p>

                    <p><b2>
                        Michael, Deirdre D. “Don’t Throw the Baby Out with the Bathwater: The Muscular Basis for Register Adjustment.”
                        <i>Journal of Singing</i> 80, no. 5 (2024): 543–52.
                        <a href="https://doi.org/10.53830/sing.00042" target="_blank" rel="noopener">https://doi.org/10.53830/sing.00042</a>.
                    </b2></p>

                    <p><b2>
                        Miller, Donald Gray.
                        <i>Resonance in Singing: Voice Building Through Acoustic Feedback.</i>
                        Inside View Press, 2008.
                    </b2></p>

                    <p><b2>
                        Miller, Richard. “Voice Skill and Vocal Longevity.”
                        <i>Journal of Singing</i> 54, no. 4 (1998): 35–7.
                    </b2></p>

                    <p><b2>
                        Miller, Richard.
                        <i>Solutions for Singers: Tools for Performers and Teachers.</i>
                        Oxford University Press, 2004.
                    </b2></p>

                    <p><b2>
                        Miller, Richard.
                        <i>The Structure of Singing: System and Art in Vocal Technique.</i>
                        Schirmer Books, 1986.
                    </b2></p>

                    <p><b2>
                        Nix, John. “Criteria for Selecting Repertoire.”
                        <i>Journal of Singing</i> 58, no. 3 (2002): 217–21.
                    </b2></p>

                    <p><b2>
                        Nix, John. “Measuring Mozart: A Pilot Study Testing the Accuracy of Objective Methods for Matching a Song to a Singer.”
                        <i>Journal of Singing</i> 70, no. 5 (2014): 561–72.
                    </b2></p>

                    <p><b2>
                        Nix, John. “Systematic Development of Vocal Technique.”
                        In <i>The Oxford Handbook of Singing</i>, edited by Graham F. Welch, David M. Howard, and John Nix.
                        Oxford University Press, 2019.
                    </b2></p>

                    <p><b2>
                        Pabon, Peter. “Future Perspectives: Voice Range Profile-based Voice Quality Feedback.”
                        In <i>The Oxford Handbook of Singing</i>, edited by Graham F. Welch, David M. Howard, and John Nix.
                        Oxford University Press, 2019.
                    </b2></p>

                    <p><b2>
                        Patinka, Paul M. “Analyzing Musical <i>passaggi</i> in <i>Erlkönig</i> by Franz Schubert: A Pilot Study.”
                        <i>Journal of Voice</i> (2025).
                        <a href="https://doi.org/10.1016/j.jvoice.2025.05.030" target="_blank" rel="noopener">https://doi.org/10.1016/j.jvoice.2025.05.030</a>.
                    </b2></p>

                    <p><b2>
                        Patinka, Paul M. “Musical Tessituragram Analysis of Arias in the G. Schirmer Opera Anthology Series.”
                        <i>Journal of Voice</i> (2026).
                        <a href="https://doi.org/10.1016/j.jvoice.2026.01.004" target="_blank" rel="noopener">https://doi.org/10.1016/j.jvoice.2026.01.004</a>.
                    </b2></p>

                    <p><b2>
                        Patinka, Paul M. “Quantitative Analysis of <i>Tessitura</i> and Density in Franz Schubert’s <i>Die schöne Müllerin</i>.”
                        <i>Journal of Voice</i> (2024).
                        <a href="https://doi.org/10.1016/j.jvoice.2024.09.035" target="_blank" rel="noopener">https://doi.org/10.1016/j.jvoice.2024.09.035</a>.
                    </b2></p>

                    <p><b2>
                        Patinka, Paul M., Jesus De Hoyos Jr., and James Rodriguez.
                        “Quantitative Analysis of the Texas Music Educators Association (TMEA) All-State Choral Audition Music.”
                        <i>Journal of Voice</i> 36, no. 5 (2022): 732.e9–e19.
                        <a href="https://doi.org/10.1016/j.jvoice.2020.08.038" target="_blank" rel="noopener">https://doi.org/10.1016/j.jvoice.2020.08.038</a>.
                    </b2></p>

                    <p><b2>
                        Pizzorni, Nicole, Antonio Schindler, Matteo Sozzi, Massimo Corbo, and Marco Gilardone.
                        “The Vocal Score Profile in Verdi’s Characters.”
                        <i>Journal of Voice</i> 33, no. 5 (2019): 805.e13–e20.
                        <a href="https://doi.org/10.1016/j.jvoice.2018.03.013" target="_blank" rel="noopener">https://doi.org/10.1016/j.jvoice.2018.03.013</a>.
                    </b2></p>

                    <p><b2>
                        Ragan, Kari.
                        <i>A Systematic Approach to Voice: The Art of Studio Application.</i>
                        Plural Publishing, 2020.
                    </b2></p>

                    <p><b2>
                        Sandage, Mary J., and Matthew Hoch. “Exercise Physiology: Perspective for Vocal Training.”
                        <i>Journal of Singing</i> 74, no. 4 (2018): 419–25.
                    </b2></p>

                    <p><b2>
                        Schloneger, Matthew, Eric J. Hunter, and Lynn Maxfield.
                        “Quantifying Vocal Repertoire Tessituras Through Real-Time Measures.”
                        <i>Journal of Voice</i> 38, no. 1 (2024): 247.e11–e25.
                        <a href="https://doi.org/10.1016/j.jvoice.2021.06.019" target="_blank" rel="noopener">https://doi.org/10.1016/j.jvoice.2021.06.019</a>.
                    </b2></p>

                    <p><b2>
                        Thürmer, Stefan. “The Tessiturogram.”
                        <i>Journal of Voice</i> 2, no. 4 (1988): 327–29.
                        <a href="https://doi.org/10.1016/S0892-1997(88)80025-0" target="_blank" rel="noopener">https://doi.org/10.1016/S0892-1997(88)80025-0</a>.
                    </b2></p>

                    <p><b2>
                        Titze, Ingo R. “Quantifying Tessitura in a Song.”
                        <i>Journal of Singing</i> 65, no. 1 (2008): 59–61.
                    </b2></p>

                    <p><b2>
                        Titze, Ingo R.
                        <i>Principles of Voice Production.</i>
                        2nd ed. National Center for Voice and Speech, 2000.
                    </b2></p>

                    <p><b2>
                        Titze, Ingo R., and Katherine Verdolini Abbott.
                        <i>Vocology: The Science and Practice of Voice Habilitation.</i>
                        National Center for Voice and Speech, 2012.
                    </b2></p>

                    <p><b2>
                        Titze, Ingo R., and Lynn Maxfield.
                        “Adapting the Voice Range Profile for Singers to Include Duration of Voicing.”
                        <i>Journal of Singing</i> 77, no. 5 (2021): 653–61.
                    </b2></p>

                    <p><b2>
                        Williams, Jenevora.
                        <i>Teaching Singing to Children and Young Adults.</i>
                        3rd ed. Full Voice Music, 2024.
                    </b2></p>
                </div>
            """,
        ],
    }


class BibliographyView(TemplateView):
    template_name = "pages/static_page.html"
    extra_context = {
        "page_title": "Selected Bibliography",
        "content": ["<b>Here is our selected bibliography.</b>"],
    }


class MethodologyView(TemplateView):
    template_name = "pages/static_page.html"
    extra_context = {
        "page_title": "Manual Analysis Methodology",
        "content": ["<b>Here is our methodology.</b>"],
    }


class InstructionsView(TemplateView):
    template_name = "pages/static_page.html"
    extra_context = {
        "page_title": "Instructions & Terminology",
        "content": [
            """
            <div class="content-card">
                <h2>File Requirements</h2>
                <p><b2>
                    All files must end with a .mid or .midi extension.
                </b2></p>
                <p><b2>
                    The file must be a single track without added instruments, voices, or layers.
                </b2></p>
                <p><b2>
                    The file must end with a C<sup>1</sup> note after any rests or pitches.
                </b2></p>
            </div>
            """,
            """
            <div class="content-card">
                <h2>File Preparation</h2>
                <p><b2>
                    For exact results and consistent data, “strip” your music before converting it to a MIDI file.
                    We use <a href="https://www.musehub.com/app/musescore-studio?utm_source=musescore-web&utm_medium=dashboard-page&utm_campaign=dashboard-banner" target="_blank" rel="noopener">MuseScore Studio</a> for all our file preparation.
                </b2></p>
                <p><b2>Remove all lyrics, text, words.</b2></p>
                <p><b2>Remove all articulation, dynamic, expression, performance markings.</b2></p>
                <p><b2>Include rests where there would be accompaniment forces.</b2></p>
                <p><b2>If you use a MIDI keyboard to enter notes, quantize your score and double check rhythms.</b2></p>
                <p><b2><b2>Be sure to include any tempo changes in your score before you export it to a MIDI format. If your score only uses descriptive markings (e.g. allegro) you can use the chart below to convert them to Beats Per Minute (BPM).</b2><p>
                <div class="table-scroll">
                    <table>
                        <thead>
                            <tr>
                                <th><b1>Tempo Marking</th>
                                <th><b1>Approximate BPM</th>
                            </tr>
                        </thead>
                        <tbody>
                            <b2>
                                <tr>
                                    <td><i>Larghissimo</i></td>
                                    <td>24</td>
                                </tr>
                                <tr>
                                    <td><i>Adagissimo and Grave</i></td>
                                    <td>40</td>
                                </tr>
                                <tr>
                                    <td><i>Largo</i></td>
                                    <td>53</td>
                                </tr>
                                <tr>
                                    <td><i>Larghetto</i></td>
                                    <td>55</td>
                                </tr>
                                <tr>
                                    <td><i>Adaigo</i></td>
                                    <td>55</td>
                                </tr>
                                <tr>
                                    <td><i>Adagietto</i></td>
                                    <td>63</td>
                                </tr>
                                <tr>
                                    <td><i>Lento</i></td>
                                    <td>80</td>
                                </tr>
                                <tr>
                                    <td><i>Andante</i></td>
                                    <td>82</td>
                                </tr>
                                <tr>
                                    <td><i>Andantino</i></td>
                                    <td>94</td>
                                </tr>
                                <tr>
                                    <td><i>Marcia Moderato</i></td>
                                    <td>73</td>
                                </tr>
                                <tr>
                                    <td><i>Andante Moderato</i></td>
                                    <td>94</td>
                                </tr>
                                <tr>
                                    <td><i>Moderato</i></td>
                                    <td>114</td>
                                </tr>
                                <tr>
                                    <td><i>Allegretto</i></td>
                                    <td>116</td>
                                </tr>
                                <tr>
                                    <td><i>Allegro Moderato</i></td>
                                    <td>118</td>
                                </tr>
                                <tr>
                                    <td><i>Allegro</i></td>
                                    <td>138</td>
                                </tr>
                                <tr>
                                    <td><i>Molto Allegro>/i> or <i>Allegro vivace</i></td>
                                    <td>140</td>
                                </tr>
                                <tr>
                                    <td><i>Vivace</i></td>
                                    <td>166</td>
                                </tr>
                                <tr>
                                    <td><i>Vivacissimo</i> and <i>Allegrissimo</i></td>
                                    <td>174</td>
                                </tr>
                                <tr>
                                    <td><i>Presto</i></td>
                                    <td>184</td>
                                </tr>
                                <tr>
                                    <td><i>Prestissimo</i></td>
                                    <td>200</td>
                                </tr>
                            </b2>
                        </tbody>
                    </table>
                </div>
            </div>

            <div class="content-card">
                <h2>Submission Instructions</h2>
                <p><b1>Step 1) Fill out the metadata form.</p>
                    <b2><p>&emsp;Include diacritical marks (ex. é, à, ç, ô, ö, ñ, æ, č) in all entries.</p>
                    <p>&emsp;&emsp;Ex: Björn Ulvaeus, instead of Bjorn Ulvaeus.</p>
                    <p>&emsp;&emsp;Ex: Régine Wieniawski, instead of Regine Wieniawski.</p>
                    <p>&emsp;For missing information, select “Unknown.”</p>
                    <p>&emsp;For non-applicable information, select “N/A.”</p>
                    </b2>
                    <p><b1>Step 2) Upload your MIDI file.</b1></p>
                    <p><b2>&emsp;Results become public (after review) by default. Please click the tick box if you do not want them to be public.</b2></p>
                    <p><b1>Step 3) View your results.</b1></p>
                    <p><b1>&emsp;You can view your results right away. After review and approval, results become public (if allowed).</b1></p>
                </b1>
            </div>
            """,
            """
            <div class="content-card">
                <h2>Metadata Definitions</h2>
                <b2>
                <p><b1>Title</b1> – the name of the piece.</b></p>
                <p><b1>Larger Work</b1> – the album, collection, cycle, production, opus, or show that the piece is from.</b></p>
                <p><b1>Musical Composer</b1> – the name of the primary person who created the notes, rhythms.</b></p>
                <p><b1>Text Author</b1> – the name of the primary person who created the lyrics, text, words.</b></p>
                <p><b1>Initial Key Signature</b1> – the musical key, or number of flats or sharps, at the beginning of the music.</b></p>
                <p><b1>Treble Clef Range</b1> – music sung in a generalized treble clef range, often by female voices.</p>
                <p><b3>&emsp;Ex: belter, countertenor, mezzo-soprano, soprano, treble voice.</b3></p>
                <p><b1>Bass Clef Range</b1> – music sung in a generalized bass clef range, often by male voices.</p>
                <p><b3>&emsp;Ex: baritone, bass, bass voice, tenor.</b3></p>
                <p><b1>Western Classical performance style</b1> – music written in a Western classical performance tradition and often sung using acoustic amplification.</p>
                <p><b3>&emsp;Ex: art song, chamber, choral, opera, oratorio.</b3></p>
                <p><b1>Musical Theatre performance style</b1> – music written in an American Musical Theatre tradition and sung using both acoustic and electronic amplification.</p>
                <p><b3>&emsp;Ex: <i>Cats, Chicago, Dear Evan Hansen, Myths &amp; Hymns, Oklahoma </i>.</b3></p>
                <p><b1>Contemporary Commercial performance style</b1> – music written in a Contemporary Commercial tradition and often sung using electronic amplification.</p>
                <p><b3>&emsp;Ex: blues, country, jazz, pop, rock.<sup>9</sup></b3></p>
                </b2>
                <footer>
                    <ol start="9">
                        <li><span class="upright">LoVetri, Jeannette. “Contemporary Commercial Music.” <i>Journal of Voice</i> 22, no. 3 (2008): 260-2.</span></li>
                    </ol>
                </footer>
            </div>
            """,
            """
            <div class="content-card">
                <h2>Metric Definitions</h2>
                <b2>
                <p><b1>%<i>p</i></b1> – The percentage of Total Time where the music has notes written in generalized passaggio zones. Note that generalized passaggio zones do not transpose based on the clef range of the singer.</p>
                <p><b3>&nbsp;&nbsp;&nbsp;&nbsp;Ex: XX.X%p</b3></p>
                <p><b1>Compositional Range</b1> – The lowest and highest fundamental frequency (F<sub>o</sub>) in a vocal line, reported as a range in either vibrations per second, or Hertz (Hz), or using pitch nomenclature.</p>
                <p><b3>&nbsp;&nbsp;&nbsp;&nbsp;Ex: XX.X–XX.X Hz or Xx–Xx</b3></p>
                <p><b1>Cycle Dose (F<sub>p</sub>t<sub>p</sub>)</b1> – The total number of vocal fold oscillations expected from a singer based on a musical score. Reported as a total number of vocal fold vibration cycles, or vibrations.</p>
                <p><b3>&nbsp;&nbsp;&nbsp;&nbsp;Ex: XX.X vibrations</b3></p>
                <p><b1>High, Middle, Low passaggio (H<i>p</i>, M<i>p</i>, L<i>p</i>)</b1> – A generalized range of frequencies where a singer might need to navigate a vocal registration shift. See the chart below for specific ranges. Note that generalized passaggio zones do not transpose based on the clef range of the singer.</b></p>
                <p><b1>High Voice (HV)</b1> – A generalized voice type that can sustainably support a higher vocal tessitura.</p>
                <p><b1>Low Voice (LV)</b1> – A generalized voice type that can sustainably support a lower vocal tessitura.</p>
                <p><b1>Medium Voice (MV)</b1> – A generalized voice type that can sustainably support a middle vocal tessitura.</p>
                <p><b1>Musical tessitura (Q<sub>1p</sub>–Q<sub>3p</sub>)</b1> – The average pitch range of a melodic line in a piece of music based on a notated musical score or capture of a live performance, measured by applying quartile analysis to equally weighted pitch subdivisions. Also known as the interquartile range, reported as a range in either Hz or using pitch nomenclature.</p>
                <p><b3>&nbsp;&nbsp;&nbsp;&nbsp;Ex: XX.X–XX.X Hz or Xx–Xx</b3></p>
                <p><b1>Generalized passaggio Zones</b1> – A generalized range of frequencies where a singer might need to navigate a vocal registration shift. See the chart below for specific ranges. Note that generalized passaggio zones do not transpose based on the clef range of the singer. Reported as %p.</b></p>
                <div class="table-scroll">
                    <table>
                        <thead>
                            <tr>
                                <th></th>
                                <th><b1>High <i>passaggio</i></b1></th>
                                <th><b1>Middle <i>passaggio</i></b1></th>
                                <th><b1>Low <i>passaggio</i></b1></th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><b1>High Voice</b1></td>
                                <td><b2>622.3–784.0 Hz<br>E&#9837;5–G5</b2></td>
                                <td><b2>311.1–392.0 Hz<br>E&#9837;4–G4</b2></td>
                                <td><b2>233.1–293.7 Hz<br>B&#9837;3–D4</b2></td>
                            </tr>
                            <tr>
                                <td><b1>Medium Voice</b1></td>
                                <td><b2>587.3–740.0 Hz<br>D5–F<sup>#</sup>5</b2></td>
                                <td><b2>293.7–370.0 Hz<br>D4–F<sup>#</sup>4</b2></td>
                                <td><b2>220.0–277.2 Hz<br>A3–C<sup>#</sup>4</b2></td>
                            </tr>
                            <tr>
                                <td><b1>Low Voice</b1></td>
                                <td><b2>523.3–659.3 Hz<br>C5–E5</b2></td>
                                <td><b2>261.6–329.6 Hz<br>C4–E4</b2></td>
                                <td><b2>196.0–246.9 Hz<br>G3–B3</b2></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <p><b1>Rest/Recovery Time</b1> – The complete unvocalized time needed to perform a piece. Reported in seconds.</p>
                <p><b3>&nbsp;&nbsp;&nbsp;&nbsp;Ex: XX.X s</b3></p>
                <p><b1>Time Dose</b1> – The complete vocalization time needed to perform a piece. Reported in seconds.</p>
                <p><b3>&nbsp;&nbsp;&nbsp;&nbsp;Ex: XX.X s</b3></p>
                <p><b1>Total Time</b1> – The complete time inclusive of both rest and vocalization needed to perform a piece. Reported in seconds.</p>
                <p><b3>&nbsp;&nbsp;&nbsp;&nbsp;Ex: XX.X s</b3></p>
                <p><b1>Vocal tessitura</b1> – An area of a singer’s voice where the singer has the highest levels of access to timbral colors, articulation clarity, comfort, ease of production and sustain, and dynamic (loudness) control.</b></p>
                </b2>
            </div>
            """,
        ],
    }


class ProjectsView(TemplateView):
    template_name = "pages/static_page.html"
    extra_context = {
        "page_title": "Future Projects",
        "content": [
            """
                <div class="content-card">
                    <p>
                        <b2>
                            We have three primary goals for the first stages of this research and website development. We aim to…
                        <ol>
                            <li>Collect and accumulate data to expand the database through user contributions and research partners,</li>
                            <li>Assess the presentational usefulness of the data to practitioners and researchers, and,</li>
                            <li>Establish a choral ensemble database.</li>
                        </ol>
                        </b2>
                    </p>
                    <h2>Data Sharing</h2>
                    <b>
                        We believe that open data sharing promotes transparency and accessibility in research and scholarship. Because of this belief, we are happy to share information and data whenever we can. We designed this website with practitioners in mind to quickly find information about musical selections. If you are interested in taking a deeper dive into the aggregate information we collect from the MIDI files in our database, please contact us.
                    </b>
                </div>
            """,
        ],
    }


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]

            email_msg = EmailMessage(
                subject=f"Contact form: {subject}",
                body=f"From: {name} ({email})\n\n{message}",
                from_email="contact@tessituragram.com",
                to=["contact@tessituragram.com"],
                reply_to=[email],
            )
            email_msg.send()
            return redirect("contact_success")
    else:
        form = ContactForm()

    return render(request, "pages/contact.html", {"form": form})


def contact_success(request):
    return render(request, "pages/contact_success.html")