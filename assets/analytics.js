(function () {
  'use strict';
  const measurementId = 'G-GGTHGX9V8E';
  // Only published Wiki traffic belongs in the production property.
  if (location.hostname !== 'wiki.topcraft.cc' || location.protocol !== 'https:') return;
  const paths = new Set(window.TopCraftSearchPaths || []);
  let active = '', previous = '', searchTimer;
  const searches = new Set();
  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
  window.gtag('js', new Date());
  window.gtag('config', measurementId, {
    send_page_view: false,
    allow_google_signals: false,
    allow_ad_personalization_signals: false
  });
  const script = document.createElement('script');
  script.async = true;
  script.src = 'https://www.googletagmanager.com/gtag/js?id=' + measurementId;
  document.head.append(script);

  function cleanReferrer(value) {
    try { const url = new URL(value); return url.origin + url.pathname; } catch (_) { return ''; }
  }
  function mount(path) {
    path = String(path || '/').split(/[?#]/)[0].replace(/\.md$/, '').replace(/\/$/, '') || '/';
    if (!paths.has(path)) { active = ''; clearTimeout(searchTimer); return; }
    if (path === active) return;
    clearTimeout(searchTimer);
    searches.clear();
    active = path;
    const page = {
      page_title: document.title,
      page_location: location.origin + location.pathname + '#' + path,
      page_referrer: previous || cleanReferrer(document.referrer),
      wiki_path: path
    };
    // Keep subsequent events attached to the current article, without its TOC/query parameters.
    window.gtag('set', page);
    window.gtag('event', 'page_view', {...page, send_to: measurementId});
    previous = page.page_location;
  }
  function search(query, resultCount, ready) {
    clearTimeout(searchTimer);
    query = String(query || '').trim().replace(/\s+/g, ' ').toLowerCase();
    if (!ready || resultCount !== 0 || !active || query.length < 2 || query.length > 80) return;
    if (/@|https?:|www\.|\d{7,}|[\u0000-\u001f]/i.test(query)) return;
    const path = active;
    searchTimer = setTimeout(() => {
      const input = document.querySelector('.search input');
      if (!input || input.value.trim().replace(/\s+/g, ' ').toLowerCase() !== query || active !== path || searches.has(query)) return;
      searches.add(query);
      window.gtag('event', 'search_no_results', {
        send_to: measurementId, search_term: query, wiki_path: path
      });
    }, 1500);
  }
  window.TopCraftAnalytics = {mount, search};
})();
