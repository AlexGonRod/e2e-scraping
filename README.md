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

If one of this two options is OK then an email is sent using MailTrap and a template.
This template is filled with the data we get before so is always a custom mail.


## Tools
- [Playwright](https://playwright.dev/python/docs/library) as the scraper
- [Mailtrap](https://github.com/mailtrap/mailtrap-python/tree/main) SDK


