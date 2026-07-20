# Research Blog

Add a new entry each week (or more often if you like). Be honest — write what actually happened, not just what went well. This log will help you write your final report.

---

## Week 1 (May 26-29)

**Successes**

- Made it through orientation!
  - Created accounts through various different Argonne services.
  - Finished safety trainings.
  - Was health screened, 0 issues arose.
  - Began to familiarise myself with the building and campus.
- Found a case to test Adapt and LMA capabilities.
  - May 2nd, 2025 1700Z-2100Z in northern Alabama using KHTX.
  - NALMA has 4302651 events and 85812 flashes (total, not for the cell of interest).
  - Adapt tracks *the same cell* from initiation to merge.
- Bhupendra's unsupervised learning talk.
  - Didn't understand everything, but some ideas about sorting algorithms started to form.

**Shortcomings**

- Adapt
  - Does not run on windows personal laptop.
  - Works on linux shell through Ubuntu, but still had errors arise.
    - County lines not plotting due to issue with proj.
    - Storm cell information shows \u2014 when not hovering over a cell.
    - Only 5 most recent scans appear in list for selection.
- LMA
  - Refamiliarising myself with the process took longer than I expected.
  - Data storage is going to be difficult...
    - 4 hours of data comes out to be 418 MB
- Still learning how to fully work with linux.
- Have not tried to write/run data with CELS servers.

**Future Plans**
- Perform a mini-case study for identified date.
  - Compare lightning data from LMA to radar statistics from Adapt
  - Compare GLM to LMA over the cell's lifespan
    - Expect GLM to see the larger/taller flashes.
    - Expect LMA to identify more parts of a flash as the cell aproaches the center of the network.
- Begin to write LMA script for mass flash sorting.
- Add all LMA data to a server.
- Get statistics for radar cells within ~150km of radar and ~75km of LMA center.
- Poster
- Presentation
- Final Report
- Manuscrpit (?)

---

## Week 2 (June 1-5)

**Successes**
- Case Study
  - Finished LMA and radar analysis using pyxlma and Adapt.
  - Compiled most interesting figures into a powerpoint.
    - View of LMA and Radar at peak reflectivity and ZDR as well as min ZDR.
    - A couple of plots when there were flashes extending outside of the cell.
    - Plots prior to and after merger of cells.
- Full Study
  - Beginning to download data from NASA's earthdata repository.
    - Only 1st year at this moment to test space on server, eventually will download all 7 years.
- Adapt Improvements
  - Background map now visible.
  - Can now view more than 5 radar scans!

**Shortcomings**
- Case Study
  - Was not able to make use of GLM for comparison with LMA.
    - Prior notebooks used are out of date and I wanted to begin working on the full study.
  - Could be imporved by more detailed lightning statistics per cell with future versions of Adapt.
- Getting used to all the linux commands again is taking time. 

**Future Plans**
- Download and process the LMA data on one of the fancy servers.
- Download the radar data.
- Process everything together to get final statistics.
- Poster
- Presentation
- Final Report
- Manuscrpit (?)

---

## Week 3 (June 8-12)

**Successes**
- Downloaded and processed all the LMA data within the gce server.
- Downloaded the radar data to the gce server.
- Attended weekly student and DOE seminars along with an extra EVS seminar.
- Adapt now has lightning processing included!

**Shortcomings**
- Stuggling to get the lightning processing to work on my end.
  - Cells not correctly linked to tracks and lightning not associating with individual cells.

**Future Plans**
- Process everything together to get final statistics.
- Poster
- Presentation
- Final Report
- Manuscrpit (?)

---

## Week 4 (June 15-19)

**Successes**
- Lightning processing is now fixed.
  - Adapt dashboard can show lightning characteristics for each cell.
  - Adapt output includes numerous lightning characteristics per cell in a series of tables.
- Developed database viewer.
  - Includes filtering for different cell and lightning characteristics.
  - Can select a single cell to observe.
  - Quick statistics on how many lightning flashes, longest cell track, highest reflectivity, etc.
  - *Still in development*

**Shortcomings**
- Threat of flooding on Wednesday lead to work from home.
  - Attended student and DOE seminars online :(
  - Was not able to supervise adapt processing.
- Got sick Wednesday night leading to a down day Thursday.
  - Got a little bit done from bed but mostly took the day off.
- Adapt run still not complete.
  - Performed some optimisations to what is output, but still taking 10-20 seconds per radar scan.

**Future Plans**
- Finish adding features to database viewer.
- Clean up, optimise, and anotate the code for better understanding of why everything functions.
- Process everything together to get final statistics.
- Poster
- Presentation
- Final Report
- Manuscrpit (?)

---

## Week 5-7 (June 22-26 - July 6-10)

- All of the time during these weeks was spent trying to debug and run Adapt over the multi-year period. Next entry will catalog what happened with that run.

---

## Week 8 (July 13-17)

