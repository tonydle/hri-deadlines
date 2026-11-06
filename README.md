# Human-Centred Computing & Robotics Deadlines

Countdowns to major extended reality (VR/AR/MR), computer graphics, human–computer interaction, human–robot interaction and robotics conference deadlines.

This is a specialised fork of [HCI Deadlines](https://github.com/hci-deadlines/hci-deadlines.github.io), which is itself based on [AI Deadlines](https://github.com/paperswithcode/ai-deadlines). The existing Jekyll countdowns, local-time conversion, detail pages, filters, past-deadline view and calendar exports are retained, with a focused conference taxonomy and curated data set.

## Conference data

Conference records are maintained directly in [`_data/conferences.yml`](_data/conferences.yml). This fork uses a single-repository workflow and does not copy data from the separate HCI Deadlines `conf-database` repository.

Only official conference or call-for-papers pages should be used as sources. Do not estimate unannounced deadlines or submission time zones. Use `TBA` when no deadline is announced, or a quoted `YYYY-MM-DD` value when the date is official but its cutoff time is not; date-only deadlines are shown without a countdown or calendar export. When event dates are unannounced, use `TBA` for `date`, `start` and `end`; these records appear in the list but have no event on the calendar.

Human–computer interaction has its own `HCI` area, including CHI, UIST, TEI, OzCHI, IUI, DIS and CSCW. Conferences can appear in multiple areas. The combined “XR and Computer Graphics” area uses `XR` and includes I3D, Eurographics, SIGGRAPH and SIGGRAPH Asia. CSCW accepts rolling PACMHCI submissions; its record uses `TBA` with an explanatory note because there is no fixed deadline.

Before opening a pull request, run:

```sh
python3 scripts/validate_conferences.py
bundle exec jekyll build --future
```

## Contributing

Contributions are welcome through pull requests to [`tonydle/hri-deadlines`](https://github.com/tonydle/hri-deadlines). Add or edit records in `_data/conferences.yml` and keep category values limited to `XR`, `HCI`, `HRI` and `ROB`.

## License and attribution

This project remains licensed under the [MIT License](LICENSE).

It uses [IcoMoon Icons](https://icomoon.io/#icons-icomoon) under [GPL](https://www.gnu.org/licenses/gpl-3.0.html) / [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
