#!/usr/bin/env python

# Paths to resources
resources = "/home/user/resources"
database = "/home/user/resources/database.db"

# Files masks
masks = {
    "articles": r"^d+\.txt$",
    "emails": r"^email_headers\.csv$",
    "reports": r"^.*clean\.txt$",
    "resumes": r"^Resume-.*\.txt$",
    "factbooks": r"^FACTBOOK-.*\.txt$",
    "texts": r".*\.txt$",
}
