# Research Blog
---
## 2026-05-26 to 2026-05-29

**What I worked on:**

Onboarding tasks, safety trainings, etc. 

Setting up GCE and ALCF accounts, setting up remote SSH

Understanding project, reviewing relevant ViT papers (dario's paper, a picture is worth 16x16 words, etc.)

**What helped:**

Good talks with Bhupendra and reviewing Dario's paper

**What was challenging:**

Everything about Vision Transformers is challenging to understand.

**What I learned:**

The general gist of what a ViT is, and what my next steps are for the project

### Next steps

- Run Dario's code run in GCE with some dummy images
- Make Dario's code work for a small sample of dummy radar data in GCE

---


## 2026-06-01 to 2026-06-25

**What I worked on:**

Final onboarding tasks

Running cloud dino on GCE and polaris

Beginning to convert cloud dino to work with radar data

**What helped:**

Dario's github repo and ALCF/GCE tutorial pages

**What was challenging:**

deprecated function calls due to a lack of repo maintenance

**What I learned:**

How to submit jobs to a supercomputer

### Next steps

- Make the code work with radar data
- Run the code with a small batch of radar data
  
---

## 2026-06-08 to 2026-06-12

**What I worked on:**

Finished converting cloud dino to work with radar data

brainstorming config ideas for variables, heights, and augmentations

downloading and processing a year of radar data

**What helped:**

Bhupendra's SSL perspective paper, and the NASA masked autoencoder paper

**What was challenging:**

Long download times, radar clutter, slow and questionably accurate KDP algorithms, and regridding.

**What I learned:**

The ViT works with a small sample of radar data

### Next steps

- Continue downloading a large amount of data
- run this on polaris with various configs
- analyze formance and computational expense
---
