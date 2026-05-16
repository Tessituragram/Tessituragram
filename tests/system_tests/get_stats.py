import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.midi_reader import MidiParser
from src.tessitura import get_tessitura_and_passaggio
from collections import defaultdict
import csv
import pandas

"""get_stats.py: System test file for reading a spreadsheet of manually-performed tessiturogram
analyses and comparing to the output provided by Tessitura."""

__author__      = "Troy Conklin"

filelist = []

def percent_error(obs, acc):
    return round((abs(acc - obs) / (acc + 0.0000001))*100, 2)
CSV_FILE = "results.csv"

def csv_results(results, filename, writer):

        # File label
        writer.writerow(["=== RESULTS FOR FILE: " + filename + "==="])
        
        # Header
        writer.writerow(["Metric", "Expected", "Observed", "Difference", "Percent Error"])

        # Write each metric
        for metric, vals in results.items():
            expected  = vals["expected"]
            observed  = vals["observed"]
            diff      = abs(vals["expected"] - vals["observed"])
            pct_error = vals["percent_error"]

            writer.writerow([
                metric,
                f"{expected:.3f}" if expected is not None else "N/A",
                f"{observed:.3f}" if observed is not None else "N/A",
                f"{diff:.3f}" if diff is not None else "N/A",
                f"{pct_error:.2f}%" if pct_error is not None else "N/A"
            ])

        writer.writerow([""])


def csv_average_errors(all_errors, writer):
    file_exists = os.path.isfile(CSV_FILE)

    # Add blank line if file already has content
    if file_exists:
        writer.writerow([])

    # Label row
    writer.writerow(["AVERAGE PERCENT ERROR ACROSS ALL FILES"])

    # Header
    writer.writerow(["Metric", "Expected", "Observed", "Difference", "Percent Error"])

    # Only “Percent Error” column is filled; others marked N/A
    for metric, errors in all_errors.items():
        if errors:
            avg_error = sum(errors) / len(errors)
            percent_error_str = f"{avg_error:.2f}%"
        else:
            percent_error_str = "N/A"

        writer.writerow([
            metric,
            "N/A",
            "N/A",
            "N/A",
            percent_error_str
        ])

def main():
    all_errors = defaultdict(list)

    excel_path = "tests\\system_tests\\Master Data Calculation.xlsx"
    excel_tab_path = "tests\\system_tests\\Tab Reference.xlsx"

    # Load workbooks
    excel_sheets = pandas.read_excel(excel_path, sheet_name=None)
    excel_tab_sheet = pandas.read_excel(excel_tab_path, sheet_name=None)
    excel_tab_nav = excel_tab_sheet["Tab Master"]

    # Extract reference columns
    arias = excel_tab_nav['ARIA NAME'].tolist()
    midi_filenames = excel_tab_nav['COMBINED ARABIC AND ROMAN AND .MID'].tolist()
    tabs = excel_tab_nav['ROMAN NUMERAL'].tolist()

    print(f"Processing {len(arias)} arias...")

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        for _, filename, tab in zip(arias, midi_filenames, tabs):
            print(f"\n--- Processing {filename} (tab {tab}) ---")
            results = {}
            # MIDI filepath
            filepath = os.path.join(
                "data\\test_data_arias",
                filename
            )
            # Parse MIDI
            try:
                parser = MidiParser(filepath)
                parser.parse_midi()
                notes = parser.get_notes()
                tess, passaggio, clefs = get_tessitura_and_passaggio(notes, "None")
            except Exception as e:
                print(f"Failed to parse {filename}: {e}")
                continue
            # Helper to record results and accumulate all_errors
            def add_result(metric, observed, expected):
                err = percent_error(observed, expected)
                results[metric] = {
                    "expected": round(expected, 2),
                    "observed": round(observed, 2),
                    "percent_error": err,
                }
                all_errors[metric].append(err)
            # Make sure the spreadsheet is formatted correctly
            if str(tab) not in excel_sheets:
                print(f"Warning: Tab '{tab}' not found in workbook.")
                continue
            measurement_df = pandas.read_excel(
                excel_path,
                sheet_name=str(tab),
                usecols="K",
                header=None,
                skiprows=1
            )
            measurement_values = measurement_df.iloc[:, 0].tolist()
            try:
                # Tessitura values
                add_result("cycle_dose", tess[0].cycle_dose, float(measurement_values[0]))  
                add_result("total_time", tess[0].total_time, float(measurement_values[1]))  
                add_result("rest_time", tess[0].rest_time, float(measurement_values[3]))    
                add_result("first_quartile", tess[0].lowFreq, float(measurement_values[5]))
                add_result("median", tess[0].median, float(measurement_values[6]))        
                add_result("third_quartile", tess[0].highFreq, float(measurement_values[7]))
                # Passaggio values
                p = passaggio[0]
                add_result("lvhp_time", p.lvhp.time_dose, float(measurement_values[12])) 
                add_result("lvhp_percent", p.lvhp.percentage, float(measurement_values[13]))
                add_result("lvmp_time", p.lvmp.time_dose, float(measurement_values[14]))
                add_result("lvmp_percent", p.lvmp.percentage, float(measurement_values[15]))
                add_result("lvlp_time", p.lvlp.time_dose, float(measurement_values[16]))
                add_result("lvlp_percent", p.lvlp.percentage, float(measurement_values[17]))
                add_result("mvhp_time", p.mvhp.time_dose, float(measurement_values[20]))
                add_result("mvhp_percent", p.mvhp.percentage, float(measurement_values[21]))
                add_result("mvmp_time", p.mvmp.time_dose, float(measurement_values[22]))
                add_result("mvmp_percent", p.mvmp.percentage, float(measurement_values[23]))
                add_result("mvlp_time", p.mvlp.time_dose, float(measurement_values[24]))
                add_result("mvlp_percent", p.mvlp.percentage, float(measurement_values[25]))
                add_result("hvhp_time", p.hvhp.time_dose, float(measurement_values[28]))
                add_result("hvhp_percent", p.hvhp.percentage, float(measurement_values[29]))
                add_result("hvmp_time", p.hvmp.time_dose, float(measurement_values[30]))
                add_result("hvmp_percent", p.hvmp.percentage, float(measurement_values[31]))
                add_result("hvlp_time", p.hvlp.time_dose, float(measurement_values[32]))
                add_result("hvlp_percent", p.hvlp.percentage, float(measurement_values[33]))
            except IndexError as e:
                print(f"Measurement index out of range for tab {tab}: {e}")
                continue
            except ValueError as e:
                print(f"Invalid number in measurement values for tab {tab}: {e}")
                continue
            # Write this file’s results to the CSV
            csv_results(results, filename, writer)
        # Write averages to the CSV
        csv_average_errors(all_errors, writer)

if __name__ == "__main__":
    main()