# Active User Input

These 2 are the only input files you'll need to configure before launching to MARS:
* [YML configuration file](#yml-configuration-file)
* [cover.tex file](#covertex-file)

## YML configuration file

This section serves as a guide for the dynamic [yml config file](working-groups-config.yml) located in this directory. It defines the repository structure for various Working Groups that are to be included in the metrics release report. The working groups would be cloned and parsed for relative links according to the structure defined here.

### File Structure

This file follows a simple yet strict structure, make sure you follow it to avoid unnecessary errors.

* The following is a template for the same, with explanation:

```yml
# WG-Name

wg-name:
  include-wg: boolean
  wg-fullname: WG-name
  github-link: git-link
  github-branch: git-branch
  focus-areas:
    focus-area1:
    - metric1-name.md
    - metric2-name.md
    focus-area2:
    - metric1-name.md
    - metric2-name.md
```

**Explanation:**
* `wg-name`: WG name that is same as the repository name for the WG
* `include-wg`: boolean flag that defines if the WG should be included in the report (mainly for debugging purposes)
* `wg-fullname`: complete name of WG that you want in the report headings
* `github-link`: github link for the WG repo (for cloning)
* `github-branch`: git branch for the WG repo (for cloning)
* `focus-area1`: focus-area name should be same as the focus-area dir name in the WG
* `metric1-name.md`: the name of metric markdown file as in the repo (should include .md extension as well)

Note: Empty focus-areas (focus-areas with no metrics) will work as well.

* A sample structure for [wg-common](https://github.com/chaoss/wg-common) would look like this:

```yml
# WG-Common

wg-common:
  include-wg: True
  wg-fullname: Common Metrics WG
  github-link: https://github.com/chaoss/wg-common
  github-branch: master
  focus-areas:
    contributions:
    - technical-fork.md
    - types-of-contributions.md
    time:
    - activity-dates-and-times.md
    - burstiness.md
    - review-cycle-duration-within-a-change-request.md
    - time-to-close.md
    - time-to-first-response.md
    place:
    people:
    - contributor-location.md
    - contributors.md
    - organizational-diversity.md
```

Apart from this you might also find `front-matter` and `end-matter` in the beginning of the file. It corresponds to the static input of contributors, release-notes and the LICENSE - to be pulled from the website repository. You might not need to change it since any modification in these files in the website repo would be anyways reflected here. So you can safetly ignore those terms.

### Usage

Now that you are familiar with the structure of the file, it is important to note that this file also determines in which order the working groups, focus-areas and metrics would be displayed in the release report. The order is from top to bottom, and is applicable for WG, focus-areas and their respective metrics. (this doesn't apply to front and end matter since they have fixed position at the beginning and the end of the PDF respectively)

This file is expected to be altered during each metrics release process.

A series of steps to be performed during the release process:
* Update this file - perform the following operations, if applicable:
    * Add new metrics to their respective focus-areas (mind the order)
    * Remove outdated/retired metrics
    * Reorder the WG, focus-areas or metrics as per convenience
* Save changes to the new finalized file
* Refer to main [README](../README.md), to continue with the release process

## `cover.tex` file

This tex file acts as the standard cover page for the PDF release. Here, you need to set 2 parameters in this file:
1. Release year and month - at line 13
2. Copyright year - at line 24
