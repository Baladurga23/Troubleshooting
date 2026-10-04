"""
Knowledge Base + Inference Engine
Computer Troubleshooting Expert System (Rule-Based AI)

Design:
  Level 1 - COMBO rules   : two or more symptoms selected together match a
                            more specific, more confident diagnosis
  Level 2 - SINGLE rules  : one symptom alone still gives a useful diagnosis
  Level 3 - DEFAULT       : nothing matched -> generic advice

Multiple symptoms can be selected at once (checkboxes), which makes this a
richer inference problem than a plain single-input lookup.
"""

SYMPTOMS = [
    "Slow Performance",
    "No Display / Black Screen",
    "No Power / Won't Turn On",
    "Overheating",
    "No Internet / No Network",
    "Strange Noise (fan/beep)",
    "Blue Screen (BSOD)",
    "Virus / Malware Suspected",
    "No Sound",
    "Keyboard or Mouse Not Working",
    "Frequent Restarts / Crashes",
    "Low Disk Space Warning",
]

# ---------- Level 1: Combo rules (frozenset of symptoms -> diagnosis) ----------
# Order doesn't matter inside a combo; frozenset makes lookup order-independent.
COMBO_RULES = {
    frozenset({"Overheating", "Strange Noise (fan/beep)"}):
        ("Cooling fan failure or dust-blocked vents",
         "Shut down, clean the air vents and fan with compressed air, "
         "and check if the fan spins freely. Replace fan if it still "
         "makes noise or the system still overheats."),

    frozenset({"Slow Performance", "Low Disk Space Warning"}):
        ("Disk is nearly full, slowing the whole system",
         "Delete temporary files, uninstall unused apps, empty Recycle Bin, "
         "and keep at least 15% of disk space free."),

    frozenset({"Slow Performance", "Virus / Malware Suspected"}):
        ("Malware actively running in the background",
         "Run a full antivirus/anti-malware scan immediately, disconnect "
         "from the internet during the scan, and update your antivirus "
         "definitions first."),

    frozenset({"No Display / Black Screen", "No Power / Won't Turn On"}):
        ("Power supply or motherboard failure",
         "Check the power cable and wall socket, remove and reseat the "
         "RAM, and if it still won't turn on get it checked by a "
         "hardware technician."),

    frozenset({"Frequent Restarts / Crashes", "Overheating"}):
        ("System is overheating and auto-restarting to protect hardware",
         "Clean the cooling system, check thermal paste on the CPU if "
         "it's an older machine, and avoid blocking the laptop's vents."),

    frozenset({"Blue Screen (BSOD)", "Frequent Restarts / Crashes"}):
        ("Driver conflict or corrupted system file",
         "Boot into Safe Mode, update or roll back recent drivers, and "
         "run 'sfc /scannow' to repair corrupted system files."),
}

# ---------- Level 2: Single-symptom rules ----------
SINGLE_RULES = {
    "Slow Performance":
        ("Too many background programs or startup apps",
         "Open Task Manager, close unused programs, and disable "
         "unnecessary startup apps."),

    "No Display / Black Screen":
        ("Loose cable or graphics driver issue",
         "Check the monitor cable connection, try a different port, "
         "and update or reinstall the graphics driver."),

    "No Power / Won't Turn On":
        ("Power supply or battery issue",
         "Check the power cable/adapter, try a different socket, and "
         "for laptops try removing and reinserting the battery."),

    "Overheating":
        ("Dust buildup or blocked ventilation",
         "Clean the vents and fan, use the device on a hard flat "
         "surface, and avoid using it on a bed or blanket."),

    "No Internet / No Network":
        ("Router, driver, or network configuration issue",
         "Restart the router, check Wi-Fi/Ethernet connection, and "
         "run Windows Network Troubleshooter."),

    "Strange Noise (fan/beep)":
        ("Worn-out fan, loose component, or hardware beep code",
         "Open the case (if comfortable) and check for loose parts or "
         "a failing fan; note the beep pattern and look it up for the "
         "exact hardware fault."),

    "Blue Screen (BSOD)":
        ("Driver conflict or hardware/software error",
         "Note the error code shown, boot into Safe Mode, and update "
         "or roll back the most recently installed driver."),

    "Virus / Malware Suspected":
        ("Possible malware infection",
         "Run a full antivirus scan, avoid clicking unknown links, and "
         "update your operating system and antivirus software."),

    "No Sound":
        ("Audio driver issue or wrong output device selected",
         "Check volume mixer settings, select the correct playback "
         "device, and update the audio driver."),

    "Keyboard or Mouse Not Working":
        ("Loose connection or outdated driver",
         "Reconnect the USB/wireless receiver, try a different port, "
         "and update the input device driver."),

    "Frequent Restarts / Crashes":
        ("Overheating, faulty RAM, or corrupted system files",
         "Run a memory diagnostic tool, check temperatures, and run "
         "'sfc /scannow' to repair system files."),

    "Low Disk Space Warning":
        ("Disk nearly full",
         "Delete temporary files, uninstall unused programs, and move "
         "large files to external storage or cloud."),
}

DEFAULT_RESULT = (
    "No matching symptom selected",
    "Please select at least one symptom to get a diagnosis.",
)


def diagnose(selected_symptoms):
    """
    Inference engine.
    selected_symptoms: list of symptom strings chosen by the user.
    Returns a dict with cause, solution, and which rule level fired.
    """
    if not selected_symptoms:
        cause, solution = DEFAULT_RESULT
        return {"cause": cause, "solution": solution, "rule_level": "Default Rule"}

    symptom_set = frozenset(selected_symptoms)

    # Level 1 - try combo rules: check if any rule's symptom set is a
    # subset of what the user selected (so extra unrelated picks don't block it)
    for combo, (cause, solution) in COMBO_RULES.items():
        if combo.issubset(symptom_set):
            return {
                "cause": cause,
                "solution": solution,
                "rule_level": "Combo Rule",
                "matched_on": " + ".join(sorted(combo)),
            }

    # Level 2 - single-symptom rule for the first matched symptom
    for symptom in selected_symptoms:
        if symptom in SINGLE_RULES:
            cause, solution = SINGLE_RULES[symptom]
            return {
                "cause": cause,
                "solution": solution,
                "rule_level": "Single-Symptom Rule",
                "matched_on": symptom,
            }

    # Level 3 - default
    cause, solution = DEFAULT_RESULT
    return {"cause": cause, "solution": solution, "rule_level": "Default Rule"}