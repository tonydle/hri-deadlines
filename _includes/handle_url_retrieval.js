// Get subjects from URL/Cache
var url = new URL(window.location);
subs = url.searchParams.get("sub");
if (subs == undefined) {
  subs = store.get("{{site.domain}}-subs");
} else {
  subs = subs.toUpperCase().split(",");
}

// Preserve saved selections and links from the former graphics-only filter.
if (Array.isArray(subs)) {
  subs = Array.from(new Set(subs.map(function (sub) {
    return sub === "CG" ? "XR" : sub;
  })));
}

// Apply selections
if (subs == undefined) {
  subs = all_subs;
}
$("#subject-select").multiselect("select", subs);
update_filtering({ subs: subs, all_subs: all_subs });
