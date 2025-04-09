import re

res = """
Here is the top 10 list of potential matches for your patent claim #US9687142B1, formatted as requested:  

1. **Medtronic StealthStation S8 Surgical Navigation System** - [https://www.medtronic.com](https://www.medtronic.com)  
   * 1.1. Yes (tubular sheath with inclined surfaces)  
   * 1.2. Yes (insertion into patient)  
   * 1.3. Yes (endoscope integration)  
   * 1.4. Yes (displayed signal)  
   * 1.5. Yes (docking guidance)  

2. **Stryker 1688 Advanced Imaging Modality System** - [https://www.stryker.com](https://www.stryker.com)  
   * 1.1. Yes (angled docking land)  
   * 1.2. Yes (insertion mechanism)  
   * 1.3. Yes (endoscope compatibility)  
   * 1.4. Yes (real-time display)  
   * 1.5. Unsure (specific maneuvering method unclear)  

3. **Boston Scientific SpyGlass DS Direct Visualization System** - [https://www.bostonscientific.com](https://www.bostonscientific.com)  
   * 1.1. Yes (inclined distal end)  
   * 1.2. Yes (patient insertion)  
   * 1.3. Yes (integrated camera)  
   * 1.4. Yes (video display)  
   * 1.5. No (lacks anatomical docking guidance)  

4. **Karl Storz Endoscopy System (IMAGE1 S)** - [https://www.karlstorz.com](https://www.karlstorz.com)  
   * 1.1. Yes (sheath with angled surfaces)  
   * 1.2. Yes (surgical insertion)  
   * 1.3. Yes (endoscope alignment)  
   * 1.4. Yes (HD visualization)  
   * 1.5. Unsure (docking method not explicit)  

5. **Olympus VISERA ELITE II Surgical Visualization** - [https://www.olympus-global.com](https://www.olympus-global.com)  
   * 1.1. Yes (tapered sheath design)  
   * 1.2. Yes (minimally invasive insertion)  
   * 1.3. Yes (camera positioning)  
   * 1.4. Yes (on-screen imaging)  
   * 1.5. No (focus on imaging, not docking)  

6. **Intuitive Surgical Da Vinci SP Endoscope** - [https://www.intuitive.com](https://www.intuitive.com)  
   * 1.1. Yes (angled distal geometry)  
   * 1.2. Yes (robotic insertion)  
   * 1.3. Yes (integrated scope)  
   * 1.4. Yes (3D display)  
   * 1.5. Yes (automated tissue contact)  

7. **Richard Wolf EndoCamLogic HD System** - [https://www.richard-wolf.com](https://www.richard-wolf.com)  
   * 1.1. Unsure (sheath angle not documented)  
   * 1.2. Yes (endoscopic insertion)  
   * 1.3. Yes (camera proximity)  
   * 1.4. Yes (live feed)  
   * 1.5. No (no described docking)  

8. **CONMED Hall Surgical EndoSheath** - [https://www.conmed.com](https://www.conmed.com)  
   * 1.1. Yes (45–75° inclined surfaces)  
   * 1.2. Yes (laparoscopic use)  
   * 1.3. Yes (scope integration)  
   * 1.4. No (third-party display required)  
   * 1.5. Unsure (docking not emphasized)  

9. **Fujifilm Synapse 3D Endoscopy Suite** - [https://www.fujifilm.com](https://www.fujifilm.com)  
   * 1.1. No (standard sheath)  
   * 1.2. Yes (patient insertion)  
   * 1.3. Yes (camera alignment)  
   * 1.4. Yes (3D visualization)  
   * 1.5. No (navigation not highlighted)  

10. **Cook Medical EchoTip Ultra Endoscopic Ultrasound** - [https://www.cookmedical.com](https://www.cookmedical.com)  
    * 1.1. No (ultrasound-focused design)  
    * 1.2. Yes (internal placement)  
    * 1.3. Unsure (scope compatibility varies)  
    * 1.4. Yes (image display)  
    * 1.5. No (no stabilization mechanism)  

Let me know if you'd like deeper analysis on any entry.
"""
# PREFIX_SUFFIX_REGEX = re.compile(r'\d+\.\d+\.')
# NUMBER_REGEX


component_list = [1,2,3,4,5]
for entry in res.split("\n\n"):
    lines = entry.split("\n")
    if len(lines) < len(component_list): # should be at least the length + 1 so this is forgiving
        continue

    name = get_name(lines[0])
    print("NAME:", name)
    link = get_link(entry)
    print("LINK:", link)
    for line in lines[1:]:
        # print(clean(outside(line)), "|", line)
        # answer = clean(remove_numbering(outside(line))), "|", line)
        # print(clean(remove_numbering(outside(line))), "|", line)
        print("\tCLASS:", get_classification(line))

        # print(line, get_links(line))

        # name, desc, link = entry.split("\n")
    print()
print(get_links(res))
