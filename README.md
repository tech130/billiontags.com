# BillionTags Website

BillionTags is a leading Multicultural Marketing Agency that empowers brands to connect authentically with diverse audiences through data-driven campaigns. This repository contains the source code for the BillionTags website.

## Project Overview

The website is a static multi-page site focused on multicultural marketing services across various regions, including Canada, USA, UK, Australia, New Zealand, South Africa, Malaysia, UAE, and India.

## Key Features

- **Country-Specific Landing Pages**: Tailored content for various international markets.
- **Service Modules**: Dedicated sections for multicultural marketing, digital ads, and audience targeting.
- **Responsive Design**: Built with Bootstrap for a seamless experience across devices.
- **SEO Optimized**: Includes structured data (JSON-LD) and meta tags for better search engine visibility.

## Directory Structure

- `index.html`: The main landing page.
- `services/`: Contains various service-related pages.
- `multicultural-marketing-company-in-[country]/`: Regional marketing agency pages.
- `multicultural-marketing-services-in-[country]/`: Regional service pages.
- `audiences/`, `brands/`, `channels/`, `platforms/`: Industry and channel-specific sections.
- `image/`: Static assets including logos and banners.
- `nav.js`: Global navigation script.

## Maintenance Scripts

### Navigation Management

The `update_meta_titles.py` script is used to inject the global navigation (`nav.js`) into all HTML files. This ensures consistency across the hundreds of pages in the repository.

**Usage:**

```powershell
python update_meta_titles.py
```

## Technologies Used

- **HTML5 / CSS3**
- **Bootstrap 5**
- **JavaScript (Vanilla)**
- **Python (for automation scripts)**
- **Font Awesome**

---
© 2026 BillionTags. All rights reserved.
