# Spanish Public Government Tender Tracker

## What is this app for?

This app gets information from public entities webpages in two different ways.
- Scraping
- Fetching

## How it works?
This app is able to combine this two ways. The Fetching one is used by default and if this fails then the scraper runs as a second chance.
If everything is ok then send an email.

First this gets info directly from an URL using reverse ingeniering with custom headers.

As said before if this first option fails then a scraper runs after over Playwright.
In this second case, scraper simulates a "human being behaviour" setting the different options withing the website.

If one of this two options is OK then an email is sent using Jinja2 templates and SMTP.
The template is filled with the scraped data so it's always a custom mail.


## Tools
- [Playwright](https://playwright.dev/python/docs/library) as the scraper
- [Jinja2](https://jinja.palletsprojects.com/) for email templates
- SMTP (any provider: Gmail, Brevo, SendGrid, etc.)


