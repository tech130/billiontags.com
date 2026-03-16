// ─────────────────────────────────────────────
// BILLIONTAGS — DYNAMIC NAV SCRIPT
// Save as: /nav.js
// Load in every page <head>:
//   <script src="/nav.js"></script>
// Then call updateNav() after header fetch completes
// ─────────────────────────────────────────────

function updateNav() {

    const COUNTRIES = {
        'south-africa': 'south-africa',
        'new-zealand': 'new-zealand',
        'australia': 'australia',
        'canada': 'canada',
        'malaysia': 'malaysia',
        'singapore': 'singapore',
        'uae': 'uae',
        'uk': 'uk',
        'usa': 'usa',
        'india': 'india',
    };

    const SERVICES = {
        'svc-campaign': 'campaign-ad-trafficking-and-optimization-company-in-{c}',
        'svc-creative-ad': 'creative-ad-production-agency-in-{c}',
        'svc-creative-dev': 'creative-development-company-in-{c}',
        'svc-data': 'data-driven-analytics-and-insights-company-in-{c}',
        'svc-diverse': 'diverse-audience-planning-in-{c}',
        'svc-ethnocultural': 'ethnocultural-strategist-in-{c}',
        'svc-influencer': 'influencer-marketing-company-in-{c}',
        'svc-media': 'media-Planning-and-buying-company-in-{c}',
        'svc-pr': 'multicultural-pr-company-in-{c}',
        'svc-multilingual': 'multilingual-transcreation-services-company-in-{c}',
    };

    const HOME_FOLDER = 'multicultural-marketing-company-in-{c}';
    const SERVICES_FOLDER = 'multicultural-marketing-services-in-{c}';
    const MARKET_FOLDER = 'market';

    // ── Detect country from URL (longest key first) ──
    const path = window.location.pathname;
    const activeKey = Object.keys(COUNTRIES)
        .sort((a, b) => b.length - a.length)
        .find(c => path.includes(c));

    if (!activeKey) return; // not on a country page

    const slug = COUNTRIES[activeKey];

    function buildUrl(template, suffix = '') {
        return '/' + template.replace(/\{c\}/g, slug) + '/' + suffix;
    }

    // ── Logo ──
    const navLogo = document.querySelector('.navbar-brand');
    if (navLogo) navLogo.href = buildUrl(HOME_FOLDER);

    // ── Market ──
    const navMarket = document.getElementById('nav-market');
    if (navMarket) navMarket.href = buildUrl(HOME_FOLDER, MARKET_FOLDER + '/');

    // ── Services ──
    const navServices = document.getElementById('nav-services');
    if (navServices) navServices.href = '/' + SERVICES_FOLDER.replace(/\{c\}/g, slug) + '/';

    // ── Individual service dropdown links ──
    Object.entries(SERVICES).forEach(([id, template]) => {
        const el = document.getElementById(id);
        if (el) el.href = buildUrl(template);
    });



    // ── Highlight active country in dropdown ──
    const countryEl = document.getElementById('country-' + activeKey);
    if (countryEl) countryEl.classList.add('active');

    // ── Highlight active nav item ──
    const isMarket = path.includes('/' + MARKET_FOLDER + '/');
    const isService = Object.values(SERVICES).some(t => path.includes(t.replace(/\{c\}/g, slug)));
    const isServices = path.includes(SERVICES_FOLDER.replace(/\{c\}/g, slug));

    if (isMarket) navMarket?.classList.add('active');
    else if (isService || isServices) navServices?.classList.add('active');
}