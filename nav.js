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

    // ─────────────────────────────────────────────
    // STEP 1 — Detect country from current URL
    // Match full folder name to avoid false positives
    // e.g. "canada" exists in "multicultural-...-canada"
    // so we match the complete folder slug instead
    // ─────────────────────────────────────────────
    const path = window.location.pathname;

    // Root path (India) special handling
    const isRoot = path === '/' || path === '/index.html' || path.toLowerCase().endsWith('/billliontags.com/') || path.toLowerCase().endsWith('/billliontags.com/index.html');

    let activeKey = Object.keys(COUNTRIES)
        .sort((a, b) => b.length - a.length)
        .find(c => {
            const folder = HOME_FOLDER.replace('{c}', c);
            return path.includes(folder)                          // homepage/subpages
                || path.includes(SERVICES_FOLDER.replace('{c}', c))  // services page
                || Object.values(SERVICES).some(t => path.includes(t.replace('{c}', c))); // individual service
        });

    if (isRoot) activeKey = 'india';

    if (activeKey) {
        // On a country page — save it for later
        localStorage.setItem('bt_country', activeKey);
    } else {
        // Not on a country page — read last saved country
        const saved = localStorage.getItem('bt_country');
        if (saved && COUNTRIES[saved]) {
            activeKey = saved;
        } else {
            activeKey = 'india'; // Default to India
        }
    }

    // ─────────────────────────────────────────────
    // STEP 1.5 — Track dropdown selection
    // ─────────────────────────────────────────────
    // When someone clicks a country, we want to update localStorage immediately
    document.querySelectorAll('[id^="country-"]').forEach(el => {
        el.addEventListener('click', () => {
            const key = el.id.replace('country-', '');
            if (COUNTRIES[key]) {
                localStorage.setItem('bt_country', key);
            }
        });
    });

    const slug = COUNTRIES[activeKey];

    function buildUrl(template, suffix = '') {
        // India homepage special case
        if (activeKey === 'india' && template === HOME_FOLDER && !suffix) {
            return '/';
        }
        return '/' + template.replace(/\{c\}/g, slug) + '/' + suffix;
    }

    function buildServiceUrl(template) {
        const folder = SERVICES_FOLDER.replace(/\{c\}/g, slug);
        const service = template.replace(/\{c\}/g, slug);
        return '/' + folder + '/' + service + '/';
    }

    // ─────────────────────────────────────────────
    // STEP 2 — Update all nav links
    // ─────────────────────────────────────────────

    // ── Logo ──
    const navLogo = document.querySelector('.navbar-brand');
    if (navLogo) navLogo.href = buildUrl(HOME_FOLDER);

    // ── Market ──
    const navMarket = document.getElementById('nav-market');
    if (navMarket) {
        const parentLi = navMarket.closest('li');
        if (activeKey === 'india') {
            if (parentLi) parentLi.style.display = 'none';
            else navMarket.style.display = 'none';
        } else {
            if (parentLi) parentLi.style.display = '';
            navMarket.style.display = '';
            navMarket.href = buildUrl(HOME_FOLDER, MARKET_FOLDER + '/');
        }
    }

    // ── Services ──
    const navServices = document.getElementById('nav-services');
    if (navServices) navServices.href = '/' + SERVICES_FOLDER.replace(/\{c\}/g, slug) + '/';

    // ── Individual service dropdown links & Footer links ──
    Object.entries(SERVICES).forEach(([id, template]) => {
        const fullUrl = buildServiceUrl(template);
        // Header links
        const headerEl = document.getElementById(id);
        if (headerEl) headerEl.href = fullUrl;

        // Footer links
        const footerEl = document.getElementById('footer-' + id);
        if (footerEl) footerEl.href = fullUrl;
    });

    // ── Pride link ──
    const prideLi = document.getElementById('nav-pride');
    if (prideLi) prideLi.href = '/audiences/pride/' + slug + '/';

    // ─────────────────────────────────────────────
    // STEP 3 — Highlight active country in dropdown
    // ─────────────────────────────────────────────
    const countryEl = document.getElementById('country-' + activeKey);
    if (countryEl) countryEl.classList.add('active');

    // ─────────────────────────────────────────────
    // STEP 4 — Highlight active nav item
    // ─────────────────────────────────────────────
    const isMarket = path.includes('/' + MARKET_FOLDER + '/');
    const isService = Object.values(SERVICES).some(t => path.includes(t.replace(/\{c\}/g, slug)));
    const isServices = path.includes(SERVICES_FOLDER.replace(/\{c\}/g, slug));

    if (isMarket) navMarket?.classList.add('active');
    else if (isService || isServices) navServices?.classList.add('active');
}