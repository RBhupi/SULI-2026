# Summer Student Repository

This repository is used to document research progress, share code and figures, and store final deliverables during the internship.

Each student has a folder under:

```text
students/firstname_lastname/
```

Work only inside your own folder.

---

## For Students

### Getting Started

If you are new to Git and GitHub, these are good starting points:
- [GitHub Hello World guide](https://guides.github.com/activities/hello-world/)
- [Git crash course (YouTube, 30 min)](https://www.youtube.com/watch?v=SWYqp7iY_Tc)

Clone the repository:

```bash
git clone <repo-url>
cd <repo>
```

Create a branch for your work:

```bash
git checkout -b alice/work
```

You may reuse the same branch for all work or create new branches whenever useful.

> **Note:** Do not clone this repository inside a folder synced with iCloud, Google Drive, or any other file sync service — synced folders can corrupt or delete Git files.

---

### Your Folder

Inside your folder you can add anything:

- blog entries
- notes
- figures and pictures
- scripts and notebooks
- presentations, reports, posters, papers

Use whatever file formats make sense. **Large datasets should not be committed to GitHub** — ask your mentor where to put them.

---

### Updating Your Work

```bash
git add students/alice_smith/
git commit -m "update blog and figures"
git push
```

Then open a Pull Request on GitHub. You may open PRs frequently, occasionally, or whenever you want feedback — there is no required schedule. Ask your mentor whether they will merge PRs themselves, or whether you or a fellow intern should do it.
---

### Blog Entries

Update `blog.md` regularly with what you worked on, problems encountered, results, and next steps. Short entries are completely fine.

---

### Deliverables

Upload final deliverables to:

```text
students/alice_smith/deliverables/
```

Any format is fine — pdf, pptx, tex, docx, md, zip. Use clear filenames.

**SULI students** — three required deliverables:
1. Poster (PPT/PDF)
2. Research Report Paper (DOCX/PDF) (This is technical documentation)
3. Blog-style science article on your work in markdown with no more than 5 figures or pictures. This is documenting your experiences as well as work for non-technical audiences.

For the blog article, use these as a guide:
- Who am I and what am I doing?
- Why is this work important?
- What instruments, sensors, or data am I using?
- What is the approach / methodology?
- What is next?
- Brief conclusion and references

---

### Documents and Spreadsheets

For shared documents, spreadsheets, or large files that don't belong in GitHub, create a folder named after your last name in **Google Drive or Box** and share it with your mentor.

---

### Communication

Use **Slack** for questions, updates, and meeting coordination.

Use **GitHub Pull Requests** for code review, figure feedback, and keeping a record of your progress.

---

## For Mentors

### Setup

1. Create a new repository from this template
2. Add student names to `config/students.yml`:

```yaml
students:
  - alice_smith
  - bob_jones
```

3. Commit and push — student folders will be created automatically
4. Add students as repository collaborators (Settings → Collaborators)

### Mentoring

Students work in their own folders and open Pull Requests whenever they want feedback or want to merge work. Review blog updates, figures, scripts, and reports through PR comments.

The repository is intentionally lightweight — a shared research notebook and archive, not a project management system.
