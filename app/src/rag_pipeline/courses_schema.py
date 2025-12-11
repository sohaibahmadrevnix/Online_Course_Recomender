def format_course_item(raw):
    return {
        "subject": raw.get("subject", ""),
        "level": raw.get("level", ""),
        "reviews": raw.get("reviews", 0),
        "price": raw.get("price", "Free"),
        "duration": raw.get("duration", ""),
        "url": raw.get("url", "")
    }
