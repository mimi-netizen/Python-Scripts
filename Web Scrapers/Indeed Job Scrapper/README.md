# Why indeed.scrapper may not work

Check [Robots.txt](https://www.indeed.com/robots.txt)

The robots.txt file for Indeed outlines the rules for web crawlers regarding which parts of the site they can access.

## Key Points from Robots.txt

### Allowed Paths:

Some paths are explicitly allowed for crawling by user agents like Googlebot, Bingbot, and others.

For example, paths containing /hire/, /personeel/, /reclutamiento/, and /recruiting/ with specific query parameters are allowed.

### Disallowed Paths:

Many paths are disallowed for all user agents, including:

- All job pages (/jobs)
- Specific API endpoints
- User profile pages

## Best Practices:

Always adhere to the rules specified in robots.txt.  
 Scraping disallowed sections can lead to IP blocking or legal issues.

Consider using allowed paths for your scraping to ensure compliance with the site's policies.

## Recommendations for our Scraper

- Focus on Allowed Paths: Make sure your scraper only accesses URLs that are permitted in the robots.txt.

- Use a User-Agent: Continue using a User-Agent header in your requests to mimic a browser and avoid being blocked.

- Monitor for Changes: Keep an eye on any updates to the robots.txt file, as websites can change their policies.

- If you plan to scrape job listings, ensure you're focusing on allowed endpoints and consider alternatives like using APIs if available.
