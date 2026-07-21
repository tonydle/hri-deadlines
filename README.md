# XR, HRI & Robotics Deadlines

Countdowns to major extended reality (VR/AR/MR), human–robot interaction and robotics conference deadlines.

This is a specialised fork of [HCI Deadlines](https://github.com/hci-deadlines/hci-deadlines.github.io), which is itself based on [AI Deadlines](https://github.com/paperswithcode/ai-deadlines). The existing Jekyll countdowns, local-time conversion, detail pages, filters, past-deadline view and calendar exports are retained, with a focused conference taxonomy and curated data set.

## Conference data

Conference records are maintained directly in [`_data/conferences.yml`](_data/conferences.yml). This fork uses a single-repository workflow and does not copy data from the separate HCI Deadlines `conf-database` repository.

Only official conference or call-for-papers pages should be used as sources. Do not estimate unannounced deadlines or submission time zones. Use `TBA` when no deadline is announced, or a quoted `YYYY-MM-DD` value when the date is official but its cutoff time is not; date-only deadlines are shown without a countdown or calendar export.

The list also includes a small, explicit set of broad crossover venues with strong XR or HRI participation: CHI, SIGGRAPH, SIGGRAPH Asia, UIST, TEI and OzCHI. Their records are labelled as crossovers rather than treating broad HCI or graphics conferences as automatically in scope.

Before opening a pull request, run:

```sh
python3 scripts/validate_conferences.py
bundle exec jekyll build --future
```

## Contributing

Contributions are welcome through pull requests to [`tonydle/hri-deadlines`](https://github.com/tonydle/hri-deadlines). Add or edit records in `_data/conferences.yml` and keep category values limited to `XR`, `HRI` and `ROB`.

## License and attribution

This project remains licensed under the [MIT License](LICENSE).

It uses [IcoMoon Icons](https://icomoon.io/#icons-icomoon) under [GPL](https://www.gnu.org/licenses/gpl-3.0.html) / [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
